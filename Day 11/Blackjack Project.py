import arts
import random

def check(hand):
    new_hand = []
    if sum(hand) <= 21:
        return hand
    if not 11 in hand:
        return hand
    for card in hand:
        if card != 11:
            new_hand.append(card)
    new_hand.append(1)
    return new_hand

cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
playing_input = "Do you want to play a game of Blackjack? Type 'y' or 'n': "
taking_input = "Type 'y' to get another card, type 'n' to pass: "
is_playing = True
if input(playing_input) == 'n':
    is_playing = False
while is_playing:
    user_hand = []
    computer_hand = []
    print("\n" * 50)
    print(arts.queen)
    user_hand.append(random.choice(cards))
    user_hand.append(random.choice(cards))
    computer_hand.append(random.choice(cards))
    print(f"\tYour cards: {user_hand}, current score: {sum(user_hand)}\n\tComputer's first card: {computer_hand[0]}")
    is_taking = True
    if input(taking_input) == "n":
        is_taking = False
    while is_taking:
        user_hand.append(random.choice(cards))
        user_hand = check(user_hand)
        print(f"\tYour cards: {user_hand}, current score: {sum(user_hand)}\n\tComputer's first card: {computer_hand[0]}")
        if sum(user_hand) > 21:
            is_taking = False
        else:
            if input(taking_input) == "n":
                is_taking = False
    if sum(user_hand) > 21:
        print(f"\tYour final hand: {user_hand}, final score: {sum(user_hand)}\n\tComputer's final hand: {computer_hand}, final score: {sum(computer_hand)}")
        print("You went over. You lose.")
    else:
        while sum(computer_hand)<17:
            computer_hand.append(random.choice(cards))
            computer_hand = check(computer_hand)
        print(f"\tYour final hand: {user_hand}, final score: {sum(user_hand)}\n\tComputer's final hand: {computer_hand}, final score: {sum(computer_hand)}")
        if sum(computer_hand)>21:
            print("Opponent went over. You win.")
        else:
            if sum(user_hand)>sum(computer_hand):
                print("You win.")
            elif sum(user_hand) == sum(computer_hand):
                print("Draw.")
            else:
                print("You lose.")
    if input(playing_input) == "n":
        is_playing = False



