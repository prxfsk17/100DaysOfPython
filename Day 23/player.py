from turtle import Turtle

class Player(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.color("green")
        self.penup()
        self.setheading(90)
        self.goto(0,-380)
        self.level = 1

    def move(self):
        self.forward(10)

    def new_level(self):
        self.level += 1
        self.teleport(0, -380)