

from lib2to3.refactor import get_all_fix_names
import random
from tkinter.tix import MAX
from typing import Counter
import copy
import chess_machine

"""
Piece scores. Eventually we will have a weighted array.
"""
piece_score = {"K": 20000, "Q": 900, "R": 500, "B": 330, "N": 320, "P": 100}

#for all the tables, white is at the bottom and black is at the top
#Need to reflect the tables to get the black piece values

mg_pawn_scores = [
                [0,   0,   0,   0,   0,   0,  0,   0],
                [ 98, 134,  61,  95,  68, 126, 34, -11],
                [ -6,   7,  26,  31,  65,  56, 25, -20],
                [-14,  13,   6,  21,  23,  12, 17, -23],
                [-27,  -2,  -5,  12,  17,   6, 10, -25],
                [-26,  -4,  -4, -10,   3,   3, 33, -12],
                [-35,  -1, -20, -23, -15,  24, 38, -22],
                [  0,   0,   0,   0,   0,   0,  0,   0]
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

mg_knight_scores =  [
                    [-167, -89, -34, -49,  61, -97, -15, -107],
                    [ -73, -41,  72,  36,  23,  62,   7,  -17],
                    [ -47,  60,  37,  65,  84, 129,  73,   44],
                    [  -9,  17,  19,  53,  37,  69,  18,   22],
                    [ -13,   4,  16,  13,  28,  19,  21,   -8],
                    [ -23,  -9,  12,  10,  19,  17,  25,  -16],
                    [ -29, -53, -12,  -3,  -1,  18, -14,  -19],
                    [-105, -21, -58, -33, -17, -28, -19,  -23]
                    ]

eg_knight_scores =  [
                    [-58, -38, -13, -28, -31, -27, -63, -99],
                    [-25,  -8, -25,  -2,  -9, -25, -24, -52],
                    [-24, -20,  10,   9,  -1,  -9, -19, -41],
                    [-17,   3,  22,  22,  22,  11,   8, -18],
                    [-18,  -6,  16,  25,  16,  17,   4, -18],
                    [-23,  -3,  -1,  15,  10,  -3, -20, -22],
                    [-42, -20, -10,  -5,  -2, -20, -23, -44],
                    [-29, -51, -23, -15, -22, -18, -50, -64]
                    ]

mg_bishop_scores =  [
                    [-29,   4, -82, -37, -25, -42,   7,  -8],
                    [-26,  16, -18, -13,  30,  59,  18, -47],
                    [-16,  37,  43,  40,  35,  50,  37,  -2],
                    [ -4,   5,  19,  50,  37,  37,   7,  -2],
                    [ -6,  13,  13,  26,  34,  12,  10,   4],
                    [  0,  15,  15,  15,  14,  27,  18,  10],
                    [  4,  15,  16,   0,   7,  21,  33,   1],
                    [-33,  -3, -14, -21, -13, -12, -39, -21]
                    ]

eg_bishop_scores = [
                [-14, -21, -11,  -8, -7,  -9, -17, -24],
                [ -8,  -4,   7, -12, -3, -13,  -4, -14],
                [  2,  -8,   0,  -1, -2,   6,   0,   4],
                [ -3,   9,  12,   9, 14,  10,   3,   2],
                [ -6,   3,  13,  19,  7,  10,  -3,  -9],
                [-12,  -3,   8,  10, 13,   3,  -7, -15],
                [-14, -18,  -7,  -1,  4,  -9, -15, -27],
                [-23,  -9, -23,  -5, -9, -16,  -5, -17]
                ]

mg_rook_scores = [
                [32,  42,  32,  51, 63,  9,  31,  43],
                [ 27,  32,  58,  62, 80, 67,  26,  44],
                [ -5,  19,  26,  36, 17, 45,  61,  16],
                [-24, -11,   7,  26, 24, 35,  -8, -20],
                [-36, -26, -12,  -1,  9, -7,   6, -23],
                [-45, -25, -16, -17,  3,  0,  -5, -33],
                [-44, -16, -20,  -9, -1, 11,  -6, -71],
                [-19, -13,   1,  17, 16,  7, -37, -26]
                ]

eg_rook_scores = [
                [13, 10, 18, 15, 12,  12,   8,   5],
                [11, 13, 13, 11, -3,   3,   8,   3],
                [ 7,  7,  7,  5,  4,  -3,  -5,  -3],
                [ 4,  3, 13,  1,  2,   1,  -1,   2],
                [ 3,  5,  8,  4, -5,  -6,  -8, -11],
                [-4,  0, -5, -1, -7, -12,  -8, -16],
                [-6, -6,  0,  2, -9,  -9, -11,  -3],
                [-9,  2,  3, -1, -5, -13,   4, -20]
            ]

mg_queen_scores = [
                [-28,   0,  29,  12,  59,  44,  43,  45],
                [-24, -39,  -5,   1, -16,  57,  28,  54],
                [-13, -17,   7,   8,  29,  56,  47,  57],
                [-27, -27, -16, -16,  -1,  17,  -2,   1],
                [ -9, -26,  -9, -10,  -2,  -4,   3,  -3],
                [-14,   2, -11,  -2,  -5,   2,  14,   5],
                [-35,  -8,  11,   2,   8,  15,  -3,   1],
                [ -1, -18,  -9,  10, -15, -25, -31, -50]
                ]

eg_queen_scores =   [
                    [-9,  22,  22,  27,  27,  19,  10,  20],
                    [-17,  20,  32,  41,  58,  25,  30,   0],
                    [-20,   6,   9,  49,  47,  35,  19,   9],
                    [  3,  22,  24,  45,  57,  40,  57,  36],
                    [-18,  28,  19,  47,  31,  34,  39,  23],
                    [-16, -27,  15,   6,   9,  17,  10,   5],
                    [-22, -23, -30, -16, -16, -23, -36, -32],
                    [-33, -28, -22, -43,  -5, -32, -20, -41]
                    ]

position_scores =   {
                    'mgN': mg_knight_scores,
                    'egN': eg_knight_scores,
                    'mgB': mg_bishop_scores,
                    'egB': eg_bishop_scores,
                    'mgQ': mg_queen_scores,
                    'egQ': eg_queen_scores,
                    'mgR': mg_rook_scores,
                    'egR': eg_rook_scores,
                    'mgP': mg_pawn_scores,
                    'egP': eg_pawn_scores,
                    'mgK': mg_king_scores,
                    'egK': eg_king_scores
                    }


"""
Global variables.
"""
CHECKMATE = 100000
STALEMATE = 0
MAX_DEPTH = 4

global game_phase
game_phase = "mg"

"""
Opening strings
"""
opening_bongcloud = ['e2e4', 'e7e5', 'e1e2', 'e8e7']
opening_ruy_lopez = ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5", "a7a6"]
opening_london = ["d2d4", "g8f6", "c1f4", "d7d5", "g1f3", "c8f5"]
opening_qgd = ["d2d4", "g8f6", "c2c4", "e7e6", "b1c3", "d7d5", "g1f3", "c7c5"]


"""
Evaluation Function.
"""
#evaluation function that scores the board. This version is based only on material
def evaluate(game_state):
    global game_phase
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
    total_material = 0

    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):       #iterate over the board
            piece = game_state.board[row][col]
            
            #calculate whether its middle or end game
            if piece[1] != 'K' and piece != '--':
                total_material += piece_score[piece[1]]
                        
            square = (row, col)
            score += get_score(piece, square, game_phase)

    if total_material < 4000:
        game_phase = "eg"

    return score    #turns the score into a decimal
        
"""
Position score getter -- takes in a piece (e.g. "wP") and a square (row, col) and outputs its total score
"""
def get_score(piece, square, game_phase):

    key = game_phase + piece[1]
    if piece[0] == 'w':
        return piece_score[piece[1]] + position_scores[key][square[0]][square[1]]
    elif piece[0] == 'b':
        return -(piece_score[piece[1]] + position_scores[key][7 - square[0]][square[1]])
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
    global best_move, minimax_counter, quiescence_counter, is_theory
    best_move = None
    is_theory = False

    get_opening_move(game_state_clone)

    

    if is_theory:
        print("Still theory")
        return best_move
    else:
        minimax_counter = 0    #for testing. Number of calls for minimax method
    #   quiescence_counter = 0
    #   minimax(game_state_clone, valid_moves, MAX_DEPTH, game_state.is_white_turn)
        minimax_alpha_beta(game_state_clone, valid_moves, MAX_DEPTH, -CHECKMATE, CHECKMATE, 1 if game_state.is_white_turn else -1)    
    #   minimax_alpha_beta_no_loop(game_state_clone, valid_moves, MAX_DEPTH, -CHECKMATE, CHECKMATE, game_state.is_white_turn)
        print("minimax call number: " + str(minimax_counter)) #for testing
    #   print("quiescence call number is " + str(quiescence_counter))

        return best_move


#return a score at a given depth
def minimax_alpha_beta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global best_move, minimax_counter

    minimax_counter += 1

    if depth == 0:
        return turn_multiplier * evaluate(game_state)   #turn multiplier is 1 if white turn, -1 if black turn. Makes evaluate function accurate
    
    #TO DO - Implement move ordering
    valid_moves = sort_moves(game_state, valid_moves)

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
        if(move.is_capture and piece_score[move.piece_moved[1]] > piece_score[move.piece_captured[1]]):
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

    for i in range(0, 6):   #find top 6 moves
        max_rating = -10000
        max_location = 0
        for j in range(len(scores)):
            if scores[j] > max_rating:
                max_rating = scores[j]
                max_location = j
        
        if len(valid_moves) > 6: #prevents an index out out of range by not swapping if valid moves is only 1 element
            scores[max_location] = -10000   #make already acquired move terrible to look for second best move
            
            #swap element at index i with element at index max_location
            get_pos = valid_moves[i], valid_moves[max_location]
            
            valid_moves[max_location], valid_moves[i] = get_pos
        
    return valid_moves

"""
Opening Database handlers
"""
def load_openings(game_state):
    for i in range(len(opening_bongcloud)):
        opening_bongcloud[i] = chess_machine.notation_to_move(opening_bongcloud[i], game_state.board)
    for i in range(len(opening_ruy_lopez)):
        opening_ruy_lopez[i] = chess_machine.notation_to_move(opening_ruy_lopez[i], game_state.board)
    for i in range(len(opening_london)):
        opening_london[i] = chess_machine.notation_to_move(opening_london[i], game_state.board)
    for i in range(len(opening_qgd)):
        opening_qgd[i] = chess_machine.notation_to_move(opening_qgd[i], game_state.board)


def get_opening_move(game_state):
    global best_move, is_theory, openings_loaded

    best_move = None
    move_log = game_state.move_log
    current_move = game_state.half_move_counter

    if move_log == opening_bongcloud[0:len(move_log)]:
        best_move = opening_bongcloud[current_move]
        is_theory = True
    elif move_log == opening_ruy_lopez[0:len(move_log)]:
        best_move = opening_ruy_lopez[current_move]
        is_theory = True
    elif move_log == opening_london[0:len(move_log)]:
        best_move = opening_london[current_move]
        is_theory = True
    elif move_log == opening_qgd[0:len(move_log)]:
        best_move = opening_qgd[current_move]
        is_theory = True
    
    return best_move
            

#Function that makes a random move
def find_random_move(valid_moves):
    num = random.randint(0, len(valid_moves) - 1) #randint is inclusive of both parameters
    return valid_moves[num]

