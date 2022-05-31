from winreg import EnumValue
import chess_evaluator, chess_machine

opening_bongcloud = ['e2e4', 'e7e5', 'e1e2', 'e8e7']
opening_ruy_lopez = ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5", "a7a6"]

test_game = ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5", "a7a6", "b5c6", "d7c6", "e1g1", "c8g4", "d2d4", "e5d4", "c1e3", "d4e3", "f2e3", 
"d8d1", "f1d1", "g8f6", "b1c3", "f8c5", "g1h1", "g4f3", "g2f3", "c5e3", "d1d3", "e3c5", "a1d1", "e8e7", "d3d7", "f6d7", 
"d1d7", "e7d7", "c3d5", "c6d5", "e4d5", "d7d6", "h1g2", "d6d5", "f3f4", "d5e4", "g2g3", "c5d6", "g3g4", "d6f4", "c2c3", 
"f4h2", "a2a4", "h7h5", "g4g5", "a6a5", "c3c4", "h2e5", "b2b3", "e5f6", "g5h4", "e5b2", "h4g3", "e4d4", "g3h3", "d4c4",
"h3g3", "c4b4", "g3h3", "a4b4", "h3g2", "h4h3", "g2f2", "h3h2", "f2e2", "h2h1", "e2d3", "h1e1", "d3c2", "a8d8", "c2b2"]


def test_checkmate():
    
    game_state = chess_machine.Game_State()

    for move in test_game:
        game_state.make_move(chess_machine.notation_to_move(move, game_state.board))

    print("Best move is ", chess_evaluator.find_best_move(game_state, game_state.valid_moves))



test_checkmate()