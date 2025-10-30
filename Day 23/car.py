import random
from turtle import Turtle
from random import choice, randint

COLORS = ["blue", "red", "yellow", "black", "grey", "purple"]

class Car(Turtle):

    def __init__(self):
        super().__init__()
        self.color(choice(COLORS))
        self.shape("square")
        self.shapesize(stretch_wid=0.5, stretch_len=1)
        self.setheading(180)
        self.penup()
        self.set_pos()

    def set_pos(self):
        random_x = randint(300, 700)
        random_y = randint(-350, 350)
        self.goto(random_x, random_y)

    def move(self, lvl):
        dist = 5*lvl
        self.forward(dist)
