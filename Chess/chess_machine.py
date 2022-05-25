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

        #Flag variables
        self.is_white_turn = True #white to move at the start of the game
        self.is_checkmate = False   #not checkmate or a draw at the start of the game
        self.is_draw = False
        self.is_in_check = False

        #initialize variables

        self.move_functions = {"P": self.get_pawn_moves, "R": self.get_rook_moves, "N": self.get_knight_moves,
                              "B": self.get_bishop_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}

        self.move_log = []      #creates a list to store all the moves played during the game
        self.valid_moves = []
        self.pins = []      #keeps track of all the pins on the board
        self.checks = []       #keeps track of all the checks on the board
        self.enpassant_possible = ()       #coordinates for the square where en passant capture is possible
        self.enpassant_possible_log = [self.enpassant_possible]

        self.game_state_log = [self.board]

        #King location variables
        self.white_king_location = (7, 4)   #white king starts at row 7 col 4    
        self.black_king_location = (0, 4)   #black king starts at row 0 col 4
        
        """
        EVAN'S SHIT
        """
        self.white_in_check = False
        self.black_in_check = False

        #yeah sorry this is very inefficient and makes some lines of code pointless
        #but it also prevents the issue of enabling castling at bad times so imma use it for now
        self.cant_white_kingside = False
        self.cant_white_queenside = False
        self.cant_black_kingside = False
        self.cant_black_queenside = False
        
        #REMOVE LATER
        self.white_in_check = False
        self.black_in_check = False

        """
        END OF EVAN'S SHIT
        """

        #Castle Rights variables
        self.current_castle_rights = Castle_Rights(True, True, True, True)  #wks, wqs, bks, bqs all true at start of game
        self.castle_rights_log = [Castle_Rights(self.current_castle_rights.white_kingside_castle, self.current_castle_rights.white_queenside_castle, 
                                                        self.current_castle_rights.black_kingside_castle, self.current_castle_rights.black_queenside_castle)]  #creates a list of castling_rights objects, taking a snapshot of the current castling rights state by creating a new Castle_Rights object 

 
    #returns true if a game state has repeated three times, false otherwise.
    def three_move_repetition(self):
    
        """
        
        game_state_log = []
        for i in range(len(self.move_log)):
            temp_game_state = Game_State()
            for j in range(0, i):
                temp_game_state.make_move(self.move_log[j])
            game_state_log.append(temp_game_state)
        """
        for board in self.game_state_log:
            counter = 0
            for i in range(len(self.game_state_log)):
                if board == self.game_state_log[i]:
                    counter += 1
            if counter == 3:
                return True
        
        return False
    

    """
    Make move method. Takes a move as a parameter and executes it.
    """
    def make_move(self, move):  #function that takes in a move object and updates the game_state according to the move made. Assumes move is valid.

        self.board[move.start_row][move.start_col] = "--" #makes the starting location an empty square 
        self.board[move.end_row][move.end_col] = move.piece_moved #sets the new square to be the piece that we moved from the old square.
        self.move_log.append(move)  #logs the move -- adds it to move log at the end of the log
        self.is_white_turn = not self.is_white_turn #changes turn from white to black or vice versa
        
        #updates the king position if king is moved
        if(move.piece_moved == 'wK'):   #if white king is moved
            self.white_king_location = (move.end_row, move.end_col) #set white king location to the end square of the king move
        elif (move.piece_moved == 'bK'):
            self.black_king_location = (move.end_row, move.end_col) #set black king location to the end square of the king move

        #pawn promotion
        if move.is_pawn_promotion:

            #Handler to let user choose piece to promote to:
            # if not is_AI:
            #     promoted_piece = input("Promote to Q, R, B, N:")    #Take this to UI later
            #     self.board[move.end_row][move.end_col] = move.piece_moved[0] + promoted_piece  
            # else:

            self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'Q' #makes the piece moved to a promotion square actually a queen. move.piece_moved[0] grabs the color.

        #enpassant move
        if move.is_enpassant_move:
            self.board[move.start_row][move.end_col] = "--" #captures the pawn on the square adjacent


        #update enpassant_possible variable
        if move.piece_moved[1] == "P" and abs(move.start_row - move.end_row) == 2:  #if move is a 2 square pawn advance
            self.enpassant_possible = ((move.start_row + move.end_row) // 2, move.start_col)    #coords of en_passant location
        else:
            self.enpassant_possible = ()

        self.enpassant_possible_log.append(self.enpassant_possible) #add enpassant_possible coordinates to the en_passant_possible log

        #castle move
        if move.is_castle_move:  #if the move is a castle move
            if move.end_col - move.start_col == 2: #kingside castle move
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1] #moves the rook - always begins one square to the right of the king's final position, and ends one square to the left of the king's final position
                self.board[move.end_row][move.end_col + 1] = "--"   #erases old rook
            else: #queenside castle
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 2] #moves the rook - always begins two squares to the left of the king's final position, and ends one square to the right of the king's final position
                self.board[move.end_row][move.end_col - 2] = "--"   #erases old rook
        
        #update castling rights - whenever it is a rook or a king move
        self.update_castle_rights(move) #updates the castling rights for each move
        self.castle_rights_log.append(Castle_Rights(self.current_castle_rights.white_kingside_castle, self.current_castle_rights.white_queenside_castle, 
                                    self.current_castle_rights.black_kingside_castle, self.current_castle_rights.black_queenside_castle))  #adds current castle_rights state to the castling rights log.

        #Update draw log
        self.game_state_log.append(self.board)
        print("Game state log is ", self.game_state_log)

    """
    Undo function that reverses previous move.
    """
    def undo_move(self):
        if len(self.move_log) != 0:     #if there is a move to undo
            move = self.move_log.pop()  #removes last element in the move_log list
            
            #undo normal move
            self.board[move.start_row][move.start_col] = move.piece_moved   #sets start square to the piece that moved
            self.board[move.end_row][move.end_col] = move.piece_captured    #sets end square to the piece that was captured
            self.is_white_turn = not self.is_white_turn     #swap turn

            #update king location
            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_col)

            #Undo enpassant move
            if move.is_enpassant_move:
                self.board[move.end_row][move.end_col] = "--" #leave landing square blank
                self.board[move.start_row][move.end_col] = move.piece_captured  #put enemy pawn back in adjacent square
            
            #Update enpassant_possible variable
            self.enpassant_possible_log.pop()   #removes last element in the list
            self.enpassant_possible = self.enpassant_possible_log[-1]   #sets enpassant_possible to be the last element in the list

            #Undo castle move
            if move.is_castle_move:
                if move.end_col - move.start_col == 2:  #if kingside castle
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]     #sets the rook back to be one square right of the king instead of one square left of the king
                    self.board[move.end_row][move.end_col - 1] = "--"    #sets the square left of the final king destination to be empty
                else:   #queenside castle
                    self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1] #moves back the rook to the square two to the left of the final king destination
                    self.board[move.end_row][move.end_col + 1] = "--" #sets the square one right of the final king destination to be empty

            #Update Castle Rights
            self.castle_rights_log.pop()  #get rid of the new castle rights from the move we are undoing
            self.current_castling_rights = self.castle_rights_log[-1] # set the current castle rights to the last one in the list

            #Update end game states
            self.is_checkmate = False
            self.is_draw = False
        
            #Update draw log
            self.game_state_log.pop()
            print("Game state log is ", self.game_state_log)
    """
    Function that gets a list of all the legal moves in a particular position.
    """
    def get_valid_moves(self):

        #Pseudo code:
        # 1 - determine what pieces are pinned and which enemy pieces are putting the king in check (using the get_pins_and_checks() method)
        # 2 - Go through a series of conditionals to determine which moves should be axed from the get_all_moves() method
        #   a - if king in check by 1 piece that is not a knight, then capture, block, or move.
        #   b - if king in check by 1 piece that is a knight, then capture or move. 
        #   c - if king in check by 2 pieces, then move. 
        # 3 - if there are no moves, then either checkmate or stalemate has occured. End the game. 

        temp_castle_rights = Castle_Rights(self.current_castle_rights.white_kingside_castle, self.current_castle_rights.white_queenside_castle, 
                                    self.current_castle_rights.black_kingside_castle, self.current_castle_rights.black_queenside_castle)    #copy the current castling rights and saves it in a temp variable so that generating the possible moves won't mess with the castle rights.
       
        moves = []
        self.is_in_check, self.pins, self.checks = self.get_pins_and_checks()  #sets field variables to be the result of the get_pins_and_checks function
        
        """
        PRINT STATEMENT FOR DEBUGGING
        """
        #print(self.pins)    


        if self.is_white_turn:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]

        if self.is_in_check:
            if len(self.checks) == 1:  # only 1 check, block the check or move the king
                moves = self.get_all_moves()
                # to block the check you must put a piece into one of the squares between the enemy piece and your king
                check = self.checks[0]  # check information
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = []  # squares that pieces can move to
                # if knight, must capture the knight or move your king, other pieces can be blocked
                if piece_checking[1] == "N":
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i,
                                        king_col + check[3] * i)  # check[2] and check[3] are the check directions
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:  # once you get to piece and check
                            break
                # get rid of any moves that don't block check or move king
                for i in range(len(moves) - 1, -1, -1):  # iterate through the list backwards when removing elements
                    if moves[i].piece_moved[1] != "K":  # move doesn't move king so it must block or capture
                        if not (moves[i].end_row,
                                moves[i].end_col) in valid_squares:  # move doesn't block or capture piece
                            moves.remove(moves[i])
            else:  # double check, king has to move
                self.get_king_moves(king_row, king_col, moves)
        else:   #not in check, all moves are fine
            moves = self.get_all_moves()
            if self.is_white_turn:
                self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves)
            else:
                self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves)

        #End of game handlers
        if len(moves) == 0: #after the filtering algorithm, if there are zero legal moves, then it is either checkmate or stalemate
            if self.in_check(): #if in check
                self.is_checkmate = True    #then it's checkmate
            else:   #if its not check  
                self.is_draw = True    #then it's stalemate
        elif self.three_move_repetition():
            self.is_draw = True


        self.current_castle_rights = temp_castle_rights #sets back the current castling rights to the saved state at the beginning of the method

        return moves

    """
    Function that gets ALL the moves in a particular position, without considering checks
    """
    def get_all_moves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == "w" and self.is_white_turn) or (turn == "b" and not self.is_white_turn):
                    piece = self.board[row][col][1]
                    self.move_functions[piece](row, col, moves)  # calls appropriate move function based on piece type
        return moves



    """
    Check Handlers
    """

    #Function that checks to see whether king is in check
    def in_check(self):
        if self.is_white_turn:  #if it's white to move
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])  #checks wehther the white king's location is being attacked
        else:   #if black to move
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])   #checks whether the black king's location is being attacked

    #Function that returns lists of the squares being pinned and the squares putting the king in check
    def get_pins_and_checks(self):
        pins = []  # squares pinned and the direction they're pinned from
        checks = []  # squares where enemy is applying a check
        in_check = False
        if self.is_white_turn:
            enemy_color = "b"
            ally_color = "w"
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = "w"
            ally_color = "b"
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]
        
        #Check outward from the king, looking for pins and checks. Keep track of pins.
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)) #unit vector list of directions
        for j in range(len(directions)):
            direction = directions[j]
            possible_pin = ()   #reset possible pins
            for i in range(1, 8):   #a square that is i units away from the king in a given direction
                end_row = start_row + direction[0] * i  #get end row and end column
                end_col = start_col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7: #if the square is on the board
                    end_piece = self.board[end_row][end_col]    #get piece at end square
                    if end_piece[0] == ally_color and end_piece[1] != "K":  #if square contains piece of allied color
                        if possible_pin == ():  # first allied piece could be pinned
                            possible_pin = (end_row, end_col, direction[0], direction[1])
                        else:  # 2nd allied piece - no check or pin from this direction
                            break
                    elif end_piece[0] == enemy_color:
                        enemy_type = end_piece[1]
                        # 5 possibilities in this complex conditional
                        # 1.) orthogonally away from king and piece is a rook
                        # 2.) diagonally away from king and piece is a bishop
                        # 3.) 1 square away diagonally from king and piece is a pawn
                        # 4.) any direction and piece is a queen
                        # 5.) any direction 1 square away and piece is a king
                        if (0 <= j <= 3 and enemy_type == "R") or (4 <= j <= 7 and enemy_type == "B") or (
                                i == 1 and enemy_type == "P" and (
                                (enemy_color == "w" and 6 <= j <= 7) or (enemy_color == "b" and 4 <= j <= 5))) or (
                                enemy_type == "Q") or (i == 1 and enemy_type == "K"):
                            if possible_pin == ():  # no piece blocking, so check
                                in_check = True
                                checks.append((end_row, end_col, direction[0], direction[1]))
                                break
                            else:  # piece blocking so pin
                                pins.append(possible_pin)
                                break
                        else:  # enemy piece not applying checks
                            break
                else:
                    break  # off board
        # check for knight checks
        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for move in knight_moves:
            end_row = start_row + move[0]
            end_col = start_col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == "N":  # enemy knight attacking a king
                    in_check = True
                    checks.append((end_row, end_col, move[0], move[1]))
        return in_check, pins, checks

    """
    Castling Handlers.
    Four conditions we need to work with:
    1 - King cannot be in check
    2 - King cannot move through check
    3 - King cannot land in check
    4 - It must be both the king and the rook's first move of the game. That's why kingside and queenside castling are separate variables
    """

    #Function that updates castling rights based on move made
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

    #Function that generates all valid castle moves for the king at (row, column). Adds them to the move list
    def get_castle_moves(self, row, col, moves):
        if self.square_under_attack(row, col):
            return  #can't castle if in check
        if((self.is_white_turn and self.current_castle_rights.white_kingside_castle) or (not self.is_white_turn and self.current_castle_rights.black_kingside_castle)): #if it's white turn and white has kingside castle rights OR it's black's turn and black has kingside castle rights
            self.get_kingside_castle_moves(row, col, moves)    #gets kingside castle moves
        if((self.is_white_turn and self.current_castle_rights.white_queenside_castle) or (not self.is_white_turn and self.current_castle_rights.black_queenside_castle)): #if it's white turn and white has queenside castle rights OR it's black's turn and black has queenside castle rights
            self.get_queenside_castle_moves(row, col, moves)      #gets queenside castle moves

    
    #generates kingside castle moves
    def get_kingside_castle_moves(self, row, column, moves):
        if column + 2 > 7:
            return
        if self.board[row][column+1] == '--' and self.board[row][column+2] == '--':   #if squares one and two columns over from the king are empty
            if (not self.square_under_attack(row, column+1) and not self.square_under_attack(row, column + 2)):   #if squares one and two columns over from the king are not being attacked
                moves.append(Move((row, column), (row, column + 2), self.board, is_castle_move = True))
    #generates queenside castle moves
    def get_queenside_castle_moves(self, row, column, moves):
        if column - 2 < 0:
            return
        if self.board[row][column - 1] == '--' and self.board[row][column - 2] == '--' and self.board[row][column - 3] == '--':
             if (not self.square_under_attack(row, column-1) and not self.square_under_attack(row, column - 2)):   #if squares one and two columns over from the king are not being attacked. DOn't have to check square three over, because the king does not pass thru that square
                moves.append(Move((row, column), (row, column - 2), self.board, is_castle_move = True))



    """
    Getters for piece movements. Does not handle checks, pins, enpassant, promotion, or castling.
    """

    #pawn
    def get_pawn_moves(self, row, col, moves):   #gets all possible moves for the pawns. Copy-paste evan's code with some slight modifications
        
        #Pin handler. Gets info about the pin
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        #Gets info on pawn based on whether it is white or black to move.
        if self.is_white_turn:
            move_amount = -1
            start_row = 6
            enemy_color = "b"
            king_row, king_col = self.white_king_location
        else:
            move_amount = 1
            start_row = 1
            enemy_color = "w"
            king_row, king_col = self.black_king_location
        
        #Advance one square.
        if self.board[row + move_amount][col] == "--":
            
            if not piece_pinned or pin_direction == (move_amount, 0):
                moves.append(Move((row, col), (row + move_amount, col), self.board))

                #advance two squares
                if row == start_row and self.board[row + 2 * move_amount][col] == "--":
                    moves.append(Move((row, col), (row + 2 * move_amount, col), self.board))
        
        #Capture to the left
        if col - 1 >= 0:
            if not piece_pinned or pin_direction == (move_amount, -1):
                if self.board[row + move_amount][col - 1][0] == enemy_color:
                    moves.append(Move((row, col), (row + move_amount, col - 1), self.board))
            
            #enpassant to the left
            if (row + move_amount, col - 1) == self.enpassant_possible:
                attacking_piece = blocking_piece = False
                if king_row == row:
                    if king_col < col:  # king is left of the pawn
                        # inside: between king and the pawn;
                        # outside: between pawn and border;
                        inside_range = range(king_col + 1, col - 1)
                        outside_range = range(col + 1, 8)
                    else:  # king right of the pawn
                        inside_range = range(king_col - 1, col, -1)
                        outside_range = range(col - 2, -1, -1)
                    for i in inside_range:
                        if self.board[row][i] != "--":  # some piece beside en-passant pawn blocks
                            blocking_piece = True
                    for i in outside_range:
                        square = self.board[row][i]
                        if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):
                            attacking_piece = True
                        elif square != "--":
                            blocking_piece = True
                if not attacking_piece or blocking_piece:
                    moves.append(Move((row, col), (row + move_amount, col - 1), self.board, is_enpassant_move=True))

        #Capture to the right
        if col + 1 <= 7:
            if not piece_pinned or pin_direction == (move_amount, 1):
                if self.board[row + move_amount][col + 1][0] == enemy_color:
                    moves.append(Move((row, col), (row + move_amount, col + 1), self.board))
                
                #enpassant to the right
                if (row + move_amount, col + 1) == self.enpassant_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == row:
                        if king_col < col:  # king is left of the pawn
                            # inside: between king and the pawn;
                            # outside: between pawn and border;
                            inside_range = range(king_col + 1, col)
                            outside_range = range(col + 2, 8)
                        else:  # king right of the pawn
                            inside_range = range(king_col - 1, col + 1, -1)
                            outside_range = range(col - 1, -1, -1)
                        for i in inside_range:
                            if self.board[row][i] != "--":  # some piece beside en-passant pawn blocks
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[row][i]
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(Move((row, col), (row + move_amount, col + 1), self.board, is_enpassant_move=True))
                
    #rook
    def get_rook_moves(self, row, col, moves):   #Copy and paste evan's code with some slight mdifications
        #Note: unlike pawn moves, the color of the rook does not affect its movement possibilities

        directions = ((-1, 0), (1, 0), (0, -1), (0, 1)) #basis vectors for directions: up, down, left, right
        
        #Pin Handlers.
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] != "Q":  # can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break


        
        if self.is_white_turn:  #sets the enemy color. If it's white to move, enemy color is black. Otherwise, it's white.
            enemy_color = 'b'
        else:
            enemy_color = 'w'
        
        for direction in directions:    #iterates through the directions: up, down, left, right
            for i in range(1, 8):   #iterates from 1 to 8
                end_row = row + direction[0] * i       #sets the end row to be the start row PLUS i rows up or down. If the direction is (0, -1) or (0, 1), aka left or right, direction[0] will be zero and the row index will not change.
                end_col = col + direction[1] * i     #sets the end column to be start column PLUS i columns left or right. If the direction is (-1, 0) or (1, 0), aka up or down, direction[1] will be zero and the column index will not change.
                if(end_row >= 0 and end_row <= 7 and end_col >=0 and end_col <= 7):   #if ending square is within boundaries of the board
                    if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--" :    #move to empty space
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:   #capture enemy piece
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                        else:   #ally piece
                            break
                else: #else off board
                    break   #go to the next direction

    #queen
    def get_queen_moves(self, row, column, moves):  #gets all possible moves for the queen. Queen is literally rook + bishop tho lol
        self.get_rook_moves(row, column, moves)   #gets all possible rook moves
        self.get_bishop_moves(row, column, moves) #gets all possible queen moves

    #knight
    def get_knight_moves(self, row, col, moves): #gets all possible moves for the knight
        
        #Pin Handlers
        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break
        
        
        directions = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2))   #tuple in form (row, column). up/left, up/right, down/left, down/right, left/up, right/up, left/down, right/down
        if self.is_white_turn:  #sets the enemy color. If it's white to move, enemy color is black. Otherwise, it's white.
            ally_color = 'w'
        else:
            ally_color = 'b'

        for direction in directions:    #iterates over all the directions
            end_row = row + direction[0]    #sets the end row to be start row + the first term of a particular direction
            end_col = col + direction[1]  #sets the end column to be start column + second term of a particular direction
            if(end_row >= 0 and end_row <= 7 and end_col >=0 and end_col <= 7):   #if ending square is within boundaries of the board
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:  # so its either enemy piece or empty square
                        moves.append(Move((row, col), (end_row, end_col), self.board))
    
    #bishop
    def get_bishop_moves(self, row, col, moves): #gets all possible moves for the bishop
        
        #Pin Handler. Get information about pin.
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))   #unit vectors for the diagonals: up/left, up/right, down/left, down/right
        if self.is_white_turn:  #sets the enemy color. If it's white to move, enemy color is black. Otherwise, it's white.
            enemy_color = 'b'
        else:
            enemy_color = 'w'


        for direction in directions: #iterates over all the directions
            for i in range(1, 8):
                end_row = row + direction[0] * i    #same as for the rook. sets the end row to be the start row PLUS i rows up or down.
                end_col = col + direction [1] * i #sets the end column to be the start column PLUS i columns up or down
                if(end_row >= 0 and end_row <= 7 and end_col >=0 and end_col <= 7):   #if ending square is within boundaries of the board
                    if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--" :                          #move to empty space
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:               #capture enemy piece
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                        else:   #ally piece
                            break
                else: #off board
                    break
    
    #king
    def get_king_moves(self, row, col, moves):   #gets all possible moves for the king
        
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)

        if self.is_white_turn:  #sets the ally color. If it's white to move, ally color is white. Otherwise, it's black.
            ally_color = 'w'
        else:
            ally_color = 'b'
        
        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color: #not an ally piece - empyy or enemy
                    #place king on end sqaure and check for checks
                    if ally_color == "w":
                        self.white_king_location = (end_row, end_col)
                    else:
                        self.black_king_location = (end_row, end_col)

                    in_check, pins, checks = self.get_pins_and_checks()
                    if not in_check:
                        moves.append(Move((row, col), (end_row, end_col), self.board))

                    #place king back on original location
                    if ally_color == "w":
                        self.white_king_location = (row, col)
                    else:
                        self.black_king_location = (row, col)

    """
    Helper Methods
    """
    #Function that determines whether a given square is under attack    
    def square_under_attack(self, row, column):   
        self.is_white_turn = not self.is_white_turn #looks at opponents moves
        opponent_moves = self.get_all_moves()
        self.is_white_turn = not self.is_white_turn #switches back perspective
        for move in opponent_moves:
            if (move.end_row == row and move.end_col == column): #if there exists a possible move that would end on the specified row and column, i.e. square is under attack
                return True
        return False


    def __eq__(self, other):    #comparing the self object to another move object, saved in the parameter other
        if isinstance(other, Game_State): #if "other" object is an instance of the Game_State class
            for row in range(len(self.board)):
                for col in range(len(self.board[row])):       #iterate over the board
                    if self.board[row][col] != other.board[row][col]:
                        return False

            return True
        return False
    def __ne__(self, other):
        return not self == other

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

    """
    Constructor.
    """
    def __init__(self, start_square, end_square, board, is_enpassant_move = False, is_castle_move = False):        #Note: start_square and end_square are tuples. Two optional parameters for whether it's a castle or an en passant
        self.start_row = start_square[0]    #creates a variable for starting row (getting the row coordinate of the tuple)
        self.start_col = start_square[1]    #creates a variable for starting column (getting the column coordinate of the tuple)
        self.end_row = end_square[0]        #same thing, but for end_row
        self.end_col = end_square[1]        #same thing, but for end_col
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        
        #flag variable if move is capture move
        
        if self.piece_captured != "--":
            self.is_capture = True
        else:
            self.is_capture = False

        #flag variable if move is a two-square pawn advance
        if self.piece_moved[1] == 'P' and abs(self.start_row - self.end_row == 2):
            self.is_two_square_advance = True
        else:
            self.is_two_square_advance = False


        #promotion move
        self.is_pawn_promotion = False      #pawn promotion presumed false
        if (self.piece_moved == 'wP' and self.end_row == 0) or (self.piece_moved == 'bP' and self.end_row == 7):
            self.is_pawn_promotion = True        #make it true if end square of move is on the last row

        #en passant move
        self.is_enpassant_move = is_enpassant_move
        if self.is_enpassant_move:
            if self.piece_moved == "bP":
                self.piece_captured = "wP"
            else:
                self.piece_captured = "bP"

        #castle move
        self.is_castle_move = is_castle_move

        #moveID
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col   #gives each move a unique move id between 0 and 7777. Useful when comparing whether two moves are equal.
        
        
    """
    Overriding the Equals method. 
    Two moves are "equal" if they have the same start_row, start_col, end_row, and end_col.
    Copy and pasted from stack exchange.
    """
    def __eq__(self, other):    #comparing the self object to another move object, saved in the parameter other
        if isinstance(other, Move): #if "other" object is an instance of the Move class
             return self.moveID == other.moveID #returns true if two move IDs are the same, and false if they are different.
        return False

    """
    Chess Notation methods.
    """
    #Function that converts from matrix notation to chess notation (e.g. [6, 4] would become ["e", "3"]).
    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)  #creates a string that is a concatenation of starting square and ending square in chess notation. E.g. "e4e5"

    def __repr__(self):
        return self.get_chess_notation()

    #Helper function. Gets  rank and file given row and column.
    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]    #returns the file corresponding to the column "col" + the rank corresponding to the row "row". File then rank, because thats how chess notation works


    def __str__(self):
        if self.is_castle_move:
            return "O-O" if self.end_col == 6 else "O-O-O"
        
        end_square = self.get_rank_file(self.end_row, self.end_col)

        if self.piece_moved[1] == "P":
            if self.is_capture:
                return self.cols_to_files[self.start_col] + "x" + end_square
            else:
                return end_square + "=Q" if self.is_pawn_promotion else end_square
        move_string = self.piece_moved[1]
        if self.is_capture:
            move_string += "x"
        return move_string + end_square