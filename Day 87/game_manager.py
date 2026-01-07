import random

from brick import Brick
colors = ["red", "orange", "green", "yellow"]
points={
    "red" : 7,
    "orange" : 5,
    "green" : 3,
    "yellow" : 1
}

class GameManager:

    def __init__(self, w, h, ball, paddle, writer):
        self.width = w
        self.height = h
        self.bricks_in_row = self.width // 80
        self.all_bricks = []
        self.is_first_level = True
        self.init_bricks()
        self.ball = ball
        self.paddle = paddle
        self.writer = writer

    def init_bricks(self):
        self.all_bricks = []
        y = self.height / 2 - 70
        for color in colors:
            for row in range(2):
                x = -self.width / 2 + 35
                for i in range(self.bricks_in_row):
                    brick = Brick(x, y, color)
                    self.all_bricks.append(brick)
                    x += 80
                y -= 40

    def get_current_bricks(self):
        return self.all_bricks

    def start_second_level(self):
        self.ball.reset_position()
        self.paddle.second_level()
        self.writer.update(self, self.ball, game_state="game")
        self.init_bricks()

    def remove_brick(self, brick):
        self.all_bricks.remove(brick)
        brick_color = brick.color()[0]
        self.ball.score += points[brick_color]
        brick.hideturtle()
        if not len(self.all_bricks)>0:
            if self.is_first_level:
                self.is_first_level = False
                self.start_second_level()
                return True
            else:
                return False
        return True

    def help(self):
        brick = random.choice(self.all_bricks)
        self.all_bricks.remove(brick)
        brick.hideturtle()

    def end_game(self):
        for brick in self.all_bricks:
            brick.hideturtle()
        self.all_bricks = []