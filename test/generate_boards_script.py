import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from board_io import write_boards_to_file
from factory import random_pieces

def main():
    boards_dir = SCRIPT_DIR / "boards"
    boards_dir.mkdir(parents=True, exist_ok=True)
    for DIMENSION in range(3, 9):
        for RANDOM_STEPS in [20, 30, 50]:
            BOARDS_COUNT = 100
            filename = f"b_{DIMENSION}x{DIMENSION}_{BOARDS_COUNT}boards_{RANDOM_STEPS}random_steps.txt"
            filepath = boards_dir / filename
            boards = random_pieces(DIMENSION, RANDOM_STEPS, BOARDS_COUNT)
            write_boards_to_file(filepath=filepath, dimension=DIMENSION, boards=boards)

if __name__ == "__main__":
    main()