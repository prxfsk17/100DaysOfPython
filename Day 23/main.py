import time
from turtle import Screen
from player import Player
from writer import Writer
from car import Car

screen = Screen()
screen.setup(width=600, height=800)
screen.bgcolor("white")
screen.tracer(0)
screen.listen()

player = Player()
writer = Writer()
cars_quantity = 40
cars = []
for i in range(cars_quantity):
    cars.append(Car())

screen.onkey(key="space", fun=player.move)
writer.level(1)
game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(0.1)

    for car in cars:
        car.move(player.level)
        if car.xcor() < -300:
            car.set_pos()

    if player.ycor()>380:
        player.new_level()
        writer.level(player.level)

    for car in cars:
        if player.distance(car) < 10:
            game_is_on = False
            writer.game_over()

screen.exitonclick()