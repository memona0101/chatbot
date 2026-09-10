from app.services.lead_validation import (
    validate_full_name,
    validate_email,
    validate_contact_number,
)


def test_validate_full_name():
    assert validate_full_name("John Doe") is True
    assert validate_full_name("Mary-Jane O'Connor") is True
    assert validate_full_name("A") is False
    assert validate_full_name("12345") is False


def test_validate_email():
    assert validate_email("user@example.com") is True
    assert validate_email("test.email+alias@domain.co.uk") is True
    assert validate_email("invalid-email") is False
    assert validate_email("user@ domain.com") is False


def test_validate_contact_number():
    assert validate_contact_number("+1 555 123 4567") is True
    assert validate_contact_number("+92 300 1234567") is True
    assert validate_contact_number("123") is False
    assert validate_contact_number("00000000") is False
