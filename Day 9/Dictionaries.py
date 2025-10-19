programming_dictionary = {
    "Bug" : "An error in program",
    "Function" : "A piece of code (over and over again)",
    "Loop" : "The action of doing again and again",
    123 : '123'
}

print(programming_dictionary["Bug"])
programming_dictionary[456] = "456"
print(programming_dictionary)

empty_dictionary = {}
# programming_dictionary = {}
# programming_dictionary["Bug"] = "new value"

for thing in programming_dictionary:
    print(thing)
    print(programming_dictionary[thing])
