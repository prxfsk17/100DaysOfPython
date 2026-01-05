import math
from turtle import Turtle
import random

class Ball(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("DarkOliveGreen3")
        self.penup()
        self.setheading(90)
        self.goto(0, -330)
        self.x_dir = 0
        self.y_dir = 0
        self.x_move = 3
        self.y_move = 3
        self.move_speed = 0.001

    def start_game(self):
        angle = random.randint(30, 150)
        rad = angle * 3.14159 / 180

        speed = 5
        self.x_move = speed * math.cos(rad)
        self.y_move = speed * math.sin(rad)

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1

    def reset_position(self):
        self.goto(0, -330)
        self.start_game()

    def check_wall_collision(self, screen_width, screen_height):
        x_pos = self.xcor()
        y_pos = self.ycor()

        if x_pos >= screen_width / 2 - 10 or x_pos <= -screen_width / 2 + 10:
            self.bounce_x()
            return True

        if y_pos >= screen_height / 2 - 10:
            self.bounce_y()
            return True

        return False

    def check_paddle_collision(self, paddle):
        for block in paddle.blocks:
            if self.distance(block) < 20:

                paddle_x = block.xcor()
                ball_x = self.xcor()


                relative_x = ball_x - paddle_x
                self.x_move = relative_x * 0.2

                self.y_move = abs(self.y_move)


                self.increase_speed()
                return True
        return False

    def check_brick_collision(self, bricks):
        for brick in bricks:
            if self.distance(brick) < 25:

                ball_x, ball_y = self.xcor(), self.ycor()
                brick_x, brick_y = brick.xcor(), brick.ycor()

                if abs(ball_x - brick_x) > abs(ball_y - brick_y):
                    self.bounce_x()
                else:
                    self.bounce_y()
                bricks.remove(brick)
                brick.hideturtle()
                return brick
        return None

    def increase_speed(self):

        self.x_move *= 1.02
        self.y_move *= 1.02