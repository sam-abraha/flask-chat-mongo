from app import app, socketio
import eventlet
import eventlet.wsgi

if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8080)), app)
