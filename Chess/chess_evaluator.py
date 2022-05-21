

from lib2to3.refactor import get_all_fix_names
import random
from tkinter.tix import MAX
from typing import Counter
import copy


"""
Piece scores. Eventually we will have a weighted array.
"""
piece_score = {"K": 20000, "Q": 900, "R": 500, "B": 330, "N": 320, "P": 100}

#for all the tables, white is at the bottom and black is at the top
#Need to reflect the tables to get the black piece values

mg_pawn_scores = [
                [0, 0, 0, 0, 0, 0, 0, 0],                 
                [78, 83, 86, 73, 102, 82, 85, 90],
                [7, 29, 21, 44, 40, 31, 44, 7],
                [-17, 16, -2, 15, 14, 0, 15, -13],
                [-26, 3, 10, 9, 6, 1, 0, -23],
                [-22, 9, 5, -11, -10, -2, 3, -19],
                [-31, 8, -7, -37, -36, -14, 3, -31],
                [0, 0, 0, 0, 0, 0, 0, 0]
                ]

eg_pawn_scores = [
                [0,   0,   0,   0,   0,   0,   0,   0],
                [178, 173, 158, 134, 147, 132, 165, 187],
                [94, 100,  85,  67,  56,  53,  82,  84],
                [32,  24,  13,   5,  -2,   4,  17,  17],
                [13,   9,  -3,  -7,  -7,  -8,   3,  -1],
                [4,   7,  -6,   1,   0,  -5,  -1,  -8],
                [13,   8,   8,  10,  13,   0,   2,  -7],
                [0,   0,   0,   0,   0,   0,   0,   0]
                ]


mg_king_scores = [
                [-65,  23,  16, -15, -56, -34,   2,  13],
                [29,  -1, -20,  -7,  -8,  -4, -38, -29],
                [-9,  24,   2, -16, -20,   6,  22, -22],
                [-17, -20, -12, -27, -30, -25, -14, -36],
                [-49,  -1, -27, -39, -46, -44, -33, -51],
                [-14, -14, -22, -46, -44, -30, -15, -27],
                [1,   7,  -8, -64, -43, -16,   9,   8],
                [-15,  36,  12, -54,   8, -28,  24,  14]
                ]

eg_king_scores = [
                [-74, -35, -18, -18, -11,  15,   4, -17],
                [-12,  17,  14,  17,  17,  38,  23,  11],
                [ 10,  17,  23,  15,  20,  45,  44,  13],
                [ -8,  22,  24,  27,  26,  33,  26,   3],
                [-18,  -4,  21,  24,  27,  23,   9, -11],
                [-19,  -3,  11,  21,  23,  16,   7,  -9],
                [-27, -11,   4,  13,  14,   4,  -5, -17],
                [-53, -34, -21, -11, -28, -14, -24, -43]
                ]

knight_scores = [
                [-66, -53, -75, -75, -10, -55, -58, -70],
                [-3, -6, 100, -36, 4, 62, -4, -14],
                [10, 67, 1, 74, 73, 27, 62, -2],
                [24, 24, 45, 37, 33, 41, 25, 17],
                [-1, 5, 31, 21, 22, 35, 2, 0],
                [-18, 10, 13, 22, 18, 15, 11, -14],
                [-23, -15, 2, 0, 2, 0, -23, -20],
                [-74, -23, -26, -24, -19, -35, -22, -69]
                ]

bishop_scores = [
                [-59, -78, -82, -76, -23,-107, -37, -50],
                [-11,  20,  35, -42, -39,  31,   2, -22],
                [-9,  39, -32,  41,  52, -10,  28, -14],
                [25,  17,  20,  34,  26,  25,  15,  10],
                [13,  10,  17,  23,  17,  16,   0,   7],
                [14,  25,  24,  15,   8,  25,  20,  15],
                [19,  20,  11,   6,   7,   6,  20,  16],
                [-7,   2, -15, -12, -14, -15, -10, -10]
                ]
rook_scores = [
            [ 35,  29,  33,   4,  37,  33,  56,  50],
            [ 55,  29,  56,  67,  55,  62,  34,  60],
            [ 19,  35,  28,  33,  45,  27,  25,  15],
            [  0,   5,  16,  13,  18,  -4,  -9,  -6],
            [-28, -35, -16, -21, -13, -29, -46, -30],
            [-42, -28, -42, -25, -25, -35, -26, -46],
            [-53, -38, -31, -26, -29, -43, -44, -53],
            [-30, -24, -18,   5,  -2, -18, -31, -32]
            ]
  
queen_scores = [
                [6,   1,  -8,-104,  69,  24,  88,  26],
                [14,  32,  60, -10,  20,  76,  57,  24],
                [-2,  43,  32,  60,  72,  63,  43,   2],
                [ 1, -16,  22,  17,  25,  20, -13,  -6],
                [-14, -15,  -2,  -5,  -1, -10, -20, -22],
                [-30,  -6, -13, -11, -16, -11, -16, -27],
                [-36, -18,   0, -19, -15, -15, -21, -38],
                [-39, -30, -31, -13, -31, -36, -34, -42]
                ]

position_scores = {
                    'N': knight_scores,
                    'B': bishop_scores,
                    'Q': queen_scores,
                    'R': rook_scores,
                    'P': mg_pawn_scores,
                    'K': mg_king_scores
                    }


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

    score = 0

    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):       #iterate over the board
            piece = game_state.board[row][col]
            square = (row, col)
            score += get_score(piece, square)

    return score    #turns the score into a decimal
        
"""
Position score getter -- takes in a piece (e.g. "wP") and a square (row, col) and outputs its total score
"""
def get_score(piece, square):
    if piece[0] == 'w':
        return piece_score[piece[1]] + position_scores[piece[1]][square[0]][square[1]]
    elif piece[0] == 'b':
        return -(piece_score[piece[1]] + position_scores[piece[1]][7 - square[0]][square[1]])
    else:
        return 0


"""
Best move functions.
"""


#TO DO: Quiescence search

#Minimax Algorithm

#Helper method. Makes first minimax call.
def find_best_move(game_state, valid_moves):
    game_state_clone = copy.deepcopy(game_state)        #copy the gamestate
    global best_move, minimax_counter, quiescence_counter
    best_move = None

  #  random.shuffle(valid_moves)

    minimax_counter = 0    #for testing. Number of calls for minimax method
    quiescence_counter = 0

 #   minimax(game_state_clone, valid_moves, MAX_DEPTH, game_state.is_white_turn)
    minimax_alpha_beta(game_state_clone, valid_moves, MAX_DEPTH, -CHECKMATE, CHECKMATE, 1 if game_state.is_white_turn else -1)    
 #   minimax_alpha_beta_no_loop(game_state_clone, valid_moves, MAX_DEPTH, -CHECKMATE, CHECKMATE, game_state.is_white_turn)
    print("minimax call number is " + str(minimax_counter)) #for testing
    print("quiescence call number is " + str(quiescence_counter))

    return best_move


#return a score at a given depth
def minimax_alpha_beta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global best_move, minimax_counter

    minimax_counter += 1

    if depth == 0:
        return turn_multiplier * evaluate(game_state)   #turn multiplier is 1 if white turn, -1 if black turn. Makes evaluate function accurate
    
    #TO DO - Implement move ordering

    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.make_move(move)
        next_moves = game_state.get_valid_moves()
        
        next_moves = sort_moves(game_state, next_moves) #sorts to improve processing time
        
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
    global best_move, minimax_counter
    minimax_counter += 1

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
    global best_move, minimax_counter
    minimax_counter += 1

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


#quiescence search algorith. Used in conjunction with minimax_alpha_beta
def quiescence_search(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global best_move, quiescence_counter
    quiescence_counter += 1

    if depth == 0:
        return turn_multiplier * evaluate(game_state)   #turn multiplier is 1 if white turn, -1 if black turn. Makes evaluate function accurate
    
    #TO DO - Implement move ordering

    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.make_move(move)
        capture_moves = None
        for move in game_state.get_valid_moves():
            if move.is_capture:
                capture_moves.append(move)
        
        score = -quiescence_search(game_state, capture_moves, depth - 1, -beta, -alpha, -turn_multiplier)         #swap alpha and beta

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


"""
Sort method. Selects the best few candidate moves and puts them first to increase pruning.
"""

def sort_moves(game_state, valid_moves):
    scores = []
    
    for i in range(len(valid_moves)):
        rating = 0
        move = valid_moves[i]
        if(move.is_capture and piece_score[move.piece_moved[1]] < piece_score[move.piece_captured[1]]):
            rating += 100
        if(move.is_capture and piece_score[move.piece_moved[1]] < piece_score[move.piece_captured[1]]):
            rating += 50
        if move.is_pawn_promotion:
            rating += 200
        if move.is_two_square_advance:
            rating += 25

        game_state.make_move(move)
        if game_state.is_in_check:
            rating += 50
        game_state.undo_move()

        scores.append(rating)        

    num_iterations = max(6, len(valid_moves))
    for i in range(0, num_iterations):   #find top 6 moves
        max_rating = -10000
        max_location = 0
        for j in range(len(scores)):
            if scores[j] > max_rating:
                max_rating = scores[j]
                max_location = j
        
        scores[max_location] = -10000   #make already acquired move terrible to look for second best move
        
        #swap element at index i with element at index max_location
        get_pos = valid_moves[i], valid_moves[max_location]
        
        valid_moves[max_location], valid_moves[i] = get_pos
        
    return valid_moves




#Function that makes a random move
def find_random_move(valid_moves):
    num = random.randint(0, len(valid_moves) - 1) #randint is inclusive of both parameters
    return valid_moves[num]

