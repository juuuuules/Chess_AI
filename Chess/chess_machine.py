class Game_State:
    def __init__(self):
        self.isWhiteTurn = True
        self.board = board
    def sidIsGreat(self):
        print("sid is great")

row1 = ["bR", "bN", "bB", "bQ", "bK", "bB", "bK", "bR"]
row2 = ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"]
row3 = ["--", "--", "--", "--", "--", "--", "--", "--"]
row4 = ["--", "--", "--", "--", "--", "--", "--", "--"]
row5 = ["--", "--", "--", "--", "--", "--", "--", "--"]
row6 = ["--", "--", "--", "--", "--", "--", "--", "--"]
row7 = ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"]
row8 = ["wR", "wN", "wB", "wQ", "wK", "wB", "wK", "wR"]

board = [row1, row2, row3, row4, row5, row6, row7, row8]
