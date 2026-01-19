from tkinter import *
from tkinter import ttk

ORANGE = "#FE7F2D"
RED = "#F63049"
GREEN = "#A5C89E"
YELLOW = "#FBEF76"
WHITE = "#F5FBE6"
BLACK = "#000000"

class DisappearingText:

    def __init__(self, window):
        self.window = window
        self.window.title("Disappearing Text")
        self.window.config(padx=100, pady=50, bg=GREEN)
        self.window.resizable(False, False)

        self.canvas = None
        self.text = None
        self.editor = None

        self.label_timer = None

        self.setup_ui()

    def setup_ui(self):

        style=ttk.Style()
        style.theme_use("clam")

        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.grid(row=0, column=0, sticky="wens")
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        self.editor = Text(
            main_frame,
            width=50,
            height=20,
            font=("Courier", 15),
            wrap="word"
        )
        self.editor.grid(column=0, row=0, columnspan=2)
        self.editor.bind("<Key>", self.key_press)
        self.label_timer = Label(text="Timer", font=("Courier", 30, "bold"), bg=GREEN, fg=BLACK)
        self.label_timer.grid(column=0, row=1, columnspan=2, pady=(20,0))

    def key_press(self, e):
        char = e.char
        print(char)