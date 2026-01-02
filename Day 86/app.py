import time
import tkinter as tk
from tkinter import ttk

from random import choice
from texts import list


def get_article():
    return choice(list)


class TypingSpeedTest:

    def __init__(self, root : tk.Tk):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("1000x900")
        self.canvas = None
        self.main_text_id = None
        self.editor : tk.Text = None
        self.text=""
        self.current_position = 0
        self.correct_chars = 0
        self.errors = 0
        self.start_time = None
        self.test_active = False

        self.setup_ui()

    def setup_ui(self):

        style = ttk.Style()
        style.theme_use("clam")

        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky="wens")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        label_app = tk.Label(main_frame, text="Typing speed test", font=("Verdana", 17, "bold italic"), background="#d9d9d9")
        label_app.grid(row=0, column=0, columnspan=2)

        self.canvas = tk.Canvas(main_frame, bg="white", width=750, height=200)
        self.canvas.grid(row=1, column=0, columnspan=2, pady=(20,0))
        self.main_text_id = self.canvas.create_text(
            370,
            90,
            text="Here you can see text you should to type in field below.",
            fill="#004D40",
            font=("Verdana", 13),
            width=720,
            justify="left"
        )

        self.editor = tk.Text(main_frame, width=50, height=15, font=("Verdana", 13), wrap="word", state="disabled")
        self.editor.grid(row=2, column=0, columnspan=2, pady=(20,0))
        self.editor.bind("<Key>", self.on_key_press)
        self.editor.tag_config("correct", background="#C8E6C9")
        self.editor.tag_config("wrong", background="#FFCDD2")

        buttons_frame = ttk.Frame(main_frame, padding=10)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=(20,0))
        button_start = tk.Button(buttons_frame, text="Start new test", command=self.start_test, font=("Verdana", 13))
        button_start.pack(side=tk.LEFT, padx=5)

    def start_test(self):
        self.current_position = 0
        self.correct_chars = 0
        self.errors = 0
        self.start_time = time.time()
        self.test_active = True
        self.editor.config(state=tk.NORMAL)
        self.update_text()
        self.editor.delete("1.0", tk.END)
        self.editor.focus_set()

    def on_key_press(self, event):
        if not self.test_active:
            return
        if event.keysym in ["Shift_L", "Shift_R", "Control_L",
                            "Control_R", "Alt_L", "Alt_R", "Caps_Lock"]:
            return
        if event.keysym == "BackSpace":
            self.handle_backspace()
            return
        char = event.char
        if char:  # Добавь проверку что char не пустой
            # ЗАПОМНИТЬ правильность символа
            is_correct = (self.text[self.current_position] == char)

            # Обновить счетчики сразу
            if is_correct:
                self.correct_chars += 1
                self.current_position += 1

            else:
                self.errors += 1

            # УВЕЛИЧИТЬ позицию сразу

            # ОТЛОЖИТЬ подсветку на 10 мс
            self.root.after(10, lambda: self.highlight_char_delayed(is_correct))
        if self.current_position >= len(self.text):
            self.handle_test_end()

    def handle_backspace(self):
        pass

    def highlight_char_delayed(self, is_correct):
        try:
            cursor_pos = self.editor.index("insert")

            if cursor_pos == "1.0":
                start_pos = "1.0"
                end_pos = "1.1"
            else:
                start_pos = self.editor.index(f"{cursor_pos} - 1 char")
                end_pos = cursor_pos

            tag_name = "correct" if is_correct else "wrong"

            self.editor.tag_add(tag_name, start_pos, end_pos)

        except Exception as e:
            print(f"{e}")

    def handle_test_end(self):
        pass

    def update_text(self):
        self.text=get_article()
        self.canvas.itemconfig(self.main_text_id, text=self.text)
