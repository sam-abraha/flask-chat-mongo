from db import User
from repositories.user_repository import (
    insert_user,
    find_user_by_username

)
from user_factory import create_user_from_data
from werkzeug.security import generate_password_hash
from validators import validate_username, validate_password

def register_user(username, password):
    username = username.strip()

    is_valid_username, error = validate_username(username)
    if not is_valid_username:
        return False, error

    is_valid_password, error = validate_password(password)
    if not is_valid_password:
        return False, error
    
    password_hash = generate_password_hash(password)

    
    try:
        insert_user(username,password_hash)
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
    
    user = create_user_from_data(user_data)

    if user.check_password(password):
        return user, None
    
    return None, "Invalid username or password"