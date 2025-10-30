from turtle import Turtle

ALIGN = "center"
FONT = ("Impact", 16, "normal")

class Writer(Turtle):

    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color("black")

    def level(self, lvl):
        self.clear()
        self.goto(-260, 360)
        text = f"Level: {lvl}"
        self.write(text, align=ALIGN, font=FONT)

    def game_over(self):
        self.goto(0, 320)
        text = "Game Over"
        self.write(text, align=ALIGN, font=FONT)

