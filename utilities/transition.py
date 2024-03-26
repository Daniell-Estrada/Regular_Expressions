from utilities.state import State
from utilities.symbol import Symbol


class Transition:
    def __init__(self, origin: State, symbol: Symbol, destiny: State):
        self._origin: State = origin
        self._symbol: Symbol = symbol
        self._destiny: State = destiny

    @property
    def origin(self):
        return self._origin

    @property
    def symbol(self):
        return self._symbol

    @property
    def destiny(self):
        return self._destiny

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Transition):
            return (
                self.origin.id == __o.origin.id
                and self.symbol.value == __o.symbol.value
                and self.destiny.id == __o.destiny.id
            )
        return False

    def json(self):
        return {
            "origin": f"S{self.origin.id}",
            "symbol": self.symbol.value,
            "destiny": f"S{self.destiny.id}",
        }
