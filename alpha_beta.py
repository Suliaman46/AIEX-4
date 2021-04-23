from copy import deepcopy
from constants import WHITE,BLACK
import pygame

def alpha_beta_mm(current_board,depth,alpha,beta,maximizing_player):
    if depth == 0 or current_board.winner() != None:
        return current_board.get_score_white(), current_board

    if maximizing_player:
        max_score = float('-inf')
        best_move = None
        for move in get_all_moves(current_board, WHITE):
            score = alpha_beta_mm(move, depth - 1,alpha,beta, False)[0]
            max_score = max(max_score, score)
            if max_score == score:
                best_move = move
            alpha = max(alpha,score)
            if beta <= alpha:
                break

        return max_score, best_move
    else:
        min_score = float('inf')
        best_move = None
        for move in get_all_moves(current_board, BLACK):
            score = alpha_beta_mm(move, depth - 1,alpha,beta, True)[0]
            min_score = min(min_score, score)
            if min_score == score:
                best_move = move
            beta = min(beta,score)
            if beta <= alpha:
                break

        return min_score, best_move


def alpha_beta_mm_BLACK(current_board,depth,alpha,beta,maximizing_player):
    if depth == 0 or current_board.winner() != None:
        return current_board.get_score_black(), current_board

    if maximizing_player:
        max_score = float('-inf')
        best_move = None
        for move in get_all_moves(current_board, BLACK):
            score = alpha_beta_mm(move, depth - 1,alpha,beta, False)[0]
            max_score = max(max_score, score)
            if max_score == score:
                best_move = move
            alpha = max(alpha,score)
            if beta <= alpha:
                break

        return max_score, best_move
    else:
        min_score = float('inf')
        best_move = None
        for move in get_all_moves(current_board, WHITE):
            score = alpha_beta_mm(move, depth - 1,alpha,beta, True)[0]
            min_score = min(min_score, score)
            if min_score == score:
                best_move = move
            beta = min(beta,score)
            if beta <= alpha:
                break
        return min_score, best_move


def get_all_moves(board,color):
    moves = []
    no_jump = jump = False
    all_pieces = board.get_all_pieces(color)

    for piece in all_pieces:
        valid_moves = board.get_possible_moves(piece)
        for move,skip in valid_moves.items():
            if skip:
                jump = True
            else:
                no_jump = True

    if jump == no_jump:
        for piece in all_pieces:
            valid_moves = board.get_possible_moves(piece)
            for move, skip in valid_moves.items():
                if skip:
                    temp_board = deepcopy(board)
                    temp_piece = temp_board.get_piece(piece.row, piece.column)
                    new_board = simulate_moves(temp_piece, move, temp_board, skip)
                    moves.append(new_board)

    else:
        for piece in all_pieces:
            valid_moves = board.get_possible_moves(piece)

            for move, skip in valid_moves.items():
                # draw_moves(game, board, piece)
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.column)
                new_board = simulate_moves(temp_piece, move, temp_board, skip)
                moves.append(new_board)



    return moves

def simulate_moves(piece,move,board,pieces_skipped):
    board.move(move[0], move[1],piece)
    if pieces_skipped:
        board.remove(pieces_skipped)
    return board

def draw_moves(game, board, piece):
    possible_moves = board.get_possible_moves(piece)
    board.draw_board(game.window)
    pygame.draw.circle(game.window, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_possible_moves(possible_moves.keys())
    pygame.display.update()



