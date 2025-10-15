print("Welcome to the rollercoaster!")
height = int(input("What is your height in cm? "))

if height >= 120:
    bill = 0
    age = int(input("What is your age? "))
    if age <= 12:
        bill += 5
    elif age < 18:
        bill += 7
    elif 45 <= age <= 55: #age >= 45 and age <= 55
        bill = 0
    else:
        bill += 12
    if input("Do u want to take photos? ") == "Yes":
        bill += 3
    print(f"The final price is {bill}")
else:
    print("You can't pass!")
