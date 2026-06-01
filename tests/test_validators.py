from validators import validate_username, validate_password


def test_validate_username_empty():
    valid, error = validate_username("")
    assert valid is False
    assert error == "Username is required"


def test_validate_username_too_short():
    valid, error = validate_username("ab")
    assert valid is False


def test_validate_username_valid():
    valid, error = validate_username("test")
    assert valid is True
    assert error is None


def test_validate_password_empty():
    valid, error = validate_password("")
    assert valid is False
    assert error == "Password is required"


def test_validate_password_too_short():
    valid, error = validate_password("123")
    assert valid is False


def test_validate_password_valid():
    valid, error = validate_password("password123")
    assert valid is True
    assert error is None