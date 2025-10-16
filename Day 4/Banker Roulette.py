import random
friends = ["Alice", "Bob", "Charlie", "David"]
print(friends[random.randint(0,len(friends)-1)])

print(random.choice(friends))

# IndexError
# print(friends[5])

