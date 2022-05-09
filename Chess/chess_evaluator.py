from lib2to3.refactor import get_all_fix_names
import random

piece_score = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 10000
STALEMATE = 0
#if position has a positive value, it's winning for white. Negative value if it's winning for black.

#random move chess engine
def find_random_move(valid_moves):
    num = random.randint(0, len(valid_moves) - 1) #randint is inclusive of both parameters
    return valid_moves[num]

def minimax(game_state, valid_moves):
    min_score = -CHECKMATE
    best_move = None
    
    turn_multiplier = 1 if game_state.is_white_turn else -1

    for player_move in valid_moves:             #player_move is move of the player who's turn it is; opponent is the other player
        game_state.make_move(player_move)
        
        if game_state.is_checkmate:
            score = CHECKMATE

        elif game_state.is_stalemate:
            score = STALEMATE
        else: 
            score = turn_multiplier * evaluate(game_state.board)

        if score > min_score:           #if the score is better than the min, then make THAT equal to the min. For both colors, the goal is to get the max score.
            score = min_score
            best_move = player_move
        
        game_state.undo_move()

    return best_move





#evaluation function that scores the board. This version is based only on material
def evaluate(board):
    score  = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]     #adds value of piece at given square if the piece is white
            if square[1] == 'b':
                score -= piece_score[square[1]]     #subtracts value of piece at given quare if the piece is black
    return score


