import random
picks = ["Rock", "Paper", "Scissors"]
user_choice = picks[int(input("What do you choose Type 0 for Rock, 1 for Paper, 2 for Scissors"))]
computer_choice = picks[random.randint(0,2)]
print(f"You choose {user_choice}.")
print(f"Computer choose {computer_choice}")

if user_choice == computer_choice:
    print("It's draw!")
else:
    if user_choice == "Rock":
        if computer_choice == "Paper":
            print("You lose")
        else:
            print("You win")
    elif user_choice == "Paper":
        if computer_choice == "Rock":
            print("You win")
        else:
            print("You lose")
    else:
        if computer_choice == "Rock":
            print("You lose")
        else:
            print("You win")