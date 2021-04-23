import pygame
from constants import ROWS, BLACK, WHITE, SQUARE_SIZE
from piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.black_left = self.white_left = 12
        self.black_kings = self.white_kings = 0
        self.init_board()

    def init_board(self):
        for row in range(ROWS):
            self.board.append([])
            for column in range(ROWS):
                if ((row == 0 or row == 2) and column % 2 != 0) or (row == 1 and column % 2 == 0):
                    self.board[row].append(Piece(row, column, BLACK))

                elif ((row == 5 or row == 7) and column % 2 == 0) or (row == 6 and column % 2 != 0):
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
        is_possible_W = self.is_movement_possible(WHITE)
        is_possible_B = self.is_movement_possible(BLACK)
        if not is_possible_W :
            return "BLACK"
        elif not is_possible_B  :
            return "WHITE"
        else:
            return None


    def is_movement_possible(self,color):
        all_pieces = self.get_all_pieces(color)
        for piece in all_pieces:
            valid_moves = self.get_possible_moves(piece)
            if  valid_moves:
                return True
        return False

    def remove(self, cordinates):
        for row,column in cordinates:

            piece = self.get_piece(row, column)
            if piece != 0:
                if piece.color == WHITE:
                    self.white_left -= 1
                else:
                    self.black_left -= 1

            self.board[row][column] = 0

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
        possible_moves.update(self._get_moves(piece,piece.row,piece.column,path_taken,1))
        possible_moves.update(self._get_moves(piece,piece.row,piece.column,path_taken,2))

        #if the possible move contains moves where a jump is possible then it must be made therefore the moves where no jumps are made become invalid
        empty_exists =  non_empty_exists = False
        for move_key in possible_moves:
            if  possible_moves[move_key]:
                non_empty_exists = True
            else:
                empty_exists = True
        if empty_exists and non_empty_exists:
            possible_moves = {x:possible_moves[x] for x in possible_moves if possible_moves[x]}


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

    def _get_moves(self, piece, row, col, path, step_size):

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
                    moves.update(self._get_moves(piece, new_row, new_col, new_path, step_size))

        return moves

    def get_all_pieces(self,color):
        # pieces = [piece for row in self.board for piece in row if  piece!= 0 and piece == color]
        pieces = []
        for row in self.board:
            for piece in row:
                if piece!= 0 and piece.color == color:
                    pieces.append(piece)

        return pieces

    def get_score_white(self):
        return 5*self.white_kings + 3*(self.white_left - self.white_kings) - (5*self.black_kings + 3*(self.black_left - self.black_kings))
        # return -(5*self.white_kings + 3*(self.white_left - self.white_kings) - (5*self.black_kings + 3*(self.black_left - self.black_kings)))

    def get_score_black(self):
        return -(self.get_score_white())

