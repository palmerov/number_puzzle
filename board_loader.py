"""
Cargador de tableros desde archivo.

Formato del archivo:
- 1ª línea: dimensión n (número entero).
- Siguientes n líneas: tablero de entrada (números separados por comas, 0 = espacio).
- Siguientes n líneas: tablero meta (mismo formato).
Los números van de 0 a n²-1.
"""

from pathlib import Path
from typing import Tuple, Union

from board import Board


def _parse_board_line(line: str) -> list:
    """Convierte una línea 'a,b,c' en lista de cadenas; 0 se convierte en '#' (espacio)."""
    parts = [p.strip() for p in line.split(",")]
    return parts


def load_boards_from_file(filepath: Union[str, Path]) -> Tuple[int, Board, Board]:
    """
    Lee un archivo de tableros y devuelve (dimensión, tablero_inicial, tablero_meta).

    Raises:
        ValueError: si el archivo tiene formato inválido o dimensiones incorrectas.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo: {path}")

    lines = path.read_text(encoding="utf-8").strip().splitlines()
    if not lines:
        raise ValueError("El archivo está vacío")

    # Dimensión
    try:
        n = int(lines[0].strip())
    except ValueError as exc:
        raise ValueError(
            f"La primera línea debe ser un número (dimensión): {lines[0]!r}"
        ) from exc

    if n < 2:
        raise ValueError(f"La dimensión debe ser al menos 2, se obtuvo {n}")

    required_lines = 1 + n + n
    if len(lines) < required_lines:
        raise ValueError(
            f"Se esperaban {required_lines} líneas (1 + {n} + {n}), hay {len(lines)}"
        )

    # Tablero de entrada (líneas 1..n)
    initial_rows = []
    for i in range(1, 1 + n):
        row = _parse_board_line(lines[i])
        if len(row) != n:
            raise ValueError(
                f"Tablero inicial, línea {i + 1}: se esperaban {n} valores separados por coma"
            )
        initial_rows.append(row)

    # Tablero meta (líneas n+1 .. 2n)
    goal_rows = []
    for i in range(1 + n, 1 + n + n):
        row = _parse_board_line(lines[i])
        if len(row) != n:
            raise ValueError(
                f"Tablero meta, línea {i + 1}: se esperaban {n} valores separados por coma"
            )
        goal_rows.append(row)

    initial_board = Board(n, None, initial_rows)
    goal_board = Board(n, None, goal_rows)

    return n, initial_board, goal_board
