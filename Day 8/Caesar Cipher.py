def caesar_cipher(oper, mes, quant):
    result = ""
    if oper == "encode":
        for let in mes:
            new_char= ord(let) + quant
            if new_char > ord('z'):
                new_char += ord('a') - 1 - ord('z')
            result += chr(new_char)
        return result
    elif oper == "decode":
        for let in mes:
            new_char= ord(let) - quant
            if new_char < ord('a'):
                new_char += ord('z') - ord('a') + 1
            result += chr(new_char)
        return result
    else:
        return "Incorrect input!"

again = "yes"
while again == "yes":
    operation = input("Type 'encode' to encrypt, type 'decode' to decrypt: ")
    message = input("Type your message: ").lower()
    shift = int(input("Type the shift number: "))
    print(caesar_cipher(operation, message, shift))
    again = input("Type 'yes' if you want to go again. Otherwise type 'no'. ")
