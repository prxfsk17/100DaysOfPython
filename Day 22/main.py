import time
from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
from line import DottedLine

def game_over():
    global game_is_on
    game_is_on = False
    score1.game_over()

screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Pong")
screen.tracer(0)
screen.listen()

player1 = Paddle(1)
player2 = Paddle(2)
ball = Ball()
score1 = Scoreboard(1)
score2 = Scoreboard(2)
dotted_line = DottedLine()

screen.onkey(key="w", fun=player1.move_up)
screen.onkey(key="s", fun=player1.move_down)
screen.onkey(key="Up", fun=player2.move_up)
screen.onkey(key="Down", fun=player2.move_down)
screen.onkey(key="q", fun=game_over)

game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(0.035)
    ball.move()

    if ball.ycor() > 290 or ball.ycor() < -290:
        ball.hit_wall_up_or_down()

    if ball.xcor() > 390:
        score1.inc()
        ball.new_game()

    if ball.xcor() < -390:
        score2.inc()
        ball.new_game()

    for block in player1.blocks:
        if ball.distance(block) < 15:
            ball.hit_wall_left_or_right()
    for block in player2.blocks:
        if ball.distance(block) < 15:
            ball.hit_wall_left_or_right()

screen.exitonclick()