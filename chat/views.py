from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer

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
