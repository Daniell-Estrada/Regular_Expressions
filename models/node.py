from utilities.symbol import Symbol


class Node:
    """
    Represents a node in a regular expression tree.

    Attributes:
        _symbol (Symbol): The symbol associated with the node.
        _left (Node): The left child node.
        _right (Node): The right child node.
        _first_pos (set[list[int]]): The set of positions where the node's symbol can occur first.
        _last_pos (set[list[int]]): The set of positions where the node's symbol can occur last.
        _nullable (bool): Indicates whether the node is nullable or not.
        position (int): The position of the node in the tree.

    """

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
        """
        Adds a position to the set of first positions.

        Args:
            pos (list[int]): The position to add.

        """
        self.first_pos.update(pos)

    def add_last_pos(self, pos: list[int]):
        """
        Adds a position to the set of last positions.

        Args:
            pos (list[int]): The position to add.

        """
        self.last_pos.update(pos)

    def position_is_null(self):
        """
        Checks if the position of the node is null.

        Returns:
            bool: True if the position is null, False otherwise.

        """
        return self.position < 0

    def is_leaf(self):
        """
        Checks if the node is a leaf node.

        Returns:
            bool: True if the node is a leaf node, False otherwise.

        """
        return not (self.left or self.right)
