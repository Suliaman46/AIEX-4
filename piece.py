from constants import SQUARE_SIZE, PIECE_SIZE, WHITE, BLACK, CROWN
import pygame


class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.column = col
        self.color = color
        self.is_king = False
        self.x = self.y = 0
        if self.color == WHITE:
            self.direction = -1
        else:
            self.direction = 1
        self.position()


    def position(self):
        self.x = self.column * SQUARE_SIZE + SQUARE_SIZE // 2
        self.y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2

    def draw_piece(self, window):
        pygame.draw.circle(window, BLACK, (self.x, self.y), PIECE_SIZE // 2 + 3)
        pygame.draw.circle(window, self.color, (self.x, self.y), PIECE_SIZE // 2)
        if self.is_king:
            window.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row, column):
        self.row = row
        self.column = column
        self.position()

    def become_king(self):
        self.is_king = True

    def __repr__(self):
        return str(self.color)
