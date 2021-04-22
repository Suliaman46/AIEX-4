import pygame
from constants import SQUARE_SIZE, HEIGHT, WIDTH
from checkers import Checkers

FPS = 60


def get_mouse_position(position):
    x, y = position
    return y // SQUARE_SIZE, x // SQUARE_SIZE


pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
game = Checkers(window)
run = True

# game.board.move(4,4,game.)
# while run:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             pos = pygame.mouse.get_pos()
#             x, y = get_mouse_position(pos)
#             piece = game.board.get_piece(x,y )
#             game.board.move(4,4,piece)
#
#     game.update()

clock = pygame.time.Clock()
# game = Game(WIN)

while run:
    clock.tick(FPS)

    if game.winner() != None:
        print(game.winner())
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row, col = get_mouse_position(pos)

            game.select(row, col)



    game.update()


