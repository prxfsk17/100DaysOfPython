with open("Input/Names/invited_names.txt") as f:
    names = f.read().split("\n")
print(names)
with open("Input/Letters/starting_letter.txt") as f:
    letter = f.readlines()
for name in names:
    new_letter=[]
    for s in letter:
        new_letter.append(s)
    new_letter[0] = new_letter[0].replace("[Name]", name)
    with open(f"output/ReadyToSend/letter_for_{name}.txt", "w") as f:
        f.writelines(new_letter)

