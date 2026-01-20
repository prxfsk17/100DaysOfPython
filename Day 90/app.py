from tkinter import *
from tkinter import ttk
import time

ORANGE = "#FE7F2D"
RED = "#F63049"
GREEN = "#A5C89E"
YELLOW = "#FBEF76"
WHITE = "#F5FBE6"
BLACK = "#000000"
BLUE = "#000080"

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

        self.is_timer_on = False
        self.timer = None
        self.count = 5

        self.setup_ui()

    def setup_ui(self):

        style=ttk.Style()
        style.theme_use("clam")

        label_title = Label(text="Disapperiang Text Writing", font=("Courier", 30, "bold"), bg=GREEN, fg=BLUE)
        label_title.grid(column=0, row=0, columnspan=2, pady=(20, 0))
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.grid(row=1, column=0, sticky="wens")
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        self.editor = Text(
            main_frame,
            width=50,
            height=20,
            font=("Courier", 17, "bold"),
            wrap="word"
        )
        self.editor.grid(column=0, row=2, columnspan=2)
        self.editor.bind("<Key>", self.key_press)
        self.label_timer = Label(text="Timer", font=("Courier", 20, "bold"), bg=GREEN, fg=BLACK)
        self.label_timer.grid(column=0, row=3, columnspan=2, pady=(20,0))

    def start_timer(self):
        self.is_timer_on = True
        self.count = 5
        self.label_timer.config(text="Your text has been deleted.", fg=BLACK)
        self.count_down(self.count)

    def count_down(self, count):
        if count > 0:
            self.timer = self.window.after(1000, self.count_down, self.count-1)
            self.label_timer.config(text=f"Timer: {count}")
            self.count -= 1
            if count == 1:
                self.editor.config(fg=RED)
            elif count == 2:
                self.editor.config(fg=ORANGE)
            elif count == 3:
                self.editor.config(fg=YELLOW)
            else:
                self.editor.config(fg=BLACK)
        else:
            self.label_timer.config(text="Your text has been deleted.", fg = RED)
            self.is_timer_on=False
            self.window.after_cancel(self.timer)
            self.editor.delete(1.0, END)

    def key_press(self, e):
        char = e.char
        if char:
            if not self.is_timer_on:
                self.start_timer()
            else:
                self.window.after_cancel(self.timer)
                self.start_timer()