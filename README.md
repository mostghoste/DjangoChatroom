# DjangoChatroom
A real time user-based messaging/chatroom webapp implemented using Django and React

# Overview
- Django backend handling real-time communication with websockets. Uses daphe to run the ASGI server.
- React frontend communicating with the backend via the API using axios

# Running
- Launch the django backend with 
`daphne -b 127.0.0.1 -p 8000 backend.asgi:application`
- Start the react frontend with
`npm start`

# Superuser
- Username: `mostghoste`
- Email address: `admin@mostghoste.lt`
- Password: `demo`

# Notes
- For authentication, the user token is stored in the browser localStorage. It works, but may be succeptible to cross site scripting attacks.