from db import save_user, get_user

def register_user(username, password):
    username = username.strip()

    if not username or not password:
        return False,'Username and Password required'

    if len(username) < 3:
        return False,'Username must be at least 3 characters long'
    
    if len(password) < 8:
        return False,'Password must be at least 8 characters long'
    
    try:
        save_user(username,password)
        return True, None
    except ValueError as e:
        return False, str(e)
    

def authenticate_user(username, password):
    username = username.strip()

    if not username or not password:
        return None, "Username and password are required"

    user = get_user(username)

    if user and user.check_password(password):
        return user, None

    return None, "Invalid username or password"