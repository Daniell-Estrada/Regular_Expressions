import regex as rx


def validate_regex(regex: str) -> bool:
    """
    Validates a regular expression.
    Args: regex (str): The regular expression to be validated.
    Returns: bool: True if the regular expression is valid, False otherwise.
    """
    regex_validator = rx.compile(r"(\w+|(\((?R)+\)))[+*?]?[+?]?(\|?(?R))?+")
    return bool(regex_validator.fullmatch(regex))
