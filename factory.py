from random import randint
from typing import List

from board import Board

def sorted_pieces(dimension: int) -> List[str]:
    num_pieces = dimension * dimension
    pieces = []
    for p in range(num_pieces - 1):
        pieces.append(str(p + 1))
    pieces.append("#")
    return pieces


def random_pieces(dimension: int, random_movementes: int, count: int) -> List[Board]:
    pieces = sorted_pieces(dimension)
    boards = []
    for _ in range(count):
        tabu_boards = []
        board = Board(dimension, pieces)
        for _ in range(random_movementes):
            future_boards = [b for b in board.get_future_boards() if b not in tabu_boards]
            index = randint(0, len(future_boards) - 1)
            next_board = future_boards[index]
            tabu_boards.append(next_board)
            board = next_board
        boards.append(board)
    return boards