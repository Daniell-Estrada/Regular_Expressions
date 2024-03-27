from abc import ABC

from graphviz import Graph

from models.tree import Tree
from utilities.state import State
from utilities.symbol import Symbol
from utilities.transition import Transition


class Automata(ABC):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        data = {"alpha": {}, "states": [], "i_state": None, "f_states": [], "trans": []}

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

    def reorganize(self):
        self.states.sort(key=lambda s: s.id)
        for i, s in enumerate(self.states):
            s.id = f"S{i}"

    def json(self) -> dict:
        self.reorganize()

        return {
            "Q": self.states,
            "S": self.alpha,
            "D": self.trans,
            "S0": self.i_state,
            "F": self.f_states,
        }

    def get_automata(self, regex: str):
        return None

    def draw(self):
        try:
            automata = Graph("Automata", format="svg")
            automata.attr(rankdir="LR")

            for state in self.states:
                automata.node(
                    f"{state.id}",
                    f"{state.id}",
                    shape="circle" if state not in self.f_states else "doublecircle",
                )

            for t in self.trans:
                automata.edge(f"{t.origin.id}", f"{t.destiny.id}", label=t.symbol.value)
        
            automata.render(f'/tmp/automata_{hash(self)}', format="png", view=False)
        
        except Exception as e:
            print(e)
