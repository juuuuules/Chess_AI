#Responsible for storing all the information about the current chess game state. Also respnsible for determining the valid moves at the current game state.
#Might keep move log????

class Game_State:
    def __init__(self):
        #Board is an 8x8 2d list, each element has 2 characters.
        #First char represents color
        #Second char represents type of piece
        row1 = ["bR", "bN", "bB", "bQ", "bK", "bB", "bK", "bR"]
        row2 = ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"]
        row3 = ["--", "--", "--", "--", "--", "--", "--", "--"]
        row4 = ["--", "--", "--", "--", "--", "--", "--", "--"]
        row5 = ["--", "--", "--", "--", "--", "--", "--", "--"]
        row6 = ["--", "--", "--", "--", "--", "--", "--", "--"]
        row7 = ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"]
        row8 = ["wR", "wN", "wB", "wQ", "wK", "wB", "wK", "wR"]
        board = [row1, row2, row3, row4, row5, row6, row7, row8]
        self.board = board

        self.is_white_turn = True
        self.move_log = []

    #return what piece is at the inputed square
    def piece_at_coordinates(self, row, column):
        return self.board[row][column]

    #return an array of all possible moves for the piece at the inputed square
    def get_valid_moves(self, row, column):
        solution = []
        piece = self.pieceAtCoordinates(self, row, column)
        
        #add to the solution variable all the possible moves if the piece is a white pawn
        if(piece == "wP"):
            if(row > 0 and self.piece_at_coordinates(self, row - 1, column)[0] != "w"):
                solution += [row - 1, column]
                if(row == 6 and self.piece_at_coordinates(self, row - 2, column)[0] != "w"):
                    solution += [row - 2, column]
            if(row > 0 and (column > 0 and column < 7)):
                if(self.piece_at_coordinates(self, row - 1, column - 1)[0] == "b"):
                    solution += [row - 1, column - 1]
                if(self.piece_at_coordinates(self, row - 1, column + 1)[0] == "b"):
                    solution += [row - 1, column + 1]
        
        #add to the solution variable all the possible moves if the piece is a black pawn
        if(piece == "bP"):
            if(row < 7 and self.piece_at_coordinates(self, row + 1, column)[0] != "b"):
                solution += [row + 1, column]
                if(row == 1 and self.piece_at_coordinates(self, row + 2, column)[0] != "b"):
                    solution += [row + 2, column]
            if(row < 7 and (column > 0 and column < 7)):
                if(self.piece_at_coordinates(self, row + 1, column - 1)[0] == "w"):
                    solution += [row + 1, column - 1]
                if(self.piece_at_coordinates(self, row + 1, column + 1)[0] == "w"):
                    solution += [row + 1, column + 1]

        #add to the solution variable all the possible moves if the piece is a rook
        if(piece[1] == "R"):
