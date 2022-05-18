from winreg import EnumValue
import chess_evaluator, chess_machine

def test_evaluator():
    game_state = chess_machine.Game_State()

    score = chess_evaluator.evaluate(game_state)

    if score != 0:
        print("evaluator failed", score)

test_evaluator()