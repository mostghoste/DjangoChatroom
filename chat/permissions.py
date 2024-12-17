# chat/permissions.py

from rest_framework import permissions
from .models import ChatRoomMembership

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the chatroom.
        return obj.owner == request.user

class IsOwnerOrMember(permissions.BasePermission):
    """
    Custom permission to allow access only to owners or members of a chatroom.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or ChatRoomMembership.objects.filter(chatroom=obj, user=request.user).exists()