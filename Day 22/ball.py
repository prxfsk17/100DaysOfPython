from turtle import Turtle

class Ball(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.penup()
        self.left(45)
        self.goto(0, 50)
        self.x_dir = 5
        self.y_dir = -5

    def new_game(self):
        self.hit_wall_left_or_right()
        self.hit_wall_up_or_down()
        self.goto(0,0)

    def move(self):
        new_pos = (self.xcor()+self.x_dir, self.ycor()+self.y_dir)
        self.goto(new_pos)

    def hit_wall_left_or_right(self):
        self.x_dir *= -1

    def hit_wall_up_or_down(self):
        self.y_dir *= -1