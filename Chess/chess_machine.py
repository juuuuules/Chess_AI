#Responsible for storing all the information about the current chess game state. Also respnsible for determining the valid moves at the current game state.
#Might keep move log????

class Game_State:
    def __init__(self):
        #Board is an 8x8 2d list, each element has 2 characters.
        #First char represents color
        #Second char represents type of piece
        row1 = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]
        row2 = ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"]
        row3 = ["--", "--", "--", "--", "--", "--", "--", "--"]
        row4 = ["--", "--", "--", "--", "--", "--", "--", "--"]
        row5 = ["--", "--", "--", "--", "--", "--", "--", "--"]
        row6 = ["--", "--", "--", "--", "--", "--", "--", "--"]
        row7 = ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"]
        row8 = ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        board = [row1, row2, row3, row4, row5, row6, row7, row8]
        self.board = board

        self.is_white_turn = True #pretty self explantory
        self.move_log = [] #this will contain all previous moves when we finally implement that function
    
    def make_move(self, move):  #function that takes in a move object and updates the game_state according to the move made. Assumes move is valid.
        self.board[move.start_row][move.start_col] = "--" #makes the starting location an empty square 
        self.board[move.end_row][move.end_col] = move.piece_moved #sets the new square to be the piece that we moved from the old square.
        self.move_log.append(move)  #logs the move -- adds it to move log at the end of the log
        self.is_white_turn = not self.is_white_turn #changes turn from white to black or vice versa

    def piece_at_coordinates(self, row, column):
        return self.board[row][column]


    #return an array of all possible moves for the piece at the inputed square
    #the array will be 2 dimensional, and each element in the array will be an array of length 2 with the row and column 
    #of a square that the inputed piece can move to
    def get_valid_moves(self, row, column):
        solution = []
        piece = self.piece_at_coordinates(self, row, column)
        
        #add to the solution variable all the possible moves if the piece is a white pawn
        if(piece == "wP"): #checks to see if the selected square has a white pawn

            #this basically says: if the white pawn is below the first row (as in it hasn't moved to the end of the board),
            #and if the piece at the square directly in front of the pawn is empty,
            #than say that the square directly in front of the pawn is a possible move (by adding that square to the solution array)
            if(row > 0 and self.piece_at_coordinates(self, row - 1, column) == "--"): 
                solution += [row - 1, column]

                #this if statements adds an extra scenario where, if the pawn is on it's starting row, it can move 2 pieces forward
                #so long as the square 2 pieces forward is empty
                if(row == 6 and self.piece_at_coordinates(self, row - 2, column) == "--"):
                    solution += [row - 2, column]

            #this collection of if statements adds the possibility of the pawn moving diagonally to the solution array
            #it says, if the pawn is not on the 0th row,
            #and if it is not on the farthest column to the left or the farthest column to the right,
            if(row > 0 and (column > 0 and column < 7)):

                #than if the piece one up and one to the left of the selected pawn is black,
                if(self.piece_at_coordinates(self, row - 1, column - 1)[0] == "b"):

                    #than allow that move to be added to the solution array
                    solution += [row - 1, column - 1]

                #alternatively, if the piece one up and to the right of the selected pawn is black,
                if(self.piece_at_coordinates(self, row - 1, column + 1)[0] == "b"):

                    #than add the square one up and to the right of the selected pawn to the solution array
                    solution += [row - 1, column + 1]
        
        #this adds to the solution variable all the possible moves if the piece is a black pawn
        #this basically works the same as the previous collection of if statements
        #the only difference is that the - signs become + signs since the pawns are moving down the board not up it
        #also instead of checking if the pawn is on a square greater than 0 it will check if it is on one less than 7
        if(piece == "bP"): #checks to see if piece is black pawn

            #checks to see if pawn is not on the last row and if so, if the square in front of the pawn is empty
            if(row < 7 and self.piece_at_coordinates(self, row + 1, column) == "--"):

                #adds the square in front of the pawn to the solution array of possible moves
                solution += [row + 1, column]

                #adds the extra check to see if the pawn is on it's starting row and if so, if it can move 2 forward
                #it checks to see if the square 2 in front of the pawn is empty
                if(row == 1 and self.piece_at_coordinates(self, row + 2, column)[0] == "--"): 

                    #adds the option to move 2 forward to the solution array
                    solution += [row + 2, column]

            #this adds the possibility of the pawn moving diagnally to take other pieces
            if(row < 7 and (column > 0 and column < 7)): #checks that the pawn is not on the last row and not on the -->
                #leftmost or rightmost columns

                #checks if the piece one below and one to the left of the pawn is white
                if(self.piece_at_coordinates(self, row + 1, column - 1)[0] == "w"):

                    #if so it adds that square (one down and one to the left) to the solution array of possible moves
                    solution += [row + 1, column - 1]

                #checks if the piece one below and one to the right of the pawn is white
                if(self.piece_at_coordinates(self, row + 1, column + 1)[0] == "w"):
                    
                    #if so it adds that square (one below and one to the right) to the solution array of possible moves
                    solution += [row + 1, column + 1]

        #add to the solution variable all the possible moves if the piece is a rook
        if(piece[1] == "R"):
            #code to determine all spots above the rook that are valid moves
            keepLooping = True
            indexVariable = 1

            while(keepLooping):
                if(row - indexVariable >= 0):
                    if(self.piece_at_coordinates(self, row - indexVariable, column) == "--"):
                        solution += [row - indexVariable, column]
                    elif(self.piece_at_coordinates(self, row - indexVariable, column)[0] == self.piece_at_coordinates(self, row, column)[0]):
                        keepLooping = False
                    elif(self.piece_at_coordinates(self, row - indexVariable, column)[0] != self.piece_at_coordinates(self, row, column)[0]):
                        solution += [row - indexVariable, column]
                        keepLooping = False
                else:
                    keepLooping = False
                indexVariable += 1

            #code to determine all spots below the rook that are valid moves
            keepLooping = True
            indexVariable = 1

            while(keepLooping):
                if(row + indexVariable <= 7):
                    if(self.piece_at_coordinates(self, row + indexVariable, column) == "--"):
                        solution += [row + indexVariable, column]
                    elif(self.piece_at_coordinates(self, row + indexVariable, column)[0] == self.piece_at_coordinates(self, row, column)[0]):
                        keepLooping = False
                    elif(self.piece_at_coordinates(self, row + indexVariable, column)[0] != self.piece_at_coordinates(self, row, column)[0]):
                        solution += [row + indexVariable, column]
                        keepLooping = False
                else:
                    keepLooping = False
                indexVariable += 1
            
            #code to determine all spots left of the rook that are valid moves
            keepLooping = True
            indexVariable = 1

            while(keepLooping):
                if(column - indexVariable >= 0):
                    if(self.piece_at_coordinates(self, row, column - indexVariable) == "--"):
                        solution += [row, column - indexVariable]
                    elif(self.piece_at_coordinates(self, row, column - indexVariable)[0] == self.piece_at_coordinates(self, row, column)[0]):
                        keepLooping = False
                    elif(self.piece_at_coordinates(self, row, column - indexVariable)[0] != self.piece_at_coordinates(self, row, column)[0]):
                        solution += [row, column - indexVariable]
                        keepLooping = False
                else:
                    keepLooping = False
                indexVariable += 1
            
            #code to determine all spots right of the rook that are valid moves
            keepLooping = True
            indexVariable = 1

            while(keepLooping):
                if(column + indexVariable <= 7):
                    if(self.piece_at_coordinates(self, row, column + indexVariable) == "--"):
                        solution += [row, column + indexVariable]
                    elif(self.piece_at_coordinates(self, row, column + indexVariable)[0] == self.piece_at_coordinates(self, row, column)[0]):
                        keepLooping = False
                    elif(self.piece_at_coordinates(self, row, column + indexVariable)[0] != self.piece_at_coordinates(self, row, column)[0]):
                        solution += [row, column + indexVariable]
                        keepLooping = False
                else:
                    keepLooping = False
                indexVariable += 1







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



