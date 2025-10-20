from arts import calculator

def preprint():
    return "+\n-\n*\n/\nPick an operation: "

def add(a, b):
    return a+b

def subtract(a, b):
    return a-b

def multiply(a,b):
    return a*b

def divide(a,b):
    return (a/b)

print(calculator)
operations = {
    "+" : add,
    "-" : subtract,
    "*" : multiply,
    "/" : divide
}

def calculator():
    calculating = True
    number1 = float(input("What's the first number? "))

    while calculating:
        operation = input(preprint())
        number2 = float(input("What's the next number? "))
        result = operations[operation](number1, number2)
        print(f"The result of {number1} {operation} {number2} is equal to {result}")
        choise = input(f"Type 'y' to continue calculating with {result} or type 'n' to start a new calculation: ")
        if choise == "y":
            number1 = result
        elif choise == "n":
            calculating = False
            calculator()
        else:
            calculating = False

calculator()