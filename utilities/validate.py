# Description: This file contains the functions that validate the input of the user.
import regex as rx


def validate_regex(regex: str) -> bool:
    regex_validator = rx.compile(r"(\w+|(\((?R)+\)))[+*?]?[+?]?(\|?(?R))?+")
    return bool(regex_validator.fullmatch(regex))
