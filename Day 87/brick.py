from turtle import Turtle

class Brick(Turtle):

    def __init__(self, x, y, col):

        super().__init__()
        self.shape("square")
        self.color(col)
        self.penup()
        self.shapesize(stretch_wid=1, stretch_len=3)
        self.goto(x, y)
        self.showturtle()

        self.x = x
        self.y = y
        self.width = 60
        self.height = 20
        self.active = True
