from typing import List
from board import Board
from constants import Constants, max_g, max_h1, max_h2, max_h3, max_h4, max_h5
from evaluator import evaluate_board
from factory import random_pieces, sorted_pieces
from node import (
    LinkedList,
    Node,
    SortedLinkedList,
    NSTAT_LIMBO,
    NSTAT_OPEN,
    NSTAT_CLOSED,
)


def get_path_to_root(node: Node) -> List[Board]:
    path = []
    while node is not None:
        path.append(node.board)
        node = node.parent
    path.reverse()
    return path


def is_open(node: Node) -> bool:
    return node.status == NSTAT_OPEN


def is_closed(node: Node) -> bool:
    return node.status == NSTAT_CLOSED


def remove_from_open(node: Node, open: SortedLinkedList):
    open.remove(node)
    node.status = NSTAT_LIMBO


def open_node(
    node: Node,
    open: SortedLinkedList,
    closed: LinkedList,
    explored: dict[str, Node],
    max_open_size: int,
    max_closed_size: int,
):
    node.status = NSTAT_OPEN
    explored[node.board.askey()] = node
    if node.children is not None:
        for child in node.children:
            child.parent = None
    node.children = None
    open.insert(node)
    if open.length > max_open_size:
        last = open.pop_end()
        close_node(last, closed, explored, max_closed_size)


def close_node(
    node: Node, closed: LinkedList, explored: dict[str, Node], max_closed_size: int
):
    closed.set_next(node)
    node.status = NSTAT_CLOSED
    if closed.length > max_closed_size:
        closed.pop_start()


def remove_from_closed(
    node: Node, open: SortedLinkedList, closed: LinkedList, explored: dict[str, Node]
):
    try:
        del explored[node.board.askey()]
    except KeyError:
        pass
    if node.status == NSTAT_CLOSED:
        closed.remove(node)
    elif node.status == NSTAT_OPEN:
        open.remove(node)
    node.status = NSTAT_LIMBO
    node.parent = None
    children = node.children
    if children is None:
        return
    for child in children:
        remove_from_closed(child, open, closed, explored)
    node.children = None


def evaluate_current(node: Node, target_board: Board, constants: Constants) -> float:
    value = evaluate_board(node.board, target_board, node.depth, constants)
    node.board.value = value
    return value


def derivate_boards(node: Node) -> List[Node]:
    future_boards = node.board.get_future_boards()
    children = []
    for future_board in future_boards:
        if node.parent is None or future_board != node.parent.board:
            children.append(Node(future_board, node))
    node.children = children
    return children


def bfs_puzzle(
    constants: Constants,
    initial: Board,
    target: Board,
    deepth_improve_threshold: int = 5,
    max_open_size: int = 500,
    max_closed_size: int = 1000,
) -> List[Board]:
    open = SortedLinkedList(None)
    closed = LinkedList(None)
    explored = dict[str, Node]()
    root = Node(initial, None)
    target.create_positions_map()

    evaluate_current(root, target, constants)
    open_node(root, open, closed, explored, max_open_size, max_closed_size)

    while not open.is_empty():
        current = open.pop_start()

        if current.board == target:
            return get_path_to_root(current)

        children = derivate_boards(current)
        for child in children:
            clone = explored.get(child.board.askey(), None)
            if clone is not None:
                if is_open(clone):
                    if child.depth < clone.depth - deepth_improve_threshold:
                        remove_from_open(clone, open)
                        evaluate_current(child, target, constants)
                        open_node(
                            child,
                            open,
                            closed,
                            explored,
                            max_open_size,
                            max_closed_size,
                        )
                elif is_closed(clone):
                    if child.depth < clone.depth - deepth_improve_threshold:
                        remove_from_closed(clone, open, closed, explored)
                        evaluate_current(child, target, constants)
                        open_node(
                            child,
                            open,
                            closed,
                            explored,
                            max_open_size,
                            max_closed_size,
                        )
            else:
                evaluate_current(child, target, constants)
                open_node(child, open, closed, explored, max_open_size, max_closed_size)
        close_node(current, closed, explored, max_closed_size)


DIMENSION = 6
target_board = Board(DIMENSION, sorted_pieces(DIMENSION))

constants = Constants(
    weight_g=0.1,
    weight_h1=0.37,
    weight_h2=0.26,
    weight_h3=0.01,
    weight_h4=0.2,
    weight_h5=0.06,
    max_g=max_g(DIMENSION),
    max_h1=max_h1(DIMENSION),
    max_h2=max_h2(DIMENSION),
    max_h3=max_h3(DIMENSION),
    max_h4=max_h4(DIMENSION),
    max_h5=max_h5(DIMENSION),
    save_statistics=True,
)


random_boards = random_pieces(DIMENSION, 100, 20)
max_steps = 0

for index, random_board in enumerate(random_boards):
    print(
        f"---- Board: {index + 1}/{len(random_boards)}, Value: {evaluate_board(random_board, target_board, 0, constants)} ----"
    )
    print(random_board)

    try:
        steps = bfs_puzzle(constants, random_board, target_board, 6, 3000, 8000)
    except MemoryError:
        print(f"Memory error: {index + 1}/{len(random_boards)}")
        print("\n")
        continue
    if steps is not None and len(steps) > 0:
        print(f"Solved: {index + 1}/{len(random_boards)}: {len(steps)} steps")
        if len(steps) > max_steps:
            max_steps = len(steps)
        print(f"-- Statistics for dimension: {DIMENSION}")
        print(constants.get_statistics())
    else:
        print(f"Not solved: {index + 1}/{len(random_boards)}: {len(steps)} steps")
    print("\n")

print(f"Max steps: {max_steps}")
print("----------------END----------------")
