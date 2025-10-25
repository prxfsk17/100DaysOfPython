from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

menu = Menu()
coffee_m = CoffeeMaker()
money_m = MoneyMachine()
is_on = True
while is_on:
    operation = input(f"What would you like? {menu.get_items()}: ")
    if operation.lower() == "off":
        is_on = False
    elif operation.lower() == "report":
        coffee_m.report()
        money_m.report()
    else:
        coffee = menu.find_drink(operation)
        if coffee is not None:
            if coffee_m.is_resource_sufficient(coffee):
                if money_m.make_payment(coffee.cost):
                    coffee_m.make_coffee(coffee)
