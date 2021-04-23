import pygame
from board import Board
from constants import WHITE, BLACK, RED,SQUARE_SIZE,PIECE_SIZE


class Checkers:
    def __init__(self, window):
        self._init()
        self.window = window

    def _init(self):
        self.selected_piece = None
        self.board = Board()
        self.turn = WHITE
        self.possible_moves = {} #valid moves available

    def update(self):
        self.board.draw_board(self.window)
        self.draw_possible_moves(self.possible_moves)
        pygame.display.update()

    def find_jump(self):
        jumps = []
        all_pieces = self.board.get_all_pieces(self.turn)
        for piece in all_pieces:
            valid_moves = self.board.get_possible_moves(piece)
            for move,skip in valid_moves.items():
                if skip:
                    jumps.append(piece)
        return jumps


    def select(self, row, column):
        jumps =self.find_jump()
        if self.selected_piece:
            move = self._move(row, column)
            if not move:
                self.selected_piece = None
                self.select(row, column)
        if jumps:
            for piece in jumps:
                if row != piece.row or column != piece.column:
                    continue

                else:
                    piece = self.board.get_piece(row, column)
                    if piece != 0 and piece.color == self.turn:
                        self.selected_piece = piece
                        self.possible_moves = self.board.get_possible_moves(piece)
                        return True

        else:

            piece = self.board.get_piece(row, column)
            if piece != 0 and piece.color == self.turn:
                self.selected_piece = piece
                self.possible_moves = self.board.get_possible_moves(piece)
                return True

            return False



    def _move(self, row, column):

        dest_piece = self.board.get_piece(row, column)

        if self.selected_piece and dest_piece == 0 and (row, column) in self.possible_moves:
            self.board.move( row, column,self.selected_piece,)
            skipped = self.possible_moves[(row, column)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False
        return True

    def change_turn(self):
        self.possible_moves = {}
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE


    def draw_possible_moves(self,possible_moves):
        for move in possible_moves:
            row,col = move
            pygame.draw.circle(self.window, RED,(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)


    def winner(self):
        return self.board.winner()


    def restart(self):
        self._init()

    def get_board(self):
        return self.board
    def turn_AI(self,board):
        self.board = board
        self.change_turn()