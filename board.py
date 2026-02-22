from typing import List, Tuple


class Board:
    def __init__(
        self, dimension: int, pieces: List[str] = None, a_board: List[List[str]] = None
    ):
        self.dimension = dimension
        self.value = 0.0
        if pieces is not None:
            self.board = []
            for i in range(dimension):
                self.board.append([pieces[i * dimension + j] for j in range(dimension)])
        elif a_board is not None:
            self.board = a_board
        else:
            raise ValueError("Either pieces or board must be provided")

    def get_piece(self, row: int, col: int) -> str:
        return self.board[row][col]

    def set_piece(self, row: int, col: int, piece: str):
        self.board[row][col] = piece

    def get_dimension(self) -> int:
        return self.dimension

    def get_board(self) -> List[List[str]]:
        return self.board

    def slide_piece(self, row: int, col: int) -> bool:
        empty_row, empty_col = self.get_empty_position()
        piece = self.get_piece(row, col)
        if row == empty_row:
            if abs(col - empty_col) == 1:
                self.set_piece(empty_row, empty_col, piece)
                self.set_piece(row, col, "#")
                return True
        elif col == empty_col:
            if abs(row - empty_row) == 1:
                self.set_piece(empty_row, empty_col, piece)
                self.set_piece(row, col, "#")
                return True
        return False

    def get_free_pieces_positions(self) -> List[Tuple[int, int]]:
        positions: List[Tuple[int, int]] = []
        empty_row, empty_col = self.get_empty_position()
        if empty_row > 0:
            positions.append((empty_row - 1, empty_col))
        if empty_row < self.dimension - 1:
            positions.append((empty_row + 1, empty_col))
        if empty_col > 0:
            positions.append((empty_row, empty_col - 1))
        if empty_col < self.dimension - 1:
            positions.append((empty_row, empty_col + 1))
        return positions

    def get_future_boards(self) -> List["Board"]:
        future_boards = []
        for position in self.get_free_pieces_positions():
            new_board = Board(
                self.dimension, None, [[p for p in row] for row in self.board]
            )
            new_board.slide_piece(position[0], position[1])
            future_boards.append(new_board)
        return future_boards

    def get_empty_position(self) -> (int, int):
        return self.get_piece_position("#")

    def get_piece_position(self, piece: str) -> (int, int):
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.get_piece(i, j) == piece:
                    return (i, j)
        raise ValueError("No piece position found")

    def __eq__(self, board: "Board") -> bool:
        if self.dimension != board.dimension:
            return False
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.get_piece(i, j) != board.get_piece(i, j):
                    return False
        return True

    def __str__(self) -> str:
        lines = []
        spaces_count = len(str((self.dimension * self.dimension) - 1)) + 1
        lines.append("." + "-" * (self.dimension * spaces_count + 1) + ".")
        for line in self.board:
            line_str = "\n| "
            for piece in line:
                line_str += piece + " " * (spaces_count - len(piece))
            lines.append(line_str + "|")
        lines.append("\n'" + "-" * (self.dimension * spaces_count + 1) + "'")
        return "".join(lines)

    def __hash__(self) -> int:
        return hash(self.askey())
    
    def askey(self) -> str:
        return ",".join([str(p) for row in self.board for p in row])
