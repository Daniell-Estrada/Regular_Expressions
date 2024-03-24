import re


class Symbol:
    def __init__(self, value: str):
        self.value = value
        self.ord = ord(value)

    def is_operator(self) -> bool:
        return re.fullmatch(r"[.()|*+?]", self.value)

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value
