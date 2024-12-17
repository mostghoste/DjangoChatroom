# chat/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        logger.info(f"Attempting to connect to WebSocket for room: {self.room_name}")

        try:
            # Get token from query string
            query_string = self.scope['query_string'].decode('utf-8')
            token = dict(q.split("=") for q in query_string.split("&")).get("token")

            # Authenticate the user
            self.scope["user"] = await self.get_user_from_token(token)

            if self.scope["user"].is_authenticated:
                # Join room group
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
                await self.accept()
                logger.info(f"WebSocket connection accepted for room: {self.room_name}")
            else:
                logger.warning("Unauthenticated user tried to connect.")
                await self.close()
        except Exception as e:
            logger.error(f"Error during WebSocket connection: {e}")
            await self.close()

    async def disconnect(self, close_code):
        logger.info(f"Disconnecting WebSocket for room: {self.room_name} with code: {close_code}")
        try:
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            logger.info(f"Disconnected from room: {self.room_name}")
        except Exception as e:
            logger.error(f"Error during WebSocket disconnect: {e}")

    async def receive(self, text_data):
        logger.info(f"Received WebSocket message: {text_data}")

        try:
            from chat.models import Message  # Lazy import to avoid circular imports
            data = json.loads(text_data)
            message = data.get("message")

            if not message:
                logger.warning("Message content is empty or invalid.")
                return

            logger.info(f"Processing message: {message}")

            # Save message to the database
            await self.save_message(message)
            logger.info(f"Saved message: {message} to database.")

            # Broadcast message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "user": "WebSocket",  # Replace with actual user if authentication is added
                }
            )
        except Exception as e:
            logger.error(f"Error processing received message: {e}")

    async def chat_message(self, event):
        logger.info(f"Broadcasting message to WebSocket clients: {event}")
        try:
            message = event.get("message")
            user = event.get("user", "Unknown")

            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                "message": message,
                "user": user,
            }))
            logger.info(f"Message sent to WebSocket: {message} from {user}")
        except Exception as e:
            logger.error(f"Error sending message to WebSocket: {e}")

    @database_sync_to_async
    def get_user_from_token(self, token):
        from rest_framework.authtoken.models import Token
        from django.contrib.auth.models import AnonymousUser

        try:
            # Validate the token
            valid_token = Token.objects.get(key=token)
            return valid_token.user
        except Token.DoesNotExist:
            logger.warning(f"Invalid token: {token}")
            return AnonymousUser()


    @database_sync_to_async
    def save_message(self, content):
        logger.info(f"Saving message to database: {content}")
        try:
            from chat.models import ChatRoom, Message

            # Ensure `self.scope["user"]` is an authenticated User
            user = self.scope["user"]

            if not user.is_authenticated:
                logger.error("Attempt to save a message from an unauthenticated user.")
                return None

            # Get the chatroom by ID
            chatroom = ChatRoom.objects.get(id=self.room_name)

            # Save the message
            return Message.objects.create(chatroom=chatroom, user=user, content=content)
        except Exception as e:
            logger.error(f"Error saving message to database: {e}")
            return None



