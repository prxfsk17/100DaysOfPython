import time

THEME_COLOR = "#375362"
WHITE = "#FFFFFF"

from tkinter import *
from quiz_brain import QuizBrain



class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain

        self.window = Tk()
        self.window.title("Quiz")
        self.window.config(padx=20, pady=20, bg = THEME_COLOR)

        self.score_label = Label(text="Score: 0", bg=THEME_COLOR, fg=WHITE)
        self.score_label.grid(column=1, row=0)

        self.canvas = Canvas(width=300, height=250, bg=WHITE, highlightthickness=0)
        self.question_text = self.canvas.create_text(150, 125, width=275, text="quest", font=("Arial", 20, "italic"), fill=THEME_COLOR)
        self.canvas.grid(column=0, row=1, columnspan=2, pady=50)

        true_image = PhotoImage(file="Day 34/images/true.png")
        false_image = PhotoImage(file="Day 34/images/false.png")

        self.button_true = Button(image=true_image, highlightthickness=0, bg=THEME_COLOR, command=self.true_answer)
        self.button_true.grid(column=0, row=2)

        self.button_false = Button(image=false_image, highlightthickness=0, bg=THEME_COLOR, command=self.false_answer)
        self.button_false.grid(column=1, row=2)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg=WHITE)
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text = q_text)
            self.score_label.config(text=f"Score: {self.quiz.score}")
        else:
            self.canvas.itemconfig(self.question_text, text=f"You've completed the quiz\nYour final score was: {self.quiz.score}/{self.quiz.question_number}")
            self.button_true.config(state="disabled")
            self.button_false.config(state="disabled")

    def true_answer(self):
        answer = self.quiz.check_answer("True")
        self.feedback(answer)

    def false_answer(self):
        answer = self.quiz.check_answer("False")
        self.feedback(answer)

    def feedback(self, ans):
        if ans:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(600, func=self.get_next_question)
