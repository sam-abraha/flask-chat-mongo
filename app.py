from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_login import current_user, login_required, login_user, LoginManager, logout_user
from pymongo.errors import DuplicateKeyError
import random
from string import ascii_uppercase
from db import save_user, get_user, get_user_by_id, save_room, get_room, update_room, delete_room, get_all_rooms
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

def create_room_code(length):
    while True:
        code = ''.join(random.choices(ascii_uppercase, k=length))
        if not get_room(code):
            return code

@app.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('login'))

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    error = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            save_user(username, password)
            return redirect(url_for('login'))
        except ValueError as e:
            error = str(e)
    return render_template('signup.html', error=error)

@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    error = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')
        user = get_user(username)

        if user and user.check_password(password_input):
            login_user(user)
            return redirect(url_for('home'))
        else:
            error = 'Failed to login!'
    return render_template('login.html', error=error)

@app.route("/", methods=["POST", "GET"])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('signup'))

    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        action = request.form.get("action")

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if action == "create":
            room_code = create_room_code(5)
            save_room(room_code)
            session["room"] = room_code
        elif action == "join":
            if not code:
                return render_template("home.html", error="Please enter a room code.", code=code, name=name)
            room = get_room(code)
            if not room:
                return render_template("home.html", error="Room does not exist.", code=code, name=name)
            session["room"] = code
        else:
            return render_template("home.html", error="Invalid action.", code=code, name=name)

        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
def room():
    room_code = session.get("room")
    if room_code is None or session.get("name") is None:
        return redirect(url_for("home"))

    room = get_room(room_code)
    if not room:
        return redirect(url_for("home"))

    return render_template("room.html", code=room_code, messages=room.get("messages", []))

@socketio.on("message")
def handle_message(data):
    room_code = session.get("room")
    if not room_code:
        return

    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room_code)

    # Append message to room in the database
    room = get_room(room_code)
    if room:
        room["messages"].append(content)
        update_room(room_code, {"messages": room["messages"]})

@socketio.on("disconnect")
def handle_disconnect():
    room_code = session.get("room")
    name = session.get("name")
    leave_room(room_code)

    room = get_room(room_code)
    if room:
        room["members"] -= 1
        if room["members"] <= 0:
            delete_room(room_code)
        else:
            update_room(room_code, {"members": room["members"]})

    send({"name": name, "message": "left the room"}, to=room_code)

@socketio.on("connect")
def handle_connect(auth):
    room_code = session.get("room")
    name = session.get("name")
    if not room_code or not name:
        return

    join_room(room_code)
    send({"name": name, "message": "entered the room"}, to=room_code)

    room = get_room(room_code)
    if room:
        room["members"] += 1
        update_room(room_code, {"members": room["members"]})

if __name__ == "__main__":
    socketio.run(app, debug=True)