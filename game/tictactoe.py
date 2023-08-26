from game.minimax import Minimax


class Tictactoe(Minimax):
    def __init__(self):
        super().__init__()
        self.h_choice = ""  # X or O
        self.c_choice = ""  # X or O
        self.first = ""  # if human is the first
        self.human_turn_ord = 0

    def run(self):
        """
        Main function that calls all functions
        """
        self.choose_x_o()
        self.choose_turn()

        # Main loop of this game
        while len(self.list_empty_cell) > 0 and not self.game_over_10():
            if self.first == "N":
                self.ai_turn()
                self.first = ""

            self.last_human_turn = self.human_turn()
            self.ai_turn()

        # # Game over message
        # if self.wins_10():
        #     self.clean()
        #     print(f"Human turn [{self.h_choice}]")
        #     self.render()
        #     print("YOU WIN!")
        # elif self.wins_10():
        #     self.clean()
        #     print(f"Computer turn [{self.c_choice}]")
        #     self.render()
        #     print("YOU LOSE!")
        # else:
        #     self.clean()
        #     self.render()
        #     print("DRAW!")

        # exit()

    def choose_x_o(self):
        # Human chooses X or O to play
        self.clean()
        while self.h_choice != "O" and self.h_choice != "X":
            try:
                print("")
                self.h_choice = input("Choose X or O\nChosen: ").upper()
            except (EOFError, KeyboardInterrupt):
                print("Bye")
                exit()
            except (KeyError, ValueError):
                print("Bad choice")

        # Setting computer's choice
        if self.h_choice == "X":
            self.c_choice = "O"
        else:
            self.c_choice = "X"

    def choose_turn(self):
        # Human may starts first
        self.clean()
        while self.first != "Y" and self.first != "N":
            try:
                self.first = input("First to start?[y/n]: ").upper()
            except (EOFError, KeyboardInterrupt):
                print("Bye")
                exit()
            except (KeyError, ValueError):
                print("Bad choice")
