import random
from string import ascii_uppercase
from db import save_room, get_room


def create_room_code(length=5):
    while True:
        code = "".join(random.choices(ascii_uppercase, k=length))

        if not get_room(code):
            return code


def create_new_room():
    room_code = create_room_code()
    save_room(room_code)
    return room_code


def can_join_room(room_code):
    if not room_code:
        return False, "Please enter a room code"

    room = get_room(room_code)

    if not room:
        return False, "Room does not exist"

    return True, None