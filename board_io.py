from pathlib import Path
from typing import List, Tuple, Union
from board import Board


def _parse_board_line(line: str) -> list:
    parts = [p.strip() for p in line.split(",")]
    return parts


def load_boards_from_file(filepath: Union[str, Path]) -> Tuple[int, Board, Board]:
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    lines = path.read_text(encoding="utf-8").strip().splitlines()
    if not lines:
        raise ValueError("File is empty")

    # Dimensión
    try:
        n = int(lines[0].strip())
    except ValueError as exc:
        raise ValueError(
            f"The first line must be a number (dimension): {lines[0]!r}"
        ) from exc

    if n < 2:
        raise ValueError(f"The dimension must be at least 2, got {n}")

    required_lines = 1 + n + n
    if len(lines) < required_lines:
        raise ValueError(
            f"Expected {required_lines} lines (1 + {n} + {n}), got {len(lines)}"
        )

    # Initial board (lines 1..n)
    initial_rows = []
    for i in range(1, 1 + n):
        row = _parse_board_line(lines[i])
        if len(row) != n:
            raise ValueError(
                f"Initial board, line {i + 1}: expected {n} values separated by comma"
            )
        initial_rows.append(row)

    # Goal board (lines n+1 .. 2n)
    goal_rows = []
    for i in range(1 + n, 1 + n + n):
        row = _parse_board_line(lines[i])
        if len(row) != n:
            raise ValueError(
                f"Goal board, line {i + 1}: expected {n} values separated by comma"
            )
        goal_rows.append(row)

    initial_board = Board(n, None, initial_rows)
    goal_board = Board(n, None, goal_rows)

    return n, initial_board, goal_board


def load_board_list_from_file(filepath: Union[str, Path]) -> Tuple[int, List[Board]]:
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    lines = path.read_text(encoding="utf-8").strip().splitlines()
    if not lines:
        raise ValueError("File is empty")

    try:
        n = int(lines[0].strip())
    except ValueError as exc:
        raise ValueError(
            f"The first line must be a number (dimension): {lines[0]!r}"
        ) from exc

    if n < 2:
        raise ValueError(f"The dimension must be at least 2, got {n}")

    remainder = len(lines) - 1
    if remainder % n != 0:
        raise ValueError(
            f"After dimension line expected a multiple of {n} lines, got {remainder}"
        )
    num_boards = remainder // n
    boards = []
    for b in range(num_boards):
        start = 1 + b * n
        rows = []
        for i in range(start, start + n):
            row = _parse_board_line(lines[i])
            if len(row) != n:
                raise ValueError(
                    f"Board {b + 1}, line {i + 1}: expected {n} values separated by comma"
                )
            rows.append(row)
        boards.append(Board(n, None, rows))
    return n, boards


def write_boards_to_file(
    filepath: str, dimension: int, boards: List[Board]
) -> None:
    path = Path(filepath)
    lines = [str(dimension)]
    for board in boards:
        if board.dimension != dimension:
            raise ValueError(
                f"Board dimension {board.dimension} does not match given dimension {dimension}"
            )
        for row in board.get_board():
            lines.append(",".join(str(p) for p in row))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
