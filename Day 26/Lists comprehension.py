# numbers = [1, 2, 3] #any sequence: str, list, tuple, range
# new_list = [item+1 for item in numbers]
# print(new_list)
# new_list = [item*2 for item in range(1,6)]
# print(new_list)
# conditional
# new_list = [item*2 for item in range(1,6) if item*2 > 5]
# print(new_list)
names = ["Alex", "Beth", "Caroline", "Freddie"]
caps_names = [name.upper() for name in names if len(name)>5]
print(caps_names)
with open("f.txt") as f:
    f.readlines()