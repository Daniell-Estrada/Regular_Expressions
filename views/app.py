import customtkinter as ctk

from controllers.automata_controller import AutomataController
from models.automata import Automata
from views.alert import Alert
from views.automata_view import AutomataView


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        try:
            self.configure()
            view = AutomataView(self)
            view.pack(expand=True, fill="both")
            model = Automata()
            controller = AutomataController(model, view)
            view.controller = controller

        except Exception as e:
            Alert(self, str(e))

    def configure(self, **kwargs):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.title("Regex to NFA and DFA")

        self.geometry("1000x550")
        self.minsize(1000, 550)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        return super().configure(**kwargs)
