# chat/serializers.py

from rest_framework import serializers
from .models import ChatRoom, Message, Invitation

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'owner', 'created_at']
        read_only_fields = ['owner', 'created_at']  # Owner and created_at are set automatically

class MessageSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Display username instead of user ID

    class Meta:
        model = Message
        fields = ['id', 'chatroom', 'user', 'content', 'timestamp']
        read_only_fields = ['chatroom', 'user', 'timestamp']  # Automatically populated fields

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id', 'sender', 'recipient', 'chatroom', 'status', 'sent_at']
        read_only_fields = ['sender', 'sent_at']  # Sender and sent_at are set automatically
