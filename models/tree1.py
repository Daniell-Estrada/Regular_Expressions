from models.node import Node
from utilities.symbol import Symbol


class Tree:
    def __init__(self, stack: list[Symbol]):
        self._root: Node = self.gen_tree(stack)

    @property
    def root(self) -> Node:
        return self._root

    def gen_tree(self, stack: list[Symbol]) -> Node:
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
        if node:
            self.show_tree(node.left)
            self.show_tree(node.right)
            print(node.symbol.value)
