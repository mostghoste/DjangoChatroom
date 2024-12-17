# chat/urls.py

from django.urls import path
from .views import (
    ChatRoomListCreateView,
    ChatRoomRetrieveUpdateDestroyView,
    MessageListCreateView,
    UserRegistrationView,
    InvitationCreateView,
    IncomingInvitationsView,
    AcceptInvitationView,
    DeclineInvitationView,
    ChatRoomMembersView
)

urlpatterns = [
    path('chatrooms/', ChatRoomListCreateView.as_view(), name='chatroom-list-create'),
    path('chatrooms/<int:pk>/', ChatRoomRetrieveUpdateDestroyView.as_view(), name='chatroom-detail'),
    path('chatrooms/<int:chatroom_id>/messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('chatrooms/<int:chatroom_id>/members/', ChatRoomMembersView.as_view(), name='chatroom-members'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('invitations/', InvitationCreateView.as_view(), name='invitation-create'),
    path('invitations/incoming/', IncomingInvitationsView.as_view(), name='incoming-invitations'),
    path('invitations/<int:invitation_id>/accept/', AcceptInvitationView.as_view(), name='accept-invitation'),
    path('invitations/<int:invitation_id>/decline/', DeclineInvitationView.as_view(), name='decline-invitation'),
]
