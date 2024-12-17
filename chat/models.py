# chat/models.py

from django.db import models
from django.contrib.auth.models import User

# ChatRoom model
class ChatRoom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_chatrooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# ChatRoom Membership
class ChatRoomMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatroom_memberships')
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='members')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'chatroom')  # Prevent duplicate memberships

    def __str__(self):
        return f"{self.user.username} in {self.chatroom.name}"

# Invitations
class Invitation(models.Model):
    INVITATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='invitations')
    status = models.CharField(max_length=10, choices=INVITATION_STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'recipient', 'chatroom')  # Prevent duplicate invitations

    def __str__(self):
        return f"Invitation from {self.sender.username} to {self.recipient.username} for {self.chatroom.name}"

# Messages
class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in {self.chatroom.name}: {self.content[:20]}"