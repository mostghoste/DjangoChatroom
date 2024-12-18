# DjangoChatroom

A real-time user-based messaging/chatroom web application built with Django and React.

## Showcase
A showcase of DjangoChatroom [ can be found in video format here](https://www.youtube.com/watch?v=HIivyTZ2d38).

## Overview
- **Backend:** Django with Django Channels for real-time communication using WebSockets. Runs on the ASGI server with Daphne.
- **Frontend:** React application communicating with the backend via REST APIs using Axios.
- **Database:** SQLite.

## Architecture
- **Client-Server Model:** The React frontend interacts with the Django backend through REST APIs and WebSockets.
- **Real-Time Communication:** Managed by Django Channels, enabling instant messaging within chatrooms.
- **Database:** SQLite is used for simplicity and ease of setup during development.

## Running the Application

Follow these steps to set up and run the DjangoChatroom application on a Linux machine:

- **Clone the repository**
```
git clone https://github.com/yourusername/DjangoChatroom.git
cd DjangoChatroom
```

- **Create and Activate a Virtual Environment**
```
   python3 -m venv venv
   source venv/bin/activate
```
- **Install Python Dependencies** 
```
pip install -r requirements.txt
```
- **Install and Start Redis Server**
```
sudo apt update
sudo apt install redis-server
sudo systemctl enable redis-server.service
sudo systemctl start redis-server.service
```
- **Apply Database Migrations**
```
python manage.py migrate
```

- **Run the backend**
```
daphne -b 127.0.0.1 -p 8000 backend.asgi:application
```

- **Set up and runthe frontend**
```
cd frontend
npm install
npm start
```

The chat should be accessible via `http://localhost:3000`, with the Django backend running on `http://127.0.0.1:8000`.
## Demo users
### Superuser
- Username: `mostghoste`
- Email address: `admin@mostghoste.lt`
- Password: `demo`
### Tester
- Username: `Tester`
- Email address: `Tester@email.com`
- Password: `demo`

## Notes
- For authentication, the user token is stored in the browser localStorage. It works, but may be succeptible to cross site scripting attacks.
- The testing plan can be found in `testing_plan.md`