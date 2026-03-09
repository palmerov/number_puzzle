import re
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from board import Board
from board_io import load_board_list_from_file
from constants import Constants, max_g, max_h1, max_h2, max_h3, max_h4, max_h5
from factory import sorted_pieces
from sli_puzz import bfs_puzzle

BOARDS_DIR = SCRIPT_DIR / "boards"
RESULTS_DIR = SCRIPT_DIR / "results"


def build_constants(dimension: int) -> Constants:
    return Constants(
        weight_g=0.1,
        weight_h1=0.37,
        weight_h2=0.26,
        weight_h3=0.01,
        weight_h4=0.2,
        weight_h5=0.06,
        max_g=max_g(dimension),
        max_h1=max_h1(dimension),
        max_h2=max_h2(dimension),
        max_h3=max_h3(dimension),
        max_h4=max_h4(dimension),
        max_h5=max_h5(dimension),
        save_statistics=False,
    )


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    if not BOARDS_DIR.exists():
        print(f"Folder {BOARDS_DIR} does not exist")
        return

    board_files = sorted(BOARDS_DIR.glob("*.txt"))
    if not board_files:
        print(f"No .txt files in {BOARDS_DIR}")
        return

    for filepath in board_files:
        filename = filepath.name
        out_path = RESULTS_DIR / filename
        if not filename.endswith(".txt"):
            continue

        try:
            dimension, initial_boards = load_board_list_from_file(filepath)
        except (ValueError, FileNotFoundError) as e:
            print(f"[{filename}] Error loading: {e}")
            continue

        if dimension < 3 or dimension > 10:
            print(f"[{filename}] Dimension {dimension} not supported (3-10). Skipping.")
            continue

        goal_board = Board(dimension, sorted_pieces(dimension))
        constants = build_constants(dimension)

        # Parse random steps from filename (e.g. b_3x3_20boards_20steps.txt -> 20)
        match = re.search(r"(\d+)random_steps", filename, re.IGNORECASE)
        random_steps = int(match.group(1)) if match else "N/A"
        boards_count = len(initial_boards)

        resolved_times_ms: list[int] = []
        resolved_solution_steps_list: list[int] = []
        times_ms: list[int] = []
        solution_steps_list: list[int] = []

        sections = []
        for idx, initial in enumerate(initial_boards):
            t0 = time.perf_counter()
            stop = lambda: (time.perf_counter() - t0) * 1000 > 150000  # 5 minutes
            try:
                steps = bfs_puzzle(
                    constants,
                    initial,
                    goal_board,
                    deepth_improve_threshold=6,
                    max_open_size=5000,
                    max_closed_size=10000,
                    stop=stop,
                )
            except MemoryError:
                elapsed_ms = int((time.perf_counter() - t0) * 1000)
                times_ms.append(elapsed_ms)
                solution_steps_list.append(0)
                print(
                    f"[{filename}] Board {idx + 1}: Memory error. (Time (ms): {elapsed_ms})"
                )
                steps = None
            else:
                elapsed_ms = int((time.perf_counter() - t0) * 1000)

            if steps is not None and len(steps) > 0:
                num_steps = len(steps) - 1
                times_ms.append(elapsed_ms)
                resolved_times_ms.append(elapsed_ms)
                resolved_solution_steps_list.append(num_steps)
                solution_steps_list.append(num_steps)
                print(f"-- {filename} / Board {idx + 1} --")
                print(initial)
                print(f"Solution Steps: {num_steps}")
                print(f"Time (ms): {elapsed_ms}")
                print(f"Output: {out_path}")
                print()

                # Each section: ##############, Board N:, board, Time:, Steps:, steps
                sections.append("##############")
                sections.append(f"Board {idx + 1}:")
                sections.append(initial.__str__())
                sections.append(f"Time (ms): {elapsed_ms}")
                sections.append(f"Solution Steps: {num_steps}:")

                steps_labels = []
                for b in steps:
                    steps_labels.append(b.label)
                sections.append(", ".join(steps_labels)[2:])
            else:
                times_ms.append(-1)
                solution_steps_list.append(-1)  # no solution
                print(
                    f"[{filename}] Board {idx + 1}: No solution found. (Time: {elapsed_ms})"
                )
                sections.append("##############")
                sections.append(f"Board {idx + 1}:")
                sections.append(initial.__str__())
                sections.append(f"Time (ms): {elapsed_ms}")
                sections.append("Solution Steps: -1:")
                sections.append("-")

        mean_time = (
            round(sum(resolved_times_ms) / len(resolved_times_ms), 2)
            if resolved_times_ms and len(resolved_times_ms) > 0
            else 0
        )
        mean_solution_steps = (
            round(
                sum(resolved_solution_steps_list) / len(resolved_solution_steps_list), 2
            )
            if resolved_solution_steps_list
            else 0
        )
        header_lines = [
            "--------------------------------",
            f"Dimension: {dimension}",
            f"Random Steps: {random_steps}",
            f"Boards Count: {boards_count}",
            f"Times (ms): {times_ms}",
            f"Solution Steps: {solution_steps_list}",
            f"Mean Time (ms): {mean_time}",
            f"Mean Solution Steps: {mean_solution_steps}",
            "--------------------------------\n",
            "",
        ]
        content = "\n".join(header_lines) + "\n".join(sections)
        out_path.write_text(content + "\n", encoding="utf-8")
        print(f"Written: {out_path}\n")


if __name__ == "__main__":
    main()
