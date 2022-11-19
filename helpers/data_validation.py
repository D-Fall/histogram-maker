def validate_int(string: str) -> int:
    if not string.isdigit():
        raise ValueError(f"String {string} need to be an integer.")

    return int(string)
