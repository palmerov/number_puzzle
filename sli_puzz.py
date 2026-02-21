from typing import List
from board import Board
from evaluator import evaluate_board
from factory import random_pieces, sorted_pieces
from node import LinkedList, Node, SortedLinkedList, NSTAT_LIMBO, NSTAT_OPEN, NSTAT_CLOSED


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


def open_node(node: Node, open: SortedLinkedList, explored: dict[Board, Node]):
    node.status = NSTAT_OPEN
    explored[node.board] = node
    if node.children is not None:
        for child in node.children:
            child.parent = None
    node.children = None
    open.insert(node)

def close_node(node: Node, closed: LinkedList, explored: dict[Board, Node]):
    closed.set_next(node)
    node.status = NSTAT_CLOSED


def remove_from_closed(
    node: Node, open: SortedLinkedList, closed: LinkedList, explored: dict[Board, Node]
):
    try:
        del explored[node.board]
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


def evaluate_current(node: Node, target_board: Board) -> float:
    value = evaluate_board(node.board, target_board, node.depth)
    node.board.set_value(value)
    return value


def derivate_boards(node: Node) -> List[Node]:
    future_boards = node.board.get_future_boards()
    children = []
    for future_board in future_boards:
        if node.parent is None or future_board != node.parent.board:
            children.append(Node(future_board, node))
    node.children = children
    return children


def bfs_puzzle(initial: Board, target: Board, deepth_improve_threshold: int = 5) -> List[Board]:
    open = SortedLinkedList(None)
    closed = LinkedList(None)
    explored = dict[Board, Node]()
    root = Node(initial, None)
    evaluate_current(root, target)
    open_node(root, open, explored)

    prev_depth = 0
    while not open.is_empty():
        current = open.pop_start()
        
        if current.depth % 10 == 0 and prev_depth != current.depth:
            prev_depth = current.depth
            print(f"Depth: {current.depth}, Value: {current.board.get_value()}")

        if current.board == target:
            return get_path_to_root(current)

        children = derivate_boards(current)
        for child in children:
            clone = explored.get(child.board, None)
            if clone is not None:
                if is_open(clone):
                    if child.depth < clone.depth - deepth_improve_threshold:
                        remove_from_open(clone, open)
                        evaluate_current(child, target)
                        open_node(child, open, explored)
                elif is_closed(clone):
                    if child.depth < clone.depth - deepth_improve_threshold:
                        remove_from_closed(clone, open, closed, explored)
                        evaluate_current(child, target)
                        open_node(child, open, explored)
            else:
                evaluate_current(child, target)
                open_node(child, open, explored)
        close_node(current, closed, explored)


DIMENSION = 4
target_board = Board(DIMENSION, sorted_pieces(DIMENSION))
random_board = random_pieces(DIMENSION, 50, 1)[0]
print("----------------START----------------")
print(f"Target: {evaluate_board(target_board, target_board, 0)}")
print(target_board)
print(f"Start: {evaluate_board(random_board, target_board, 0)}")
print(random_board)

steps = bfs_puzzle(random_board, target_board, 5)
if steps is not None and len(steps) > 0:
    print("Solution found:")
    for step in steps:
        print(step)
else:
    print("No solution found")
