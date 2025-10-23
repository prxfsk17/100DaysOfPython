import data

def work():
    fl = True
    while fl:
        answer = input("What would you like? (espresso, latte, cappuccino): ")
        if answer == "off":
            fl = False
        if answer in data.operations:
            data.operations[answer]()
work()