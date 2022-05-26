from winreg import EnumValue
import chess_evaluator, chess_machine

opening_bongcloud = ['e2e4', 'e7e5', 'e1e2', 'e8e7']
opening_ruy_lopez = ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5", "a7a6"]

def test_opening():
    
    game_state = chess_machine.Game_State()
    str = "e2e4"
    move = chess_machine.notation_to_move(str, game_state.board)
    game_state.make_move(move)

    opening_move = chess_evaluator.get_opening_move(game_state)

    print("opening move is: ", opening_move)

    if opening_move != None:
        game_state.make_move(opening_move)

    print("Move made")
    print(game_state.board)



test_opening()