# chat/views.py

from rest_framework import generics, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer, UserRegistrationSerializer

# API to create and list chatrooms
class ChatRoomListCreateView(ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# API to retrieve and send messages in a chatroom
class MessageListCreateView(ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chatroom_id = self.kwargs['chatroom_id']
        return Message.objects.filter(chatroom__id=chatroom_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, chatroom_id=self.kwargs['chatroom_id'])

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Allow any user (authenticated or not) to access this view

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user)
            return Response({
                "user": {
                    "username": user.username,
                    "email": user.email,
                },
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
