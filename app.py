from flask import Flask, flash, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_login import current_user, login_required, login_user, LoginManager, logout_user
from pymongo.errors import DuplicateKeyError
from config import Config
from auth_service import register_user, authenticate_user
from room_service import create_new_room, can_join_room, increment_room_members, decrement_room_members,validate_room_session,delete_room_if_owner
from message_service import save_message_to_room, create_message
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from user_factory import get_user_by_id

app = Flask(__name__)
csrf = CSRFProtect(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[]
)
app.config.from_object(Config)
app.config["SECRET_KEY"] = Config.SECRET_KEY
socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

@app.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('login'))

@app.route("/signup", methods=["POST", "GET"])
@limiter.limit("3 per Minute",methods=["POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    error = ''
    if request.method == 'POST':
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        success, error = register_user(username, password)

        if success:
            return redirect(url_for('login'))

    return render_template('signup.html', error=error)

@app.route("/login", methods=["POST", "GET"])
@limiter.limit("5 per Minute",methods=["POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    error = ''
    if request.method == 'POST':
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user, error = authenticate_user(username, password)
        
        if user:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route("/", methods=["POST", "GET"])
@login_required
def home():

    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        action = request.form.get("action")

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if action == "create":
            room_code = create_new_room(current_user.id)
            session["room"] = room_code
        elif action == "join":
            can_join, error = can_join_room(code)
            if not can_join:
                return render_template("home.html", error=error, code=code, name=name)
            session["room"] = code
        else:
            return render_template("home.html", error="Invalid action.", code=code, name=name)

        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
@login_required
def room():
    room_code = session.get("room")
    name = session.get("name")

    is_valid, room = validate_room_session(room_code, name)

    if not is_valid:
        return redirect(url_for("home"))

    return render_template("room.html", code=room_code, room=room,messages=room.get("messages", []))

@app.route("/room/delete", methods=["POST"])
@login_required
def delete_current_room():
    room_code = session.get("room")

    success, error = delete_room_if_owner(room_code, current_user.id)

    if success:
        socketio.emit(
            "room_deleted",
            {"message": "Room was deleted by the owner."},
            to=room_code
        )
        session.pop("room", None)
        session.pop("name", None)
        flash("Room deleted successfully.", "success")
        return redirect(url_for("home"))

    return redirect(url_for("room"))

@socketio.on("message")
def handle_message(data):
    if not current_user.is_authenticated:
        return
    room_code = session.get("room")
    name = session.get("name")

    if not room_code or not name:
        return

    message_text = data.get("data", "").strip()


    if not message_text:
        return

    content = create_message(name, message_text)
    send(content, to=room_code)
    save_message_to_room(room_code, content)

@socketio.on("disconnect")
def handle_disconnect():
    if not current_user.is_authenticated:
        return
    room_code = session.get("room")
    if not room_code:
        return
    name = session.get("name")
    leave_room(room_code)

    decrement_room_members(room_code)

    send({"name": name, "message": "left the room"}, to=room_code)

@socketio.on("connect")
def handle_connect(auth):
    if not current_user.is_authenticated:
        return False
    room_code = session.get("room")
    name = session.get("name")
    if not room_code or not name:
        return

    join_room(room_code)
    send({"name": name, "message": "entered the room"}, to=room_code)
    increment_room_members(room_code)

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(403)
def forbidden(error):
    return render_template("403.html"), 403


@app.errorhandler(429)
def ratelimit_handler(error):
    return render_template("429.html"), 429


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500

if __name__ == "__main__":
    socketio.run(app, debug=True)