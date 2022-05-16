"""
Adding alpha-beta pruning to minimax. See this video for more info: https://www.youtube.com/watch?v=l-hh51ncgDI&t=497
"""

def minimax_algorithm(game_state, valid_moves, depth, is_white_turn):
    best_move = None
    if depth == 0 or game_state.is_checkmate or game_state.is_draw:
        return evaluate(game_state), best_move
    
    if is_white_turn:
        max_score = -CHECKMATE

        for move in valid_moves:
            game_state.make_move(move)
            next_moves = game_state.get_valid_moves()

            score = minimax_algorithm(game_state, next_moves, depth - 1, not is_white_turn)[0]

            if score > max_score:
                max_score = score
                if depth == MAX_DEPTH:
                    best_move = move

            game_state.undo_move()

    else:
        min_score = CHECKMATE

        for move in valid_moves:
            game_state.make_move(move)
            next_moves = game_state.get_valid_moves()

            score = minimax_algorithm(game_state, next_moves, depth - 1, not is_white_turn)[0]

            if score < min_score:
                min_score = score
                if depth == MAX_DEPTH:
                    best_move = move
            game_state.undo_move()
        return min_score, best_move
        












"""


Changes to undo_move:


undo_move(self)
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
        if move.is_castle_move
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
        


"""












# #Changes to mouse handler

# if len(player_clicks) == 2:     #after the second click
#     #now we make our move!

#     move = chess_machine.Move(player_clicks[0], player_clicks[1], game_state.board)
#     print(move.get_chess_notation())

#     for i in range(len(valid_moves)):
#         if move == valid_moves[i]:
#             game_state.make_move(valid_moves[i])        #move generated by the engine, not the move generated by the player
#             move_made = True
#             square_selected = ()    #reset user clicks
#             player_clicks = []      #resets user clicks
#     if not move_made:
#         player_clicks = [square_selected]



# # en-passant method drafts





# '''
# PAWN PROMOTION
# '''
# #Changes to Move class (In constructor)

# self.is_pawn_promotion = False      #presumed false
# if (self.piece_moved == 'wP' and self.end_row == 0) or (self.piece_moved == 'bP' and self.end_row == 7):
#     self.is_pawn_promotion = True        #make it true if pawn reaches end row


# #CHANGES TO MAKE MOVE METHOD
# if move.is_pawn_promotion:
#     self.board[move.end_row][move.end_col] = move.pieced_moved[0] + 'Q' #makes the piece moved to a promotion square actually a queen. move.piece_moved[0] grabs the color.
    





# #Note: To add promotion to other pieces, have to change main function in chess display, right after game_state.make_move.
# #Otherwise bug in code when computer generates all moves to see whcih are valid -- it'll stop to ask for user input even if
# #the move wasn't made

# #for now lets just make it only queen