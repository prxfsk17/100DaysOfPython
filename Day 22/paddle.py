import turtle
from turtle import Turtle

class Paddle(Turtle):

    def __init__(self, pl):
        super().__init__()
        self.player = pl
        self.len = 5
        self.blocks = [Turtle("square"), Turtle("square"), Turtle("square"), Turtle("square"), Turtle("square")]
        for i in range(self.len):
            self.create_block(self.blocks[i], 350, 50-i*20)
        # self.shape("square")

    def create_block(self, segment, x_cord, y_cord):
        segment.penup()
        segment.color("white")
        if self.player == 1:
            x_cord *= -1
        segment.setpos(x=x_cord, y=y_cord)
        segment.penup()

    def move_up(self):
        if self.blocks[0].ycor()+20 < 300:
            for block in self.blocks:
                block.goto(block.xcor(),block.ycor()+20)

    def move_down(self):
        if self.blocks[-1].ycor()-20 > -300:
            for block in self.blocks:
                block.goto(block.xcor(), block.ycor() - 20)