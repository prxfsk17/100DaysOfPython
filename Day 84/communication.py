class Communication:

    def __init__(self):
        print("Welcome to Tic Tac Toe Game!")

    def print_table(self, table):
        for i, row in enumerate(table):
            display_row = [char for char in row]
            print(" " + " | ".join(display_row) + " ")

            if i < len(table) - 1:
                print("---+" * (len(row) - 1) + "---")

    def user_turn(self, free_space):
        try:
            cell = int(input("Where do you want to put X? Input the number between 1 and 9: "))
        except ValueError:
            print("Please input decimal value.")
            return self.user_turn(free_space)
        else:
            if not 1 <= cell <= 9:
                print("Please input the number between 1 and 9.")
                return self.user_turn(free_space)
            else:
                if cell not in free_space:
                    print("Please input the number between 1 and 9 but the cell have to be empty.")
                    return self.user_turn(free_space)
                else:
                    return cell

    def round_winner(self, winner, table):
        if winner == "Draw":
            print("\nIt's draw!\n")
        else:
            print(f"\n{winner} wins this round!\n")
        self.print_table(table)

    def is_new_game(self):
        answer = input("Do you want to play another one round? Please type 'y' for yes and 'n' for no: ")
        if answer == 'y':
            return True
        elif answer == "n":
            return False
        else:
            print("Please type answer in correct format.")
            return self.is_new_game()

    def final_score(self, u_s, c_s):
        print(f"\nUser final score: {u_s}\nComputer final score: {c_s}.")
        if u_s > c_s:
            print("User wins the match! =)")
        elif u_s == c_s:
            print("It's draw.")
        else:
            print("Computers wins the match. =(")
