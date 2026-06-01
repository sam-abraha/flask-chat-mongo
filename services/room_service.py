import random
from string import ascii_uppercase
from repositories.room_repository import (
    insert_room,
    find_room_by_code,
    update_room_by_code,
    delete_room_by_code
)

def create_room_code(length=5):
    while True:
        code = "".join(random.choices(ascii_uppercase, k=length))

        if not find_room_by_code(code):
            return code


def create_new_room(owner_id):
    room_code = create_room_code()
    insert_room(room_code, owner_id)
    return room_code


def can_join_room(room_code):
    if not room_code:
        return False, "Please enter a room code"

    room = find_room_by_code(room_code)

    if not room:
        return False, "Room does not exist"

    return True, None

def increment_room_members(room_code):
    room = find_room_by_code(room_code)

    if not room:
        return False

    members = room.get("members", 0) + 1
    update_room_by_code(room_code, {"members": members})

    return True


def decrement_room_members(room_code):
    room = find_room_by_code(room_code)

    if not room:
        return False

    members = max(room.get("members", 1) - 1, 0)
    update_room_by_code(room_code, {"members": members})

    return True

def validate_room_session(room_code, name):
    if not room_code or not name:
        return False, None

    room = find_room_by_code(room_code)

    if not room:
        return False, None

    return True, room

def delete_room_if_owner(room_code, user_id):
    room = find_room_by_code(room_code)

    if not room:
        return False,"Room not found"
    
    if room.get("owner_id") != str(user_id):
        return False,"You are not allowed to delete this room"
    
    delete_room_by_code(room_code)
    return True, None