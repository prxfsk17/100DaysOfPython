import random
import words
import arts

def new_word(old_word, index, letter):
    word_to_return = ""
    for ind in range(len(old_word)):
        if ind == index:
            word_to_return += letter
        else:
            word_to_return += old_word[ind]
    return word_to_return

print(arts.hangman)
word = random.choice(words.word_list)
word_for_user = ""
for q in range(len(word)):
    word_for_user += "_"
times_to_guess = 6
i = 0
while i < times_to_guess:
    print(word_for_user)
    print(f"You have {6-i} tries to guess")
    char_to_guess = input("Guess a letter: ").lower()[0]
    fl = False
    for j in range(len(word)):
        if word[j] == char_to_guess:
            word_for_user = new_word(word_for_user, j, char_to_guess)
            fl = True
    if not fl:
        i += 1
        print("Bad guess!")
    else:
        print("Good guess!")
    if not "_" in word_for_user:
        print(arts.win)
        print(f"You win! The word was {word}")
        i = times_to_guess
if "_" in word_for_user:
    print(arts.lose)
    print(f"You lose! The word was {word}")