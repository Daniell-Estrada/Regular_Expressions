import re


class Symbol:
    def __init__(self, value: str):
        """
        Initializes a new Symbol object.

        Args:
            value (str): The value of the symbol.

        Attributes:
            value (str): The value of the symbol.
            ord (int): The ASCII value of the symbol.
        """
        self.value = value
        self.ord = ord(value)

    def is_operator(self) -> bool:
        """
        Checks if the symbol is an operator.

        Returns:
            bool: True if the symbol is an operator, False otherwise.
        """
        return bool(re.fullmatch(r"[.()|*+?]", self.value))

    def json(self):
        """
        Converts the symbol to a JSON object.

        Returns:
            dict: A dictionary representation of the symbol.
        """
        return {"value": self.value, "ord": self.ord}

    @staticmethod
    def from_json(data: dict):
        """
        Creates a Symbol object from a JSON object.

        Args:
            data (dict): The JSON object representing the symbol.

        Returns:
            Symbol: The Symbol object created from the JSON object.
        """
        return Symbol(data["value"])
