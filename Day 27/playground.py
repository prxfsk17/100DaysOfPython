def add(*args):
    summ=0
    for n in args:
        summ += n
    return summ

print(add(1,2,23,45,6,4,432,3213231,423,4,))

def calculate(n, **kwargs):
    print(kwargs)
    for key, value in kwargs.items():
        print(key)
        print(value)
    print(kwargs["add"])
    print(n)

calculate(1, add=3, multiply=5)

class Car:

    def __init__(self, **kw):
        self.make = kw["make"]
        self.model = kw.get("model")

my_car = Car(make="Audi")