from enum import Enum


class Type(Enum):
    INITIAL = 1
    TRANS = 2
    FINAL = 3


class State:
    """
    Represents a state in a finite automaton.

    Attributes:
        id (int): The unique identifier of the state.
        typ (Type): The type of the state (initial, final, or intermediate).

    Methods:
        is_final(): Checks if the state is a final state.
        compare(__o: object) -> int: Compares the state with another state.
        json(): Returns the state as a JSON object.
        from_json(data: dict): Creates a state object from a JSON object.
    """

    def __init__(self, id, typ: int):
        self.id = id
        self.typ: Type = Type(typ)

    def is_final(self):
        """
        Checks if the state is a final state.

        Returns:
            bool: True if the state is a final state, False otherwise.
        """
        return self.typ == Type.FINAL

    def compare(self, __o: object) -> int:
        """
        Compares the state with another state.

        Args:
            __o (object): The state object to compare with.

        Returns:
            int: 1 if the current state is greater than the other state,
                 -1 if the current state is less than the other state,
                 0 if the states are equal or cannot be compared.
        """
        if isinstance(__o, State):
            return {
                self.id > __o.id: 1,
                self.id < __o.id: -1,
            }.get(True, 0)
        return 0

    def json(self):
        """
        Returns the state as a JSON object.

        Returns:
            dict: The state represented as a JSON object.
        """
        return {"id": self.id, "type": self.typ.name}

    @staticmethod
    def from_json(data: dict):
        """
        Creates a state object from a JSON object.

        Args:
            data (dict): The JSON object representing the state.

        Returns:
            State: The state object created from the JSON object.
        """
        return State(data["id"], Type[data["type"]])
