from django.contrib import admin
from .models import ChatRoom, ChatRoomMembership, Invitation, Message

admin.site.register(ChatRoom)
admin.site.register(ChatRoomMembership)
admin.site.register(Invitation)
admin.site.register(Message)
