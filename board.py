import pygame
from constants import ROWS, BLACK, WHITE, SQUARE_SIZE
from piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.chosen_piece = None
        self.black_left = self.white_left = 12
        self.black_kings = self.white_kings = 0
        self.init_board()

    def init_board(self):
        for row in range(ROWS):
            self.board.append([])
            for column in range(ROWS):
                if ((row == 0 or row == 2) and column % 2 == 0) or (row == 1 and column % 2 != 0):
                    self.board[row].append(Piece(row, column, BLACK))

                elif ((row == 5 or row == 7) and column % 2 != 0) or (row == 6 and column % 2 == 0):
                    self.board[row].append(Piece(row, column, WHITE))
                else:
                    self.board[row].append(0)

    def draw_background(self, window):
        window.fill(BLACK)
        for row in range(ROWS):
            for column in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, WHITE, (row * SQUARE_SIZE, column * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self, window):
        for row in range(ROWS):
            for column in range(ROWS):
                piece = self.board[row][column]
                if piece != 0:
                    piece.draw_piece(window)

    def draw_board(self,window):
        self.draw_background(window)
        self.draw_pieces(window)

    def get_chose_piece(self):
        return self.chosen_piece
    def get_piece(self,row,column):
        return self.board[row][column]

    def set_chose_piece(self,piece):
        self.chosen_piece = piece

    def winner(self):
        if self.white_left <= 0:
            return "BLACK"
        elif self.black_left <= 0:
            return "WHITE"
        else:
            return None

    def remove(self, cordinates):
        for row,column in cordinates:

            # self.board[piece.row][piece.column] = 0
            piece = self.get_piece(row, column)
            if piece != 0:
                if piece.color == WHITE:
                    self.white_left -= 1
                else:
                    self.black_left -= 1

            self.board[row][column] = 0


            # if piece != 0:
            #     if piece.color == WHITE:
            #         self.white_left -= 1
            #     else:
            #         self.black_left -= 1


    def move(self, row, column, piece):
        self.board[piece.row][piece.column], self.board[row][column] = self.board[row][column], self.board[piece.row][piece.column]
        piece.move(row, column)

        if row == ROWS - 1 or row == 0:
            piece.become_king()
            if piece.color == BLACK:
                self.black_kings += 1
            else:
                self.white_kings += 1

    def get_possible_moves(self,piece):
        possible_moves = {}
        path_taken =[]
        possible_moves.update(self._get_valid_moves(piece,piece.row,piece.column,path_taken,1))
        possible_moves.update(self._get_valid_moves(piece,piece.row,piece.column,path_taken,2))
        return possible_moves


    def check_surrondings(self, piece, old_row, old_column, new_row, new_column, step_size):

        #Checks all basic conditons for moving and  checks destiantion had differnt colred piece

        if not (piece.is_king or new_row == old_row + piece.direction * step_size):             # wrong direction
            return False
        if not (0 <= new_row < ROWS and 0 <= new_column < ROWS):             # outside of board
            return False
        destination = self.get_piece(new_row, new_column)             # jump location not empty
        if destination != 0:
            return False

        # all basic obstacles  overcome

        if step_size == 2: # Check for JUMP
            middle_row = (old_row + new_row) // 2
            middle_column = (old_column + new_column) // 2
            middle_piece = self.get_piece(middle_row, middle_column)
            if middle_piece == 0 or middle_piece.color == piece.color:
                return False
        return True

    def _get_valid_moves(self, piece, row, col, path, step_size):

        #Takes piece's current position also takes path so the king does not jump back to where it came from and does not jump over the same piece twice
        # If step size is 1 only single jumps are considered
        # If step size is 2 multiple jumps are considered involving recursion


        row_up, row_down, col_left, col_right = [x + y * step_size for x in [row, col] for y in [-1, +1]]
        moves = {}

        for new_col in [col_left, col_right]:
            for new_row in [row_up, row_down]:
                if not self.check_surrondings(piece, row, col, new_row, new_col, step_size):
                    continue
                if step_size == 1:
                    moves[new_row, new_col] = []
                else:
                    middle_row = (new_row + row) // 2
                    middle_col = (new_col + col) // 2
                    if (middle_row, middle_col) in path:
                        continue
                    new_path = path.copy()
                    new_path.append((middle_row, middle_col))
                    moves[(new_row, new_col)] = new_path
                    # recursive call
                    moves.update(self._get_valid_moves(piece, new_row, new_col, new_path, step_size))

        return moves

