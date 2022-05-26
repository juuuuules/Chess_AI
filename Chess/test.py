from winreg import EnumValue
import chess_evaluator, chess_machine

def test_eval():
    
    game_state = chess_machine.Game_State()
    move_1 = chess_machine.Move((6, 4), (4, 4), game_state.board)
    game_state.make_move(move_1)

    eval = chess_evaluator.evaluate(game_state)
    print("Eval is ", eval)

test_eval()