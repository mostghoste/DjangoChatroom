from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from backend.consumers import ChatConsumer

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path("ws/chat/<str:room_name>/", ChatConsumer.as_asgi()),
    ]),
})
