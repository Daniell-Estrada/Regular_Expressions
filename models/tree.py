from models.node import Node
from utilities.symbol import Symbol


class Tree:
    def __init__(self, regex_postfix: list[Symbol]):
        self._root: Node = self.get_tree(regex_postfix)
        self._follow_pos: dict[int, list[int]] = {}
        self._pos_symbol: dict[int, Symbol] = {}
        self.new_pos = 0
        self.last_pos = 0

        self.gen_pos(self._root)
        self.gen_follow_pos(self._root)

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        self._root = value

    @property
    def follow_pos(self):
        return self._follow_pos

    @property
    def pos_symbol(self):
        return self._pos_symbol

    def get_tree(self, stack: list[Symbol]):
        nodes: list[Node] = []

        for s in stack:
            if not s.is_operator():
                node = Node(s)
                if node.symbol.value == "ε":
                    node.null = True
            else:
                if s.value in ["+", "*", "?"]:
                    node = Node(s, nodes.pop())

                    if s.value in ["*", "?"]:
                        node.null = True

                    if node.left and node.left.null:
                        node.null = True

                else:
                    right = nodes.pop()
                    left = nodes.pop()
                    node = Node(s, left, right)

                    if s.value == ".":
                        if left.null and right.null:
                            node.null = True

                    elif s.value == "|":
                        if left.null or right.null:
                            node.null = True

            nodes.append(node)

        return nodes.pop()

    def gen_pos(self, node: Node):
        if node:
            self.gen_pos(node.left)
            self.gen_pos(node.right)

            if node.symbol.is_operator():
                if node.symbol.value == ".":
                    if node.left.null:
                        node.add_first_pos(node.left.first_pos)
                        node.add_first_pos(node.right.first_pos)
                    else:
                        node.add_first_pos(node.left.first_pos)

                    if node.right.null:
                        node.add_last_pos(node.left.last_pos)
                        node.add_last_pos(node.right.last_pos)
                    else:
                        node.add_last_pos(node.right.last_pos)

                elif node.symbol.value in ["+", "*", "?"]:
                    node.add_first_pos(node.left.first_pos)
                    node.add_last_pos(node.left.last_pos)

                elif node.symbol.value == "|":
                    node.add_first_pos(node.left.first_pos)
                    node.add_first_pos(node.right.first_pos)

                    node.add_last_pos(node.left.last_pos)
                    node.add_last_pos(node.right.last_pos)

            elif node.symbol.value == "$":
                self.new_pos += 1
                node.first_pos.add(self.new_pos)
                node.last_pos.add(self.new_pos)
                node.position = self.new_pos

                self.follow_pos[self.new_pos] = []

                self.last_pos = self.new_pos
                self.pos_symbol[self.new_pos] = node.symbol

            elif node.symbol.value == "ε":
                self.follow_pos[self.new_pos] = []

            else:
                self.new_pos += 1
                node.first_pos.add(self.new_pos)
                node.last_pos.add(self.new_pos)
                node.position = self.new_pos

                self.follow_pos[self.new_pos] = []
                self.pos_symbol[self.new_pos] = node.symbol

    def gen_follow_pos(self, node: Node):
        if node:
            self.gen_follow_pos(node.left)
            self.gen_follow_pos(node.right)

            if node.symbol.value == '.':
                for i in node.left.last_pos:
                    for j in node.right.first_pos:
                        if j not in self.follow_pos.get(i):
                            self.follow_pos[i].append(j)

            elif node.symbol.value in ['+', '*']:
                for i in node.last_pos:
                    for j in node.first_pos:
                        if j not in self.follow_pos.get(i):
                            self.follow_pos[i].append(j)

    def show_tree(self, node: Node):
        if node:
            self.show_tree(node.left)
            self.show_tree(node.right)

            res = '[' + node.symbol.value
            if not node.position_is_null():
                res += f', ({node.position})'

            res += ", {"
            for i in node.first_pos:
                res += f'{i}, '
            res += "}"

            res += ", {"
            for i in node.last_pos:
                res += f'{i}, '
            res += "}"

            if not node.symbol.is_operator():
                if not node.position_is_null():
                    res += ", ["
                    for i in self.follow_pos.get(node.position):
                        res += f'{i}, '
                    res += ']'

            if node.null:
                res += ', nullable'
            else:
                res += ', not nullable'

            res += ']'
            print(res)
