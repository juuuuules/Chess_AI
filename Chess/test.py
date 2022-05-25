from winreg import EnumValue
import chess_evaluator, chess_machine

def test_repetitions():
    
    game_state_real = chess_machine.Game_State()
    move_1 = chess_machine.Move((6, 4), (4, 4), game_state_real.board)  #e4
    move_2 = chess_machine.Move((1, 4), (3, 4), game_state_real.board)  #e5
    move_3 = chess_machine.Move((7, 6), (5, 5), game_state_real.board)  #Nf3
    move_4 = chess_machine.Move((0, 1), (2, 2), game_state_real.board)  #Nc6

    game_state_real.make_move(move_1)
    game_state_real.make_move(move_2)
    game_state_real.make_move(move_3)
    game_state_real.make_move(move_4)

    chess_machine.game_state_real.three_move_repetition()


test_repetitions()