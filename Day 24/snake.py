from turtle import Turtle

MOVE_DISTANCE = 20
RIGHT = 0
UP = 90
LEFT = 180
DOWN = 270


def create_segment(segment, x_cord, y_cord):
    segment.penup()
    segment.color("white")
    segment.setpos(x=x_cord, y=y_cord)

class Snake:

    def __init__(self):
        self.len = 3
        self.tail = [Turtle("square"), Turtle("square"), Turtle("square")]
        self.init_snake()
        self.head = self.tail[0]

    def init_snake(self):
        for i in range(self.len):
            create_segment(self.tail[i], -20*i, 0)
        self.tail[0].color("green")

    def grow(self):
        last_tail = Turtle("square")
        create_segment(last_tail, self.tail[self.len-1].xcor(), self.tail[self.len-1].ycor())
        self.len += 1
        self.tail.append(last_tail)

    def reset(self):
        for segment in self.tail:
            segment.goto(1000, 1000)
        self.len = 3
        self.tail = [Turtle("square"), Turtle("square"), Turtle("square")]
        self.init_snake()
        self.head = self.tail[0]
        self.head.setheading(RIGHT)

    def move(self):
        for seg_num in range(self.len - 1, 0, -1):
            new_x = self.tail[seg_num - 1].xcor()
            new_y = self.tail[seg_num - 1].ycor()
            self.tail[seg_num].goto(new_x, new_y)
        self.head.forward(MOVE_DISTANCE)

    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)

    def up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)