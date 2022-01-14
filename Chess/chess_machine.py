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

        #i couldn't figure out how to deal with checks, so i decided to just keep track of kings location. Also should help w castling
        self.white_king_location = (7, 4)   #white king starts at row 7 col 4    
        self.black_king_location = (0, 4)   #black king starts at row 0 col 4
        self.is_checkmate = False
        self.is_stalemate = False


    def make_move(self, move):  #function that takes in a move object and updates the game_state according to the move made. Assumes move is valid.
        self.board[move.start_row][move.start_col] = "--" #makes the starting location an empty square 
        self.board[move.end_row][move.end_col] = move.piece_moved #sets the new square to be the piece that we moved from the old square.
        self.move_log.append(move)  #logs the move -- adds it to move log at the end of the log
        self.is_white_turn = not self.is_white_turn #changes turn from white to black or vice versa
        
        #updates the king position if king is movedmoved
        if(move.piece_moved == 'wK'):   #if white king is moved
            self.white_king_location = (move.end_row, move.end_col) #set white king location to the end square of the king move
        elif (move.piece_moved == 'bK'):
            self.black_king_location = (move.end_row, move.end_col) #set black king location to the end square of the king move


    def undo_move(self):    #function that undoes last move
        if len(self.move_log) != 0: #checks to see whether there is a move to undo
            move = self.move_log[-1]  #gets the last element in the move_log list
            self.move_log = self.move_log[:-1]  #removes the last element in the move_log list
            self.board[move.start_row][move.start_col] = move.piece_moved   #sets the start row and column of the move back to what it was before the move was made
            self.board[move.end_row][move.end_col] = move.piece_captured    #sets the end row and column of the move back to what it was before the move was made
            self.is_white_turn = not self.is_white_turn #changes turn
        #updates the king position if king is moved
        if(move.piece_moved == 'wK'):   #if white king is moved
            self.white_king_location = (move.start_row, move.start_col) #set white king location back to the start square of the king move
        elif (move.piece_moved == 'bK'):
            self.black_king_location = (move.start_row, move.start_col) #set black king location back to the start square of the king move
      
        self.is_checkmate = False
        self.is_stalemate = False   #sets checkmate and stalemate to be false, just in case we undo a move that causes checkmate/stalemate. 
        



    def square_under_attack(self, row, column):   #determines whether an enemy can attack the square row / col
        self.is_white_turn = not self.is_white_turn #looks at opponents moves
        opponent_moves = self.get_possible_moves_MODIFIED()
        self.is_white_turn = not self.is_white_turn #switches back perspective
        for move in opponent_moves:
            if (move.end_row == row and move.end_col == column): #if there exists a possible move that would end on the specified row and column, i.e. square is under attack
                return True
        return False

    #checks to see whether king is in check
    def in_check(self):
        if self.is_white_turn:  #if it's white to move
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])  #checks wehther the white king's location is being attacked
        else:   #if black to move
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])   #checks whether the black king's location is being attacked

    #of the possible moves that can occur, filters out the ones that would result in a check
    def get_valid_moves(self):
        #Pseudo code:
        # 1 - get all possible moves. Calls the get_possible_moves method.
        # 2 - Make each move. 
        # 3 - For each move, generates all moves for the OPPOSING player, and sees whether any of them will result in the king being threatened
        # 4 - sees if any of those moves attacks king
        # 5 - if it does, remove it from the list.
        moves = self.get_possible_moves_MODIFIED()
        for i in range(len(moves)-1, -1, -1): #iterates through the moves list backwards. Starts at last index, goes until just before -1 index, over increments of -1. We go backwards to avoid list reindexing when removing things
            self.make_move(moves[i])    #makes each move.
            self.is_white_turn = not self.is_white_turn #IMPORTANT: the make_move function switches turns automatcically. If this line didn't exist, we'd be looking at the wrong player's king
            if self.in_check(): #if move puts king in check, then it's not a valid move
                moves.remove(moves[i])  #remove the move at index i

            #now we need to undo our algorithm so that the moves made dont actually occur on the board
            self.is_white_turn = not self.is_white_turn
            self.undo_move()    #undoes each move as it occurs. Reminder: undo_move deletes the last move in the move log

        if len(moves) == 0: #after the filtering algorithm, if there are zero legal moves, then it is either checkmate or stalemate
            if self.in_check(): #if in check
                self.is_checkmate = True    #then it's checkmate
            else:   #if its not check  
                self.is_stalemate = True    #then it's stalemate

        return moves

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

    def get_queen_moves(self, row, column, moves):  #gets all possible moves for the queen. Queen is literally rook + bishop tho lol
        self.get_rook_moves(row, column, moves)   #gets all possible rook moves
        self.get_bishop_moves(row, column, moves) #gets all possible queen moves

    def get_knight_moves(self, row, column, moves): #gets all possible moves for the knight
        directions = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2))   #tuple in form (row, column). up/left, up/right, down/left, down/right, left/up, right/up, left/down, right/down
        if self.is_white_turn:  #sets the enemy color. If it's white to move, enemy color is black. Otherwise, it's white.
            enemy_color = 'b'
        else:
            enemy_color = 'w'
        
        for direction in directions:    #iterates over all the directions
            end_row = row + direction[0]    #sets the end row to be start row + the first term of a particular direction
            end_column = column + direction[1]  #sets the end column to be start column + second term of a particular direction
            if(end_row >= 0 and end_row <= 7 and end_column >=0 and end_column <= 7):   #if ending square is within boundaries of the board
                if(self.board[end_row][end_column] == "--"):    #if ending square is empty
                    moves.append(Move((row, column), (end_row, end_column), self.board))    #add move to moves list
                elif(self.board[end_row][end_column][0] == enemy_color):    #if ending square contains piece of enemy color
                    moves.append(Move((row, column), (end_row, end_column), self.board))    #add move to moves list
    

    def get_bishop_moves(self, row, column, moves): #gets all possible moves for the bishop
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))   #unit vectors for the diagonals: up/left, up/right, down/left, down/right
        if self.is_white_turn:  #sets the enemy color. If it's white to move, enemy color is black. Otherwise, it's white.
            enemy_color = 'b'
        else:
            enemy_color = 'w'

        for direction in directions: #iterates over all the directions
            for i in range(1, 8):
                end_row = row + direction[0] * i    #same as for the rook. sets the end row to be the start row PLUS i rows up or down.
                end_column = column + direction [1] * i #sets the end column to be the start column PLUS i columns up or down
                if(end_row >= 0 and end_row <= 7 and end_column >=0 and end_column <= 7):   #if ending square is within boundaries of the board
                    if(self.board[end_row][end_column] == "--"):    #if ending square is empty
                        moves.append(Move((row, column), (end_row, end_column), self.board))    #add move to moves list
                    elif(self.board[end_row][end_column][0] == enemy_color):    #if ending square contains piece of enemy color
                        moves.append(Move((row, column), (end_row, end_column), self.board))    #add move to move list
                        break   #same as for the Rook. Break the inner for loop to go to a new direction, now that the current diagonal has been found to be blocked off by a piece
                    else: #friendly piece
                        break   #break inner loop for same reason. Diagonal is blocked off. Tells computer to go to new direction.
                else: #off board
                    break
    

    def get_king_moves(self, row, column, moves):   #gets all possible moves for the king
        #other than the direction vectors, this method is literally the same as the knight moves method
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)) #possible king moves: up/left, up, up/right, left, right, down/left, down, down/right
        if self.is_white_turn:  #sets the enemy color. If it's white to move, enemy color is black. Otherwise, it's white.
            enemy_color = 'b'
        else:
            enemy_color = 'w'
        
        for direction in directions:    #iterates over all the directions
            end_row = row + direction[0]    #sets the end row to be start row + the first term of a particular direction
            end_column = column + direction[1]  #sets the end column to be start column + second term of a particular direction
            if(end_row >= 0 and end_row <= 7 and end_column >=0 and end_column <= 7):   #if ending square is within boundaries of the board
                if(self.board[end_row][end_column] == "--"):    #if ending square is empty                 
                    moves.append(Move((row, column), (end_row, end_column), self.board))    #add move to moves list
                elif(self.board[end_row][end_column][0] == enemy_color):    #if ending square contains piece of enemy color
                    moves.append(Move((row, column), (end_row, end_column), self.board))    #add move to moves list














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
#--------------------------------------------
        self.piece_moved = board[self.start_row][self.start_col]    #gets the piece located on the board at the beginning square
        self.piece_captured = board[self.end_row][self.end_col]     #gets the piece located on the board at the ending square. This is the piece that is captured by any given move. Might end up being "--".
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col   #gives each move a unique move id between 0 and 7777. Useful when comparing whether two moves are equal.
#--------------------------------------------

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



print("wrong file bozo")