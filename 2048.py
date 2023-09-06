import pygame as pg
import random as rnd

# initializes the Pygame library
pg.init()

# initial set up
timer = pg.time.Clock() # the timer and fps ensure that our game runs at a -
fps = 60                # consistent speed and frame rate across different systems.
font = pg.font.Font('freesansbold.ttf', 24)

# 2048 color dictionary
colors = {0: (205, 195, 180),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light-text': (255, 255, 255),
          'dark-text': (107, 97, 73),
          'dark': (50, 50, 50),
          'darker': (0, 0, 0),
          'bg': (180, 170, 150)}

# initializes game variables
board_values = [[0 for _ in range(4)] for _ in range(4)] # creates a 4x4 two-dimensional list with zeros
game_over = False
insert_new = True
insert_twice = 0 # to insert two values at the beginning of the game
direction = ''
score = 0
file = open('high_score', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high

# draws background for the board
def draw_board():
    pg.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 2)
    score_text = font.render(f'Score: {score}', True, 'white')
    high_score_text = font.render(f'High Score: {high_score}', True, 'white')
    screen.blit(score_text, (10, 420)) # displays the score on the screen
    screen.blit(high_score_text, (10, 455)) # displays the high score on the screen

# draws tiles for the game
def draw_tiles(board):
    for i in range(4): # these two for loops iterate through all the tiles
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light-text']
            else:
                value_color = colors['dark-text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['darker']

            # positions the tiles in the right place with the right spacing
            pg.draw.rect(screen, color, [j * 97.75 + 10, i * 97.75 + 10, 87.75, 87.75], 0, 2) 
            
            if value > 0:
                value_len = len(str(value))
                font = pg.font.Font('freesansbold.ttf', 48 - (5 * value_len)) # decreases the font size as the length increases.
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 97.75 + 53, i * 97.75 + 53)) # positions the number at the center of the tile.
                screen.blit(value_text, text_rect)

# shifts and/or merges the tiles based on the users turn direction
def take_turn(direc, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)] # set merged to false for all tiles initially
    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                # checks all rows above i for zeros and adds 1 to the shift variable if it finds one
                for q in range(i):
                    if board[q][j] == 0:
                        shift += 1
                # shifts the tiles that have a zero above them upwards
                if shift > 0:
                    board[i - shift][j] = board[i][j]
                    board[i][j] = 0
                # merges the tiles upwards if their values are the same
                if board[i - shift - 1][j] == board[i - shift][j] \
                        and not merged[i - shift][j] \
                        and not merged[i - shift - 1][j]:
                    board[i - shift - 1][j] *= 2
                    score += board[i - shift - 1][j]
                    board[i - shift][j] = 0
                    merged[i - shift - 1][j] = True

    elif direc == 'DOWN':
        for i in range(4):
            for j in range(4):
                shift = 0
                # checks all rows below i for zeros and adds 1 to the shift variable if it finds one
                for q in range(i):
                    if board[3 - q][j] == 0:
                        shift += 1
                # shifts the tiles that have a zero below them downwards
                if shift > 0:
                    board[3 - i + shift][j] = board[3 - i][j]
                    board[3 - i][j] = 0
                if 4 - i + shift <= 3:
                    # merges the tiles downwards if their values are the same
                    if board[4 - i + shift][j] == board[3 - i + shift][j] \
                            and not merged[4 - i + shift][j] \
                            and not merged[3 - i + shift][j]:
                        board[4 - i + shift][j] *= 2
                        score += board[4 - i + shift][j]
                        board[3 - i + shift][j] = 0
                        merged[4 - i + shift][j] = True

    elif direc == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                # checks all rows to the left of i for zeros and adds 1 to the shift variable if it finds one
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                # shifts the tiles that have a zero to thier left to the left
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                # merges the tiles to the left if their values are the same
                if board[i][j - shift] == board[i][j - shift - 1] \
                        and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                # checks all rows to the right of i for zeros and adds 1 to the shift variable if it finds one
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                # shifts the tiles that have a zero to thier right to the right
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                # merges the tiles to the right if their values are the same
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] \
                            and not merged[i][4 - j + shift] \
                            and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
    return board

# inserts in new tiles randomly when the user makes a turn
def new_tiles(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = rnd.randint(0, 3)
        col = rnd.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if rnd.randint(1, 10) == 10: # sometimes the game inserts a 4 instead of 2
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full

# draws game over and restart instructions text
def draw_over():
    pg.draw.rect(screen, colors['dark'], [50, 50, 300, 100], 0, 2)
    game_over_text1 = font.render('Game Over!', True, 'red')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))

# sets the dimensions and caption of the game
screen = pg.display.set_mode([400, 500])
pg.display.set_caption('2048')

# main game loop
run = True
while run:
    #calls the necessary functions to start the game
    timer.tick(fps)
    screen.fill(colors['dark'])
    draw_board()
    draw_tiles(board_values)
    
    # calls the new_tiles function twice to start the game with two non zero tiles on the board
    if insert_new or insert_twice < 2:
        board_values, game_over = new_tiles(board_values)
        insert_new = False
        insert_twice += 1
        
    # calls the function take_turn when the user clicks on an arrow key
    if direction != '':
        board_values = take_turn(direction, board_values)
        direction = ''
        insert_new = True
        
    # calls the function draw_over() when the board is full and no tiles can be merged and
    # writes the new high score to the high score file
    if game_over:
        draw_over()
        if high_score > init_high:
            file = open('high_score', 'w')
            file.write(f'{high_score}')
            file.close()
            init_high = high_score

    # links the keyboard events with the value of the direction variable
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYUP:
            if event.key == pg.K_UP and not game_over:
                direction = 'UP'
            elif event.key == pg.K_DOWN and not game_over:
                direction = 'DOWN'
            elif event.key == pg.K_LEFT and not game_over:
                direction = 'LEFT'
            elif event.key == pg.K_RIGHT and not game_over:
                direction = 'RIGHT'

            # resets the game when game over is true and the user clicks the enter key
            if game_over:
                if event.key == pg.K_RETURN:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    insert_new = True
                    insert_twice = 0
                    score = 0
                    direction = ''
                    game_over = False

    # updates high score
    if score > high_score:
        high_score = score

    pg.display.flip() # update the contents of the game after making changes
pg.quit()


# Group Memebers
# 1.Ahmed Mensur UGR/9668/15
# 2.Betretsion Aklilu UGR/4566/15
# 3.Essey Tesfamichael UGR/9377/15
# 4.Habtewold Degifie UGR/9789/15
# 5.Kaleab Simachew UGR/4523/15
# 6.Yohannes Demeke UGR/4620/15