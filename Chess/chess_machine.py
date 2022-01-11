#Responsible for storing all the information about the current chess game state. Also respnsible for determining the valid moves at the current game state.
#Might keep move log????

class Game_State:

    #constructor
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

        self.valid_moves = []

#        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

        
    #overriding the equals method
 #   def __eq__(self, other):
  #      if isinstance(other, Move):
   #         return self.moveID == other.moveID
    #    return False

    def make_move(self, move):  #function that takes in a move object and updates the game_state according to the move made. Assumes move is valid.
        self.board[move.start_row][move.start_col] = "--" #makes the starting location an empty square 
        self.board[move.end_row][move.end_col] = move.piece_moved #sets the new square to be the piece that we moved from the old square.
        self.move_log.append(move)  #logs the move -- adds it to move log at the end of the log
        self.is_white_turn = not self.is_white_turn #changes turn from white to black or vice versa

    def undo_move(self):    #function that undoes last move
        if len(self.move_log) != 0: #checks to see whether there is a move to undo
            move = self.move_log[-1]  #gets the last element in the move_log list
            self.move_log = self.move_log[:-1]  #removes the last element in the move_log list
            self.board[move.start_row][move.start_col] = move.piece_moved   #sets the start row and column of the move back to what it was before the move was made
            self.board[move.end_row][move.end_col] = move.piece_captured    #sets the end row and column of the move back to what it was before the move was made
            self.is_white_turn = not self.is_white_turn #changes turn
            


    def piece_at_coordinates(self, row, column):
        return self.board[row][column]


    #return an array of all possible moves for the piece at the inputed square
    #the array will be 2 dimensional, and each element in the array will be an array of length 2 with the row and column 
    #of a square that the inputed piece can move to

    #EVAN, IMO WE SHOULD MAKE DIFFERENT METHODS BASED ON PAWNS, ROOK, NIGHT, BISHOP, ETC. SO WE WOULD HAVE get_pawn_moves, get_bishop_moves, etc.
    # THEN, WE COULD CREATE A MAP AT THE TOP THAT SAYS SOMETHING LIKE {"P": self. get_pawn_moves, "R": self.get_rook_moves, etc}.
    # THEN, the get_valid_moves method would just call the appropriate getter method depending on the given piece at the location.
    # Makes it much easier to read and less computationally intensive, bc the computer doesn't have to read a ton of if statements many times per frame 
    
    #also, i changed the name to get_possible_moves, because we should have a SEPARATE function that considers checks. I.e. a pawn cannot move if it is pinned
    def get_possible_moves(self, row, column):
        possible_moves = []
        piece = self.piece_at_coordinates(self, row, column)
        
        #add to the solution variable all the possible moves if the piece is a white pawn
        if(piece == "wP"): #checks to see if the selected square has a white pawn

            #this basically says: if the white pawn is below the first row (as in it hasn't moved to the end of the board),
            #and if the piece at the square directly in front of the pawn is empty,
            #than say that the square directly in front of the pawn is a possible move (by adding that square to the solution array)
            if(row > 0 and self.piece_at_coordinates(self, row - 1, column) == "--"): 
                self.possible_moves += [row - 1, column]

                #this if statements adds an extra scenario where, if the pawn is on it's starting row, it can move 2 pieces forward
                #so long as the square 2 pieces forward is empty
                if(row == 6 and self.piece_at_coordinates(self, row - 2, column) == "--"):
                    self.possible_moves += [row - 2, column]

            #this collection of if statements adds the possibility of the pawn moving diagonally to the solution array
            #it says, if the pawn is not on the 0th row

            #than if the piece one up and one to the left of the selected pawn is black,
            if(column > 0 and self.piece_at_coordinates(self, row - 1, column - 1)[0] == "b"):
                #than allow that move to be added to the solution array
                self.possible_moves += [row - 1, column - 1]

            #alternatively, if the piece one up and to the right of the selected pawn is black,
            if(column < 7 and self.piece_at_coordinates(self, row - 1, column + 1)[0] == "b"):
                    #than add the square one up and to the right of the selected pawn to the solution array
                    self.possible_moves += [row - 1, column + 1]
        
        #this adds to the solution variable all the possible moves if the piece is a black pawn
        #this basically works the same as the previous collection of if statements
        #the only difference is that the - signs become + signs since the pawns are moving down the board not up it
        #also instead of checking if the pawn is on a square greater than 0 it will check if it is on one less than 7
        if(piece == "bP"): #checks to see if piece is black pawn

            #checks to see if pawn is not on the last row and if so, if the square in front of the pawn is empty
            if(row < 7 and self.piece_at_coordinates(self, row + 1, column) == "--"):

                #adds the square in front of the pawn to the solution array of possible moves
                self.possible_moves += [row + 1, column]

                #adds the extra check to see if the pawn is on it's starting row and if so, if it can move 2 forward
                #it checks to see if the square 2 in front of the pawn is empty
                if(row == 1 and self.piece_at_coordinates(self, row + 2, column)[0] == "--"): 

                    #adds the option to move 2 forward to the solution array
                    self.possible_moves += [row + 2, column]

            #this adds the possibility of the pawn moving diagnally to take other pieces

            #checks if the piece one below and one to the left of the pawn is white
            if(column > 0 and self.piece_at_coordinates(self, row + 1, column - 1)[0] == "w"):

                    #if so it adds that square (one down and one to the left) to the solution array of possible moves
                    self.possible_moves += [row + 1, column - 1]

                #checks if the piece one below and one to the right of the pawn is white
            if(self.piece_at_coordinates(self, row + 1, column + 1)[0] == "w"):
                #if so it adds that square (one below and one to the right) to the solution array of possible moves
                self.possible_moves += [row + 1, column + 1]

            #checks if the piece one below and one to the right of the pawn is white
            if(column < 7 and self.piece_at_coordinates(self, row + 1, column + 1)[0] == "w"):
                #if so it adds that square (one below and one to the right) to the solution array of possible moves
                self.possible_moves += [row + 1, column + 1]

        #add to the solution variable all the possible moves if the piece is a rook
        if(piece[1] == "R"):
            #code to determine all spots above the rook that are valid moves
            keepLooping = True
            indexVariable = 1

            while(keepLooping):
                if(row - indexVariable >= 0):
                    if(self.piece_at_coordinates(self, row - indexVariable, column) == "--"):
                        self.possible_moves += [row - indexVariable, column]
                    elif(self.piece_at_coordinates(self, row - indexVariable, column)[0] == self.piece_at_coordinates(self, row, column)[0]):
                        keepLooping = False
                    elif(self.piece_at_coordinates(self, row - indexVariable, column)[0] != self.piece_at_coordinates(self, row, column)[0]):
                        self.possible_moves += [row - indexVariable, column]
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
                        self.possible_moves += [row + indexVariable, column]
                    elif(self.piece_at_coordinates(self, row + indexVariable, column)[0] == self.piece_at_coordinates(self, row, column)[0]):
                        keepLooping = False
                    elif(self.piece_at_coordinates(self, row + indexVariable, column)[0] != self.piece_at_coordinates(self, row, column)[0]):
                        self.possible_moves += [row + indexVariable, column]
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
                        self.possible_moves += [row, column - indexVariable]
                    elif(self.piece_at_coordinates(self, row, column - indexVariable)[0] == self.piece_at_coordinates(self, row, column)[0]):
                        keepLooping = False
                    elif(self.piece_at_coordinates(self, row, column - indexVariable)[0] != self.piece_at_coordinates(self, row, column)[0]):
                        self.possible_moves += [row, column - indexVariable]
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
                        self.possible_moves += [row, column + indexVariable]
                    elif(self.piece_at_coordinates(self, row, column + indexVariable)[0] == self.piece_at_coordinates(self, row, column)[0]):
                        keepLooping = False
                    elif(self.piece_at_coordinates(self, row, column + indexVariable)[0] != self.piece_at_coordinates(self, row, column)[0]):
                        self.possible_moves += [row, column + indexVariable]
                        keepLooping = False
                else:
                    keepLooping = False
                indexVariable += 1

    #of the possible moves that can occur, filters out the ones that would result in a check
    def get_valid_moves(self):
        #Pseudo code:
        # 1 - get all possible moves. Calls the get_possible_moves method.
        # 2 - generates all moves for the OPPOSING player
        # 3 - sees if any of those moves attacks king
        # 4 - if and only if the king is safe, add that element of possible_moves[] to valid_moves[]
        return self.get_possible_moves_MODIFIED()

    #looks at the whole board, and generates all the possible moves that a given side can make. This includes pieces moving while pinned, kings moving into check, etc.
    def get_possible_moves_MODIFIED(self):
        moves = []
        for r in range(len(self.board)): #iterates through the rows
            for c in range(len(self.board[r])):  #iterates through the columns in a given row
                color = self.board[r][c][0]  #extracts the first character of a given string in the 8x8 array. That returns the COLOR of the piece at any particular square.
                if (color == 'w' and self.is_white_turn) or (color == 'b' and not self.is_white_turn):   #if color of piece matches who's turn it is, then look at that piece as a valid piece to move
                    piece = self.board[r][c][1] #extracts the second character of the string -- that gives the piece type, i.e. 'P', 'R', 'Q', etc.
                    if piece == 'P':   #if piece is a pawn
                        self.get_pawn_moves(r, c, moves)    #gets all possible pawn moves
                    elif piece == 'R': 
                        self.get_rook_moves(r, c, moves)
                    elif piece == 'Q':
                        self.get_queen_moves(r, c, moves)
                    elif piece == 'N':
                        self.get_knight_moves(r, c, moves)
                    elif piece == 'B':
                        self.get_bishop_moves(r, c, moves)
                    elif piece == 'K':
                        self.get_king_moves(r, c, moves)
        return moves

    def get_pawn_moves(self, row, column, moves):   #gets all possible moves for the pawns. Copy-paste evan's code with some slight modifications
        if self.is_white_turn:  #limits out to just look at the white pawn moves

            #one square move
            if(row > 0 and self.board[row-1][column] == "--"):  #if white pawn has not reached the end of the board and if square in front of pawn is empty
                moves.append(Move((row, column), (row - 1, column), self.board))    #creates a new move object, up 1 square, adds it to the list of moves
                #two square move
                if(row == 6 and self.board[row-2][column] == "--"): #if white pawn is on sixth row (can move two squares) and square two in front of pawn is empty
                    moves.append(Move((row, column), (row-2, column), self.board))  #adds a new 2 square move to the list of moves
            #captures to the left
            if(column > 0): #if pawn is not on the left-most file
                if(self.board[row - 1][column - 1][0] == 'b'):  #if square diagonally upwards and to the left contains a black piece
                    moves.append(Move((row, column), (row - 1, column - 1), self.board))   #adds a new diagonal capture to the list of moves   
            #captures to the right
            if(column < 7): #if pawn is not on right-most file
                if(self.board[row-1][column+1][0] == 'b'): #if square diagonally upwards and to the right contains a black piece
                    moves.append(Move((row, column), (row - 1, column + 1), self.board))    #adds a new diagonal capture to the list of moves
        
        else:   #black pawn moves
            #one-square moves
            if(row < 7 and self.board[row + 1][column] == "--"):  #if black pawn has not reached the end of the board and if square in front of pawn is empty
                moves.append(Move((row, column), (row + 1, column), self.board))    #creates a new move object, up 1 square, adds it to the lsit of moves
                #two square moves
                if(row == 1 and self.board[row + 2][column] == "--"):   #if black pawn is on first row (can move two squares) and square two in front of pawn is empty
                    moves.append(Move((row, column), (row + 2, column), self.board))    #adds a new 2 square move to the list of moves
            #captures to the left
            if(column > 0):     #if pawn is not on the left-most file
                if(self.board[row + 1][column - 1][0] == 'w'):  #if square diagonally downwards and to the left contains a white piece
                    moves.append(Move((row, column), (row + 1, column - 1), self.board))
            #captures to the right
            if(column < 7): #if pawn is not on the right-most file
                if(self.board[row + 1][column + 1][0] == 'w'):      #if square diagonally downwards and to the right contains a white piece
                    moves.append(Move((row, column), (row + 1, column + 1), self.board))    #adds a new diagonal capture to the list of moves

    def get_rook_moves(self, row, column, moves):   #gets all possible moves for the rook. Copy and paste evan's code with some slight mdifications
        #Note: unlike pawn moves, the color of the rook does not affect its movement possibilities

        directions = ((-1, 0), (1, 0), (0, -1), (0, 1)) #basis vectors for directions: up, down, left, right
        if self.is_white_turn:  #sets the enemy color. If it's white to move, enemy color is black. Otherwise, it's white.
            enemy_color = 'b'
        else:
            enemy_color = 'w'
        
        for direction in directions:    #iterates through the directions: up, down, left, right
            for i in range(1, 8):   #iterates from 1 to 8
                end_row = row + direction[0] * i       #sets the end row to be the start row PLUS i rows up or down. If the direction is (0, -1) or (0, 1), aka left or right, direction[0] will be zero and the row index will not change.
                end_column = column + direction[1] * i     #sets the end column to be start column PLUS i columns left or right. If the direction is (-1, 0) or (1, 0), aka up or down, direction[1] will be zero and the column index will not change.
                if(end_row >= 0 and end_row <= 7 and end_column >=0 and end_column <= 7):   #if ending square is within boundaries of the board
                    if(self.board[end_row][end_column] == "--"):    #if ending square is empty
                        moves.append(Move((row, column), (end_row, end_column), self.board))    #add that move to the list of moves
                    elif(self.board[end_row][end_column][0] == enemy_color):    #if ending square contains a piece of enemy color
                        moves.append(Move((row, column), (end_row, end_column), self.board))    #add that move to the list of moves
                        break   #break the inner for loop (the one with i) -- now that the rook has hit a piece, it can't go any further in this direction. Break tells the computer iterate to the next available direction
                    else:       #if the square is a friendly piece
                        break   #break the inner for loop for the same reasons as above
                else: #else off board
                    break   #go to the next direction

    def get_queen_moves(self, row, column, moves):
        #figure this out later and copy-paste evan's code
        pass

    def get_knight_moves(self, row, column, moves):
        directions = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2))   #tuple in form (row, column). up/left, up/right, down/left, down/right, left/up, right/up, left/down, right/down
        if self.is_white_turn:  #sets the enemy color. If it's white to move, enemy color is black. Otherwise, it's white.
            enemy_color = 'b'
        else:
            enemy_color = 'w'
        
        for direction in directions:
            end_row = row + direction[0]    #sets the end row to be start row + the first term of a particular direction
            end_column = column + direction[1]  #sets the end column to be start column + second term of a particular direction
        if(end_row >= 0 and end_row <= 7 and end_column >=0 and end_column <= 7):   #if ending square is within boundaries of the board
            if(self.board[end_row][end_column] == "--"):    #if ending square is empty
                moves.append(Move((row, column), (end_row, end_column), self.board))    #add move to moves list
            elif(self.board[end_row][end_column][0] == enemy_color):    #if ending square contains piece of enemy color
                moves.append(Move((row, column), (end_row, end_column), self.board))    #add move to moves list
    

    def get_bishop_moves(self, row, column, moves):
        #figure this out later and copy-paste evan's code
        pass

    def get_king_moves(self, row, column, moves):
        #figure this out later and copy-paste evan's code
        pass















class Move():

    #conversion strings -- changing the ranks and files found in common chess notation to the rows and columns of our board matrix 
    #maps keys to values
    #key : value
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}       #converts each rank of squares in standard chess notation to a row in the board matrix. For reference, the black pieces start out at RANK 8 but ROW 0. The white pieces start at RANK 1 but ROW 7.  
    rows_to_ranks = {7: "1", 6: "2", 5: "3", 4: "4", 3: "5", 2: "6", 1: "7", 0: "8"}       #same thing but vice versa
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}       #converts each file of squares in standard chess notation to a column in the board matrix.
    cols_to_files = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}       #same thing but vice versa

    #constructor
    def __init__(self, start_square, end_square, board):        #Note: start_square and end_square are tuples
        self.start_row = start_square[0]    #creates a variable for starting row (getting the row coordinate of the tuple)
        self.start_col = start_square[1]    #creates a variable for starting column (getting the column coordinate of the tuple)
        self.end_row = end_square[0]        #same thing, but for end_row
        self.end_col = end_square[1]        #same thing, but for end_col
        self.piece_moved = board[self.start_row][self.start_col]    #gets the piece located on the board at the beginning square
        self.piece_captured = board[self.end_row][self.end_col]     #gets the piece located on the board at the ending square. This is the piece that is captured by any given move. Might end up being "--".
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col   #gives each move a unique move id between 0 and 7777. Useful when comparing whether two moves are equal.
    
    #Overriding the equals method. This means that two moves are considered "equal" if they have the same start row, start col, end row, and end col. That information is nicely tracked in the move ID variable
    #This is copy-pasted from stack exchange lol
    def __eq__(self, other):    #comparing the self object to another move object, saved in the parameter other
        if isinstance(other, Move): #if "other" object is an instance of the Move class
             return self.moveID == other.moveID #returns true if two move IDs are the same, and false if they are different.
        return False

    #conversion method from matrix notation to chess notation (e.g. [6, 4] would become ["e", "3"]). I'm lazy. That's why this exists.
    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)  #creates a string that is a concatenation of starting square and ending square in chess notation. E.g. "e4e5"

    #helper method to get rank and file given row and column
    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]    #returns the file corresponding to the column "col" + the rank corresponding to the row "row". File then rank, because thats how chess notation works



