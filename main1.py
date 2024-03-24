import networkx as nx
import matplotlib.pyplot as plt

import re

import regex as rx


def main():
    regex = "ab*"
    dfa = {
        'Q': ['q0', 'q1', 'q2', 'q3'],
        'S': ['a', 'b', 'c'],
        'D': {
            'q0': {'a': 'q1', 'b': 'q0'},
            'q1': {'a': 'q1', 'b': 'q2'},
            'q2': {'a': 'q1', 'b': 'q0', 'c': 'q3'},
            'q3': {},
        },
        'q0': 'q0',
        'F': ['q2', 'q3']
    }
    G = nx.MultiGraph()

    G.add_nodes_from(dfa['Q'])

    for q, t in dfa['D'].items():
        for s, q_ in t.items():
            print(q, s, q_)
            G.add_edge(q, q_, label=s)

    pos = nx.spring_layout(G)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='black')
    nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), node_color='r', node_size=500)
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

    plt.axis('off')
    plt.show()


def build_automaton(rgx):
    tns = find_transitions(rgx)
    return {
        'Q': tns.keys(),
        'S': re.findall(r'\w', rgx),
        'D': tns,
        'q0': 'q0',
        'F': list(tns.keys())[-1]
    }


def find_transitions(rgx: str, ste=0, tns={}):
    '''
        "q0": {"a": "q1"},
        "q1": {"b": "q2"},
        "q2": {"c": "q3"},
    '''

    for c in rgx:
        if c == '*':
            tns[f'q{ste}'] = find_transitions(rgx[:1], ste, tns)

        elif c.isalpha():
            tns[f'q{ste}'] = {c: f'q{ste + 1}'}
    return tns


if __name__ == "__main__":
    main()
    #rgx = "ab*"
    #print(find_transitions(rgx[::1]))
