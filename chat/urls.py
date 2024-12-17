# chat/urls.py

from django.urls import path
from .views import ChatRoomListCreateView, MessageListCreateView, UserRegistrationView

urlpatterns = [
    path('chatrooms/', ChatRoomListCreateView.as_view(), name='chatroom-list-create'),
    path('chatrooms/<int:chatroom_id>/messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),  # Registration endpoint
]
