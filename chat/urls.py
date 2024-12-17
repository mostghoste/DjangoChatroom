# chat/urls.py

from django.urls import path
from .views import (
    ChatRoomListCreateView,
    ChatRoomRetrieveUpdateDestroyView,
    MessageListCreateView,
    UserRegistrationView,
    InvitationCreateView,
    # IncomingInvitationsView,
    # AcceptInvitationView,
    # DeclineInvitationView,
    # ChatRoomMembersView
)

urlpatterns = [
    path('chatrooms/', ChatRoomListCreateView.as_view(), name='chatroom-list-create'),
    path('chatrooms/<int:pk>/', ChatRoomRetrieveUpdateDestroyView.as_view(), name='chatroom-detail'),
    path('chatrooms/<int:chatroom_id>/messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('invitations/', InvitationCreateView.as_view(), name='invitation-create'),
]
