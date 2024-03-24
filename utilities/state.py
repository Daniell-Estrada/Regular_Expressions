from enum import Enum


class Type(Enum):
    INITIAL = 1
    TRANS = 2
    FINAL = 3


class State:
    def __init__(self, id, typ: int):
        self.id = id
        self.typ: Type = Type(typ)

    def is_final(self):
        return self.typ == Type.FINAL

    def compare(self, __o: object) -> int:
        if isinstance(__o, State):
            return {
                self.id > __o.id: 1,
                self.id < __o.id: -1,
            }.get(True, 0)
        return 0

    def __repr__(self) -> str:
        return f"{self.id}"

    def __str__(self) -> str:
        return f"{self.id}"
