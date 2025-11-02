import pandas

#1. Create a dictionary in this format:
alphabet_nato_dict = {row.letter:row.code for (index, row) in pandas.read_csv("Day 26/nato_phonetic_alphabet.csv").iterrows()}

#2. Create a list of the phonetic code words from a word that the user inputs.
word = ""
while word.lower() != "exit":
    word = input("Enter a word: ")
    new_list=[alphabet_nato_dict[letter.upper()] for letter in word]
    print(new_list)
