from turtle import Turtle

ALIGN = "center"
FONT=("Impact", 24, "normal")

class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.score = 0
        self.highscore = 0
        with open("Day 24\\highscore.txt", mode="r") as file:
            self.highscore = int(file.read())
        self.color("white")
        self.penup()
        self.goto(0, 265)
        self.hideturtle()
        self.update_score()


    def update_score(self):
        self.clear()
        text = f"Score: {self.score} High Score: {self.highscore}"
        self.write(text, align=ALIGN, font=FONT)

    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.update_score()
        with open("Day 24\\highscore.txt", mode="w") as file:
            file.write(str(self.highscore))


    def inc(self):
        self.score += 1
        self.update_score()

    def game_over(self):
        self.goto(0,0)
        self.write("GAME OVER", align=ALIGN, font=FONT)
