from os import system
import platform
from copy import deepcopy


class Board:
    def __init__(self):
        self.board = self.init_board()
        self.straight_point = self.how_to_win()
        self.HUMAN = -1
        self.COMP = +1
        self.list_empty_cell = self.init_empty_cells()
        self.check_index = 0

    def init_board(self):
        board_length = 0
        while not board_length or board_length not in [3, 5, 10]:
            try:
                board_length = int(
                    input(
                        "Choose board length. We have 3x3 (input 3), 5x5 (input 5) 10x10 (input 10): "
                    )
                )
                if not board_length or board_length not in [3, 5, 10]:
                    print("Please type in 3, 5 or 10")
                    board_length = 0

                return [[0] * board_length for _ in range(board_length)]
            except (EOFError, KeyboardInterrupt):
                print("Bye")
                exit()
            except (KeyError, ValueError):
                print("Bad choice")

    def how_to_win(self):
        to_win = 0
        while not to_win or to_win not in [3, 4, 5]:
            try:
                to_win = int(
                    input("Choose how many point on a rows to win. We have 3 to 5: ")
                )
                if not to_win or to_win not in [3, 4, 5]:
                    print("Please type in 3,4 or 5")
                    to_win = 0

                if to_win > len(self.board):
                    print(
                        f"It's more than length of board {len(self.board)}. Please re-select"
                    )
                    to_win = 0

            except (EOFError, KeyboardInterrupt):
                print("Bye")
                exit()
            except (KeyError, ValueError):
                print("Bad choice")

        return to_win

    def init_empty_cells(self):
        list_empty_cell = list()
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                list_empty_cell.append([i, j])

        return list_empty_cell

    def clean(self):
        """
        Clears the console
        """
        os_name = platform.system().lower()
        if "windows" in os_name:
            system("cls")
        else:
            system("clear")

    def render(self):
        """
        Print the board on console
        """

        chars = {-1: self.h_choice, +1: self.c_choice, 0: " "}
        str_line = f"---------------------------------------"

        print("\n" + str_line)
        for row in self.board:
            for cell in row:
                symbol = chars[cell]
                print(f"| {symbol} |", end="")
            print("\n" + str_line)

    def empty_cells(self):
        """
        Each empty cell will be added into cells' list
        :return: a list of empty cells
        """
        cells = []

        for x, row in enumerate(self.board):
            for y, cell in enumerate(row):
                if cell == 0:
                    cells.append([x, y])
        return cells

    def valid_move(self, x, y):
        """
        A move is valid if the chosen cell is empty
        :param x: X coordinate
        :param y: Y coordinate
        :return: True if the board[x][y] is empty
        """
        if [x, y] in self.list_empty_cell:
            return True
        else:
            return False

    def wins(self, player):
        """
        This function tests if a specific player wins. Possibilities:
        * Three rows    [X X X] or [O O O]
        * Three cols    [X X X] or [O O O]
        * Two diagonals [X X X] or [O O O]
        :param state: the state of the current board
        :param player: a human or a computer
        :return: True if the player wins
        """
        win_state = [
            [self.board[0][0], self.board[0][1], self.board[0][2]],
            [self.board[1][0], self.board[1][1], self.board[1][2]],
            [self.board[2][0], self.board[2][1], self.board[2][2]],
            [self.board[0][0], self.board[1][0], self.board[2][0]],
            [self.board[0][1], self.board[1][1], self.board[2][1]],
            [self.board[0][2], self.board[1][2], self.board[2][2]],
            [self.board[0][0], self.board[1][1], self.board[2][2]],
            [self.board[2][0], self.board[1][1], self.board[0][2]],
        ]
        if [player, player, player] in win_state:
            return True
        else:
            return False

    def wins_10(self, temp_board=None):
        self.check_index += 1
        if not temp_board:
            temp_board = deepcopy(self.board)

        # print(temp_board)
        print(f"Check wins: {self.check_index} times")
        if point := self.check_win(temp_board):
            if point * self.HUMAN > 0:
                return self.HUMAN
            else:
                return self.COMP
        return False

    def game_over(self):
        """
        This function test if the human or computer wins
        :param state: the state of the current board
        :return: True if the human or computer wins
        """
        return self.wins(self.HUMAN) or self.wins(self.COMP)

    def game_over_10(self):
        """
        This function test if the human or computer wins
        :param state: the state of the current board
        :return: True if the human or computer wins
        """
        temp_board = deepcopy(self.board)
        result = self.wins_10(temp_board)
        del temp_board
        return result

    def set_move(self, x, y, player):
        """
        Set the move on board, if the coordinates are valid
        :param x: X coordinate
        :param y: Y coordinate
        :param player: the current player
        """
        if self.valid_move(x, y):
            self.board[x][y] = player
            self.list_empty_cell.remove([x, y])
            return True
        else:
            return False

    def check_win(self, temp_board):
        for r in range(1, len(temp_board)):
            for h in range(1, len(temp_board[0])):
                if temp_board[r - 1][h - 1] * temp_board[r][h] > 0:
                    temp_board[r][h] += temp_board[r - 1][h - 1]
                    if abs(temp_board[r][h]) == self.straight_point:
                        return temp_board[r][h]

        for r in range(0, len(temp_board)):
            for h in range(1, len(temp_board[0])):
                if temp_board[r][h - 1] * temp_board[r][h] > 0:
                    temp_board[r][h] += temp_board[r][h - 1]
                    if abs(temp_board[r][h]) == self.straight_point:
                        return temp_board[r][h]

        for r in range(1, len(temp_board)):
            for h in range(0, len(temp_board[0])):
                if temp_board[r - 1][h] * temp_board[r][h] > 0:
                    temp_board[r][h] += temp_board[r - 1][h]
                    if abs(temp_board[r][h]) == self.straight_point:
                        return temp_board[r][h]

        return
