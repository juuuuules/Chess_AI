
# Main driver file - responsible for handling user input and displaying current GameState object

import pygame as p
from pygame.constants import KEYDOWN, K_z
import chess_machine, chess_evaluator
import os
import time

p.init()        #initializes pygame
if os.path.isdir("images"): #since Evan's laptop is small enough that having a 1000 by 1000 pixel board is inconvenient, this if statment alters the size of the board depending on which computer is being used
    #this works because on Evan's computer the images directory is not in the directory chess_display is running in
    WIDTH = HEIGHT = 700   #sets width and height of display to 700x700 pixels if it's Evan's laptop
else:
    WIDTH = HEIGHT = 1000  #sets width and height of display to 1000x1000 pixels if it's Julien's laptop
DIMENSION = 8 #dimensions are 8x8
SQ_SIZE = HEIGHT // DIMENSION #sets the size of each square
#Do we need MAX_FPS variable?????
IMAGES = {} #Creates a global images directory


#Method that initializes a global directory of images. Minimize calling this method bc it takes a lot of computing time lol
def load_images(): 
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']   #array of all the pieces
    for piece in pieces:
        if os.path.isdir("images"):
            IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)) #iterates through the array and loads each image into the global IMAGES directory. transform.scale() method ensures that the piece images are the same size as the square
        else:
            IMAGES[piece] = p.transform.scale(p.image.load("Chess_AI/Chess/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)) 

    #Note: Use  ' IMAGES['wP'] '  to access an image
    
#Main method - handles user input, updates graphics
def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))    #sets a drawing window according to the HEIGHT and WIDTH specifications set above
    clock = p.time.Clock()  #creates a clock object (built into pygame)
    screen.fill((255, 255, 255))    #sets the screen to be white lol
    
    animate = False #flag variable for when we want to animate a move

    game_state = chess_machine.Game_State() #creates a game_state object named game_state that calls the constructor and creates appropriate field variables (defined in the chess_machine class)
    valid_moves = game_state.get_valid_moves()  #greates a list of valid moves by calling the get_valid_moves method. Don't want to call this every frame, because it costs a lot of computing time
    move_made = False   #flag variable - used so that we only generate a new set of valid moves by calling get_valid_moves once the game_state has been updated
    possible_moves = []

    
    load_images()   #calls load_images method - we only do it once to conserve computing time
    square_selected = ()    #creates a tuple (for rows and columns) to store the coordinates of a selected square. No square is selected initially. Keeps track of the most recent click of the user.
    player_clicks = []      #keeps track of player clicks. Two tuples: [(starting x, starting y) and (ending x, ending y)]. Empty to start.

    player_one = True   #if a human is playing white than this is true. If an AI is playing white, this is false
    player_two = False  #if a human is playing black than this is true. If an AI is playing black, this is false

    #Run until user asks to quit
    running = True
    while running:

        is_human_turn = (game_state.is_white_turn and player_one) or (not game_state.is_white_turn and player_two)

        for event in p.event.get(): #iterates through all the "events" -- includes clicks, button presses, etc
            if event.type == p.QUIT:    #asks whether user has clicked window close button
                running = False     #if so, quits game

        #mouse handler
            elif event.type == p.MOUSEBUTTONDOWN: #asks whether user clicks somewhere on the screen
                if is_human_turn:
                    location = p.mouse.get_pos() #gets the (x, y) location of mouse
                    col = location[0]//SQ_SIZE #gets the x coordinate, then divides it by the square size to determine the column 
                    row = location[1]//SQ_SIZE #gets the y coordinate, then divides it by the square size to determine the row

                    possible_moves = [] #reset possible moves so the highlighted squares go away


                    #check if square is ALREADY SELECTED
                    if square_selected == (row, col):        #the user clicked the same square twice
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
                                game_state.make_move(valid_moves[i])        #move generated by the engine, not the move generated by the player
                                move_made = True
                                animate = True
                                print(move.get_chess_notation())
                                square_selected = ()    #reset user clicks
                                player_clicks = []      #resets user clicks
                        if not move_made:
                            player_clicks = [square_selected]

            #key handler
            elif event.type == p.KEYDOWN:
                #UNDO MOVE
                if event.key == p.K_z and p.key.get_mods() & p.KMOD_CTRL:   #undo when 'ctrl + z' is pressed -- thanks stack exchange!
                    for i in range(2):
                        game_state.undo_move(caused_by_undo = True)  #calls undo move
                        move_made = True    #sets flag variable to true in order to generate a new set of valid moves
                        animate = False
                        square_selected = ()    #reset user clicks
                        player_clicks = []      #resets user clicks

                if event.key == p.K_f:
                    print(game_state.current_castle_rights.white_kingside_castle)


                if event.key == p.K_r and p.key.get_mods() & p.KMOD_CTRL:   #reset board when 'ctrl + z' is pressed
                    game_state = chess_machine.Game_State()
                    valid_moves = game_state.get_valid_moves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
        
        #logic for AI move finder
        if not is_human_turn:
            time.sleep(0.3)
            ai_move = chess_evaluator.minimax(game_state, valid_moves)
            if ai_move is None:
                ai_move = chess_evaluator.find_random_move(valid_moves)
            game_state.make_move(ai_move)
            move_made = True
            animate = True



        if move_made:   #once a move has been made, generate a new set of valid moves
            if animate:
                animate_move(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.get_valid_moves()
            move_made = False
            animate = False

        draw_game_state(screen, game_state, valid_moves, square_selected, possible_moves) #calls draw_game_state to draw the current state



        clock.tick()    #updates the clock -- called once per frame; computes how many milliseconds have passed since previous call
        p.display.flip()    #updates entire display



#Method responsible for all the graphics within a current game state
def draw_game_state(screen, game_state, valid_moves, square_selected, possible_moves):
    draw_board(screen) #draw squares on the board
    highlight_squares(screen, game_state, valid_moves, square_selected, possible_moves)

    draw_pieces(screen, game_state.board) #draw pieces on top of squares

    if len(valid_moves) == 0: #this code displays who won after checkmate is reached

                font = p.font.Font('freesansbold.ttf', 80) #creates a font object to generate text
                white_wins_text = font.render("white wins", True, (0, 0, 0), (255, 0, 255)) #create the white wins text
                black_wins_text = font.render("black wins", True, (0, 0, 0), (255, 0, 255)) #create the black wins text
                stalemate_text = font.render("stalemate", True, (0, 0, 0), (255, 0, 255)) #create the stalemate text
                
                white_text_rect = white_wins_text.get_rect() #create memory rectangle for white text
                black_text_rect = black_wins_text.get_rect() #create memory rectangle for black text
                stalemate_text_rect = stalemate_text.get_rect() #create memory rectangle for stalemate text

                white_text_rect.center = (WIDTH // 2, HEIGHT // 2) #centers memory box for white text
                black_text_rect.center = (WIDTH // 2, HEIGHT // 2) #centers memory box for black text
                stalemate_text_rect.center = (WIDTH //2, HEIGHT // 2) #centers memory box for stalemate text
                
                if game_state.is_stalemate:
                    screen.blit(stalemate_text, stalemate_text_rect) #displays the message stalemate
                elif game_state.is_white_turn:
                    screen.blit(black_wins_text, black_text_rect) #displays the message white wins
                else:
                    print("white wins")
                    screen.blit(white_wins_text, white_text_rect) #displays the message black wins

#Draw squares on the board. Uses white and grey colors. Call draw board first. Top left square is always white square
def draw_board(screen):
    global colors
    colors = [p.Color("white"), p.Color("brown")]   #chooses white and brown to be colors. Perhaps later we could let users pick the color?
    for r in range(DIMENSION):      #double for loop to iterate over the board and go square by square
        for c in range(DIMENSION):
            color = colors[ ((r+c)%2) ]    #selects 'color' to be either index 0 (white) or index 1 (brown). Relies on the following fact: if a chessboard is represented by an 8x8 matrix, with the top left entry (00) and bottom right entry (77), then the sum of the coordinates of the white squares will always be even, and the sum of the coordinates of the dark squares will always be odd.
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE)) #draws a colored rectangle beginning at c*SQ_SIZE and r*SQ_SIZE with dimmensions SQ_SIZE * SQ_SIZE


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
            

#Draw pieces on the board using current game_state.board
def draw_pieces(screen, board):
    for r in range(DIMENSION):      #double for loop to iterate over the board and go square by square
        for c in range(DIMENSION):
            piece = board[r][c] #access the piece corresponding to each square of the board
            if piece != "--": #if not an empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE)) #outputs the image of the identified piece at location c*SQ_SIZE r*SQ_SIZE with dimensions SQ_SIZE * SQ_SIZE


#def draw_move_log(screen, game_state): #FOR LATER

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
            screen.blit(IMAGES[move.piece_captured], end_square)
        
        #draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)  #framerate


main() #calls the main method


