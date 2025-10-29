from turtle import Turtle

ALIGN = "center"
FONT=("Impact", 24, "normal")

class Scoreboard(Turtle):

    def __init__(self, pl):
        super().__init__()
        self.score = 0
        self.player = pl
        self.color("white")
        self.penup()
        self.hideturtle()
        if self.player == 1:
            self.goto(-50, 260)
        else:
            self.goto(50, 260)
        self.update_score()

    def update_score(self):
        self.clear()
        text = f"{self.score}"
        self.write(text, align=ALIGN, font=FONT)

    def inc(self):
        self.score += 1
        self.update_score()

    def game_over(self):
        self.goto(0,0)
        self.write("GAME OVER", align=ALIGN, font=FONT)