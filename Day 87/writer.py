from turtle import Turtle

class Writer(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color("white")
        self.current_display = "instructions"  # "instructions", "game", "win", "game_over"

    def show_instructions(self):
        self.clear()
        self.goto(0, 50)
        self.write("A/D - Move Paddle",
                   align="center",
                   font=("Courier", 24, "normal"))
        self.goto(0, 0)
        self.write("SPACE - Start Game",
                   align="center",
                   font=("Courier", 24, "normal"))
        self.current_display = "instructions"

    def update_game_display(self, game_manager, ball):
        self.clear()

        if hasattr(game_manager, 'is_first_level'):
            level = 1 if game_manager.is_first_level else 2
        else:
            level = getattr(game_manager, 'current_level', 1)

        self.goto(-350, 400)
        self.write(f"Level: {level}/2",
                   align="left",
                   font=("Courier", 18, "normal"))

        self.goto(0, 400)
        lives = getattr(ball, 'lives', 0)
        self.write(f"Lives: {lives}",
                   align="center",
                   font=("Courier", 18, "normal"))

        self.goto(350, 400)
        score = getattr(ball, 'score', 0)
        self.write(f"Score: {score}",
                   align="right",
                   font=("Courier", 18, "normal"))

        self.current_display = "game"

    def show_win_message(self, ball):
        self.clear()
        self.goto(0, 0)
        score = getattr(ball, 'score', 0)
        self.write(f"You Won!\nScore: {score}",
                   align="center",
                   font=("Courier", 40, "bold"))
        self.current_display = "win"

    def show_game_over(self, ball):
        self.clear()
        self.goto(0, 0)
        score = getattr(ball, 'score', 0)
        self.write(f"Game Over\nScore: {score}",
                   align="center",
                   font=("Courier", 40, "bold"))
        self.current_display = "game_over"

    def update(self, game_manager=None, ball=None, game_state="game"):
        if game_state == "instructions":
            self.show_instructions()
        elif game_state == "game" and game_manager is not None and ball is not None:
            self.update_game_display(game_manager, ball)
        elif game_state == "win" and ball is not None:
            self.show_win_message(ball)
        elif game_state == "game_over" and ball is not None:
            self.show_game_over(ball)
        else:
            self.clear()

    def clear_display(self):
        self.clear()