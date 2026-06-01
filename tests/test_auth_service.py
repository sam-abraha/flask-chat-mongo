from unittest.mock import patch

from auth_service import register_user, authenticate_user
from db import User


@patch("auth_service.insert_user")
def test_register_user_success(mock_insert_user):
    success, error = register_user("user", "password123")

    assert success is True
    assert error is None
    mock_insert_user.assert_called_once()


def test_register_user_invalid_username():
    success, error = register_user("ab", "password123")

    assert success is False
    assert error == "Username must be at least 3 characters long"


def test_register_user_invalid_password():
    success, error = register_user("user", "123")

    assert success is False
    assert error == "Password must be at least 8 characters long"


@patch("auth_service.insert_user")
def test_register_user_duplicate_username(mock_insert_user):
    mock_insert_user.side_effect = ValueError("Username already exists")

    success, error = register_user("user", "password123")

    assert success is False
    assert error == "Username already exists"


@patch("auth_service.find_user_by_username")
def test_authenticate_user_not_found(mock_find_user):
    mock_find_user.return_value = None

    user, error = authenticate_user("lucas", "password123")

    assert user is None
    assert error == "Invalid username or password"


@patch("auth_service.find_user_by_username")
@patch("auth_service.create_user_from_data")
def test_authenticate_user_success(mock_create_user, mock_find_user):
    fake_user = User(
        id="123",
        username="user",
        password_hash="fake-hash"
    )

    fake_user.check_password = lambda password: True

    mock_find_user.return_value = {
        "_id": "123",
        "username": "user",
        "password_hash": "fake-hash"
    }

    mock_create_user.return_value = fake_user

    user, error = authenticate_user("user", "password123")

    assert user == fake_user
    assert error is None