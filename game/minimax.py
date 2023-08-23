#!/usr/bin/env python3
from math import inf as infinity
from random import choice
import time
from game.board import Board


class Minimax(Board):
    def __init__(self):
        super().__init__()

    def minimax(self, depth, player):
        """
        AI function that choice the best move
        :param state: current state of the board
        :param depth: node index in the tree (0 <= depth <= 9),
        but never nine in this case (see iaturn() function)
        :param player: an human or a computer
        :return: a list with [the best row, best col, best score]
        """
        if player == self.COMP:
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, +infinity]

        if depth == 0 or self.game_over():
            score = self.evaluate()
            return [-1, -1, score]

        for cell in self.empty_cells():
            x, y = cell[0], cell[1]
            self.board[x][y] = player
            score = self.minimax(depth - 1, -player)
            self.board[x][y] = 0
            score[0], score[1] = x, y

            if player == self.COMP:
                if score[2] > best[2]:
                    best = score  # max value
            else:
                if score[2] < best[2]:
                    best = score  # min value

        return best

    def ai_turn(self):
        """
        It calls the minimax function if the depth < 9,
        else it choices a random coordinate.
        :param c_choice: computer's choice X or O
        :param h_choice: human's choice X or O
        :return:
        """
        depth = len(self.empty_cells())
        if depth == 0 or self.game_over():
            return

        self.clean()
        print(f"Computer turn [{self.c_choice}]")
        self.render()

        if depth == 9:
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])
        else:
            move = self.minimax(depth, self.COMP)
            x, y = move[0], move[1]

        self.set_move(x, y, self.COMP)
        time.sleep(1)

    def human_turn(self):
        """
        The Human plays choosing a valid move.
        :param c_choice: computer's choice X or O
        :param h_choice: human's choice X or O
        :return:
        """
        depth = len(self.empty_cells())
        if depth == 0 or self.game_over():
            return

        # Dictionary of valid moves
        move = -1
        moves = {
            1: [0, 0],
            2: [0, 1],
            3: [0, 2],
            4: [1, 0],
            5: [1, 1],
            6: [1, 2],
            7: [2, 0],
            8: [2, 1],
            9: [2, 2],
        }

        self.clean()
        print(f"Human turn [{self.h_choice}]")
        self.render()

        while move < 1 or move > 9:
            try:
                move = int(input("Use numpad (1..9): "))
                coord = moves[move]
                can_move = self.set_move(coord[0], coord[1], self.HUMAN)

                if not can_move:
                    print("Bad move")
                    move = -1
            except (EOFError, KeyboardInterrupt):
                print("Bye")
                exit()
            except (KeyError, ValueError):
                print("Bad choice")

    def evaluate(self):
        """
        Function to heuristic evaluation of state.
        :param state: the state of the current board
        :return: +1 if the computer wins; -1 if the human wins; 0 draw
        """
        if self.wins(self.COMP):
            score = +1
        elif self.wins(self.HUMAN):
            score = -1
        else:
            score = 0

        return score
