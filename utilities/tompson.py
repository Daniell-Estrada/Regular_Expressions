from models.nfa import NFA
from models.node import Node
from utilities.state import State, Type
from utilities.symbol import Symbol
from utilities.transition import Transition


class Thompson:
    def __init__(self, alpha: dict[int, Symbol]) -> None:
        self.alpha = alpha
        self.num_states = 0
        self.epsilon = Symbol("ε")

    def _set_trans(self, o_state: State, f_state: State) -> Transition:
        return Transition(o_state, self.epsilon, f_state)

    def _pos_child(self, states: list[State], typ: Type, _v=0) -> int:
        return next((i for i, v in enumerate(states) if v.typ == typ), _v)

    def subset_construction(self, node: Node):
        o_new_state = State(self.num_states, 1)
        f_new_state = State(self.num_states + 1, 3)

        if node.is_leaf() or node.symbol.value in "*?|":
            self.num_states += 2

        if node.is_leaf():
            new_trans = Transition(o_new_state, node.symbol, f_new_state)
            states = [o_new_state, f_new_state]
            trans = [new_trans]

            return NFA(self.alpha, states, o_new_state, f_new_state, trans)

        if not node.right:
            nfa = self.subset_construction(node.left)
            c_states = nfa.states
            states = [*c_states]
            trans = [*nfa.trans]

            i_pos = self._pos_child(c_states, Type.INITIAL)
            f_pos = self._pos_child(c_states, Type.FINAL, -1)

            if node.symbol.value in "*?":
                for v in c_states:
                    if v.typ in [Type.INITIAL, Type.FINAL]:
                        v.typ = Type.TRANS

                skip = self._set_trans(o_new_state, f_new_state)
                first = self._set_trans(o_new_state, c_states[i_pos])
                last = self._set_trans(c_states[f_pos], f_new_state)

                trans.extend([skip, first, last])
                states = [o_new_state, *c_states, f_new_state]

            if node.symbol.value in "*+":
                back = Transition(c_states[f_pos], self.epsilon, c_states[i_pos])
                trans.extend([back])

            if node.symbol.value == "+":
                o_new_state, f_new_state = nfa.i_state, nfa.f_state

            return NFA(self.alpha, states, o_new_state, f_new_state, trans)

        left = self.subset_construction(node.left)
        right = self.subset_construction(node.right)

        if node.symbol.value == "|":
            states_left = left.states
            states_right = right.states

            states = [o_new_state, *states_left, *states_right, f_new_state]

            for v in states_left:
                if v.typ in [Type.INITIAL, Type.FINAL]:
                    v.typ = Type.TRANS

            for v in states_right:
                if v.typ in [Type.INITIAL, Type.FINAL]:
                    v.typ = Type.TRANS

            trans = [*left.trans, *right.trans]

            i_pos_left = self._pos_child(states_left, Type.INITIAL)
            f_pos_left = self._pos_child(states_left, Type.FINAL, -1)

            i_pos_right = self._pos_child(states_right, Type.INITIAL)
            f_pos_right = self._pos_child(states_right, Type.FINAL, -1)

            begin_or_p1 = self._set_trans(o_new_state, states_left[i_pos_left])
            begin_or_p2 = self._set_trans(o_new_state, states_right[i_pos_right])

            end_or_p1 = self._set_trans(states_left[f_pos_left], f_new_state)
            end_or_p2 = self._set_trans(states_right[f_pos_right], f_new_state)

            trans.extend([begin_or_p1, begin_or_p2, end_or_p1, end_or_p2])

            return NFA(self.alpha, states, o_new_state, f_new_state, trans)

        first_state = left.i_state
        last_state = right.f_state

        states_left = left.states
        states_right = right.states
        states = [*states_left, *states_right]

        i_pos = self._pos_child(states_right, Type.INITIAL)
        f_pos = self._pos_child(states_left, Type.FINAL, -1)

        for v in states_left:
            if v.typ == Type.FINAL:
                v.typ = Type.TRANS

        for v in states_right:
            if v.typ == Type.INITIAL:
                v.typ = Type.TRANS

        dot = self._set_trans(states_left[f_pos], states_right[i_pos])
        trans = [*left.trans, *right.trans, dot]

        return NFA(self.alpha, states, first_state, last_state, trans)
