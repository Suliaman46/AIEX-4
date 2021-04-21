import pygame
from board import Board
from constants import WHITE, BLACK


class Checkers:
    def __init__(self, window):
        self.board = Board()
        self.board.init_board(window)
        self.window = window
        self.turn = WHITE
        self.selected = None
        self.moves = {} #valid moves

    def update(self):
        self.board.draw_board(self.window)
        self.board.draw_pieces(self.window)
        pygame.display.update()

    def move(self, row, column):
        pass #TODO

    def select(self, row, column):
            pass #TODO

