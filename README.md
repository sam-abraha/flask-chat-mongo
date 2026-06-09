# Real-Time Chat Application

A production-oriented real-time chat application built with Flask, MongoDB, and Socket.IO. Users can securely register, authenticate, create chat rooms, and exchange messages instantly through 
WebSockets.


## Live Demo

Production Deployment:

🌍 https://mylittlechatroom.up.railway.app/


## Features

### Real-Time Communication

* Create unique chat rooms with randomly generated room codes
* Join existing chat rooms
* Exchange messages in real time using WebSockets
* Automatic room management and member tracking


### Authentication & Security

* User registration and login
* Secure password hashing using Werkzeug
* Session-based authentication with Flask-Login
* CSRF protection using Flask-WTF
* Rate limiting for login and signup endpoints
* Authorization checks for room ownership
* Secure session cookie configuration

### Monitoring & Reliability

* Health check endpoint (`/health`)
* MongoDB connectivity validation
* Prometheus metrics endpoint (`/metrics`)
* Application logging
* Custom error handling pages
* Structured service and repository architecture

## Architecture

```text
Browser
   │
   ▼
Flask + Socket.IO
   │
   ├── Services Layer
   │      ├── auth_service
   │      ├── room_service
   │      └── message_service
   │
   ├── Repository Layer
   │      ├── user_repository
   │      └── room_repository
   │
   ▼
MongoDB
```

## Tech Stack

### Backend

* Python
* Flask
* Flask-SocketIO
* Flask-Login
* Flask-WTF
* Flask-Limiter
* PyMongo
* Prometheus Client

### Database

* MongoDB

### Frontend

* HTML
* Tailwind CSS
* JavaScript

### Testing

* Pytest

## Project Structure

```text
flask_chat/
│
├── app.py
├── wsgi.py
├── config.py
├── db.py
│
├── repositories/
│   ├── user_repository.py
│   └── room_repository.py
│
├── services/
│   ├── auth_service.py
│   ├── room_service.py
│   └── message_service.py
│
├── templates/
├── static/
│
├── tests/
│
└── requirements.txt
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd flask_chat
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
MONGO_URI=your_mongodb_connection_string
DB_NAME=ChatApp
```

## Running the Application

### Development

```bash
flask run
```

### Production

```bash
python wsgi.py
```

## Monitoring

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "ok",
  "database": "connected",
  "service": "flask-chat",
  "version": "1.0.0"
}
```

### Metrics

```http
GET /metrics
```

Prometheus metrics include:

* Total successful logins
* Total messages sent
* Active room count

## Testing

Run all tests:

```bash
python -m pytest -v
```

## Future Improvements

* Private chat rooms
* User roles and permissions
* Room invitations
* Message persistence optimization
* Docker deployment
* CI/CD pipeline
* Redis-based rate limiting
* Grafana dashboards
* Kubernetes deployment

## Preview

<img width="960" alt="flask-chat-mongo" src="https://github.com/user-attachments/assets/3a7c10d4-5312-4ccb-a9b9-e04bc42b21ce">

## Key Learning Outcomes

* Authentication and authorization
* WebSocket communication
* Repository and service patterns
* Secure session management
* CSRF protection
* Rate limiting
* Monitoring and observability
* MongoDB integration
* Test-driven backend development
