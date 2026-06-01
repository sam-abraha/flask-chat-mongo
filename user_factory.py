from db import User
from repositories.user_repository import find_user_by_id


def create_user_from_data(user_data):
    if not user_data:
        return None

    return User(
        id=user_data["_id"],
        username=user_data["username"],
        password_hash=user_data["password_hash"]
    )


def get_user_by_id(user_id):
    user_data = find_user_by_id(user_id)
    return create_user_from_data(user_data)