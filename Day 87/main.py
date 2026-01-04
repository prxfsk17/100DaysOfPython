import time
from turtle import Screen

from paddle import Paddle
from ball import Ball


screen = Screen()
screen.setup(width=800, height=900)
screen.bgcolor("black")
screen.title("Breaker")
screen.tracer(0)
screen.listen()

paddle = Paddle()
screen.onkeypress(key="a", fun=paddle.move_left)
screen.onkeypress(key="d", fun=paddle.move_right)
screen.onkeyrelease(key="a", fun=paddle.stop_moving)
screen.onkeyrelease(key="d", fun=paddle.stop_moving)

ball = Ball()
ball.start_game()

game_is_on = True
while game_is_on:
    time.sleep(ball.move_speed)


    ball.move()
    paddle.update()


    if ball.check_wall_collision(800, 900):

        pass


    if ball.check_paddle_collision(paddle):

        pass


    if ball.ycor() < -450:
        ball.reset_position()

    screen.update()



screen.exitonclick()