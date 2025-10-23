def report():
    print(f"Water: {resources["water"]}ml")
    print(f"Milk: {resources["milk"]}ml")
    print(f"Coffee: {resources["coffee"]}g")
    print(f"Money: ${round(money_in_machine, 2)}")

def check_resources(coffee):
    try:
        if coffee["ingredients"]["water"] > resources["water"]:
            print("Sorry there is not enough water.")
            return False
        elif coffee["ingredients"]["milk"] > resources["milk"]:
            print("Sorry there is not enough milk.")
            return False
        elif coffee["ingredients"]["coffee"] > resources["coffee"]:
            print("Sorry there is not enough coffee.")
            return False
        else:
            return True
    except KeyError:
        if coffee["ingredients"]["coffee"] > resources["coffee"]:
            print("Sorry there is not enough coffee.")
            return False
        return True

def process_coins():
    inserted_money = 0
    print("Please insert coins.")
    inserted_money += int(input("How many quarters?: ")) * 0.25
    inserted_money += int(input("How many dimes?: ")) * 0.1
    inserted_money += int(input("How many nickles?: ")) * 0.05
    inserted_money += int(input("How many pennies?: ")) * 0.01
    return inserted_money

def make_a_coffee(coffee, coffee_name):
    global money_in_machine
    if check_resources(coffee):
        money = process_coins()
        if money >= coffee["cost"]:
            for ingredient in coffee["ingredients"]:
                resources[ingredient] -= coffee["ingredients"][ingredient]
            money_in_machine += coffee["cost"]
            print(f"Here is ${round(money - coffee["cost"], 2)} in change.")
            print(f"Here is your {coffee_name}. Enjoy! {coffee_emoji}")
        else:
            print("Sorry that's not enough money. Money refunded.")

def cappuccino():
    coffee = MENU["cappuccino"]
    make_a_coffee(coffee, "cappuccino")

def latte():
    coffee = MENU["latte"]
    make_a_coffee(coffee, "latte")

def espresso():
    coffee = MENU["espresso"]
    make_a_coffee(coffee, "espresso")

coffee_emoji = "☕"
money_in_machine = 0

MENU = {
    "espresso" : {
        "ingredients": {
            "water" : 50,
            "coffee" : 10,
        },
        "cost" : 1.5,
    },
    "latte" : {
        "ingredients": {
            "water" : 200,
            "milk" : 150,
            "coffee" : 24,
        },
        "cost" : 2.5,
    },
    "cappuccino" : {
        "ingredients": {
            "water" : 250,
            "milk" : 100,
            "coffee" : 24,
        },
        "cost" : 3.0,
    },
}

resources = {
    "water" : 1000,
    "milk" : 500,
    "coffee" : 250
}

operations = {
    "cappuccino" : cappuccino,
    "latte" : latte,
    "espresso" : espresso,
    "report" : report,
}