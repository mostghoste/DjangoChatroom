# chat/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import ChatRoom, ChatRoomMembership, Invitation

class ChatAppTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='pass1234')
        self.user2 = User.objects.create_user(username='user2', password='pass1234')
        self.chatroom = ChatRoom.objects.create(name='TestRoom', owner=self.user1)
        ChatRoomMembership.objects.create(user=self.user1, chatroom=self.chatroom)

    def test_user_registration(self):
        response = self.client.post('/api/register/', {
            'username': 'user3',
            'email': 'user3@example.com',
            'password': 'pass1234',
            'password2': 'pass1234'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.data)

    def test_obtain_token(self):
        response = self.client.post('/api/token/', {
            'username': 'user1',
            'password': 'pass1234'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_create_chatroom(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post('/api/chatrooms/', {'name': 'NewRoom'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'NewRoom')
        self.assertTrue(ChatRoomMembership.objects.filter(user=self.user1, chatroom__name='NewRoom').exists())

    def test_invite_user(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post('/api/invitations/', {'recipient': 'user2', 'chatroom': 'TestRoom'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['sender'], 'user1')
        self.assertEqual(response.data['recipient'], 'user2')
        self.assertEqual(response.data['chatroom'], 'TestRoom')
        self.assertEqual(response.data['status'], 'pending')

    def test_accept_invitation(self):
        # Create invitation
        invitation = Invitation.objects.create(sender=self.user1, recipient=self.user2, chatroom=self.chatroom)
        
        # Authenticate as user2 and accept the invitation
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(f'/api/invitations/{invitation.id}/accept/')
        self.assertEqual(response.status_code, 200)
        invitation.refresh_from_db()
        self.assertEqual(invitation.status, 'accepted')
        self.assertTrue(ChatRoomMembership.objects.filter(user=self.user2, chatroom=self.chatroom).exists())

    def test_decline_invitation(self):
        # Create invitation
        invitation = Invitation.objects.create(sender=self.user1, recipient=self.user2, chatroom=self.chatroom)
        
        # Authenticate as user2 and decline the invitation
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(f'/api/invitations/{invitation.id}/decline/')
        self.assertEqual(response.status_code, 200)
        invitation.refresh_from_db()
        self.assertEqual(invitation.status, 'rejected')
        self.assertFalse(ChatRoomMembership.objects.filter(user=self.user2, chatroom=self.chatroom).exists())

    def test_send_message(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(f'/api/chatrooms/{self.chatroom.id}/messages/', {'content': 'Hello!'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['content'], 'Hello!')
        self.assertEqual(response.data['user'], 'user1')
