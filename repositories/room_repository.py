from db import rooms_collection

def insert_room(room_code, owner_id):
    rooms_collection.insert_one({
        "room_code": room_code,
        "owner_id": str(owner_id),
        "members": 0,
        "messages": []
    })


def find_room_by_code(room_code):
    return rooms_collection.find_one({"room_code": room_code})


def update_room_by_code(room_code, updates):
    rooms_collection.update_one(
        {"room_code": room_code},
        {"$set": updates}
    )


def delete_room_by_code(room_code):
    rooms_collection.delete_one({"room_code": room_code})


def find_all_rooms():
    return list(rooms_collection.find())