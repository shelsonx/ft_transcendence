from .str_is_empty_or_none import is_string_empty_or_none


def has_value(value):
    if isinstance(value, str):
        return not is_string_empty_or_none(value)
    return value is not None
