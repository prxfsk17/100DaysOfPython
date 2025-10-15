print("Welcome to the tip calculator!")
total = float(input("What was the total bill? $"))
percentage = int(input("How much tip would you like to give? 10, 12, or 15? "))
people_amount=int(input("How many people to split the bill? "))

print(f"Each person should pay: ${round(total * (percentage / 100 + 1) / people_amount, 2)}")

# 0.1 ≈ 0.1000000000000000055511151231257827021181583404541015625
# 0.2 ≈ 0.200000000000000011102230246251565404236316680908203125
# 0.1 + 0.2 ≈ 0.3000000000000000444089209850062616169452667236328125