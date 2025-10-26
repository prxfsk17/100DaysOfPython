from turtle import Turtle, Screen
import random
screen = Screen()

# def move_forwards():
#     tim.forward(10)
#
# def move_backwards():
#     tim.backward(10)
#
# def left_turn():
#     tim.left(10)
#
# def right_turn():
#     tim.right(10)
#
# def clear():
#     tim.home()
#     tim.clear()
#     tim.setheading(0)
#
# screen.listen()
# screen.onkey(key="w", fun=move_forwards)
# screen.onkey(key="s", fun=move_backwards)
# screen.onkey(key="a", fun=left_turn)
# screen.onkey(key="d", fun=right_turn)
# screen.onkey(key="c", fun=clear)

def check_result(u, win):
    if u.lower() == win:
        print("You win!")
    else:
        if win != "rainbow":
            print(f"You lose! The winner is the {win} turtle.")
        else:
            print("Incorrect input!")

def initialization(list_of_turtles):
    for i in range(len(list_of_turtles)):
        list_of_turtles[i].shape("turtle")
        list_of_turtles[i].color(colors[i])
        step = h / len(list_of_turtles)
        start_y = len(list_of_turtles) / 2 * step - step * (i + 0.5)
        list_of_turtles[i].penup()
        list_of_turtles[i].goto(start_x, start_y)

colors = ["red", "orange", "yellow", "green", "blue", "purple", "cyan", "indigo"]
is_race_on = False
screen.setup(width=500, height=400)
user_guess = screen.textinput("Turtles races", "What turtle will win the race? Enter a color: ")
w=screen.window_width()
h=screen.window_height()
start_x=20-w/2
turtles = [Turtle(), Turtle(), Turtle(), Turtle(), Turtle(), Turtle(), Turtle(), Turtle()]
initialization(turtles)

if user_guess:
    is_race_on = True

winner = "rainbow"
while is_race_on:
    for i in range(len(turtles)):
        if turtles[i].position()[0] >= w/2-31:
            winner = colors[i]
            is_race_on=False
        else:
            turtles[i].forward(random.randint(0,10))

check_result(user_guess, winner)

screen.exitonclick()