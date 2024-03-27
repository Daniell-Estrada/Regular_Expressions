from models.automata import Automata
from utilities.state import State


class NFA(Automata):
    """
    Represents a Non-Deterministic Finite Automaton (NFA).

    Inherits from the Automata class.
    """

    def __init__(self, *args, **kwargs):
        args = list(args)
        temp = kwargs.get("f_states") or args[-2]

        kwargs["f_states"] = isinstance(temp, State) and [temp] or temp
        super().__init__(*tuple(args), **kwargs)

    @property
    def f_state(self) -> State:
        """
        Returns the initial/final state of the NFA.

        Returns:
            State: The initial/final state of the NFA.
        """
        return self.f_states[0]
