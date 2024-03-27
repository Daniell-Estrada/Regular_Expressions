from customtkinter import CTkLabel, CTkToplevel


class Alert(CTkToplevel):
    def __init__(self, master, message: str) -> None:
        super().__init__(master)
        self.title("Alert")
        self.geometry("200x100")
        self.resizable(False, False)
        self.minsize(200, 100)
        self.maxsize(200, 100)

        self.label = CTkLabel(self, text=message, font=("ubuntu", 18))
        self.label.pack(expand=True, fill="both", padx=10, pady=10)
        self.wait_visibility()
        self.grab_set()
        self.wait_window()
