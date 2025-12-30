import numpy as np
from random import choice

from communication import Communication

cells = {
    1 : [0, 0],
    2 : [0, 1],
    3 : [0, 2],
    4 : [1, 0],
    5 : [1, 1],
    6 : [1, 2],
    7 : [2, 0],
    8 : [2, 1],
    9 : [2, 2]
}

class Game:

    def __init__(self):
        self.game_is_on=True
        self.user_score = 0
        self.computer_score = 0
        self.is_player_turn = True
        self.table = np.full((3,3), " ")
        self.communicator = Communication()

    def game(self):

        self.communicator.print_table(self.table)
        while not self.is_game_end() and self.game_is_on:
            if self.is_player_turn:
                self.player_turn()
                self.is_player_turn = False
            else:
                self.computer_turn()
                self.communicator.print_table(self.table)
                self.is_player_turn = True

    def player_turn(self):
        indices = np.argwhere(self.table == " ")
        free_cells = {key for key, val in cells.items() if any(np.array_equal(val, idx) for idx in indices)}
        cell = cells[self.communicator.user_turn(free_cells)]
        self.table[cell[0], cell[1]] = "X"

    def computer_turn(self):
        indices = np.argwhere(self.table == " ")
        index = choice(indices)
        self.table[index[0], index[1]] = "O"

    def is_game_end(self):
        winner_char = " "

        indices = np.argwhere(self.table == " ")
        if len(indices) == 0:
            winner_char = "D"

        for row in self.table:
            if np.all(row == row[0]) and row[0]!=" ":
                winner_char = row[0]
                break

        if winner_char == " ":
            for col in range(self.table.shape[1]):
                if np.all(self.table[:, col] == self.table[0, col]) and self.table[0, col] != " ":
                    winner_char = self.table[0, col]
                    break

        if winner_char == " ":
            main_diagonal = self.table.diagonal()
            if np.all(main_diagonal == main_diagonal[0]) and main_diagonal[0] != " ":
                winner_char = main_diagonal[0]

        if winner_char == " ":
            sec_diagonal = np.fliplr(self.table).diagonal()
            if np.all(sec_diagonal == sec_diagonal[0]) and sec_diagonal[0] != " ":
                winner_char = sec_diagonal[0]
        if winner_char != " ":
            if winner_char == "X":
                self.user_score += 1
                self.communicator.round_winner("User", self.table)
            elif winner_char == "O":
                self.computer_score += 1
                self.communicator.round_winner("Computer", self.table)
            else:
                self.communicator.round_winner("Draw", self.table)
            if self.communicator.is_new_game():
                self.reset()
            else:
                self.communicator.final_score(self.user_score, self.computer_score)
                self.game_is_on=False

    def reset(self):
        self.is_player_turn = True
        self.table = np.full((3,3), " ")
        self.communicator.print_table(self.table)