from collections import deque
from multipledispatch import dispatch

from models.automata import Automata
from models.nfa import NFA
from utilities.state import State
from utilities.symbol import Symbol
from utilities.transition import Transition


class DFA(Automata):
    @dispatch(dict)
    def __init__(self, alpha: dict[int, Symbol]):
        super().__init__(alpha=alpha)

    @dispatch(dict, NFA)
    def __init__(self, alpha: dict[int, Symbol], nfa: NFA):
        super().__init__(alpha=alpha, nfa=nfa)
        epsilon = Symbol("ε")
        self.alpha.pop(epsilon.ord, None)

        self.config()

    @property
    def nfa(self) -> NFA:
        return getattr(self, "__nfa")

    @property
    def i_state(self) -> State:
        return getattr(self, "__i_state")

    @i_state.setter
    def i_state(self, value):
        setattr(self, "__i_state", value)

    def add_state(self, state: State, is_final: bool = False):
        if state:
            if state not in self.states:
                self.states.append(state)

            if is_final:
                self.f_states.append(state)

    def add_transition(self, origin: State, symbol: Symbol, destiny: State):
        if all([origin, symbol, destiny]):
            tran = Transition(origin, symbol, destiny)
            if tran not in self.trans:
                self.trans.append(tran)

    def move(self, nfa: NFA, current: list[State], symbol: Symbol) -> list[State]:
        next_states = []

        for s in current:
            for t in nfa.trans:
                if s.id == t.origin.id and t.symbol.value == symbol.value:
                    if t.destiny not in next_states:
                        next_states.append(t.destiny)

        return next_states

    def move_state(self, state: State, v: str) -> State | None:
        for t in self.trans:
            if t.origin.id == state.id and t.symbol.value == v:
                return t.destiny

    def e_closure(self, nfa: NFA, current: list[State]) -> list[State]:
        e_states = current

        while True:
            new_states = []
            for s in e_states:
                for t in nfa.trans:
                    if t.origin.id == s.id and t.symbol.value == "ε":
                        if t.destiny not in e_states and t.destiny not in new_states:
                            new_states.append(t.destiny)

            if not new_states:
                break

            e_states.extend(new_states)

        return e_states

    def config(self):
        current_states = self.e_closure(self.nfa, [self.nfa.i_state])
        base_states = [current_states]
        unverified_states = [current_states]

        if self.nfa.f_state in current_states:
            self.i_state = State(0, 3)
            self.f_states.append(self.i_state)
        else:
            self.i_state = State(0, 1)

        self.states.append(self.i_state)

        while unverified_states:
            current_states = unverified_states.pop()

            for v in self.alpha.values():
                move_res = self.move(self.nfa, current_states, v)
                move_res = self.e_closure(self.nfa, move_res)

                if move_res not in base_states:
                    if move_res:
                        base_states.append(move_res)
                        unverified_states.append(move_res)

                        new_state = State(
                            len(base_states) - 1,
                            self.nfa.f_state in move_res and 3 or 1,
                        )

                        if self.nfa.f_state in move_res:
                            self.f_states.append(new_state)

                        self.states.append(new_state)
                        i_s = base_states.index(current_states)
                        f_s = base_states.index(move_res)
                        tran = Transition(
                            self.states[i_s], v, self.states[f_s])

                        self.trans.append(tran)
                else:
                    i_s = base_states.index(current_states)
                    f_s = base_states.index(move_res)
                    tran = Transition(self.states[i_s], v, self.states[f_s])

                    if tran not in self.trans:
                        self.trans.append(tran)

    def minimize(self):
        accept_states = set(self.f_states)
        reject_states = set(self.states).difference(accept_states)

        partitions = [accept_states, reject_states]
        worklist = deque([accept_states, reject_states])

        while worklist:
            partition = worklist.popleft()

            for a in self.alpha.values():
                trans = {}

                for state in partition:
                    next_state = self.move_state(state, a.value)
                    sub = trans.get(next_state, set())
                    sub.add(state)
                    trans[next_state] = sub

                for t in trans.values():
                    if len(t) < len(partition):
                        partitions.remove(partition)
                        partitions.append(t)
                        worklist.append(t)

        state_map = {}
        start_state = self.i_state

        for part in partitions:
            if part:
                rep = next(iter(part))
                for state in part:
                    state_map[state] = rep

                if start_state in part:
                    start_state = rep

        minimized = DFA(self.alpha)
        minimized.i_state = start_state

        for part in partitions:
            if part:
                rep = next(iter(part))
                is_accept = any(state in accept_states for state in part)
                minimized.add_state(rep, is_accept)

                for a in self.alpha.values():
                    next_state = self.move_state(rep, a.value)
                    mapped_state = state_map.get(next_state)
                    minimized.add_transition(rep, a, mapped_state)

        return minimized
