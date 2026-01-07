import time
from turtle import Screen

from paddle import Paddle
from ball import Ball
from game_manager import GameManager
from writer import Writer

game_is_on = False

def start_game():
    global game_is_on
    game_is_on = True
    ball.start_game()
    while game_is_on:
        time.sleep(ball.move_speed)
        ball.move()
        paddle.update()

        writer.update(game_manager, ball, game_state="game")

        if ball.check_wall_collision(800, 900):
            pass

        if not ball.check_paddle_collision(paddle):
            pass

        brick_to_remove = ball.check_brick_collision(game_manager.get_current_bricks())
        if not brick_to_remove is None:
            if not game_manager.remove_brick(brick_to_remove):
                win()
                return

        screen.update()

        if ball.ycor() < -450:
            if not ball.decrement_lives():
                end_game()
                return

def win():
    global game_is_on
    game_is_on = False
    screen.update()
    writer.update(ball=ball, game_state="win")

def end_game():
    global game_is_on
    game_is_on = False
    game_manager.end_game()
    screen.update()
    writer.update(ball=ball, game_state="game_over")

screen = Screen()
screen.setup(width=800, height=900)
screen.bgcolor("black")
screen.title("Breaker")
screen.tracer(0)
screen.listen()

paddle = Paddle()
ball = Ball()
writer = Writer()
game_manager = GameManager(800, 900, ball, paddle, writer)
writer.update(game_state="instructions")

screen.onkeypress(key="a", fun=paddle.move_left)
screen.onkeypress(key="d", fun=paddle.move_right)
screen.onkeyrelease(key="a", fun=paddle.stop_moving)
screen.onkeyrelease(key="d", fun=paddle.stop_moving)
screen.onkey(key="space", fun=start_game)
screen.onkey(key="h", fun=game_manager.help)

screen.exitonclick()