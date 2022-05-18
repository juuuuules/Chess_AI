

from lib2to3.refactor import get_all_fix_names
import random
from typing import Counter
import copy


"""
Piece scores. Eventually we will have a weighted array.
"""
piece_score = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}



"""
Global variables.
"""
CHECKMATE = 10000
STALEMATE = 0
MAX_DEPTH = 4




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
            if square[0] == 'b':
                score -= piece_score[square[1]]     #subtracts value of piece at given quare if the piece is black
    
    return score
        

"""
Best move functions.
"""

#Minimax Algorithm

#Helper method. Makes first minimax call.
def find_best_move(game_state, valid_moves):
    game_state_clone = copy.deepcopy(game_state)        #copy the gamestate
    global best_move, counter
    best_move = None

  #  random.shuffle(valid_moves)

    counter = 0    #for testing. Number of calls for minimax method
 #   minimax(game_state_clone, valid_moves, MAX_DEPTH, game_state.is_white_turn)
    minimax_alpha_beta_no_loop(game_state_clone, valid_moves, MAX_DEPTH, -CHECKMATE, CHECKMATE, game_state.is_white_turn)
    print("minimax call number is " + str(counter)) #for testing

    return best_move


#return a score at a given depth
def minimax_alpha_beta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global best_move, counter

    counter += 1

    if depth == 0:
        return turn_multiplier * evaluate(game_state)   #turn multiplier is 1 if white turn, -1 if black turn. Makes evaluate function accurate
    
    #TO DO - Implement move ordering

    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.make_move(move)
        next_moves = game_state.get_valid_moves()

        score = -minimax_alpha_beta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)         #swap alpha and beta

        if score > max_score:
            max_score = score
            if depth == MAX_DEPTH:
                best_move = move

        game_state.undo_move()

        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


def minimax(game_state, valid_moves, depth, is_white_turn):
    global best_move, counter
    counter += 1

    if depth == 0:
        return evaluate(game_state)
    
    if is_white_turn:
        max_score = -CHECKMATE
        for move in valid_moves:
            game_state.make_move(move)
            next_moves = game_state.get_valid_moves()

            score = minimax(game_state, next_moves, depth - 1, False)
            if score > max_score:
                max_score = score
                if depth == MAX_DEPTH:
                    best_move = move
            
            game_state.undo_move()
        return max_score
    
    else:
        min_score = CHECKMATE
        for move in valid_moves:
            game_state.make_move(move)
            next_moves = game_state.get_valid_moves()
            score = minimax(game_state, next_moves, depth - 1, True)
            if score < min_score:
                min_score = score
                if depth == MAX_DEPTH:
                    best_move = move
            game_state.undo_move()
        return min_score


def minimax_alpha_beta_no_loop(game_state, valid_moves, depth, alpha, beta, is_white_turn):
    global best_move, counter
    counter += 1

    if depth == 0:
        return evaluate(game_state)
    
    if is_white_turn:
        max_score = -CHECKMATE
        for move in valid_moves:
            game_state.make_move(move)
            next_moves = game_state.get_valid_moves()

            score = minimax_alpha_beta_no_loop(game_state, next_moves, depth - 1, alpha, beta, False)
            if score > max_score:
                max_score = score
                if depth == MAX_DEPTH:
                    best_move = move
            game_state.undo_move()

            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return max_score
    
    else:
        min_score = CHECKMATE
        for move in valid_moves:
            game_state.make_move(move)
            next_moves = game_state.get_valid_moves()
            score = minimax_alpha_beta_no_loop(game_state, next_moves, depth - 1, alpha, beta, True)
            if score < min_score:
                min_score = score
                if depth == MAX_DEPTH:
                    best_move = move

            game_state.undo_move()

            beta = min(beta, score)
            if beta <= alpha:
                break
        return min_score


#Function that makes a random move
def find_random_move(valid_moves):
    num = random.randint(0, len(valid_moves) - 1) #randint is inclusive of both parameters
    return valid_moves[num]

