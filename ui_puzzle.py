"""
Interfaz de usuario para el sliding puzzle.

Lee tablero de entrada y tablero meta desde un archivo, ejecuta el solver
y muestra la solución (secuencia de tableros).

Requisito: Python 3.9+ (el módulo sli_puzz lo necesita).

Uso:
    python ui_puzzle.py <ruta_archivo>
    python ui_puzzle.py   # pide la ruta por teclado
"""

import sys

if sys.version_info < (3, 9):
    print("Se requiere Python 3.9 o superior (el solver usa anotaciones que lo requieren).")
    sys.exit(1)

from board_loader import load_boards_from_file
from evaluator import evaluate_board
from sli_puzz import bfs_puzzle


def main() -> None:
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
    else:
        filepath = input("Ruta del archivo de tableros: ").strip()
        if not filepath:
            print("Debe indicar un archivo.")
            sys.exit(1)

    try:
        dimension, initial_board, goal_board = load_boards_from_file(filepath)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
    except ValueError as e:
        print(f"Error en el archivo: {e}")
        sys.exit(1)

    print("--- Tablero de entrada ---")
    print(initial_board)
    print("\n--- Tablero meta ---")
    print(goal_board)
    print(f"\nDimensión: {dimension}")
    print(f"Valor inicial (heurística): {evaluate_board(initial_board, goal_board, 0)}")
    print("\nBuscando solución...\n")

    steps = bfs_puzzle(initial_board, goal_board, deepth_improve_threshold=15)

    if steps is not None and len(steps) > 0:
        print(f"--- Solución encontrada ({len(steps) - 1} movimientos) ---")
        for i, board in enumerate(steps):
            print(f"Paso {i}:")
            print(board)
            print()
    else:
        print("No se encontró solución.")


if __name__ == "__main__":
    main()
