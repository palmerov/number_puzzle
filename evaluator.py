from typing import List
from board import Board
from constants import Constants

def evaluate_board(
    board: Board, target_board: Board, deep: int, constants: Constants
) -> int:
    if board == target_board:
        return 0
    
    v_g = g_depth(deep, board)
    v_h1 = h1_distances(board, target_board)
    v_h2 = h2_bad_pieces(board, target_board)
    v_h3 = h3_distance_from_blank(board, target_board)
    v_h4 = h4_linear_conflict(board, target_board)
    v_h5 = h5_corner_conflict(board, target_board)
    
    if constants.SAVE_STATISTICS:
        if v_g > constants.LAST_MAX_G:
            constants.LAST_MAX_G = v_g
        if v_h1 > constants.LAST_MAX_H1:
            constants.LAST_MAX_H1 = v_h1
        if v_h2 > constants.LAST_MAX_H2:
            constants.LAST_MAX_H2 = v_h2
        if v_h3 > constants.LAST_MAX_H3:
            constants.LAST_MAX_H3 = v_h3
        if v_h4 > constants.LAST_MAX_H4:
            constants.LAST_MAX_H4 = v_h4
        if v_h5 > constants.LAST_MAX_H5:
            constants.LAST_MAX_H5 = v_h5
    
    score = 0.0
    score += constants.WEIGHT_G * v_g / constants.MAX_G
    score += constants.WEIGHT_H1 * v_h1 / constants.MAX_H1
    score += constants.WEIGHT_H2 * v_h2 / constants.MAX_H2
    score += constants.WEIGHT_H3 * v_h3 / constants.MAX_H3
    score += constants.WEIGHT_H4 * v_h4 / constants.MAX_H4
    score += constants.WEIGHT_H5 * v_h5 / constants.MAX_H5
    return score


# g_deepth is the depth of the board from the root node
def g_depth(depth: int, board: Board) -> float:
    return float(depth)


# h1_distances is the sum of the distances of the pieces from their target positions
def h1_distances(board: Board, target_board: Board) -> int:
    total = 0.0
    for i in range(board.dimension):
        for j in range(board.dimension):
            cur_piece = board.get_piece(i, j)
            tar_pos = target_board.get_piece_position(cur_piece)
            total += abs(i - tar_pos[0]) + abs(j - tar_pos[1])
    final = total / (board.dimension * board.dimension)
    return final

# h2_bad_pieces is the number of pieces that are not in their target positions
def h2_bad_pieces(board: Board, target_board: Board) -> int:
    total = 0.0
    for i in range(board.dimension):
        for j in range(board.dimension):
            cur_piece = board.get_piece(i, j)
            if cur_piece == "#":
                continue
            tar_piece = target_board.get_piece(i, j)
            if cur_piece != tar_piece:
                total += 1
    return total


# h3_distance_from_blank is the sum of the distances of the pieces from the blank position
def h3_distance_from_blank(board: Board, target_board: Board) -> float:
    total = 0.0
    bad_count = 0
    cur_blank_pos = board.get_piece_position("#")
    for i in range(board.dimension):
        for j in range(board.dimension):
            cur_piece = board.get_piece(i, j)
            if cur_piece != target_board.get_piece(i, j):
                bad_count += 1
                total += abs(i - cur_blank_pos[0]) + abs(j - cur_blank_pos[1])
    return total / bad_count


# h4_linear_conflict is the number of linear conflicts
def h4_linear_conflict(board: Board, target_board: Board) -> float:
    conflicts = 0
    for cur_col in range(board.dimension):
        ok_tar_rows = []
        for cur_row in range(board.dimension):
            cur_piece = board.get_piece(cur_row, cur_col)
            if cur_piece == "#":
                continue
            tar_row, tar_col = target_board.get_piece_position(cur_piece)
            if cur_col == tar_col and cur_row != tar_row:
                for oth_tar_row in ok_tar_rows:
                    if oth_tar_row > tar_row:
                        conflicts += 1
                ok_tar_rows.append(tar_row)
    for cur_row in range(board.dimension):
        ok_tar_cols = []
        for cur_col in range(board.dimension):
            cur_piece = board.get_piece(cur_row, cur_col)
            if cur_piece == "#":
                continue
            tar_row, tar_col = target_board.get_piece_position(cur_piece)
            if cur_row == tar_row and cur_col != tar_col:
                for oth_tar_col in ok_tar_cols:
                    if oth_tar_col > tar_col:
                        conflicts += 1
                ok_tar_cols.append(tar_col)
    return conflicts


# h5_corner_conflict is the number of corner conflicts
def h5_corner_conflict(board: Board, target_board: Board) -> float:
    conflicts = 0
    lim = board.dimension - 1
    if (
        board.get_piece(0, 0) == target_board.get_piece(0, 0)
        and board.get_piece(0, 0) != "#"
    ):
        if (
            board.get_piece(0, 1) != target_board.get_piece(0, 1)
            and board.get_piece(0, 1) != "#"
        ):
            conflicts += 1
        if (
            board.get_piece(1, 0) != target_board.get_piece(1, 0)
            and board.get_piece(1, 0) != "#"
        ):
            conflicts += 1
    if (
        board.get_piece(0, lim) == target_board.get_piece(0, lim)
        and board.get_piece(0, lim) != "#"
    ):
        if (
            board.get_piece(0, lim - 1) != target_board.get_piece(0, lim - 1)
            and board.get_piece(0, lim - 1) != "#"
        ):
            conflicts += 1
        if (
            board.get_piece(1, lim) != target_board.get_piece(1, lim)
            and board.get_piece(1, lim) != "#"
        ):
            conflicts += 1
    if (
        board.get_piece(lim, 0) == target_board.get_piece(lim, 0)
        and board.get_piece(lim, 0) != "#"
    ):
        if (
            board.get_piece(lim - 1, 0) != target_board.get_piece(lim - 1, 0)
            and board.get_piece(lim - 1, 0) != "#"
        ):
            conflicts += 1
        if (
            board.get_piece(lim, 1) != target_board.get_piece(lim, 1)
            and board.get_piece(lim, 1) != "#"
        ):
            conflicts += 1
    if (
        board.get_piece(lim, lim) == target_board.get_piece(lim, lim)
        and board.get_piece(lim, lim) != "#"
    ):
        if (
            board.get_piece(lim - 1, lim) != target_board.get_piece(lim - 1, lim)
            and board.get_piece(lim - 1, lim) != "#"
        ):
            conflicts += 1
        if (
            board.get_piece(lim, lim - 1) != target_board.get_piece(lim, lim - 1)
            and board.get_piece(lim, lim - 1) != "#"
        ):
            conflicts += 1
    return conflicts