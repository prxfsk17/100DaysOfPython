from arts import vs, title
from game_data import data
import random

def print_compare(first_index, second_index):
    print(f"Compare A: {first_index["name"]}, a {first_index["description"]}, from {first_index["country"]}")
    print(vs)
    print(f"Against B: {second_index["name"]}, a {second_index["description"]}, from {second_index["country"]}")

def compare(first_index, second_index):
    guess = input("Who has more followers? Type 'A' or 'B': ")
    if first_index["follower_count"] > second_index["follower_count"]:
        return guess == "A"
    else:
        return guess == "B"

def game():
    is_game = True
    score = 0
    obj1 = random.choice(data)
    while is_game:
        print("\n"*50)
        print(title)
        print(f"Your current score: {score}")
        obj2 = random.choice(data)
        while obj1 == obj2:
            obj2 = random.choice(data)
        print_compare(obj1, obj2)
        if compare(obj1, obj2):
            score += 1
            obj1 = obj2
        else:
            print("\n"*50)
            print(title)
            print(f"Sorry, that's wrong. Final score: {score}")
            is_game = False

game()