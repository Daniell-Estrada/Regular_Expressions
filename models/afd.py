from models.tree import Tree
from utilities.state import State
from utilities.symbol import Symbol
from utilities.transition import Transition


class AFD:
    states: list[State] = []
    initial_state: State = None
    final_states: list[State] = []
    trans: list[Transition] = []

    def __init__(self, alphabet: dict[int, Symbol], tree: Tree):
        epsilon = Symbol("ε")
        alphabet.pop(epsilon.ord, None)

        self.alphabet = alphabet
        self.tree = tree

        self.config()

    def config(self):
        base_states = []
        unverified_states = []
        current_states = []
        initial = self.tree.root.first_pos

        if self.tree.last_pos in initial:
            new_state = State(0, 3)
        else:
            new_state = State(0, 1)

        self.initial_state = new_state
        self.states.append(new_state)
        base_states.append(initial)
        unverified_states.append(initial)

        while unverified_states:
            current_states = unverified_states.pop()

            for v in self.alphabet.values():
                next_state = []
                for pos in current_states:
                    if self.tree.pos_symbol.get(pos).value == v.value:
                        for add_pos in self.tree.follow_pos.get(pos):
                            if add_pos not in next_state:
                                next_state.append(add_pos)

                if next_state:
                    if next_state in base_states:
                        origin = base_states.index(current_states)
                        destiny = base_states.index(next_state)
                        new_trans = Transition(self.states[origin],
                                               v, self.states[destiny])

                        if new_trans not in self.trans:
                            self.trans.append(new_trans)
                    else:
                        base_states.append(next_state)
                        unverified_states.append(next_state)
                        origin = base_states.index(current_states)
                        destiny = base_states.index(next_state)

                        if self.tree.last_pos in next_state:
                            new_state = State(destiny, 3)
                        else:
                            new_state = State(destiny, 2)

                        self.states.append(new_state)
                        new_trans = Transition(
                            self.states[origin], v, new_state)

                        if new_trans not in self.trans:
                            self.trans.append(new_trans)

    def __str__(self) -> str:
        return f'''Symbols: {self.alphabet.values()}
        \rStates: {self.states}
        \rTransitions: {self.trans}
        \rInital State: {self.initial_state}
        \rAccepting States: {self.final_states}
    '''
