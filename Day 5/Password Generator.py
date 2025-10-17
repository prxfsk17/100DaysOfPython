import random
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+']
print("Welcome to the PyPassword Generator!")
print("How many letters would you like in your password?")
let_count = int(input())
print("How many symbols would you like in your password?")
symb_count = int(input())
print("How many numbers would you like in your password?")
num_count = int(input())
password_first = []
for i in range(let_count):
    password_first.append(letters[random.randint(0, len(letters)-1)])
for i in range(symb_count):
    password_first.append(symbols[random.randint(0, len(symbols)-1)])
for i in range(num_count):
    password_first.append(numbers[random.randint(0, len(numbers)-1)])
print(password_first)
random.shuffle(password_first)
print(password_first)
password = "".join(password_first)
print(f"Your password is {password}")