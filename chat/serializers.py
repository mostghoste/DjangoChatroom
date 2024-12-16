from rest_framework import serializers
from .models import ChatRoom, Message, Invitation

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'owner', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chatroom', 'user', 'content', 'timestamp']

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id', 'sender', 'recipient', 'chatroom', 'status', 'sent_at']
