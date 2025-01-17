import customtkinter as ctk
from PIL import Image

from utilities.validate import validate_regex
from views.alert import Alert


class AutomataView(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk) -> None:
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.controller = None
        self.entry_regex = None
        self.toplevel_window = None
        self.img_automata: str
        self.content = None

        self.header()
        self.body()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def header(self):
        header = ctk.CTkFrame(self, height=80)
        header.pack(side="top", fill="x", padx=2, pady=(2, 3))

        self.entry = ctk.CTkEntry(
            header, width=50, font=("ubuntu", 13), placeholder_text="Enter a regex"
        )
        self.entry.pack(side="left", padx=10, pady=10, expand=True, fill="both")
        self.entry.bind("<Return>", self.on_return)

        btn_nfa = ctk.CTkButton(header, text="NFA", width=10)
        btn_nfa._command = lambda: self.on_automata("NFA")
        btn_nfa.pack(side="left", padx=(10, 5), pady=10)

        btn_dfa = ctk.CTkButton(header, text="DFA", width=10)
        btn_dfa._command = lambda: self.on_automata("DFA")
        btn_dfa.pack(side="left", padx=(5, 10), pady=10)

    def body(self):
        self.content = ctk.CTkFrame(self, fg_color="grey17")
        self.content.pack(side="bottom", fill="both", expand=True, padx=2, pady=(2, 3))
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

    def on_return(self, event):
        regex = event.widget.get()
        if not validate_regex(regex):
            self.open_toplevel("Invalid regex")
        else:
            self.entry_regex = regex
            self.on_automata("NFA")

    def on_automata(self, aut_type: str):
        if self.entry:
            self.entry_regex = self.entry.get()

        if not self.entry_regex:
            self.open_toplevel("Enter a regex")
            return

        self.controller.get_type_automata(self.entry_regex, aut_type)
        self.controller.draw_automata()
        self.show_automata()

    def show_automata(self):
        if self.content:
            for widget in self.content.winfo_children():
                widget.destroy()

        if self.img_automata:
            img = Image.open(self.img_automata)
            size = (self.content.winfo_width(), self.content.winfo_height())
            img = ctk.CTkImage(dark_image=Image.open(self.img_automata), size=size)
            lable = ctk.CTkLabel(
                self.content,
                text="",
                image=img,
                width=size[0],
                height=size[1],
            )
            lable.pack(side="left", fill="both", expand=True)
            # img_aut = ImagAutomata(self.master, self.content)
            # img_aut.set_image(self.img_automata)

    def open_toplevel(self, message: str):
        if self.toplevel_window:
            self.toplevel_window.destroy()

        self.toplevel_window = Alert(self, message)
