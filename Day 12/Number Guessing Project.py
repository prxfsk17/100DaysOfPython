EASY_LEVEL = 10
HARD_LEVEL = 5
from arts import text, diff, welcome, a_number
import random

def set_difficulty():
    difficulty = input(diff)
    if difficulty == "hard":
        return HARD_LEVEL
    elif difficulty == "easy":
        return EASY_LEVEL
    else:
        return 0

def check_answer(user, actual):
    if user > actual:
        print("Too high.\nGuess again.")
        return False
    elif user < actual:
        print("Too low.\nGuess again.")
        return False
    else:
        print(f"You got it! The answer was {number}.")
        return True

def game(guesses):
    while guesses > 0:
        print(f"You have {guesses} remaining to guess the number.")
        guess = int(input("Make a guess: "))
        is_guessed = check_answer(guess, number)
        guesses -= 1
        if is_guessed:
            return -1
    return 0

print(text)
print(welcome)
print(a_number)

attempts=set_difficulty()
number = random.randint(1, 100)
attempts = game(attempts)
if attempts == 0:
    print("You are out of guesses. Unluck!")
