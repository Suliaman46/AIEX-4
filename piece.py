from constants import SQUARE_SIZE, PIECE_SIZE, WHITE, BLACK, CROWN
import pygame


class Piece:
    def __init__(self, row, col, colour, window):
        self.row = row
        self.column = col
        self.colour = colour
        self.is_king = False
        self.x = self.y = 0
        self.position()
        self.draw_piece(window)

    def position(self):
        self.x = self.column * SQUARE_SIZE + SQUARE_SIZE // 2
        self.y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2

    def draw_piece(self, window):
        pygame.draw.circle(window, BLACK, (self.x, self.y), PIECE_SIZE // 2 + 3)
        pygame.draw.circle(window, self.colour, (self.x, self.y), PIECE_SIZE // 2)
        if self.is_king:
            window.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row, column):
        self.row = row
        self.column = column
        self.position()

    def become_king(self, window):
        self.is_king = True
