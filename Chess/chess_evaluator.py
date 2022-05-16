import copy

from lib2to3.refactor import get_all_fix_names
import random


"""
Piece scores. Eventually we will have a weighted array.
"""
piece_score = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}



"""
Global variables.
"""
CHECKMATE = 10000
STALEMATE = 0
MAX_DEPTH = 3




"""
Evaluation Function.
"""
#evaluation function that scores the board. This version is based only on material
def evaluate(game_state):
    #Checkmate handler
    if game_state.is_checkmate:
        if game_state.is_white_turn:
            return -CHECKMATE
        else:
            return CHECKMATE

    #Stalemate handler
    elif game_state.is_draw:
        return STALEMATE


    score  = 0
    for row in game_state.board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]     #adds value of piece at given square if the piece is white
            if square[1] == 'b':
                score -= piece_score[square[1]]     #subtracts value of piece at given quare if the piece is black
    return score
        

"""
Best move functions.
"""

#Minimax Algorithm

#Helper method. Makes first minimax call.
def minimax(game_state, valid_moves):
    return minimax_algorithm(game_state, valid_moves, MAX_DEPTH, game_state.is_white_turn)[1]


#return a score, best move at a given depth
def minimax_algorithm(game_state, valid_moves, depth, is_white_turn):
    best_move = None
    if depth == 0:
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
        


#Function that makes a random move
def find_random_move(valid_moves):
    num = random.randint(0, len(valid_moves) - 1) #randint is inclusive of both parameters
    return valid_moves[num]

