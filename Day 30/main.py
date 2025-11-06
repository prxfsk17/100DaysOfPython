# #FileNotFound error
# with open("non_exist.txt") as f:
#     f.read()
#
# #KeyError
# a_dict = {"key":1}
# print(a_dict["non_existing_key"])
#
# #IndexError
# nm_list=[1,2,3]
# nm = nm_list[10]
#
# #TypeError
# text="abc"
# print(text+5)

# try:
#     file = open("a_file.txt", "r")
#     a_dict = {"key": 1}
#     print(a_dict["key"])
# except FileNotFoundError:
#     file = open("a_file.txt", "+w")
#     file.write("Smth")
# except KeyError as error_message:
#     print(f"That key does not exist: {error_message}")
# else:
#     print(file.read())
# finally:
#     raise KeyError("HMMM")

# height=float(input("Height:"))
# weight=int(input("Weight:"))
#
# if height>3:
#     raise ValueError("Human height <= 3 meters")
#
# bmi = weight/height ** 2
# print(bmi)

# import pandas
#
# #1. Create a dictionary in this format:
# alphabet_nato_dict = {row.letter:row.code for (index, row) in pandas.read_csv("nato_phonetic_alphabet.csv").iterrows()}
#
# #2. Create a list of the phonetic code words from a word that the user inputs.
# word = ""
# while word.lower() != "exit":
#     try:
#         word = input("Enter a word: ")
#         new_list=[alphabet_nato_dict[letter.upper()] for letter in word]
#     except KeyError:
#         print("Sorry, only letters in the alphabet please")
#     except KeyboardInterrupt:
#         print("Please enter 'exit'")
#     else:
#         print(new_list)

