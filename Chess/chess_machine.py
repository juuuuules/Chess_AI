class Game_State:
    def __init__(self):
        self.isWhiteTurn = True
        self.board = board

row1 = ["bR", "bN", "bB", "bQ", "bK", "bB", "bK", "bR"]
row2 = ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"]
row3 = ["--", "--", "--", "--", "--", "--", "--", "--"]
row4 = ["--", "--", "--", "--", "--", "--", "--", "--"]
row5 = ["--", "--", "--", "--", "--", "--", "--", "--"]
row6 = ["--", "--", "--", "--", "--", "--", "--", "--"]
row7 = ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"]
row8 = ["wR", "wN", "wB", "wQ", "wK", "wB", "wK", "wR"]

board = [row1, row2, row3, row4, row5, row6, row7, row8]
#asdffdsa



#JULIENS ADDITIONAL STUFF

#Responsible for storing all the information about the current chess game state. Also respnsible for determining the valid moves at the current game state.
#Might keep move log????

class game_state():
    def __init__(self):
        #Board is an 8x8 2d list, each element has 2 characters.
        #First char represents color
        #Second char represents type of piece
        
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.white_to_move = True
        self.move_love = []

