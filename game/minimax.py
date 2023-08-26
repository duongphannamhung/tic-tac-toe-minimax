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

        if depth == 0 or self.game_over_10():
            score = self.evaluate_10()
            return [-1, -1, score]

        for cell in self.list_empty_cell:
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

    def minimax_alpha_beta(self, depth, alpha, beta, maximizing_player):
        if result := self.evaluate_10():
            return result

        if maximizing_player:
            max_eval = -infinity
            for i in range(len(self.board)):
                for j in range(len(self.board)):
                    if self.board[i][j] == 0:
                        self.board[i][j] = self.COMP
                        _eval = self.minimax_alpha_beta(depth + 1, alpha, beta, False)
                        self.board[i][j] = 0
                        max_eval = max(max_eval, _eval)
                        alpha = max(alpha, _eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = +infinity
            for i in range(len(self.board)):
                for j in range(len(self.board)):
                    if self.board[i][j] == 0:
                        self.board[i][j] = self.HUMAN
                        _eval = self.minimax_alpha_beta(depth + 1, alpha, beta, True)
                        self.board[i][j] = 0
                        min_eval = min(min_eval, _eval)
                        beta = min(beta, _eval)
                        if beta <= alpha:
                            break
            return min_eval

    def ai_find_best_move(self):
        best_move = None
        best_eval = -infinity
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == 0:
                    self.board[i][j] = self.COMP
                    _eval = self.minimax_alpha_beta(0, -infinity, +infinity, False)
                    self.board[i][j] = 0
                    if _eval > best_eval:
                        best_eval = _eval
                        best_move = (i, j)
        return best_move

    def ai_find_relative_move(self):
        x, y = self.last_human_turn
        move_x, move_y = choice(
            [
                [x, y - 1],
                [x, y + 1],
                [x - 1, y],
                [x + 1, y],
                [x - 1, y - 1],
                [x - 1, y + 1],
                [x + 1, y - 1],
                [x + 1, y + 1],
            ]
        )
        self.set_move(move_x, move_y, self.COMP)
        # while not :
        #     move_x, move_y = choice(
        #         [
        #             [x, y - 1],
        #             [x, y + 1],
        #             [x - 1, y],
        #             [x + 1, y],
        #             [x - 1, y - 1],
        #             [x - 1, y + 1],
        #             [x + 1, y - 1],
        #             [x + 1, y + 1],
        #         ]
        #     )

    def ai_init_move(self):
        if self.human_turn_ord == 0 or (
            self.last_human_turn[0] == 0 or self.last_human_turn[1] == 0
        ):
            return self.set_move(
                len(self.board) // 2, len(self.board[0]) // 2, self.COMP
            )
        return self.ai_find_relative_move()

    def ai_turn(self):
        """
        It calls the minimax function if the depth < 9,
        else it choices a random coordinate.
        :param c_choice: computer's choice X or O
        :param h_choice: human's choice X or O
        :return:
        """
        if self.human_turn_ord <= 3:
            return self.ai_init_move()

        depth = len(self.list_empty_cell)
        if depth == 0 or self.game_over():
            return

        # self.clean()
        print(f"Computer turn [{self.c_choice}]")
        self.render()

        max_depth = len(self.board) * len(self.board[0])
        if depth == max_depth:
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])
        else:
            # move = self.minimax(depth, self.COMP)
            move = self.ai_find_best_move()
            x, y = move[0], move[1]

        self.set_move(x, y, self.COMP)
        # time.sleep(1)

    def human_turn(self):
        """
        The Human plays choosing a valid move.
        :param c_choice: computer's choice X or O
        :param h_choice: human's choice X or O
        :return:
        """
        self.human_turn_ord += 1  # Count on human turn

        depth = len(self.list_empty_cell)
        if depth == 0 or self.game_over():
            return

        # Dictionary of valid moves
        move = -1

        # self.clean()
        print(f"Human turn [{self.h_choice}]")
        self.render()

        while move == -1:
            try:
                X = int(input("Input coord [X,Y]. X first: "))
                Y = int(input("Input coord [X,Y]. Then Y: "))
                can_move = self.set_move(X, Y, self.HUMAN)

                if not can_move:
                    print("Bad move")
                    move = -1
                else:
                    return (X, Y)
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

    def evaluate_10(self):
        """
        Function to heuristic evaluation of state.
        :param state: the state of the current board
        :return: +1 if the computer wins; -1 if the human wins; 0 draw
        """
        wins = self.wins_10()
        if wins == self.COMP:
            score = +1
        elif wins == self.HUMAN:
            score = -1
        else:
            score = 0

        return score
