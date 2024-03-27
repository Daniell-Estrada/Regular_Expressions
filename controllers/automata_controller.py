from PIL import Image

from models.automata import Automata
from models.dfa import DFA
from models.tree1 import Tree
from utilities.infix_postfix import InfixPostFix
from utilities.tompson import Thompson
from views.automata_view import AutomataView


class AutomataController:
    def __init__(self, model: Automata, view: AutomataView) -> None:
        self.model = model
        self.view = view
        self.regex = str(self.view.entry_regex).strip()
        self.automata = Automata()
        self.nfa = None
        self.dfa = None

    def get_automata(self, regex: str):
        try:
            automata = self.model.get_automata(regex)
            if automata:
                self.nfa = automata.nfa
                self.dfa = automata.dfa
            else:
                self.base_automata(regex)

        except Exception as e:
            self.view.open_toplevel(str(e))

    def base_automata(self, regex: str):
        ipt = InfixPostFix(regex)
        stack = ipt.convert()

        apha = ipt.stack
        tree = Tree(stack)
        thompson = Thompson(apha)
        self.nfa = thompson.subset_construction(tree.root)
        self.dfa = DFA(apha, self.nfa).minimize()

    def get_type_automata(self, regex: str, aut_type: str):
        regex = regex.strip()

        if regex != self.regex:
            self.get_automata(regex)

        if aut_type == "NFA":
            self.automata = self.nfa
        elif aut_type == "DFA":
            self.automata = self.dfa

    def draw_automata(self):
        self.automata.draw()
        aut_id = hash(self.automata)
        self.view.img_automata = self.get_image(aut_id)

    def get_image(self, name):
        return Image.open(f"/tmp/automata_{name}.png")
