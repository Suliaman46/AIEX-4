import pygame
from constants import SQUARE_SIZE, HEIGHT, WIDTH
from checkers import Checkers


def get_mouse_position(position):
    x, y = position
    return y // SQUARE_SIZE, x // SQUARE_SIZE


pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
game = Checkers(window)
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x, y = get_mouse_position(pos)
            piece = game.board.get_piece(x, y)

    game.update()

pygame.quit()