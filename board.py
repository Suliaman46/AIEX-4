import pygame
from constants import ROWS, BLACK, WHITE, SQUARE_SIZE
from piece import Piece


class Board:
    def __init__(self):
        self.board = []

    def draw_board(self, window):
        window.fill(BLACK)
        for row in range(ROWS):
            for column in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, WHITE, (row * SQUARE_SIZE, column * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def init_board(self, window):
        for row in range(ROWS):
            self.board.append([])
            for column in range(ROWS):
                if ((row == 0 or row == 2) and column % 2 == 0) or (row == 1 and column % 2 != 0):
                    self.board[row].append(Piece(row, column, BLACK, window))
                elif ((row == 5 or row == 7) and column % 2 != 0) or (row == 6 and column % 2 == 0):
                    self.board[row].append(Piece(row, column, WHITE, window))
                else:
                    self.board[row].append(0)

    def draw_pieces(self, window):
        for row in range(ROWS):
            for column in range(ROWS):
                piece = self.board[row][column]
                if piece != 0:
                    piece.draw_piece(window)

    def get_piece(self, row, column):
        return self.board[row][column]

    def move(self, row, column, piece):
        self.board[piece.row][piece.column], self.board[row][column] = self.board[row][column], self.board[piece.row][piece.column]
        piece.move(row, column)
        #TODO make king