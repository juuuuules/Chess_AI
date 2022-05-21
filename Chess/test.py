from winreg import EnumValue
import chess_evaluator, chess_machine

def test_sort():
    game_state = chess_machine.Game_State()

    valid_moves = game_state.get_valid_moves()

    print("Unsorted valid moves: ", valid_moves)

    sorted_valid_moves = chess_evaluator.sort_moves(game_state, valid_moves)
    print("Sorted valid moves: ", sorted_valid_moves)

test_sort()