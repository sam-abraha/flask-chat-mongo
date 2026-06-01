from db import get_room, update_room


def create_message(name, message_text):
    return {
        "name": name,
        "message": message_text
    }


def save_message_to_room(room_code, message):
    room = get_room(room_code)

    if not room:
        return False

    messages = room.get("messages", [])
    messages.append(message)

    update_room(room_code, {"messages": messages})

    return True