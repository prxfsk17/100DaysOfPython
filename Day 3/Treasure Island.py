print('''
                                     _
                                    (_)
              |    .
          .   |L  /|   .          _
      _ . |\ _| \--+._/| .       (_)
     / ||\| Y J  )   / |/| ./
    J  |)'( |        ` F`.'/        _
  -<|  F         __     .-<        (_)
    | /       .-'. `.  /-. L___       
    J \      <    \  | | O\|.-'  _   
  _J \  .-    \/ O | | \  |F    (_) 
 '-F  -<_.     \   .-'  `-' L__    
__J  _   _.     >-'  )._.   |-'  
`-|.'   /_.           \_|   F    
  /.-   .                _.<     
 /'    /.'             .'  `\    
  /L  /'   |/      _.-'-\
 /'J       ___.---'\|
   |\  .--' V  | `. `
   |/`. `-.     `._)
      / .-.\
VK    \ (  `\
       `.\
''')
print("Welcome to Treasure Island!")
print("Your mission is to find the treasure.")
print("You're at a cross road. Where do you want to go?\n\t Type 'left' or 'right'")
side_to_go = input("").lower()
if side_to_go == "left":
    wait_or_swim = input("You've come to a lake. There is an island in the middle of the lake.\n\tType 'wait' to wait for a boat. Type 'swim' to swim across\n").lower()
    if wait_or_swim == "wait":
        door = input("You arrive at the island unharmed. There is a house with 3 doors.\n\tOne red, one yellow and one blue. Which colour do you choose?\n").lower()
        if door == "yellow":
            print("You found the treasure! You win!")
        elif door == "red":
            print("It's fire. Game over!")
        elif door == "blue":
            print("There is a beast. Game over!")
        else:
            print("Incorrect input!")
    elif wait_or_swim == "swim":
        print("Game over!")
    else:
        print("Incorrect input!")
elif side_to_go == "right":
    print("Game over!")
else:
    print("Incorrect input!")