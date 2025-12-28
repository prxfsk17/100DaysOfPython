from converter import MorseConverter

cipher = MorseConverter("cipher")
decipher = MorseConverter("decipher")
operator = ""
is_working=True
print('='*50)
print("Welcome to Morse-code Converter App")
print('='*50)

while is_working:
    operation = input("Please print 'c' if you want to convert text to Morse-code or print 'd' if you want reversed operation\n"
                      "If you want to end up with working, please type 'exit'.\n")
    if operation.lower() == "exit":
        is_working = False
        break
    if operation.lower().startswith('c'):
        operator = cipher
    elif operation.lower().startswith('d'):
        operator = decipher
    else:
        print("Incorrect input of operation. Please try again")
        continue
    data = input("What text you want to convert?\n")
    output = operator.operate(data)
    print("\n"*30)
    print(f"Your input was {data}\n"
          f"And the result of converting is {output}")

print("Goodbye!")