# chat/serializers.py

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import ChatRoom, Message, Invitation

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password", style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

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
    sender = serializers.ReadOnlyField(source='sender.username')
    recipient = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    chatroom = serializers.SlugRelatedField(
        slug_field='name',
        queryset=ChatRoom.objects.all()
    )
    status = serializers.CharField(read_only=True)
    sent_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Invitation
        fields = ['id', 'sender', 'recipient', 'chatroom', 'status', 'sent_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
