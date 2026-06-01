from pymongo.errors import DuplicateKeyError
from bson import ObjectId

from db import users_collection

def insert_user(username, password):

    try:
        users_collection.insert_one({
            "username": username,
            "password_hash": password
        })
    except DuplicateKeyError:
        raise ValueError("Username already exists")


def find_user_by_username(username):
    return users_collection.find_one({"username": username})


def find_user_by_id(user_id):
    try:
        object_id = ObjectId(user_id)
    except Exception:
        return None

    return users_collection.find_one({"_id": object_id})


def find_user_by_id(user_id):
    try:
        object_id = ObjectId(user_id)
    except Exception:
        return None

    return users_collection.find_one({"_id": object_id})