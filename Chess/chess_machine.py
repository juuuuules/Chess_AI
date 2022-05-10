#Responsible for storing all the information about the current chess game state. Also respnsible for determining the valid moves at the current game state.
#Might keep move log????

from string import whitespace
from xmlrpc.client import FastMarshaller


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

        #castling global variables. For more information see the heading above the Castle_Rights class
        self.current_castle_rights = Castle_Rights(True, True, True, True)  #wks, wqs, bks, bqs all true at start of game
        self.castle_rights_log = [Castle_Rights(self.current_castle_rights.white_kingside_castle, self.current_castle_rights.white_queenside_castle, 
                                                        self.current_castle_rights.black_kingside_castle, self.current_castle_rights.black_queenside_castle)]  #creates a list of castling_rights objects, taking a snapshot of the current castling rights state by creating a new Castle_Rights object 

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

        #castle move
        if move.is_castle_move:  #if the move is a castle move
            if move.end_col - move.start_col == 2: #kingside castle move
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1] #moves the rook - always begins one square to the right of the king's final position, and ends one square to the left of the king's final position
                self.board[move.end_row][move.end_col + 1] = "--"   #erases old rook
            else: #queenside castle
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 2] #moves the rook - always begins two squares to the left of the king's final position, and ends one square to the right of the king's final position
                self.board[move.end_row][move.end_col - 2] = "--"   #erases old rook
        
        #empassant move
        if move.is_enpassant_move: #if the move is an enpassant move
            self.board[move.start_row][move.end_col] = "--" 

        self.update_castle_rights(move) #updates the castling rights for each move
        self.castle_rights_log.append(Castle_Rights(self.current_castle_rights.white_kingside_castle, self.current_castle_rights.white_queenside_castle, 
                                    self.current_castle_rights.black_kingside_castle, self.current_castle_rights.black_queenside_castle))  #adds current castle_rights state to the castling rights log.
        
        #promotion
        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'Q' #makes the piece moved to a promotion square actually a queen. move.piece_moved[0] grabs the color.

        #enpassant move
        if move.is_enpassant_move: #if the move is an enpassant move
            self.board[move.start_row][move.end_col] = "--" 


    def undo_move(self, caused_by_undo = False):    #function that undoes last move
        if len(self.move_log) != 0: #checks to see whether there is a move to undo

            if caused_by_undo:
                print("you just undid a move")
                print("white kingside castle right is " + str(self.castle_rights_log[-1].white_kingside_castle))

            move = self.move_log[-1]  #gets the last element in the move_log list
            self.move_log = self.move_log[:-1]  #removes the last element in the move_log list


            #undo enpassant move
            if move.is_enpassant_move:
                self.board[move.start_row][move.end_col] = move.piece_captured

            self.board[move.start_row][move.start_col] = move.piece_moved   #sets the start row and column of the move back to what it was before the move was made (somehow this is breaking)
            self.board[move.end_row][move.end_col] = "--"

            if not move.is_enpassant_move: #adds the captured piece back only if the move wasn't enpassant
                self.board[move.end_row][move.end_col] = move.piece_captured    #sets the end row and column of the move back to what it was before the move was made
            self.is_white_turn = not self.is_white_turn #changes turn
       
        #updates the king position if king is moved
        if(move.piece_moved == 'wK'):   #if white king is moved
            self.white_king_location = (move.start_row, move.start_col) #set white king location back to the start square of the king move
        elif (move.piece_moved == 'bK'):
            self.black_king_location = (move.start_row, move.start_col) #set black king location back to the start square of the king move
      
        self.is_checkmate = False
        self.is_stalemate = False   #sets checkmate and stalemate to be false, just in case we undo a move that causes checkmate/stalemate. 
        
        #undo castling rights
        self.castle_rights_log.pop()    #removes last element in castle_rights log
        self.current_castle_rights = self.castle_rights_log[-1] #after removal, sets current castle rights to last one in the list

        #undo castle move
        if (move.is_castle_move):
            if move.end_col - move.start_col == 2: #kingside castle
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]     #sets the rook back to be one square right of the king instead of one square left of the king
                self.board[move.end_row][move.end_col - 1] = "--"    #sets the square left of the final king destination to be empty
            
                if self.is_white_turn:
                    self.current_castle_rights.white_kingside_castle = True
                else:
                    self.current_castle_rights.black_kingside_castle = True
            
            else:   #queenside castle
                self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1] #moves back the rook to the square two to the left of the final king destination
                self.board[move.end_row][move.end_col + 1] = "--" #sets the square one right of the final king destination to be empty
                
                if self.is_white_turn:
                    self.current_castle_rights.white_queenside_castle = True
                else:
                    self.current_castle_rights.black_queenside_castle = True

                

    #determines whether an enemy can attack the square row / col    
    def square_under_attack(self, row, column):   
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
        temp_castle_rights = Castle_Rights(self.current_castle_rights.white_kingside_castle, self.current_castle_rights.white_queenside_castle, 
                                    self.current_castle_rights.black_kingside_castle, self.current_castle_rights.black_queenside_castle)    #copy the current castling rights and saves it in a temp variable so that generating the possible moves won't mess with the castle rights.
       
        moves = self.get_possible_moves_MODIFIED()
        
        #now generate the castle moves
        if (self.is_white_turn):
            ally_color = 'w'
            self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves, ally_color)
        else:
            ally_color = 'b'
            self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves, ally_color)

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

        self.current_castle_rights = temp_castle_rights #sets back the current castling rights to the saved state at the beginning of the method

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

    #Getters for piece movements: Pawn, Rook, Queen, Kight, Bishop King
    #Adds move objects to a list of moves. Does not handle checks, pins, en passant, or castling
    def get_pawn_moves(self, row, column, moves):   #gets all possible moves for the pawns. Copy-paste evan's code with some slight modifications
        
        enpassant_direction = "" #makes sure that a pawn can only enpassant in to take the pawn that moved last

        if len(self.move_log) > 1: #makes it so you can't enpassant as first move. helps avoid errors
            last_move_was_pawn_2 = abs(self.move_log[-1].start_row - self.move_log[-1].end_row) > 1 and self.board[self.move_log[-1].end_row][self.move_log[-1].end_col][1] == 'P' #if the last move involved moving a pawn 2 pieces
            can_enpassant = (abs(column - self.move_log[-1].start_col) < 2) and last_move_was_pawn_2

            if can_enpassant: #adds a variable that determines which direction the pawn can enpassant in
                if self.move_log[-1].end_col < column:
                    enpassant_direction = "left"
                else:
                    enpassant_direction = "right"

        else: 
            last_move_was_pawn_2 = False
            can_enpassant = False

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

                #from this point forward we look for enpassant moves
                #------------
                if(self.board[row - 1][column - 1] == '--' and self.board[row][column - 1] == 'bP'):  #if square diagonally upwards and to the left is empty and the square in front of the pawn is a black pawn
                    if can_enpassant and enpassant_direction == "left":
                        moves.append(Move((row, column), (row - 1, column - 1), self.board, is_enpassant_move = True))   #adds a new diagonal left enpassant capture to the list of moves

            
            #captures to the right
            if(column < 7): #if pawn is not on right-most file
                if(self.board[row - 1][column + 1][0] == 'b'): #if square diagonally upwards and to the right contains a black piece
                    moves.append(Move((row, column), (row - 1, column + 1), self.board))    #adds a new diagonal capture to the list of moves

                #------------
                if(self.board[row - 1][column + 1] == '--' and self.board[row][column + 1] == 'bP'):  #if square diagonally upwards and to the right is empty and the square in front of the pawn is a black pawn
                    if can_enpassant and enpassant_direction == "right":
                        moves.append(Move((row, column), (row - 1, column + 1), self.board, is_enpassant_move = True))   #adds a new diagonal right enpassant capture to the list of moves

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

                #----------
                if(self.board[row + 1][column - 1] == '--' and self.board[row][column - 1] == 'wP'):  #if square diagonally downwards and to the left is empty and the square in front of the pawn is a white pawn
                    if can_enpassant and enpassant_direction == "left":
                        moves.append(Move((row, column), (row + 1, column - 1), self.board, is_enpassant_move = True))   #adds a new diagonal left enpassant capture to the list of moves

                
            #captures to the right
            if(column < 7): #if pawn is not on the right-most file
                if(self.board[row + 1][column + 1][0] == 'w'):      #if square diagonally downwards and to the right contains a white piece
                    moves.append(Move((row, column), (row + 1, column + 1), self.board))    #adds a new diagonal capture to the list of moves

                #----------
                if(self.board[row + 1][column + 1] == '--' and self.board[row][column + 1] == 'wP'):  #if square diagonally downwards and to the right is empty and the square in front of the pawn is a white pawn
                    if can_enpassant and enpassant_direction == "right":
                        moves.append(Move((row, column), (row + 1, column + 1), self.board, is_enpassant_move = True))   #adds a new diagonal right enpassant capture to the list of moves
                

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
        if self.is_white_turn:  #sets the ally color. If it's white to move, ally color is white. Otherwise, it's black.
            ally_color = 'w'
        else:
            ally_color = 'b'
        
        for direction in directions:    #iterates over all the directions
            end_row = row + direction[0]    #sets the end row to be start row + the first term of a particular direction
            end_column = column + direction[1]  #sets the end column to be start column + second term of a particular direction
            if(end_row >= 0 and end_row <= 7 and end_column >=0 and end_column <= 7):   #if ending square is within boundaries of the board
                if(self.board[end_row][end_column][0] != ally_color):    #if ending square does not contain a piece of the allied color                 
                    moves.append(Move((row, column), (end_row, end_column), self.board))    #add move to moves list
            
    #Castling Handlers.
    #Four conditions we need to work with:
    #1 - King cannot be in check
    #2 - King cannot move through check
    #3 - King cannot land in check
    #4 - It must be both the king and the rook's first move of the game. That's why kingside and queenside castling are separate variables
    
    #Updates castling rights given the move
    def update_castle_rights(self, move):
        if(move.piece_moved == 'wK'):    #If the white king was moved
            self.current_castle_rights.white_kingside_castle = False    #set kingside castling rights to false
            self.current_castle_rights.white_queenside_castle = False   #set queenside castling rights to false
        elif(move.piece_moved == 'bK'):    #If the black king was moved
            self.current_castle_rights.black_kingside_castle = False    #set kingside castling rights to false
            self.current_castle_rights.black_queenside_castle = False   #set queenside castling rights to false
        elif(move.piece_moved == 'wR'):   #If pieced move was a white rook
            if(move.start_row == 7):      #If rook's starting row is 7
                if(move.start_col == 0):  #left rook
                    self.current_castle_rights.white_queenside_castle = False   #set queenside castling rights to false
                elif(move.start_col == 7): #right rook
                    self.current_castle_rights.white_kingside_castle = False
        elif(move.piece_moved == 'bR'):   #If pieced move was a white rook
            if(move.start_row == 0):      #If rook's starting row is 7
                if(move.start_col == 0):  #left rook
                    self.current_castle_rights.black_queenside_castle = False   #set queenside castling rights to false
                elif(move.start_col == 7): #right rook
                    self.current_castle_rights.black_kingside_castle = False

    #generate all valid castle moves for the king at (row, column) and add them to the list of moves
    def get_castle_moves(self, row, column, moves, ally_color):
        if(self.in_check()):
            print("king in check")
            return #can't castle if in check
        if((self.is_white_turn and self.current_castle_rights.white_kingside_castle) or (not self.is_white_turn and self.current_castle_rights.black_kingside_castle)): #if it's white turn and white has kingside castle rights OR it's black's turn and black has kingside castle rights
            self.get_kingside_castle_moves(row, column, moves)    #gets kingside castle moves
        if((self.is_white_turn and self.current_castle_rights.white_queenside_castle) or (not self.is_white_turn and self.current_castle_rights.black_queenside_castle)): #if it's white turn and white has queenside castle rights OR it's black's turn and black has queenside castle rights
            self.get_queenside_castle_moves(row, column, moves)      #gets queenside castle moves

    
    #generates kingside castle moves
    def get_kingside_castle_moves(self, row, column, moves):
        if self.board[row][column+1] == '--' and self.board[row][column+2] == '--':   #if squares one and two columns over from the king are empty
            if (not self.square_under_attack(row, column+1) and not self.square_under_attack(row, column + 2)):   #if squares one and two columns over from the king are not being attacked
                moves.append(Move((row, column), (row, column + 2), self.board, is_castle_move = True))
    #generates queenside castle moves
    def get_queenside_castle_moves(self, row, column, moves):
        if self.board[row][column - 1] == '--' and self.board[row][column - 2] == '--' and self.board[row][column - 3] == '--':
             if (not self.square_under_attack(row, column-1) and not self.square_under_attack(row, column - 2)):   #if squares one and two columns over from the king are not being attacked. DOn't have to check square three over, because the king does not pass thru that square
                moves.append(Move((row, column), (row, column - 2), self.board, is_castle_move = True))


#Castling Rights class. Creates objects with 4 boolean parameters indicating whether/how white and black can castle.
#Several rules must be taking into account:
#Note: it is not enough to just have a castle rights class. We must also have a global variable in Game_state that is of type Castle_Rights that we can then update depending on the move made
#Also note: in addition, we will need a castle rights log so that we know if a rook has moved or something.
#Finally, the castling rights updater methods will need to go into the Game_State class
class Castle_Rights():
    def __init__(self, white_kingside_castle, white_queenside_castle, black_kingside_castle, black_queenside_castle):   #passes in four booleans for kingside/queenside castling rights
        self.white_kingside_castle = white_kingside_castle
        self.white_queenside_castle = white_queenside_castle
        self.black_kingside_castle = black_kingside_castle
        self.black_queenside_castle = black_queenside_castle
    def set_castle_rights(self, wkc, wqc, bkc, bqc):
        self.white_kingside_castle = wkc
        self.white_queenside_castle = wqc
        self.black_kingside_castle = bkc
        self.black_queenside_castle = bqc









class Move():

    #conversion strings -- changing the ranks and files found in common chess notation to the rows and columns of our board matrix 
    #maps keys to values
    #key : value
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}       #converts each rank of squares in standard chess notation to a row in the board matrix. For reference, the black pieces start out at RANK 8 but ROW 0. The white pieces start at RANK 1 but ROW 7.  
    rows_to_ranks = {7: "1", 6: "2", 5: "3", 4: "4", 3: "5", 2: "6", 1: "7", 0: "8"}       #same thing but vice versa
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}       #converts each file of squares in standard chess notation to a column in the board matrix.
    cols_to_files = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}       #same thing but vice versa

    #constructor
    def __init__(self, start_square, end_square, board, is_enpassant_move = False, is_castle_move = False):        #Note: start_square and end_square are tuples. Two optional parameters for whether it's a castle or an en passant
        self.start_row = start_square[0]    #creates a variable for starting row (getting the row coordinate of the tuple)
        self.start_col = start_square[1]    #creates a variable for starting column (getting the column coordinate of the tuple)
        self.end_row = end_square[0]        #same thing, but for end_row
        self.end_col = end_square[1]        #same thing, but for end_col
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        #promotion
        self.is_pawn_promotion = False      #pawn promotion presumed false
        if (self.piece_moved == 'wP' and self.end_row == 0) or (self.piece_moved == 'bP' and self.end_row == 7):
            self.is_pawn_promotion = True        #make it true if end square of move is on the last row

        #en passant
        self.is_enpassant_move = is_enpassant_move

#--------------------------------------------
        self.piece_moved = board[self.start_row][self.start_col]    #gets the piece located on the board at the beginning square
        if not self.is_enpassant_move: #checks if the move is enpassant
            self.piece_captured = board[self.end_row][self.end_col]     #gets the piece located on the board at the ending square. This is the piece that is captured by any given move. Might end up being "--".
        else: #if the move is enpassant, update the piece_captured attribute to reflect the pawn that was captured
            self.piece_captured = board[self.start_row][self.end_col]
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col   #gives each move a unique move id between 0 and 7777. Useful when comparing whether two moves are equal.
#--------------------------------------------
        self.is_castle_move = is_castle_move


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