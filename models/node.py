from utilities.symbol import Symbol


class Node:
    def __init__(self, symbol: Symbol, left=None, right=None):
        self._symbol = symbol
        self._left: Node = left
        self._right: Node = right

        self._first_pos: set[list[int]] = set()
        self._last_pos: set[list[int]] = set()
        self._nullable = False
        self.position = -1

    @property
    def symbol(self):
        return self._symbol

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def first_pos(self):
        return self._first_pos

    @property
    def last_pos(self):
        return self._last_pos

    @symbol.setter
    def symbol(self, value):
        self._symbol = value

    @left.setter
    def left(self, value):
        self._left = value

    @right.setter
    def right(self, value):
        self._right = value

    @first_pos.setter
    def first_pos(self, value):
        self._first_pos = value

    @last_pos.setter
    def last_pos(self, value):
        self._last_pos = value

    @property
    def null(self):
        return self._nullable

    @null.setter
    def null(self, value):
        self._nullable = value

    def add_first_pos(self, pos: list[int]):
        self.first_pos.update(pos)

    def add_last_pos(self, pos: list[int]):
        self.last_pos.update(pos)

    def position_is_null(self):
        return self.position < 0

    def is_leaf(self):
        return not (self.left or self.right)
