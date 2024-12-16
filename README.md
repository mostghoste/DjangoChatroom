# DjangoChatroom
A real time user-based messaging/chatroom webapp implemented using Django and React

# Overview
- Django backend handling real-time communication with websockets. Uses daphe to run the ASGI server.

# Running
Launch the django backend with 
`daphne -b 127.0.0.1 -p 8000 backend.asgi:application`