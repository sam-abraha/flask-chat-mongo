from unittest.mock import patch

from room_service import (
    can_join_room,
    validate_room_session,
    delete_room_if_owner
)


@patch("room_service.find_room_by_code")
def test_can_join_room_missing_code(mock_find_room):
    can_join, error = can_join_room("")

    assert can_join is False
    assert error == "Please enter a room code"


@patch("room_service.find_room_by_code")
def test_can_join_room_not_found(mock_find_room):
    mock_find_room.return_value = None

    can_join, error = can_join_room("ABCDE")

    assert can_join is False
    assert error == "Room does not exist"


@patch("room_service.find_room_by_code")
def test_can_join_room_success(mock_find_room):
    mock_find_room.return_value = {
        "room_code": "ABCDE"
    }

    can_join, error = can_join_room("ABCDE")

    assert can_join is True
    assert error is None


def test_validate_room_session_missing_data():
    valid, room = validate_room_session(None, None)

    assert valid is False
    assert room is None


@patch("room_service.find_room_by_code")
def test_validate_room_session_success(mock_find_room):
    fake_room = {
        "room_code": "ABCDE",
        "owner_id": "123"
    }

    mock_find_room.return_value = fake_room

    valid, room = validate_room_session("ABCDE", "Lucas")

    assert valid is True
    assert room == fake_room


@patch("room_service.find_room_by_code")
def test_delete_room_if_owner_not_owner(mock_find_room):
    mock_find_room.return_value = {
        "room_code": "ABCDE",
        "owner_id": "123"
    }

    success, error = delete_room_if_owner("ABCDE", "999")

    assert success is False
    assert error == "You are not allowed to delete this room"


@patch("room_service.delete_room_by_code")
@patch("room_service.find_room_by_code")
def test_delete_room_if_owner_success(mock_find_room, mock_delete_room):
    mock_find_room.return_value = {
        "room_code": "ABCDE",
        "owner_id": "123"
    }

    success, error = delete_room_if_owner("ABCDE", "123")

    assert success is True
    assert error is None
    mock_delete_room.assert_called_once_with("ABCDE")