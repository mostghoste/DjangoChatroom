# chat/views.py

from rest_framework import generics, status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    UpdateAPIView
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404

from .models import ChatRoom, Message, Invitation, ChatrRoomMembership
from .serializers import (
    ChatRoomSerializer,
    MessageSerializer,
    UserRegistrationSerializer,
    InvitationSerializer,
    UserSerializer
)
from .permissions import IsOwner, IsOwnerOrMember

# API to create and list chatrooms
class ChatRoomListCreateView(ListCreateAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(
            models.Q(owner=user) |
            models.Q(members__user=user)
        ).distinct()

    def perform_create(self, serializer):
        chatroom = serializer.save(owner=self.request.user)
        # Automatically add the owner as a member
        ChatRoomMembership.objects.create(user=self.request.user, chatroom=chatroom)

# API to retrieve, update, and delete a chatroom
class ChatRoomRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrMember]

    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(
            models.Q(owner=user) |
            models.Q(members__user=user)
        ).distinct()

# API to retrieve and send messages in a chatroom
class MessageListCreateView(ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chatroom_id = self.kwargs['chatroom_id']
        user = self.request.user

        # Ensure the user is a member of the chatroom
        if not ChatRoomMembership.objects.filter(user=user, chatroom__id=chatroom_id).exists():
            return Message.objects.none()

        return Message.objects.filter(chatroom__id=chatroom_id).order_by('timestamp')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, chatroom_id=self.kwargs['chatroom_id'])

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Allow any user (authenticated or not) to access this view

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                # Handle the case where the token wasn't created for some reason
                token = Token.objects.create(user=user)
            return Response({
                "user": {
                    "username": user.username,
                    "email": user.email,
                },
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InvitationCreateView(generics.CreateAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sender = request.user
        recipient = serializer.validated_data['recipient']
        chatroom = serializer.validated_data['chatroom']

        # Check if sender is a member of the chatroom
        if not ChatRoomMembership.objects.filter(user=sender, chatroom=chatroom).exists():
            return Response({"detail": "You are not a member of this chatroom."}, status=status.HTTP_403_FORBIDDEN)

        # Prevent inviting oneself
        if sender == recipient:
            return Response({"detail": "You cannot invite yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if recipient is already a member
        if ChatRoomMembership.objects.filter(user=recipient, chatroom=chatroom).exists():
            return Response({"detail": "User is already a member of this chatroom."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the invitation
        invitation, created = Invitation.objects.get_or_create(
            sender=sender,
            recipient=recipient,
            chatroom=chatroom
        )
        if not created:
            return Response({"detail": "Invitation already exists."}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(InvitationSerializer(invitation).data, status=status.HTTP_201_CREATED, headers=headers)

# API to list incoming invitations
class IncomingInvitationsView(ListAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Invitation.objects.filter(recipient=user, status='pending')

# API to accept an invitation
class AcceptInvitationView(UpdateAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        invitation_id = self.kwargs['invitation_id']
        invitation = get_object_or_404(Invitation, id=invitation_id, recipient=self.request.user, status='pending')
        return invitation

    def update(self, request, *args, **kwargs):
        invitation = self.get_object()
        invitation.status = 'accepted'
        invitation.save()

        # Add user to ChatRoomMembership
        ChatRoomMembership.objects.create(user=request.user, chatroom=invitation.chatroom)

        serializer = self.get_serializer(invitation)
        return Response(serializer.data, status=status.HTTP_200_OK)

# API to decline an invitation
class DeclineInvitationView(UpdateAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        invitation_id = self.kwargs['invitation_id']
        invitation = get_object_or_404(Invitation, id=invitation_id, recipient=self.request.user, status='pending')
        return invitation

    def update(self, request, *args, **kwargs):
        invitation = self.get_object()
        invitation.status = 'rejected'
        invitation.save()

        serializer = self.get_serializer(invitation)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChatRoomMembersView(generics.ListAPIView):
    serializer_class = UserRegistrationSerializer  # Alternatively, create a UserSerializer

    def get_queryset(self):
        chatroom_id = self.kwargs['chatroom_id']
        user = self.request.user

        # Check if user is a member of the chatroom
        if not ChatRoomMembership.objects.filter(user=user, chatroom__id=chatroom_id).exists():
            return User.objects.none()

        # Return all members of the chatroom
        return User.objects.filter(chatroom_memberships__chatroom__id=chatroom_id)