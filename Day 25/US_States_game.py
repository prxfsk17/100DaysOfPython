import turtle
import pandas

def play():
    screen = turtle.Screen()
    screen.title("Game")
    img_path="Day 25/blank_states_img.gif"
    screen.addshape(img_path)
    turtle.shape(img_path)

    data = pandas.read_csv("Day 25/50_states.csv")
    score = 0
    correct_guesses = []
    game_is_on = True

    writer = turtle.Turtle()
    writer.penup()
    writer.hideturtle()
    writer.speed("fastest")

    while game_is_on:
        answer_state = screen.textinput(title=f"Correct: {score}/50", prompt="What's another state name?").title()
        current_state = data[data.state == answer_state]
        if len(current_state) > 0:
            current_name, x, y = current_state.state.item(), int(current_state.x.item()), int(current_state.y.item())
            if current_name not in correct_guesses:
                correct_guesses.append(current_name)
                score += 1
                writer.goto((x, y))
                writer.write(current_name, align="center", font=("Arial", 8, "normal"))
        if correct_guesses == 50:
            game_is_on = False
        if answer_state == "Exit":
            break

    all_states = data.state.to_list()
    missing_states = []
    for state in all_states:
        if state not in correct_guesses:
            missing_states.append(state)
    data_dict = {
        "Missing states" : missing_states
    }
    pandas.DataFrame(data_dict).to_csv("Day 25/states_to_learn.csv")
    turtle.mainloop()