from repositories.room_repository import (
    find_room_by_code,
    update_room_by_code
)


def create_message(name, message_text):
    return {
        "name": name,
        "message": message_text
    }


def save_message_to_room(room_code, message):
    room = find_room_by_code(room_code)

    if not room:
        return False

    messages = room.get("messages", [])
    messages.append(message)

    update_room_by_code(room_code, {"messages": messages})

    return True