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