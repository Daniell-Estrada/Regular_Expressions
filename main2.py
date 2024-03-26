import matplotlib.pyplot as plt
import networkx as nx

from models.dfa import DFA
from models.tree1 import Tree
from utilities.infix_postfix import InfixPostFix
from utilities.symbol import Symbol
from utilities.tompson import Thompson


def main():
    regex = "a|b" 
    concat = Symbol(".")
    end_symbol = Symbol("$")

    ipt = InfixPostFix(regex)
    stack = ipt.convert()
    # stack.append(end_symbol)
    # stack.append(concat)
    aphabet = ipt.stack

    tree = Tree(stack)
    tree.show_tree(tree.root)

    thompson = Thompson(aphabet)
    nfa = thompson.subset_construction(tree.root)
    dfa_trans = DFA(aphabet, nfa).minimize()
    #print(nfa.json())
    print(dfa_trans.json())
    # dfa = DFA(aphabet, tree)
    # print(dfa.json())

    G = nx.MultiGraph()

    G.add_nodes_from(dfa_trans.states)

    """
        'D' {
            'q0': {'a': 'q1', 'b': 'q0'},
            'q1': {'a': 'q1', 'b': 'q2'},
            'q2': {'a': 'q1', 'b': 'q0', 'c': 'q3'},
            'q3': {},
        },
    """
    G.add_edges_from([(t.origin, t.destiny) for t in dfa_trans.trans])

    pos = nx.spring_layout(G)

    options = {
        "font_size": 10,
        "node_size": 500,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 5,
        "width": 5,
    }

    nx.draw_networkx(G, pos, with_labels=True, **options)
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels={(t.origin, t.destiny): t.symbol.value for t in dfa_trans.trans}
    )
    # Set margins for the axes so that nodes aren't clipped
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    main()


"""
states: list[State] = []
    i_state: State = None
    f_states: list[State] = []
    trans: list[Transition] = []

"""
