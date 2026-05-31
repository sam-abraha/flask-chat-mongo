from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client[Config.DB_NAME]

users_collection = db["users"]
rooms_collection = db["rooms"]

users_collection.create_index("username", unique=True)
rooms_collection.create_index("room_code", unique=True)


class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    @staticmethod
    def get(username):
        return get_user(username)


def save_user(username, password):
    password_hash = generate_password_hash(password)

    try:
        users_collection.insert_one({
            "username": username,
            "password_hash": password_hash
        })
    except DuplicateKeyError:
        raise ValueError("Username already exists")


def get_user(username):
    user_data = users_collection.find_one({"username": username})

    if user_data:
        return User(
            id=user_data["_id"],
            username=user_data["username"],
            password_hash=user_data["password_hash"]
        )

    return None


def get_user_by_id(user_id):
    try:
        object_id = ObjectId(user_id)
    except Exception:
        return None

    user_data = users_collection.find_one({"_id": object_id})

    if user_data:
        return User(
            id=user_data["_id"],
            username=user_data["username"],
            password_hash=user_data["password_hash"]
        )

    return None


def save_room(room_code):
    rooms_collection.insert_one({
        "room_code": room_code,
        "members": 0,
        "messages": []
    })


def get_room(room_code):
    return rooms_collection.find_one({"room_code": room_code})


def update_room(room_code, updates):
    rooms_collection.update_one(
        {"room_code": room_code},
        {"$set": updates}
    )


def delete_room(room_code):
    rooms_collection.delete_one({"room_code": room_code})


def get_all_rooms():
    return list(rooms_collection.find())