import random

random_int = random.randint(1, 10)
print(random_int)

random_simple = random.random()
print(random_simple)

random_float = random.uniform(1, 10)
print(random_float)

if random.random() < 0.5:
    print("Heads")
else:
    print("Tails")