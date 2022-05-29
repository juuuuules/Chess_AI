
# Main driver file - responsible for handling user input and displaying current GameState object

from pickle import FALSE
import pygame as p
from pygame.constants import KEYDOWN, K_z
import chess_machine, chess_evaluator
import os
import time

print(os.path.isdir("images"))

p.init()        #initializes pygame
if os.path.isdir("Chess"): #since Evan's laptop is small enough that having a 1000 by 1000 pixel board is inconvenient, this if statment alters the size of the board depending on which computer is being used
    #this works because on Evan's computer the images directory is not in the directory chess_display is running in
    WIDTH = HEIGHT = 700   #sets width and height of display to 700x700 pixels if it's Evan's laptop
else:
    WIDTH = HEIGHT = 1000  #sets width and height of display to 1000x1000 pixels if it's Julien's laptop
DIMENSION = 8 #dimensions are 8x8
SQ_SIZE = HEIGHT // DIMENSION #sets the size of each square
#Do we need MAX_FPS variable?????
IMAGES = {} #Creates a global images directory


MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = HEIGHT


"""
EVAN'S SHIT
"""

def reset_castle_rights(game_state):
    game_state.current_castle_rights.set_castle_rights(True, True, True, True)
    game_state.castle_rights_log.append([game_state.current_castle_rights])

    if not game_state.cant_white_kingside:
        for move in game_state.move_log:
            if move.piece_moved == 'wR' and move.start_col == 7: #if the right white rook was moved:
                game_state.current_castle_rights.white_kingside_castle = False
                game_state.cant_white_kingside = True

    if not game_state.cant_white_queenside:
        for move in game_state.move_log:
            if move.piece_moved == 'wR' and move.start_col == 0: #if the left white rook was moved:
                game_state.current_castle_rights.white_queenside_castle = False
                game_state.cant_white_queenside = True

    if not game_state.cant_black_kingside:
        for move in game_state.move_log:
            if move.piece_moved == 'bR' and move.start_col == 7: #if the right black rook was moved:
                game_state.current_castle_rights.black_kingside_castle = False
                game_state.cant_black_kingside = True

    if not game_state.cant_black_queenside:
        for move in game_state.move_log:
            if move.piece_moved == 'bR' and move.start_col == 0: #if the left black rook was moved:
                game_state.current_castle_rights.black_queenside_castle = False
                game_state.cant_black_queenside = True

    if not (game_state.cant_white_kingside or game_state.cant_white_queenside):
        for move in game_state.move_log:
            if move.piece_moved == 'wK': #if the white king was moved:
                game_state.current_castle_rights.white_kingside_castle = False
                game_state.current_castle_rights.white_queenside_castle = False

                game_state.cant_white_kingside = True
                game_state.cant_white_queenside = True

    if not (game_state.cant_black_kingside or game_state.cant_black_queenside):
        for move in game_state.move_log:
            if move.piece_moved == 'bK': #if the black king was moved:
                game_state.current_castle_rights.black_kingside_castle = False
                game_state.current_castle_rights.black_queenside_castle = False

                game_state.cant_black_kingside = True
                game_state.cant_black_queenside = True

        
        # row = game_state.white_king_location[0]
        # column = game_state.white_king_location[1]
        # if game_state.board[row][column+1] == '--' and game_state.board[row][column+2] == '--':   #if squares one and two columns over from the king are empty
        #     if (not game_state.square_under_attack(row, column+1) and not game_state.square_under_attack(row, column + 2)):
        #         game_state.current_castle_rights.white_kingside_castle = True

    game_state.castle_rights_log.append(game_state.current_castle_rights)

"""
END EVAN'S SHIT
"""


#Method that initializes a global directory of images. Minimize calling this method bc it takes a lot of computing time lol
def load_images(): 
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']   #array of all the pieces
    for piece in pieces:
        if os.path.isdir("Chess"):
            IMAGES[piece] = p.transform.scale(p.image.load("Chess/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)) #iterates through the array and loads each image into the global IMAGES directory. transform.scale() method ensures that the piece images are the same size as the square
        else:
            IMAGES[piece] = p.transform.scale(p.image.load("Chess_AI/Chess/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)) 

    #Note: Use  ' IMAGES['wP'] '  to access an image
    
#Main method - handles user input, updates graphics
def main():
    screen = p.display.set_mode((WIDTH + MOVE_LOG_PANEL_WIDTH, HEIGHT))    #sets a drawing window according to the HEIGHT and WIDTH specifications set above
    clock = p.time.Clock()  #creates a clock object (built into pygame)
    screen.fill((255, 255, 255))    #sets the screen to be white lol
    move_log_font = p.font.SysFont("Arial", 18, False, False) #creates a font object; helvetica, size 12, not bold, not italicized



    animate = False #flag variable for when we want to animate a move

    game_state = chess_machine.Game_State() #creates a game_state object named game_state that calls the constructor and creates appropriate field variables (defined in the chess_machine class)
    valid_moves = game_state.get_valid_moves()  #greates a list of valid moves by calling the get_valid_moves method. Don't want to call this every frame, because it costs a lot of computing time
    move_made = False   #flag variable - used so that we only generate a new set of valid moves by calling get_valid_moves once the game_state has been updated
    possible_moves = []

    
    load_images()   #calls load_images method - we only do it once to conserve computing time
    square_selected = ()    #creates a tuple (for rows and columns) to store the coordinates of a selected square. No square is selected initially. Keeps track of the most recent click of the user.
    player_clicks = []      #keeps track of player clicks. Two tuples: [(starting x, starting y) and (ending x, ending y)]. Empty to start.

    game_over = False

    player_one = True   #if a human is playing white than this is true. If an AI is playing white, this is false
    player_two = True  #if a human is playing black than this is true. If an AI is playing black, this is false

    in_menu = True
    in_choose_color_menu = False

    while in_menu: #create the menu

        #this just adds the text above the boxes saying what they do
        screen.fill((102, 153, 204))
        font = p.font.SysFont("Cambria", 75)
        font2 = p.font.SysFont("Comic Sans", 150)

        shallow_blue_text = font2.render("SHALLOW BLUE", True, (3, 37, 126))
        sandbox_text = font.render("Sandbox", True, (3, 37, 126))
        against_computer_text = font.render("Play Computer", True, (3, 37, 126))

        shallow_blue_text_rect = shallow_blue_text.get_rect()
        sandbox_text_rect = sandbox_text.get_rect()
        against_computer_text_rect = sandbox_text.get_rect()

        shallow_blue_text_rect.center = (625, 300)
        sandbox_text_rect.center = (350, 650)
        against_computer_text_rect.center = (825, 650)

    #    p.draw.rect(screen, (0, 255, 255), shallow_blue_text_rect)

        screen.blit(shallow_blue_text, shallow_blue_text_rect)
        screen.blit(sandbox_text, sandbox_text_rect)
        screen.blit(against_computer_text, against_computer_text_rect)

        p.draw.rect(screen, (135, 206, 250), p.Rect(300, 500, 100, 100))
        p.draw.rect(screen, (0, 0, 139), p.Rect(850, 500, 100, 100))
        p.display.flip()

        for event in p.event.get():
            if event.type == p.QUIT:
                in_menu = False

            if event.type == p.MOUSEBUTTONUP: #get mouse position
                x_pos = p.mouse.get_pos()[0]
                y_pos = p.mouse.get_pos()[1]

                if (x_pos < 400 and x_pos > 300) and (y_pos < 600 and y_pos > 500): #check if left box is clicked
                    player_one = True
                    player_two = True
                    in_menu = False
                    #set it to sandbox mode

                if (x_pos < 950 and x_pos > 850) and (y_pos < 600 and y_pos > 500): #check if right box is clicked
                    in_menu = False
                    in_choose_color_menu = True
                    #bring it to the select color phase

    while in_choose_color_menu: #create the choose color menu
        #makes the text above the boxes

        screen.fill((102, 153, 204))
        font = p.font.SysFont("Cambria", 75)

        p.draw.rect(screen, (255, 255, 255), p.Rect(250, 400, 200, 200))
        p.draw.rect(screen, (0, 0, 0), p.Rect(800, 400, 200, 200))

        white_text = font.render("Play White", True, (255, 255, 255))
        black_text = font.render("Play Black", True, (0, 0, 0))

        white_text_rect = white_text.get_rect()
        black_text_rect = black_text.get_rect()

        white_text_rect.center = (350, 650)
        black_text_rect.center = (900, 650)

        screen.blit(white_text, white_text_rect)
        screen.blit(black_text, black_text_rect)


        for event in p.event.get():
            if event.type == p.QUIT:
                in_choose_color_menu = False
                quit()

            if event.type == p.MOUSEBUTTONUP: #get mouse position
                x_pos = p.mouse.get_pos()[0]
                y_pos = p.mouse.get_pos()[1]

                if (x_pos < 450 and x_pos > 250) and (y_pos < 600 and y_pos > 400): #check if left box is clicked
                    player_one = True
                    player_two = False
                    in_choose_color_menu = False
                    #have player play as white

                if (x_pos < 1000 and x_pos > 800) and (y_pos < 600 and y_pos > 400): #check if right box is clicked
                    player_one = False
                    player_two = True
                    in_choose_color_menu = False
                    #have player play as black
        p.display.flip()
    
    
    chess_evaluator.load_openings(game_state)
    

    #Run until user asks to quit
    running = True
    resigned = False
    while running:
        
        is_human_turn = (game_state.is_white_turn and player_one) or (not game_state.is_white_turn and player_two)

        for event in p.event.get(): #iterates through all the "events" -- includes clicks, button presses, etc
            if event.type == p.QUIT:    #asks whether user has clicked window close button
                running = False     #if so, quits game

        #mouse handler
            elif event.type == p.MOUSEBUTTONDOWN: #asks whether user clicks somewhere on the screen

                if not game_over:
                    if is_human_turn:
                        location = p.mouse.get_pos() #gets the (x, y) location of mouse

                        if (location[0] > WIDTH + 50 and location[0] < WIDTH + 200) and (
                            location[1] > HEIGHT - 100 and location[1] < HEIGHT - 25):
                            resigned = True

                        col = location[0]//SQ_SIZE #gets the x coordinate, then divides it by the square size to determine the column 
                        row = location[1]//SQ_SIZE #gets the y coordinate, then divides it by the square size to determine the row

                        possible_moves = [] #reset possible moves so the highlighted squares go away


                        #check if square is ALREADY SELECTED
                        if square_selected == (row, col) or col >= 8:        #the user clicked the same square twice or user clicked move log
                            square_selected = ()        #deselect
                            player_clicks = []  #clear player_clicks
                        else:
                            square_selected = (row, col) #stores location of click in square_selected variable
                            player_clicks.append(square_selected) #adds the location of the click to the list 
                            
                            if len(player_clicks) == 1: #if this is the first click by the player
                                possible_moves = [] #set possible_moves to an empty array that will hold all the possible moves the player can make
                                for possible_move in valid_moves:
                                    if possible_move.start_row == row and possible_move.start_col == col: #if a valid move starts at the square the user clicked
                                        possible_moves.append(possible_move) #this list is used to highlight valid moves when a player clicks a square

                        #was that the second click?
                        if len(player_clicks) == 2:     #after the second click
                            #now we make our move!

                            move = chess_machine.Move(player_clicks[0], player_clicks[1], game_state.board)

                            for i in range(len(valid_moves)):
                                if move == valid_moves[i]:
                                    game_state.make_move(valid_moves[i], is_real_move=True)        #move generated by the engine, not the move generated by the player
                                    move_made = True
                                    animate = True
                                    square_selected = ()    #reset user clicks
                                    player_clicks = []      #resets user clicks
                            if not move_made:
                                player_clicks = [square_selected]

            #key handler
            elif event.type == p.KEYDOWN:
                #UNDO MOVE
                if event.key == p.K_z and p.key.get_mods() & p.KMOD_CTRL:   #undo when 'ctrl + z' is pressed -- thanks stack exchange!
                    for i in range(2):      #forces u to undo twice
                        game_state.undo_move(is_real_undo=True)  #calls undo move
                        move_made = True    #sets flag variable to true in order to generate a new set of valid moves
                        animate = False
                        square_selected = ()    #reset user clicks
                        player_clicks = []      #resets user clicks
                    reset_castle_rights(game_state)

                if event.key == p.K_f:
                    print(game_state.current_castle_rights.white_kingside_castle)


                if event.key == p.K_r and p.key.get_mods() & p.KMOD_CTRL:   #reset board when 'ctrl + r' is pressed
                    game_state = chess_machine.Game_State()
                    valid_moves = game_state.get_valid_moves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
        
        #logic for AI move finder
        if not game_over and not is_human_turn:

            start_time = time.process_time()
            ai_move = chess_evaluator.find_best_move(game_state, valid_moves)
            if ai_move is None:
                ai_move = chess_evaluator.find_random_move(valid_moves)
            game_state.make_move(ai_move)
            move_made = True
            animate = True
#            reset_castle_rights(game_state)



        if move_made:   #once a move has been made, generate a new set of valid moves
            if animate:
                animate_move(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.get_valid_moves()
            move_made = False
            animate = False

        draw_game_state(screen, game_state, valid_moves, square_selected, possible_moves, move_log_font) #calls draw_game_state to draw the current state

        #End game handlers
        #Checkmate:
        if game_state.is_checkmate:
            game_over = True
            if game_state.is_white_turn:
                draw_endgame_text(screen, 'Black Wins by Checkmate')

            else:
                draw_endgame_text(screen, 'White Wins by Checkmate')

        elif game_state.is_draw:
            game_over = True
            draw_endgame_text(screen, 'The Game Ends in a Draw')
        elif resigned:
            if player_one:
                draw_endgame_text(screen, "Black Wins by Resignation")
            else:
                draw_endgame_text(screen, "white Wins by Resignation")
            game_over = True



        clock.tick()    #updates the clock -- called once per frame; computes how many milliseconds have passed since previous call
        p.display.flip()    #updates entire display



#Method responsible for all the graphics within a current game state
def draw_game_state(screen, game_state, valid_moves, square_selected, possible_moves, move_log_font):
    draw_board(screen) #draw squares on the board
    highlight_squares(screen, game_state, valid_moves, square_selected, possible_moves)
    draw_pieces(screen, game_state.board) #draw pieces on top of squares
    draw_move_log(screen, game_state, move_log_font)
    draw_resign_button(screen)

def draw_resign_button(screen):
    font = p.font.SysFont("Comic sans", 50, True, False)
    resign_text_object = font.render("Resign", True, (3, 37, 126))
    resign_text_location = p.Rect(0, 0, resign_text_object.get_width(), resign_text_object.get_height()).move(WIDTH + 50, HEIGHT - 100)
    screen.blit(resign_text_object, resign_text_location) #blits the text_object at the proper location.

    # print("width = " + str(resign_text_object.get_width()))
    # print("height = " + str(resign_text_object.get_height()))


#Draw squares on the board. Uses white and grey colors. Call draw board first. Top left square is always white square
def draw_board(screen):
    global colors
    colors = [p.Color(255, 255, 255), p.Color(102, 153, 204)]   #chooses white and brown to be colors. Perhaps later we could let users pick the color?
    for r in range(DIMENSION):      #double for loop to iterate over the board and go square by square
        for c in range(DIMENSION):
            color = colors[ ((r+c)%2) ]    #selects 'color' to be either index 0 (white) or index 1 (brown). Relies on the following fact: if a chessboard is represented by an 8x8 matrix, with the top left entry (00) and bottom right entry (77), then the sum of the coordinates of the white squares will always be even, and the sum of the coordinates of the dark squares will always be odd.
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE)) #draws a colored rectangle beginning at c*SQ_SIZE and r*SQ_SIZE with dimmensions SQ_SIZE * SQ_SIZE


#Function that highlights the squares
def highlight_squares(screen, game_state, valid_moves, square_selected, possible_moves): #Highlights square selected. Highlights valid moves for piece selected
    
    #highlight last move
    if(len(game_state.move_log) > 0):
            last_move = game_state.move_log[-1]
            start_square = p.Surface((SQ_SIZE, SQ_SIZE))    #creates a new surface object of size sq_size * sq_size so that the highlighted start sqaure and end square of the previous move will be blitted onto the screen later
            start_square.set_alpha(100)
            start_square.fill(p.Color("blue"))
            end_square = p.Surface((SQ_SIZE, SQ_SIZE))
            end_square.set_alpha(100)
            end_square.fill(p.Color("blue"))
            screen.blit(start_square, (last_move.start_col * SQ_SIZE, last_move.start_row * SQ_SIZE))
            screen.blit(end_square, (last_move.end_col * SQ_SIZE, last_move.end_row * SQ_SIZE))

    #highlights the legal moves a selected piece can make
    for possible_move in possible_moves:
        highlighted_square = p.Surface((SQ_SIZE, SQ_SIZE))
        highlighted_square.set_alpha(90)
        highlighted_square.fill(p.Color("green"))
        screen.blit(highlighted_square, (possible_move.end_col * SQ_SIZE, possible_move.end_row * SQ_SIZE))


    if square_selected != ():   #if square selected is not an empty tuple
        row = square_selected[0]    #sets row to be x coordinate of the tuple
        column = square_selected[1] #sets column to be y coordinate of the tuple

        #highlight selected square
        if( (game_state.board[row][column][0] == 'w' and game_state.is_white_turn == True) or (game_state.board[row][column][0] == 'b' and game_state.is_white_turn == False) ):  #if color of piece matches who's turn it is
            selected_square_highlighting = p.Surface((SQ_SIZE, SQ_SIZE))    #creates a new surface object of size square_size
            selected_square_highlighting.set_alpha(100) #sets transparency value. 0 = transparent, 255 = opaque. Thanks stack exchange!
            selected_square_highlighting.fill(p.Color("blue"))
            screen.blit(selected_square_highlighting, (column * SQ_SIZE, row * SQ_SIZE))
            #highlight valid moves from that square
            

#Function that draws the pieces onto the board using current game_state.board
def draw_pieces(screen, board):
    for r in range(DIMENSION):      #double for loop to iterate over the board and go square by square
        for c in range(DIMENSION):
            piece = board[r][c] #access the piece corresponding to each square of the board
            if piece != "--": #if not an empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE)) #outputs the image of the identified piece at location c*SQ_SIZE r*SQ_SIZE with dimensions SQ_SIZE * SQ_SIZE

#Function that draws the move log
def draw_move_log(screen, game_state, font):
    #draw side rectangle
    move_log_rect = p.Rect(WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), move_log_rect)
    move_log = game_state.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i//2 + 1) + ". " + str(move_log[i]) + " "
        if i + 1 < len(move_log): #make sure black made a move
            move_string += str(move_log[i+1]) + "  "
        move_texts.append(move_string)

    moves_per_row = 3
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i+j]

        text_object = font.render(text, True, p.Color('white'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing


#Function that animates the moves
def animate_move(move, screen, board, clock):
    global colors
    coordinates = []    #list of row/column coordinates the animation will move through
    delta_row = move.end_row - move.start_row   #change in row
    delta_col = move.end_col - move.start_col   #change in column
    frames_per_square = 5      #number of frames it takes to move one square
    total_frames = frames_per_square * (abs(delta_row) + abs(delta_col))    #total number of frames the animation will take
    
    for frame in range(total_frames + 1):   #iterates through all the frames
        r, c = move.start_row + (delta_row * frame / total_frames), move.start_col + (delta_col * frame / total_frames) #add the row coordinate of the nth frame of the animation. E.g., for a knight move, first would be frame 0 so start row would be appended. Then start_row + 1/30, etc.
        draw_board(screen)
        draw_pieces(screen, board)
        
        #erase piece from ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col*SQ_SIZE, move.end_row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, end_square)

        #draw captured piece onto rectangle
        if move.piece_captured != '--':
            if move.is_enpassant_move:
                en_passant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = p.Rect(move.end_col*SQ_SIZE, en_passant_row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)
        
        #draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)  #framerate

def draw_endgame_text(screen, text):
    if os.path.isdir("Chess"):
        font = p.font.SysFont("Comic Sans", 40, True, False) #creates a font object; helvetica, size 80, bold, not italicized
    else:
        font = p.font.SysFont("Comic Sans", 60, True, False) #creates a font object; helvetica, size 80, bold, not italicized

    text_object = font.render(text, True, (3, 37, 126))
    text_object_shadow = font.render(text, True, 0) 

    if os.path.isdir("Chess"):
        WIDTH = HEIGHT = 500
        text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH // 2 - text_object.get_width() // 3, HEIGHT // 2)
    else:
        WIDTH = HEIGHT = 1000
        text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH // 2 - text_object.get_width() // 2, HEIGHT // 2 - text_object.get_height() // 2)    #centers the text

    screen.blit(text_object_shadow, text_location.move(5, 5))
    screen.blit(text_object, text_location) #blits the text_object at the proper location.

def draw_text():
    pass




main() #calls the main method


