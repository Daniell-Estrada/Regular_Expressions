from abc import ABC

from models.tree import Tree
from utilities.state import State
from utilities.symbol import Symbol
from utilities.transition import Transition


class Automata(ABC):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        data = {"alpha": {}, "states": [],
                "i_state": None, "f_states": [], "trans": []}

        data.update(zip(data.keys(), args))
        data.update(kwargs)

        for k, v in data.items():
            setattr(self, f"__{k}", v)

    @property
    def alpha(self) -> dict[int, Symbol]:
        return getattr(self, "__alpha")

    @property
    def states(self) -> list[State]:
        return getattr(self, "__states")

    @property
    def i_state(self) -> State:
        return getattr(self, "__i_state")

    @property
    def f_states(self) -> list[State]:
        return getattr(self, "__f_states")

    @property
    def trans(self) -> list[Transition]:
        return getattr(self, "__trans")

    @i_state.setter
    def i_state(self, value):
        setattr(self, "__i_state", value)

    def convert_tran(self):
        data = {}

        for t in self.trans:
            orgn, symb, dest = t.json().values()

            if orgn in data:
                if symb in data[orgn]:
                    data[orgn][symb] = {dest, *data[orgn][symb]}

                else:
                    data[orgn][symb] = {dest}

            else:
                data[orgn] = {symb: {dest}}

        return data

    def json(self) -> dict:
        states = set([f"S{i}" for i in self.states])
        alphabet = sorted([s.value for s in self.alpha.values()])

        return {
            "Q": states,
            "S": alphabet,
            "D": self.convert_tran(),
            "S0": f"S{self.i_state}",
            "F": [f"S{i}" for i in self.f_states],
        }
