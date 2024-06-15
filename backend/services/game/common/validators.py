import uuid


def is_valid_uuid4(uuid_str: str) -> bool:
    try:
        uuid_obj = uuid.UUID(uuid_str, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_str
