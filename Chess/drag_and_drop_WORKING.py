
# Main driver file - responsible for handling user input and displaying current GameState object

import pygame as p
from pygame.constants import KEYDOWN, K_z
import chess_machine

p.init()        #initializes pygame
WIDTH = HEIGHT = 1000   #sets width and height of display to 1000x1000 pixels 
DIMENSION = 8 #dimensions are 8x8
SQ_SIZE = HEIGHT // DIMENSION #sets the size of each square
#Do we need MAX_FPS variable?????
IMAGES = {} #Creates a global images directort


#Method that initializes a global directory of images. Minimize calling this method bc it takes a lot of computing time lol
def load_images(): 
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']   #array of all the pieces
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Chess_AI/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)) #iterates through the array and loads each image into the global IMAGES directory. transoform.scale() method ensures that the piece images are the same size as the square
    #Note: Use  ' IMAGES['wP'] '  to access an image

class Piece(p.sprite.Sprite):
    def __init__(self, piece_type, xpos, ypos):
        super(Piece, self).__init__()
        self.piece_type = piece_type    #string
        self.image = IMAGES[piece_type]
        self.rect.x = xpos
        self.rect.y = ypos
        self.square = (xpos//SQ_SIZE, ypos//SQ_SIZE)
        self.clicked = False



    
#Main method - handles user input, updates graphics
def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))    #sets a drawing window according to the HEIGHT and WIDTH specifications set above
    clock = p.time.Clock()  #creates a clock object (built into pygame)
    screen.fill((255, 255, 255))    #sets the screen to be white lol
    
    game_state = chess_machine.Game_State() #creates a game_state object named game_state that calls the constructor and creates appropriate field variables (defined in the chess_machine class)
    valid_moves = game_state.get_valid_moves()  #greates a list of valid moves by calling the get_valid_moves method. Don't want to call this every frame, because it costs a lot of computing time
    move_made = False   #flag variable - used so that we only generate a new set of valid moves by calling get_valid_moves once the game_state has been updated

    
    load_images()   #calls load_images method - we only do it once to conserve computing time
    square_selected = ()    #creates a tuple (for rows and columns) to store the coordinates of a selected square. No square is selected initially. Keeps track of the most recent click of the user.
    player_clicks = []      #keeps track of player clicks. Two tuples: [(starting x, starting y) and (ending x, ending y)]. Empty to start.
    piece_dragging = False

    #Run until user asks to quit
    running = True
    while running:
        
        for event in p.event.get(): #iterates through all the "events" -- includes clicks, button presses, etc
            if event.type == p.QUIT:    #asks whether user has clicked window close button
                running = False     #if so, quits game

        #mouse handler
            elif event.type == p.MOUSEBUTTONDOWN: #asks whether user clicks somewhere on the screen
                location = p.mouse.get_pos() #gets the (x, y) location of mouse
                col = location[0]//SQ_SIZE #gets the x coordinate, then divides it by the square size to determine the column 
                row = location[1]//SQ_SIZE #gets the y coordinate, then divides it by the square size to determine the row
 
 
                square_selected = (row, col)
                player_clicks.append(square_selected)
                if (game_state.board[row][col] != "--"):
                    piece_dragging = True
                    mouse_x, mouse_y

            elif event.type == p.MOUSEBUTTONUP:
                piece_dragging = False

            elif event.type == p.MOUSEMOTION:
                if piece_dragging:
                    mouse_x, mouse_y = event.pos
                    


 #               #check if square is ALREADY SELECTED
 #               if square_selected == (row, col):        #the user clicked the same square twice
 #                   square_selected = ()        #deselect
 #                   player_clicks = []  #clear player_clicks
 #               else:
 #                   square_selected = (row, col) #stores location of click in square_selected variable
 #                   player_clicks.append(square_selected) #adds the location of the click to the list 

#                #was that the second click?
#                if len(player_clicks) == 2:     #after the second click
#                    #now we make our move!
#                    move = chess_machine.Move(player_clicks[0], player_clicks[1], game_state.board)   #creates new move object with start_square as player_clicks[0] (the location of the first click) and end_square as player_clicks[1] (the location of the second click)
#                    print(move.get_chess_notation())    #prints chess notation for the above move
#                    if move in valid_moves:    #checks whether the move is an element of a valid move. PROBLEM: THIS WILL NOT WORK WITHOUT OVERWRITING THE EQUALS METHOD. OTHERWISE, THE COMPUTER HAS NO WAY OF KNOWING WHETHER THE MOVE MADE BY THE USER'S CLICKS IS EQUAL TO A MOVE IN THE MOVES[] LIST
#                        game_state.make_move(move)  #calls the make move method to actually update the game_state
#                        move_made = True    #sets flag variable to true -- indication that a new set of valid_moves needs to be generated
#                    square_selected = ()    #reset user clicks
#                    player_clicks = []      #resets user clicks

            #key handler
            elif event.type == p.KEYDOWN:
                #UNDO MOVE
                if event.key == p.K_z and p.key.get_mods() & p.KMOD_CTRL:   #undo when 'ctrl + z' is pressed -- thanks stack exchange!
                    game_state.undo_move()  #calls undo move
                    move_made = True    #sets flag variable to true in order to generate a new set of valid moves
                    square_selected = ()    #reset user clicks
                    player_clicks = []      #resets user clicks

        if move_made:   #once a move has been made, generate a new set of valid moves
            valid_moves = game_state.get_valid_moves()
            move_made = False


        draw_game_state(screen, game_state, valid_moves, square_selected) #calls draw_game_state to draw the current state



        clock.tick()    #updates the clock -- called once per frame; computes how many milliseconds have passed since previous call
        p.display.flip()    #updates entire display



#Method responsible for all the graphics within a current game state
def draw_game_state(screen, game_state, valid_moves, square_selected):
    draw_board(screen) #draw squares on the board
    highlight_squares(screen, game_state, valid_moves, square_selected)

    draw_pieces(screen, game_state.board) #draw pieces on top of squares

#Draw squares on the board. Uses white and grey colors. Call draw board first. Top left square is always white square
def draw_board(screen):
    colors = [p.Color("white"), p.Color("brown")]   #chooses white and brown to be colors. Perhaps later we could let users pick the color?
    for r in range(DIMENSION):      #double for loop to iterate over the board and go square by square
        for c in range(DIMENSION):
            color = colors[ ((r+c)%2) ]    #selects 'color' to be either index 0 (white) or index 1 (brown). Relies on the following fact: if a chessboard is represented by an 8x8 matrix, with the top left entry (00) and bottom right entry (77), then the sum of the coordinates of the white squares will always be even, and the sum of the coordinates of the dark squares will always be odd.
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE)) #draws a colored rectangle beginning at c*SQ_SIZE and r*SQ_SIZE with dimmensions SQ_SIZE * SQ_SIZE


def highlight_squares(screen, game_state, valid_moves, square_selected): #Highlights square selected. Highlights valid moves for piece selected
    
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

main() #calls the main method


