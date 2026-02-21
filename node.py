from typing import List, Optional, Tuple
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
        self._length: int = 0
        if root is not None:
            root.next = None
            root.prev = None
            self._start: Node = root
            self._end: Node = root
            self._length = 1
        else:
            self._start = None
            self._end = None
            
    @property
    def start(self) -> Optional[Node]:
        return self._start
            
    @property
    def end(self) -> Optional[Node]:
        return self._end
    
    @property
    def length(self) -> int:
        return self._length

    def set_next(self, next: Node, to: Optional[Node] = None):
        next.prev = None
        next.next = None

        if self._start is None and self._end is None:
            self._start = next
            self._end = next
            return

        if to is None:
            to = self._end
            self._end = next
        else:
            next_of_to = to.next
            if next_of_to is not None:
                next_of_to.prev = next
                next.next = next_of_to
            else:
                self._end = next

        to.next = next
        next.prev = to
        self._length += 1

    def set_prev(self, prev: Node, to: Optional[Node] = None):
        prev.next = None
        prev.prev = None

        if self._start is None and self._end is None:
            self._start = prev
            self._end = prev
            return

        if to is None:
            to = self._start
            self._start = prev
        else:
            prev_of_to = to.prev
            if prev_of_to is not None:
                prev_of_to.next = prev
                prev.prev = prev_of_to
            else:
                self._start = prev

        to.prev = prev
        prev.next = to
        self._length += 1

    def pop_start(self) -> Node:
        if self._start is None:
            return None
        node = self._start
        if node is None:
            return None

        self._start = node.next
        node.next = None

        if self._start is not None:
            self._start.prev = None
        else:
            self._end = None
        self._length -= 1
        return node

    def pop_end(self) -> Node:
        if self._end is None:
            return None
        node = self._end
        if node is None:
            return None

        self._end = node.prev
        node.prev = None

        if self._end is not None:
            self._end.next = None
        else:
            self._start = None
        self._length -= 1
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
                self._end = prev
        else:
            if next is not None:
                next.prev = None
                self._start = next
            else:
                self._start = None
                self._end = None
        node.next = None
        node.prev = None
        self._length -= 1

    def find(self, board: Board) -> Optional[Node]:
        current = self._start
        while current is not None:
            if current.board == board:
                return current
            current = current.next
        return None

    def is_empty(self) -> bool:
        return self._start is None and self._end is None

    def to_list(self) -> List[Node]:
        nodes: List[Node] = []
        current = self._start
        while current is not None:
            nodes.append(current)
            current = current.next
        return nodes

    def print(self):
        nodes = self.to_list()
        print(f"LinkedList: {[str(node.board.get_value()) for node in nodes]}")

    def test(self):
        if self._start is None or self._end is None:
            return
        if self._start.prev is not None:
            raise Exception("Start has previous")
        if self._end.next is not None:
            raise Exception("End has next")


class SortedLinkedList(LinkedList):
    def __init__(self, root: Optional[Node] = None):
        super().__init__(root)
        self._range: Tuple[Optional[Node], Optional[Node]] = (None, None)

    @property
    def min(self) -> Optional[Node]:
        return self._range[0]

    @property
    def max(self) -> Optional[Node]:
        return self._range[1]

    def pop_start(self) -> Node:
        node = super().pop_start()
        self._update_range()
        return node

    def pop_end(self) -> Node:
        node = super().pop_end()
        self._update_range()
        return node

    def remove(self, node: Node):
        super().remove(node)
        self._update_range()

    def find(self, board: Board) -> Optional[Node]:
        return super().find(board)

    def is_empty(self) -> bool:
        return super().is_empty()

    def to_list(self) -> List[Node]:
        return super().to_list()

    def print(self):
        super().print()

    def test(self):
        super().test()
        min = self.min()
        if min is None:
            return
        for node in self.to_list():
            if min.board.get_value() > node.board.get_value():
                raise Exception("Min is greater than next node")

    def _update_range(self):
        if self.is_empty():
            self._range = (None, None)
            return
        self._range = (self._start, self._end)

    def insert(self, node: Node):
        if self.is_empty():
            super().set_next(node)
            self._update_range()
            return

        start = self._start
        start_diff = start.board.get_value() - node.board.get_value()

        if start_diff > 0:
            super().set_prev(node, start)
            self._update_range()
            return

        end = self._end
        end_diff = end.board.get_value() - node.board.get_value()

        if end_diff < 0:
            super().set_next(node, end)
            self._update_range()
            return

        if abs(start_diff) < abs(end_diff):
            while (
                start is not None and start.board.get_value() < node.board.get_value()
            ):
                start = start.next
            super().set_prev(node, start)
            self._update_range()
        else:
            while end is not None and end.board.get_value() > node.board.get_value():
                end = end.prev
            super().set_next(node, end)
            self._update_range()