from turtle import Turtle

class Paddle(Turtle):

    def __init__(self):
        super().__init__()
        self.len = 10
        self.blocks = []
        self.create_blocks()
        self.moving_left = False
        self.moving_right = False
        self.move_speed = 2.5

    def create_blocks(self):
        y_cord = -350
        total_width = self.len * 20
        start_x = -total_width / 2 + 10
        for i in range(self.len):
            segment = Turtle("square")
            segment.color("white")
            segment.penup()
            segment.shapesize(stretch_wid=1, stretch_len=1)
            segment.goto(start_x + (i * 20), y_cord)
            self.blocks.append(segment)

    def move_left(self):
        self.moving_left = True
        self.moving_right = False

    def move_right(self):
        self.moving_right = True
        self.moving_left = False

    def stop_moving(self):
        self.moving_left = False
        self.moving_right = False

    def update(self):
        if self.moving_left and self.blocks[0].xcor() - self.move_speed > -400:
            for block in self.blocks:
                block.goto(block.xcor() - self.move_speed, block.ycor())
        elif self.moving_right and self.blocks[-1].xcor() + self.move_speed < 400:
            for block in self.blocks:
                block.goto(block.xcor() + self.move_speed, block.ycor())

    def second_level(self):
        for block in self.blocks:
            block.hideturtle()
        self.len = 5
        self.blocks = []
        self.create_blocks()
