import pygame
import sys
import game
import ghost

# map indicators:
# | - ┏ ┓ ┗ ┛ ┝ ┥  ┯ ┷ ┼ for walls
# . for points O for power points
# G for ghost house

map = [
    ['┏', '-', '-', '-','-', '-', '-', '-', '-', '┯', '-', '-', '-', '-', '-', '-', '-', '-', '┓'],
    ['|', '.', '.', '.','.', '.', '.', '.', '.', '|', '.', '.', '.', '.', '.', '.', '.', '.', '|'],
    ['|', 'O', '┏', '┓','.', '┏', '-', '┓', '.', '|', '.', '┏', '-', '┓', '.', '┏', '┓', 'O', '|'],
    ['|', '.', '┗', '┛','.', '┗', '-', '┛', '.', '|', '.', '┗', '-', '┛', '.', '┗', '┛', '.', '|'],
    ['|', '.', '.', '.','.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '|'],
    ['|', '.', '-', '-','.', '|', '.', '-', '-', '┯', '-', '-', '.', '|', '.', '-', '-', '.', '|'],
    ['|', '.', '.', '.','.', '|', '.', '.', '.', '|', '.', '.', '.', '|', '.', '.', '.', '.', '|'],
    ['┗', '-', '-', '┓','.', '┝', '-', '-', ' ', '|', ' ', '-', '-', '┥', '.', '┏', '-', '-', '┛'],
    [' ', ' ', ' ', '|','.', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', '.', '|', ' ', ' ', ' '],
    ['-', '-', '-', '┛','.', '|', ' ', '┏', '-', '_', '-', '┓', ' ', '|', '.', '┗', '-', '-', '-'],
    ['.', '.', '.', '.','.', ' ', ' ', '|', 'G', 'G', 'G', '|', ' ', ' ', '.', '.', '.', '.', '.'],
    ['-', '-', '-', '┓','.', '|', ' ', '┗', '-', '-', '-', '┛', ' ', '|', '.', '┏', '-', '-', '-'],
    [' ', ' ', ' ', '|','.', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', '.', '|', ' ', ' ', ' '],
    ['┏', '-', '-', '┛','.', '|', ' ', '-', '-', '┯', '-', '-', ' ', '|', '.', '┗', '-', '-', '┓'],
    ['|', '.', '.', '.','.', '.', '.', '.', '.', '|', '.', '.', '.', '.', '.', '.', '.', '.', '|'],
    ['|', '.', '-', '┓','.', '-', '-', '-', '.', '|', '.', '-', '-', '-', '.', '┏', '-', '.', '|'],
    ['|', 'O', '.', '|','.', '.', '.', '.', '.', ' ', '.', '.', '.', '.', '.', '|', '.', 'O', '|'],
    ['┝', '-', '.', '|','.', '|', '.', '-', '-', '┯', '-', '-', '.', '|', '.', '|', '.', '-', '┥'],
    ['|', '.', '.', '.','.', '|', '.', '.', '.', '|', '.', '.', '.', '|', '.', '.', '.', '.', '|'],
    ['|', '.', '-', '-','-', '┷', '-', '-', '.', '|', '.', '-', '-', '┷', '-', '-', '-', '.', '|'],
    ['|', '.', '.', '.','.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '|'],
    ['┗', '-', '-', '-','-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '┛'],
]


#constants
FPS = 45
#Square size
SSIZE = 30
WIDTH = len(map[0]) * SSIZE
HEIGHT = len(map) * SSIZE
SCOREBOARD_HEIGHT = 50
WALL_THICKNESS = 7
DOTS_COLOR = (225, 184, 174)
CYAN = (0, 255, 255)


#init
start_location = [9, 16]
game = game.Game(map, start_location)

#pygame init
pygame.init()
font = pygame.font.Font('font/Emulogic-zrEw.ttf', 15)
large_font = pygame.font.Font('font/Emulogic-zrEw.ttf', 20)

window = pygame.display.set_mode([WIDTH, HEIGHT + SCOREBOARD_HEIGHT])
pygame.display.set_caption('Pacman')
clock = pygame.time.Clock()

def MapDraw(map):
    map = game.map
    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] == '|':
                pygame.draw.line(window, (0, 0, 255), (col * SSIZE + SSIZE/2, row * SSIZE), (col * SSIZE + SSIZE/2, (row+1) * SSIZE), WALL_THICKNESS)
            elif map[row][col] == '┏':
                pygame.draw.line(window, (0, 0, 255), (col * SSIZE + SSIZE/2, row * SSIZE + SSIZE/2), (col * SSIZE + SSIZE/2, (row+1) * SSIZE), WALL_THICKNESS)
                pygame.draw.line(window, (0, 0, 255), (col * SSIZE + SSIZE/2, row * SSIZE + SSIZE/2), (col * SSIZE + SSIZE, row * SSIZE + SSIZE/2), WALL_THICKNESS)
            elif map[row][col] == '-':
                pygame.draw.line(window, (0, 0, 255), (col * SSIZE, row * SSIZE + SSIZE/2), (col * SSIZE + SSIZE, row * SSIZE + SSIZE/2), WALL_THICKNESS)
            elif map[row][col] == '_':
                pygame.draw.line(window, (255, 255, 255), (col * SSIZE, row * SSIZE + SSIZE/2), (col * SSIZE + SSIZE, row * SSIZE + SSIZE/2), WALL_THICKNESS)
            elif map[row][col] == '┓':
                pygame.draw.line(window, (0, 0, 255), (col * SSIZE + SSIZE/2, row * SSIZE + SSIZE/2), (col * SSIZE + SSIZE/2, (row+1) * SSIZE), WALL_THICKNESS)
                pygame.draw.line(window, (0, 0, 255), (col * SSIZE, row * SSIZE + SSIZE/2), (col * SSIZE + SSIZE/2, row * SSIZE + SSIZE/2), WALL_THICKNESS)
            elif map[row][col] == '┗':
                pygame.draw.line(window, (0, 0, 255), (col * SSIZE + SSIZE/2, row * SSIZE), (col * SSIZE + SSIZE/2, row * SSIZE + SSIZE/2), WALL_THICKNESS)
                pygame.draw.line(window, (0, 0, 255), (col * SSIZE + SSIZE/2, row * SSIZE + SSIZE/2), (col * SSIZE + SSIZE, row * SSIZE + SSIZE/2), WALL_THICKNESS)
            elif map[row][col] == '┛':
                pygame.draw.line(window, (0, 0, 255), (col * SSIZE + SSIZE/2, row * SSIZE), (col * SSIZE + SSIZE/2, row * SSIZE + SSIZE/2), WALL_THICKNESS)
                pygame.draw.line(window, (0, 0, 255), (col * SSIZE, row * SSIZE + SSIZE/2), (col * SSIZE + SSIZE/2, row * SSIZE + SSIZE/2), WALL_THICKNESS)
            elif map[row][col] == '┝':
                pygame.draw.line(window, (0, 0, 255), (col * SSIZE + SSIZE/2, row * SSIZE), (col * SSIZE + SSIZE/2, (row+1) * SSIZE), WALL_THICKNESS)
                pygame.draw.line(window, (0, 0, 255), (col * SSIZE + SSIZE/2, row * SSIZE + SSIZE/2), (col * SSIZE + SSIZE, row * SSIZE + SSIZE/2), WALL_THICKNESS)
            elif map[row][col] == '┥':
                pygame.draw.line(window, (0, 0, 255), (col * SSIZE + SSIZE/2, row * SSIZE), (col * SSIZE + SSIZE/2, (row+1) * SSIZE), WALL_THICKNESS)
                pygame.draw.line(window, (0, 0, 255), (col * SSIZE, row * SSIZE + SSIZE/2), (col * SSIZE + SSIZE/2, row * SSIZE + SSIZE/2), WALL_THICKNESS)
            elif map[row][col] == '┯':
                pygame.draw.line(window, (0, 0, 255), (col * SSIZE, row * SSIZE + SSIZE/2), (col * SSIZE + SSIZE, row * SSIZE + SSIZE/2), WALL_THICKNESS)
                pygame.draw.line(window, (0, 0, 255), (col * SSIZE + SSIZE/2, row * SSIZE + SSIZE/2), (col * SSIZE + SSIZE/2, (row+1) * SSIZE), WALL_THICKNESS)
            elif map[row][col] == '┷':
                pygame.draw.line(window, (0, 0, 255), (col * SSIZE, row * SSIZE + SSIZE/2), (col * SSIZE + SSIZE, row * SSIZE + SSIZE/2), WALL_THICKNESS)
                pygame.draw.line(window, (0, 0, 255), (col * SSIZE + SSIZE/2, row * SSIZE), (col * SSIZE + SSIZE/2, row * SSIZE + SSIZE/2), WALL_THICKNESS)
            elif map[row][col] == '┼':
                pygame.draw.line(window, (0, 0, 255), (col * SSIZE, row * SSIZE + SSIZE/2), (col * SSIZE + SSIZE, row * SSIZE + SSIZE/2), WALL_THICKNESS)
                pygame.draw.line(window, (0, 0, 255), (col * SSIZE + SSIZE/2, row * SSIZE), (col * SSIZE + SSIZE/2, (row+1) * SSIZE), WALL_THICKNESS)
            elif map[row][col] == 'O':
                pygame.draw.circle(window, DOTS_COLOR, (col * SSIZE + SSIZE/2, row * SSIZE + SSIZE/2), SSIZE*4/10, 99999999)
            elif map[row][col] == '.':
                pygame.draw.circle(window, DOTS_COLOR, (col * SSIZE + SSIZE/2, row * SSIZE + SSIZE/2), SSIZE*1/10, 99999999)

scores = []
score = 0
counter = 0
while True:
    counter += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:           
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    game.move(keys)
    game.collision_check()

    MapDraw(map)

    new_score = game.score
    if new_score - score >= 200: scores.append([new_score - score, counter, game.pacman_pos])

    #temporarily draw score for killed ghosts
    for score, start_counter, pos in scores:
        score_text = font.render(str(round(score, -2)), True, CYAN)
        window.blit(score_text, (pos[0] * SSIZE, pos[1] * SSIZE))
        if counter - start_counter >= 25:
            scores.remove([score, start_counter, pos])
    score = new_score
    
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    window.blit(score_text, (10, HEIGHT + 5))


    lives = game.get_lives()
    for i in range(len(lives)):

        image = pygame.transform.scale(lives[i], (SSIZE*2/3, SSIZE*2/3))
        window.blit(image, (WIDTH - (i+1)*SSIZE, HEIGHT + 5))
    
    if game.lives == 0:
        game_over_text = large_font.render("GAME OVER", True, (255, 0, 0))
        window.blit(game_over_text, (WIDTH/2 - game_over_text.get_rect()[2]/2, HEIGHT/2 + 30))


    pacman = game.get_packman()
    image = pygame.transform.scale(pacman['image'], (SSIZE, SSIZE))
    window.blit(image, (pacman['pos'][0] * SSIZE, pacman['pos'][1] * SSIZE))

    for ghost in game.get_ghosts():
        image = pygame.transform.scale(ghost['image'], (SSIZE, SSIZE))
        window.blit(image, (ghost['pos'][0] * SSIZE, ghost['pos'][1] * SSIZE))

    pygame.display.update()
    window.fill((0, 0, 0))  
    clock.tick(FPS)

