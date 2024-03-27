from interfaces.automata_interface import AutomataInterface
from models.automata import Automata
from models.dfa import DFA
from models.nfa import NFA
from models.tree import Tree
from utilities.infix_postfix import InfixPostFix
from utilities.tompson import Thompson
from views.automata_view import AutomataView


class AutomataController:
    """
    Controller class for managing automata operations.

    Args:
        model (Automata): The automata model.
        view (AutomataView): The automata view.

    Attributes:
        connection (AutomataInterface): The automata interface for database connection.
        model (Automata): The automata model.
        view (AutomataView): The automata view.
        regex (str): The regular expression.
        automata (Automata): The automata object.
        nfa (NFA): The NFA object.
        dfa (DFA): The DFA object.
    """

    def __init__(self, model: Automata, view: AutomataView) -> None:
        self.connection = AutomataInterface()
        self.model = model
        self.view = view
        self.regex = str(self.view.entry_regex).strip()
        self.automata = Automata()
        self.nfa: NFA
        self.dfa: DFA

    def get_automata(self, regex: str):
        """
        Retrieves the automata from the database or generates a new one based on the given regular expression.

        Args:
            regex (str): The regular expression.

        Raises:
            Exception: If there is an error retrieving or generating the automata.

        Returns:
            None
        """
        try:
            automata = self.connection.select_automata(regex)
            if automata:
                self.nfa = self.automata.from_hex(automata[0][0])
                self.dfa = self.automata.from_hex(automata[0][1])
            else:
                self.base_automata(regex)
                hexs = (self.nfa.to_hex(), self.dfa.to_hex())
                self.connection.insert_automata((regex, *hexs))
        except Exception as e:
            self.view.open_toplevel("Error", str(e))

    def base_automata(self, regex: str):
        """
        Generates the base automata based on the given regular expression.

        Args:
            regex (str): The regular expression.

        Returns:
            None
        """
        ipt = InfixPostFix(regex)
        stack = ipt.convert()

        apha = ipt.stack
        tree = Tree(stack)
        thompson = Thompson(apha)
        self.nfa = thompson.subset_construction(tree.root)
        self.dfa = DFA(apha, self.nfa).minimize()

    def get_type_automata(self, regex: str, aut_type: str):
        """
        Retrieves the specified type of automata (NFA or DFA) based on the given regular expression.

        Args:
            regex (str): The regular expression.
            aut_type (str): The type of automata to retrieve ("NFA" or "DFA").

        Returns:
            None
        """

        if regex.strip() != self.regex.strip():
            self.get_automata(regex)

        if aut_type == "NFA":
            self.automata = self.nfa
        elif aut_type == "DFA":
            self.automata = self.dfa

    def draw_automata(self):
        """
        Draws the automata and saves the image.
        """
        aut_id = self.automata.draw()
        self.view.img_automata = f"/tmp/automata_{aut_id}.png"
