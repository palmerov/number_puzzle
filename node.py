from typing import List, Optional
from board import Board

NSTAT_LIMBO = -1
NSTAT_OPEN = 0
NSTAT_CLOSED = 1


class Node:
    def __init__(
        self,
        board: Board,
        parent: Optional["Node"],
    ):
        self.board = board
        self.parent: Optional[Node] = parent
        self.depth: int = 1 if parent is None else parent.depth + 1
        self.status: int = NSTAT_LIMBO
        self.children: List[Node] = []
        self.next: Optional[Node] = None
        self.prev: Optional[Node] = None


class LinkedList:
    def __init__(self, root: Optional[Node] = None):
        if root is not None:
            root.next = None
            root.prev = None
            self.start: Node = root
            self.end: Node = root
        else:
            self.start = None
            self.end = None

    def set_next(self, next: Node, to: Optional[Node] = None):
        next.prev = None
        next.next = None

        if self.start is None and self.end is None:
            self.start = next
            self.end = next
            return

        if to is None:
            to = self.end
            self.end = next
        else:
            next_of_to = to.next
            if next_of_to is not None:
                next_of_to.prev = next
                next.next = next_of_to
            else:
                self.end = next

        to.next = next
        next.prev = to

    def set_prev(self, prev: Node, to: Optional[Node] = None):
        prev.next = None
        prev.prev = None

        if self.start is None and self.end is None:
            self.start = prev
            self.end = prev
            return

        if to is None:
            to = self.start
            self.start = prev
        else:
            prev_of_to = to.prev
            if prev_of_to is not None:
                prev_of_to.next = prev
                prev.prev = prev_of_to
            else:
                self.start = prev
                
        to.prev = prev
        prev.next = to

    def pop_start(self) -> Node:
        if self.start is None:
            return None
        node = self.start
        if node is None:
            return None
        
        self.start = node.next
        node.next = None
        
        if self.start is not None:
            self.start.prev = None
        else:
            self.end = None
        return node

    def pop_end(self) -> Node:
        if self.end is None:
            return None
        node = self.end
        if node is None:
            return None
        
        self.end = node.prev
        node.prev = None
        
        if self.end is not None:
            self.end.next = None
        else:
            self.start = None
        return node

    def remove(self, node: Node):
        prev = node.prev
        next = node.next

        if prev is not None:
            if next is not None:
                prev.next = next
                next.prev = prev
            else:
                prev.next = None
                self.end = prev
        else:
            if next is not None:
                next.prev = None
                self.start = next
            else:
                self.start = None
                self.end = None
        node.next = None
        node.prev = None

    def find(self, board: Board) -> Optional[Node]:
        current = self.start
        while current is not None:
            if current.board == board:
                return current
            current = current.next
        return None

    def is_empty(self) -> bool:
        return self.start is None and self.end is None
    
    def to_list(self) -> List[Node]:
        nodes: List[Node] = []
        current = self.start
        while current is not None:
            nodes.append(current)
            current = current.next
        return nodes
    
    def print(self):
        nodes = self.to_list()
        print(f"LinkedList: {[str(node.board.get_value()) for node in nodes]}")
    
    def test(self):
        if self.start is None or self.end is None:
            return
        if self.start.prev is not None:
            raise Exception("Start has previous")
        if self.end.next is not None:
            raise Exception("End has next")