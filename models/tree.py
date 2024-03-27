from models.node import Node
from utilities.symbol import Symbol


class Tree:
    """
    Represents a tree structure for regular expressions.

    Attributes:
        _root (Node): The root node of the tree.

    Methods:
        __init__(self, stack: list[Symbol]): Initializes a Tree object.
        gen_tree(self, stack: list[Symbol]) -> Node: Generates the tree structure from a stack of symbols.
        show_tree(self, node: Node): Prints the tree structure in post-order traversal.
    """

    def __init__(self, stack: list[Symbol]):
        """
        Initializes a Tree object.

        Args:
            stack (list[Symbol]): A stack of symbols representing a regular expression.
        """
        self._root: Node = self.gen_tree(stack)

    @property
    def root(self) -> Node:
        """
        Returns the root node of the tree.

        Returns:
            Node: The root node of the tree.
        """
        return self._root

    def gen_tree(self, stack: list[Symbol]) -> Node:
        """
        Generates the tree structure from a stack of symbols.

        Args:
            stack (list[Symbol]): A stack of symbols representing a regular expression.

        Returns:
            Node: The root node of the generated tree.
        """
        nodes: list[Node] = []

        for v in stack:
            if not v.is_operator():
                nodes.append(Node(v))
            else:
                if v.value in ["+", "*", "?"]:
                    nodes.append(Node(v, nodes.pop()))
                else:
                    right = nodes.pop()
                    left = nodes.pop()
                    nodes.append(Node(v, left, right))

        return nodes.pop()

    def show_tree(self, node: Node):
        """
        Prints the tree structure in post-order traversal.

        Args:
            node (Node): The current node being traversed.
        """
        if node:
            self.show_tree(node.left)
            self.show_tree(node.right)
            print(node.symbol.value)
