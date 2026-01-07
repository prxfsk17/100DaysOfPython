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
        self.x_move = 0
        self.y_move = 0
        self.radius = 10
        self.move_speed = 0.001
        self.lives = 3
        self.score=0

    def start_game(self):
        if self.x_move == 0 and self.y_move == 0:
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
        self.x_move = 0
        self.y_move = 0

    def decrement_lives(self):
        self.lives -=1
        if self.lives > 0:
            self.reset_position()
            return True
        else:
            self.reset_position()
            self.hideturtle()
            return False

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
                return True
        return False

    def check_brick_collision(self, bricks):

        h = 20
        w = 60

        for brick in bricks:

            x = brick.xcor()
            y = brick.ycor()

            brick_top = y + h/2
            brick_bottom = y - h/2
            brick_left = x - w/2
            brick_right = x + w/2

            ball_top = self.ycor() + self.radius
            ball_bottom = self.ycor() - self.radius
            ball_left = self.xcor() - self.radius
            ball_right = self.xcor() + self.radius

            if (ball_top >= brick_bottom and
                ball_bottom <= brick_top and
                ball_left <= brick_right and
                ball_right >= brick_left):

                from_top = abs(ball_top - brick_bottom)
                from_bottom = abs(ball_bottom - brick_top)
                from_left = abs(ball_left - brick_right)
                from_right = abs(ball_right - brick_left)

                min_overlap = min(from_left, from_right,
                                  from_top, from_bottom)

                if min_overlap == from_left or min_overlap == from_right:
                    self.bounce_x()
                else:
                    self.bounce_y()
                self.increase_speed()
                return brick
        return None

    def increase_speed(self):

        self.x_move *= 1.02
        self.y_move *= 1.02