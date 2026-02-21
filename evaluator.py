from board import Board
from factory import sorted_pieces

P_G = 0.05
P_H1 = 0.6
P_H2 = 0.25
P_H3 = 0.1
P_H4 = 0.1
P_H5 = 0.1

def evaluate_board(board: Board, target_board: Board, deep: int) -> int:
    if board == target_board:
        return 0
    score = 0.0
    score += P_G * g_depth(deep, board)
    score += P_H1 * h1_distances(board, target_board)
    score += P_H2 * h2_bad_pieces(board, target_board)
    score += P_H3 * h3_distance_from_blank(board, target_board)
    # score += P_H4 * h4_linear_conflict(board, target_board)
    # score += P_H5 * h5_corner_conflict(board, target_board)
    return score


# g_deepth is the depth of the board from the root node
def g_depth(depth: int, board: Board) -> float:
    return float(depth) / max_g(board.dimension)


# h1_distances is the sum of the distances of the pieces from their target positions
def h1_distances(board: Board, target_board: Board) -> int:
    max = max_h1(board.dimension)
    total = 0.0
    for i in range(board.dimension):
        for j in range(board.dimension):
            cur_piece = board.get_piece(i, j)
            tar_pos = target_board.get_piece_position(cur_piece)
            total += abs(i - tar_pos[0]) + abs(j - tar_pos[1])
    return total / (board.dimension * board.dimension) / max


# h2_bad_pieces is the number of pieces that are not in their target positions
def h2_bad_pieces(board: Board, target_board: Board) -> int:
    max = max_h2(board.dimension)
    total = 0.0
    for i in range(board.dimension):
        for j in range(board.dimension):
            cur_piece = board.get_piece(i, j)
            tar_piece = target_board.get_piece(i, j)
            if cur_piece != tar_piece:
                total += 1
    return total / max


# h3_distance_from_blank is the sum of the distances of the pieces from the blank position
def h3_distance_from_blank(board: Board, target_board: Board) -> float:
    max = max_h3(board.dimension)
    total = 0.0
    bad_count = 0
    cur_blank_pos = board.get_empty_position()
    for i in range(board.dimension):
        for j in range(board.dimension):
            cur_piece = board.get_piece(i, j)
            if cur_piece != target_board.get_piece(i, j):
                bad_count += 1
                total += abs(i - cur_blank_pos[0]) + abs(j - cur_blank_pos[1])
    return total / bad_count / max


# h4_linear_conflict is the number of linear conflicts
def h4_linear_conflict(board: Board, target_board: Board) -> float:
    conflicts = 0
    for cur_col in range(board.dimension):
        ok_tar_rows = []
        for cur_row in range(board.dimension):
            cur_piece = board.get_piece(cur_row, cur_col)
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
            tar_row, tar_col = target_board.get_piece_position(cur_piece)
            if cur_row == tar_row and cur_col != tar_col:
                for oth_tar_col in ok_tar_cols:
                    if oth_tar_col > tar_col:
                        conflicts += 1
                ok_tar_cols.append(tar_col)
    return conflicts / max_h4(board.dimension)


# h5_corner_conflict is the number of corner conflicts
def h5_corner_conflict(board: Board, target_board: Board) -> float:
    conflicts = 0
    lim = board.dimension - 1
    max = max_h5(board.dimension)
    if board.get_piece(0, 0) == target_board.get_piece(0, 0):
        if board.get_piece(0, 1) != target_board.get_piece(0, 1):
            conflicts += 1
        if board.get_piece(1, 0) != target_board.get_piece(1, 0):
            conflicts += 1
    if board.get_piece(0, lim) == target_board.get_piece(0, lim):
        if board.get_piece(0, lim - 1) != target_board.get_piece(0, lim - 1):
            conflicts += 1
        if board.get_piece(1, lim) != target_board.get_piece(1, lim):
            conflicts += 1
    if board.get_piece(lim, 0) == target_board.get_piece(lim, 0):
        if board.get_piece(lim - 1, 0) != target_board.get_piece(lim - 1, 0):
            conflicts += 1
        if board.get_piece(lim, 1) != target_board.get_piece(lim, 1):
            conflicts += 1
    if board.get_piece(lim, lim) == target_board.get_piece(lim, lim):
        if board.get_piece(lim - 1, lim) != target_board.get_piece(lim - 1, lim):
            conflicts += 1
        if board.get_piece(lim, lim - 1) != target_board.get_piece(lim, lim - 1):
            conflicts += 1
    return conflicts / max


# max_g is the maximum value of g
def max_g(dimension: int) -> float:
    if dimension == 3:
        return 40
    if dimension == 4:
        return 42
    if dimension == 5:
        return 44
    if dimension == 6:
        return 46
    if dimension == 7:
        return 48
    if dimension == 8:
        return 50
    if dimension == 9:
        return 52
    if dimension == 10:
        return 54


# max_h1 is the maximum value of h1
def max_h1(dimension: int) -> float:
    if dimension == 3:
        return 4
    if dimension == 4:
        return 16
    if dimension == 5:
        return 25
    if dimension == 6:
        return 36
    if dimension == 7:
        return 49
    if dimension == 8:
        return 64
    if dimension == 9:
        return 81
    if dimension == 10:
        return 100


# max_h2 is the maximum value of h2
def max_h2(dimension: int) -> float:
    if dimension == 3:
        return 9
    if dimension == 4:
        return 16
    if dimension == 5:
        return 25
    if dimension == 6:
        return 36
    if dimension == 7:
        return 49
    if dimension == 8:
        return 64
    if dimension == 9:
        return 81
    if dimension == 10:
        return 100

# max_h3 is the maximum value of h3
def max_h3(dimension: int) -> float:
    if dimension == 3:
        return 4
    if dimension == 4:
        return 16
    if dimension == 5:
        return 25
    if dimension == 6:
        return 36
    if dimension == 7:
        return 49
    if dimension == 8:
        return 64
    if dimension == 9:
        return 81
    if dimension == 10:
        return 100


# max_h4 is the maximum value of h4
def max_h4(dimension: int) -> float:
    if dimension == 3:
        return 4
    if dimension == 4:
        return 16
    if dimension == 5:
        return 25
    if dimension == 6:
        return 36
    if dimension == 7:
        return 49
    if dimension == 8:
        return 64
    if dimension == 9:
        return 81
    if dimension == 10:
        return 100


# pon_h4 is the penalty value of h4
def max_h5(dimension: int) -> float:
    if dimension == 3:
        return 8
    if dimension == 4:
        return 16
    if dimension == 5:
        return 25
    if dimension == 6:
        return 36
    if dimension == 7:
        return 49
    if dimension == 8:
        return 64
    if dimension == 9:
        return 81
    if dimension == 10:
        return 100


# pon_g is the penalty value of g
def pon_g(dimension: int) -> float:
    if dimension == 3:
        return 0.2
    if dimension == 4:
        return 0.2
    if dimension == 5:
        return 0.2
    if dimension == 6:
        return 0.2
    if dimension == 7:
        return 0.2
    if dimension == 8:
        return 0.2
    if dimension == 9:
        return 0.2
    if dimension == 10:
        return 0.2

# pon_h1 is the penalty value of h1
def pon_h1(dimension: int) -> float:
    if dimension == 3:
        return 0.3
    if dimension == 4:
        return 0.3
    if dimension == 5:
        return 0.3
    if dimension == 6:
        return 0.3
    if dimension == 7:
        return 0.3
    if dimension == 8:
        return 0.3
    if dimension == 9:
        return 0.3
    if dimension == 10:
        return 0.3


# pon_h2 is the penalty value of h2
def pon_h2(dimension: int) -> float:
    if dimension == 3:
        return 0.1
    if dimension == 4:
        return 0.1
    if dimension == 5:
        return 0.1
    if dimension == 6:
        return 0.1
    if dimension == 7:
        return 0.1
    if dimension == 8:
        return 0.1
    if dimension == 9:
        return 0.1
    if dimension == 10:
        return 0.1


# pon_h3 is the penalty value of h3
def pon_h3(dimension: int) -> float:
    if dimension == 3:
        return 0.002


# pon_h3 is the penalty value of h3
def pon_h4(dimension: int) -> float:
    if dimension == 3:
        return 0.4
    if dimension == 4:
        return 0.4
    if dimension == 5:
        return 0.4
    if dimension == 6:
        return 0.4
    if dimension == 7:
        return 0.4
    if dimension == 8:
        return 0.4
    if dimension == 9:
        return 0.4
    if dimension == 10:
        return 0.4


# max_h5 is the maximum value of h5
def pon_h5(dimension: int) -> float:
    if dimension == 3:
        return 0.05
    if dimension == 4:
        return 0.05
    if dimension == 5:
        return 0.05
    if dimension == 6:
        return 0.05
    if dimension == 7:
        return 0.05
    if dimension == 8:
        return 0.05
    if dimension == 9:
        return 0.05
    if dimension == 10:
        return 0.05