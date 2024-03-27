from copy import deepcopy

from utilities.symbol import Symbol


class InfixPostFix:
    """
    Converts an infix regular expression to postfix notation.
    """

    def __init__(self, regex: str):
        """
        Initializes an instance of the InfixPostFix class.

        Args:
            regex (str): The infix regular expression to convert.
        """
        self._regex = regex

        epsilon = Symbol("ε")
        self.stack: dict[int, Symbol] = {epsilon.ord: epsilon}

    @property
    def regex(self):
        """
        Gets or sets the infix regular expression.

        Returns:
            str: The infix regular expression.
        """
        return self._regex

    @regex.setter
    def regex(self, value: str):
        """
        Sets the infix regular expression.

        Args:
            value (str): The infix regular expression to set.
        """
        self._regex = value

    def convert(self):
        """
        Converts the infix regular expression to postfix notation.

        Returns:
            list[Symbol]: The postfix notation of the regular expression.
        """
        stack: list[Symbol] = []
        postfix: list[Symbol] = []

        data = self.convert_symbols(self.regex)
        data = self.add_concat(data)

        for s in data:
            if s.value.isalnum() or s.value == "ε":
                postfix.append(s)

            elif s.value == "(":
                stack.append(s)

            elif s.value == ")":
                while stack and stack[-1].value != "(":
                    postfix.append(stack.pop())

                stack.pop()

            else:
                while stack and self.pre(s) <= self.pre(stack[-1]):
                    postfix.append(stack.pop())
                stack.append(s)

        while stack:
            postfix.append(stack.pop())

        return postfix

    def convert_symbols(self, regex: str) -> list[Symbol]:
        """
        Converts the characters in the infix regular expression to Symbol objects.

        Args:
            regex (str): The infix regular expression.

        Returns:
            list[Symbol]: The list of Symbol objects representing the infix regular expression.
        """
        infix = []

        for c in regex:
            symbol = Symbol(c)
            infix.append(symbol)

            if not (self.stack.get(symbol.ord) or symbol.is_operator()):
                self.stack[symbol.ord] = symbol

        return infix

    def add_concat(self, data: list[Symbol]) -> list[Symbol]:
        """
        Adds the concatenation operator (.) to the infix regular expression.

        Args:
            data (list[Symbol]): The list of Symbol objects representing the infix regular expression.

        Returns:
            list[Symbol]: The list of Symbol objects with the concatenation operator added.
        """
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
        """
        Returns the precedence of the given symbol.

        Args:
            symbol (Symbol): The symbol to get the precedence for.

        Returns:
            int: The precedence value.
        """
        return dict(zip("*+?|.", [3, 3, 3, 2, 1])).get(symbol.value, -1)
