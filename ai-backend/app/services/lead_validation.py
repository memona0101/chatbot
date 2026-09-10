import re


def validate_full_name(value: str) -> bool:
    value = value.strip()

    if len(value) < 2:
        return False

    if len(value) > 255:
        return False

    if not re.fullmatch(r"[A-Za-zÀ-ÿ]+(?:[ '\-][A-Za-zÀ-ÿ]+)*", value):
        return False

    return True


def validate_email(value: str) -> bool:
    value = value.strip().lower()

    if len(value) > 320:
        return False

    if " " in value:
        return False

    pattern = r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"

    return bool(re.fullmatch(pattern, value))


def validate_contact_number(value: str) -> bool:
    value = value.strip()

    digits = re.sub(r"\D", "", value)

    if len(digits) < 7:
        return False

    if len(digits) > 15:
        return False

    # Reject obvious placeholders such as 0000000 / 1111111
    if len(set(digits)) == 1:
        return False

    return True