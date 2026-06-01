from db import User
from repositories.user_repository import (
    insert_user,
    find_user_by_username
)

def register_user(username, password):
    username = username.strip()

    if not username or not password:
        return False,'Username and Password required'

    if len(username) < 3:
        return False,'Username must be at least 3 characters long'
    
    if len(password) < 8:
        return False,'Password must be at least 8 characters long'
    
    try:
        insert_user(username,password)
        return True, None
    except ValueError as e:
        return False, str(e)
    

def authenticate_user(username, password):
    username = username.strip()

    if not username or not password:
        return None, "Username and password are required"
    
    user_data = find_user_by_username(username)

    if not user_data:
        return None, "Invalid username or password"

    user = User(
        id=user_data["_id"],
        username=user_data["username"],
        password_hash=user_data["password_hash"]
    )

    if user.check_password(password):
        return user, None
    
    return None, "Invalid username or password"