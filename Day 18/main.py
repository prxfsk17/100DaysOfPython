import turtle
from turtle import Turtle, Screen
import random
# if color in rgb format
turtle.colormode(255)

COLORS = ["sky blue", "gold", "SpringGreen2", "purple1", "gray", "navy", "blue violet", "cyan4", "green4"]
ANGLES = [0, 90, 180, 270]

timmy = Turtle()
timmy.shape("turtle")
timmy.color("blue violet")
# square
# for _ in range(4):
#     timmy.forward(100)
#     timmy.right(90)

# dotted line
# for _ in range(20):
#     timmy.pendown()
#     timmy.forward(10)
#     timmy.penup()
#     timmy.forward(10)

# different shapes
# for n in range(3, 11):
#     angle =180-int(180*(n-2)/n)
#     timmy.color(random.choice(COLORS))
#     for _ in range(n):
#         timmy.forward(100)
#         timmy.right(angle)

# random walk
timmy.speed("fastest")
# timmy.pensize(2)
# for _ in range(200):
#     timmy.forward(20)
#     timmy.color((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
#     timmy.setheading(random.choice(ANGLES))

# Spirograph
# for _ in range(90):
#     timmy.circle(100)
#     timmy.setheading(timmy.heading() + 4)
#     timmy.color((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))



screen = Screen()
screen.exitonclick()

# import heroes
