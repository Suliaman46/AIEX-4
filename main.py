import pygame, math
from constants import SQUARE_SIZE, HEIGHT, WIDTH, WHITE,BLACK
from checkers import Checkers
from alpha_beta import  alpha_beta_mm_BLACK,alpha_beta_mm

FPS = 60
max_depth = 4

def get_mouse_position(position):
    x, y = position
    return y // SQUARE_SIZE, x // SQUARE_SIZE

def message(msg):
    font = pygame.font.Font('freesansbold.ttf', 85)
    text = font.render(msg, True, WHITE, BLACK)
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT // 2)
    window.blit(text, textRect)
    pygame.display.update()


pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
game = Checkers(window)
run = True



clock = pygame.time.Clock()
while run:
    clock.tick(FPS)

    # AI is WHITE
    if game.turn == WHITE:

        value, new_board = alpha_beta_mm(game.get_board(),max_depth,-math.inf,math.inf, WHITE)
        game.turn_AI(new_board)

    if game.winner() != None:
        # print(game.winner())
        message(game.winner() + ' WINS')
        pygame.time.delay(5000)
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row, col = get_mouse_position(pos)
            game.select(row, col)



    # AI IS BLACK
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         run = False
    #
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         pos = pygame.mouse.get_pos()
    #         row, col = get_mouse_position(pos)
    #         game.select(row, col)
    #     #FOR WINNING BY ELIMINATION
    # if game.winner() != None:
    #     print(game.winner())
    #     run = False
    #     #FOR WINNING BY BLOCKADE
    # if game.Winner != None:
    #     print(game.Winner)
    #     run = False
    #
    # if game.turn == BLACK:
    #     value, new_board = alpha_beta_mm_BLACK(game.get_board(), max_depth,-math.inf,math.inf, BLACK)
    #
    #     game.turn_AI(new_board)
    #


    # # AI vs AI
    # if game.turn == WHITE:
    #     value, new_board = alpha_beta_mm(game.get_board(), max_depth,-math.inf,math.inf, WHITE)
    #     game.turn_AI(new_board)
    #
    # if game.winner() != None:
    #     print(game.winner())
    #     run = False
    # pygame.time.delay(500)
    # if game.turn == BLACK:
    #     value, new_board = alpha_beta_mm_BLACK(game.get_board(), max_depth, -math.inf, math.inf, BLACK)
    #     game.turn_AI(new_board)

    game.update()
pygame.quit()