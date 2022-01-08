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


class Move():

    #conversion strings -- changing the ranks and files found in common chess notation to the rows and columns of our board matrix 
    #maps keys to values
    #key : value
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}       #converts each rank of squares in standard chess notation to a row in the board matrix. For reference, the black pieces start out at RANK 8 but ROW 0. The white pieces start at RANK 1 but ROW 7.  
    rows_to_ranks = {7: "1", 6: "2", 5: "3", 4: "4", 3: "5", 2: "6", 1: "7", 0: "8"}       #same thing but vice versa
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}       #converts each file of squares in standard chess notation to a column in the board matrix.
    cols_to_files = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}       #same thing but vice versa


    def __init__(self, start_square, end_square, board):        #Note: start_square and end_square are tuples
        self.start_row = start_square[0]    #creates a variable for starting row (getting the row coordinate of the tuple)
        self.start_col = start_square[1]    #creates a variable for starting column (getting the column coordinate of the tuple)
        self.end_row = end_square[0]        #same thing, but for end_row
        self.end_col = end_square[1]        #same thing, but for end_col
        self.piece_moved = board[self.start_row][self.start_col]    #gets the piece located on the board at the beginning square
        self.piece_captured = board[self.end_row][self.end_col]     #gets the piece located on the board at the ending square. This is the piece that is captured by any given move. Might end up being "--".


    #conversion method from matrix notation to chess notation (e.g. [6, 4] would become ["e", "3"]). I'm lazy. That's why this exists.
    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)  #creates a string that is a concatenation of starting square and ending square in chess notation. E.g. "e4e5"

    #helper method to get rank and file given row and column
    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]    #returns the file corresponding to the column "col" + the rank corresponding to the row "row". File then rank, because thats how chess notation works




def make_move(self, move):  #function that takes in a move object and updates the game_state according to the move made. Assumes move is valid.
    self.board[move.start_row][move.start_col] = "--" #makes the starting location an empty square 
    self.board[move.end_row][move.end_col] = move.piece_moved #sets the new square to be the piece that we moved from the old square.
    self.move_log.append(move)  #logs the move -- adds it to move log at the end of the log
    self.is_white_turn = not self.is_white_turn #changes turn from white to black or vice versa