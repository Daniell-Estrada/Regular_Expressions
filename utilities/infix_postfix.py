from copy import deepcopy

from utilities.symbol import Symbol


class InfixPostFix:
    def __init__(self, regex: str):
        self._regex = regex

        epsilon = Symbol('ε')
        self.stack: dict[int, Symbol] = {epsilon.ord: epsilon}

    @property
    def regex(self):
        return self._regex

    @regex.setter
    def regex(self, value: str):
        self._regex = value

    def convert(self):
        stack: list[Symbol] = []
        postfix: list[Symbol] = []

        data = self.convert_symbols(self.regex)
        data = self.add_concat(data)

        for s in data:
            if isinstance(s.value, int) or s.value.isalpha() or s.value == "ε":
                postfix.append(s)

            elif s.value == "(":
                stack.append(s)

            elif s.value == ")":
                while stack and stack[-1].value != "(":
                    postfix.append(stack.pop())

                stack.pop()

            else:
                while (stack and self.pre(s) <= self.pre(stack[-1])):
                    postfix.append(stack.pop())
                stack.append(s)

        while stack:
            postfix.append(stack.pop())

        return postfix

    def convert_symbols(self, regex: str) -> list[Symbol]:
        infix = []

        for c in regex:
            symbol = Symbol(c)
            infix.append(symbol)

            if not (self.stack.get(symbol.ord) or symbol.is_operator()):
                self.stack[symbol.ord] = symbol

        return infix

    def add_concat(self, data: list[Symbol]) -> list[Symbol]:
        concat = Symbol(".")
        temp = deepcopy(data)

        cont = 1
        for i in range(len(data) - 1):
            v = data[i]
            symb_next = data[i + 1]

            if v.is_operator() and v.value in ["*", "+", "?", ")"]:
                if not symb_next.is_operator() or symb_next.value in ["(", "ε"]:
                    temp.insert(i + cont, concat)
                    cont += 1
            elif not v.is_operator():
                if not symb_next.is_operator() or symb_next.value in ["(", "ε"]:
                    temp.insert(i + cont, concat)
                    cont += 1

        return temp

    def pre(self, symbol: Symbol) -> int:
        return dict(zip('*+?|.', [3, 3, 3, 2, 1])).get(symbol.value, -1)
