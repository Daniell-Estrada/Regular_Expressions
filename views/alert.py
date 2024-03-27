from customtkinter import CTkLabel, CTkToplevel


class Alert(CTkToplevel):
    """
    A class representing an alert window.

    Args:
        master: The master widget.
        message (str): The message to be displayed in the alert window.
    """

    def __init__(self, master, message: str) -> None:
        super().__init__(master)
        self.title("Alert")
        self.geometry("300x100")
        self.resizable(True, False)
        self.minsize(300, 100)
        self.maxsize(300, 100)

        self.label = CTkLabel(self, text=message, font=("ubuntu", 18))
        self.label.pack(expand=True, fill="both", padx=10, pady=10)
        self.wait_visibility()
        self.grab_set()
        self.wait_window()
