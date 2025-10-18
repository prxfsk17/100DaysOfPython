# Funcs with more than 1 input
def greet_with(name, location):
    print(f"Hello {name}")
    print(f"What is it like in {location}?")

greet_with("Alessandro", "Italy") #positional arguments

greet_with(location="England", name="Alex") #keyword arguments