import json
from abc import ABC

from graphviz import Graph

from utilities.state import State
from utilities.symbol import Symbol
from utilities.transition import Transition


class Automata(ABC):
    """
    Represents an abstract base class for automata.

    Attributes:
        alpha (dict[int, Symbol]): The alphabet of the automata.
        states (list[State]): The list of states in the automata.
        i_state (State): The initial state of the automata.
        f_states (list[State]): The list of final states in the automata.
        trans (list[Transition]): The list of transitions in the automata.
    """

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
        """
        Reorganizes the states of the automata.

        This method sorts the states based on their IDs and assigns new IDs to the states.
        """
        self.states.sort(key=lambda s: s.id)
        for i, s in enumerate(self.states):
            s.id = f"S{i}"

    def json(self) -> dict:
        """
        Converts the automata to a JSON representation.

        Returns:
            dict: The JSON representation of the automata.
        """
        self.reorganize()

        return {
            "alpha": self.alpha,
            "states": self.states,
            "trans": self.trans,
            "i_state": self.i_state,
            "f_states": self.f_states,
        }

    def to_hex(self) -> str:
        """
        Converts the automata to a hexadecimal string.

        Returns:
            str: The hexadecimal representation of the automata.
        """
        try:
            return (
                json.dumps(self.json(), default=lambda o: o.json(), ensure_ascii=False)
                .encode("utf-8")
                .hex()
            )

        except Exception as e:
            print(e)
        return ""

    def from_hex(self, hexs: str):
        """
        Creates an automata from a hexadecimal string.

        Args:
            hexs (str): The hexadecimal representation of the automata.
        """
        try:
            data = json.loads(bytes.fromhex(hexs).decode("utf-8"))
            alpha = data["alpha"]
            states = [State.from_json(s) for s in data["states"]]
            i_state = State.from_json(data["i_state"])
            f_states = [State.from_json(f) for f in data["f_states"]]
            trans = [Transition.from_json(t) for t in data["trans"]]

            return Automata(alpha, states, i_state, f_states, trans)

        except Exception as e:
            print(e)

    def draw(self):
        """
        Draws the automata using the Graphviz library.

        This method generates a visual representation of the automata and saves it as a PNG image.
        """
        attr_node = {"color": "white", "fontcolor": "white"}
        attr_label = {
            "color": "white",
            "fontcolor": "white",
            "dir": "forward",
            "arrowhead": "vee",
        }

        try:
            automata = Graph("Automata", format="svg")
            automata.attr(fontname="Ubuntu")
            automata.attr(rankdir="LR")
            automata.attr(bgcolor="transparent")
            automata.attr(dpi="300")
            automata.attr(fontsize="8")
            automata.attr("node", **attr_node)
            automata.attr("edge", **attr_label)

            automata.node("initial", shape="point", width=".1", height=".1")
            automata.edge("initial", f"{self.i_state.id}", label="Start")

            for state in self.states:
                is_fs = state.id in [s.id for s in self.f_states]

                automata.node(
                    f"{state.id}", shape="doublecircle" if is_fs else "circle"
                )

            for t in self.trans:
                automata.edge(
                    f"{t.origin.id}", f"{t.destiny.id}", label=f"{t.symbol.value}"
                )

            automata.render(f"/tmp/automata_{hash(self)}", format="png", view=False)
            return hash(self)
        except Exception as e:
            print(e)
