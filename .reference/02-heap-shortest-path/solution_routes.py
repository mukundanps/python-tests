"""Hand-written min-heap, weighted graph, and Dijkstra shortest paths."""


class MinHeap:
    """Binary min-heap of (priority, item). Equal priorities pop in FIFO order."""

    def __init__(self):
        self._data = []
        self._counter = 0

    def __len__(self):
        return len(self._data)

    def push(self, priority, item):
        self._data.append((priority, self._counter, item))
        self._counter += 1
        self._sift_up(len(self._data) - 1)

    def peek(self):
        if not self._data:
            raise IndexError("peek from empty heap")
        entry = self._data[0]
        return entry[0], entry[2]

    def pop(self):
        if not self._data:
            raise IndexError("pop from empty heap")
        last = self._data.pop()
        if not self._data:
            return last[0], last[2]
        top = self._data[0]
        self._data[0] = last
        self._sift_down(0)
        return top[0], top[2]

    def _less(self, i, j):
        a = self._data[i]
        b = self._data[j]
        return (a[0], a[1]) < (b[0], b[1])

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._less(i, parent):
                self._data[i], self._data[parent] = self._data[parent], self._data[i]
                i = parent
            else:
                break

    def _sift_down(self, i):
        n = len(self._data)
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            smallest = i
            if left < n and self._less(left, smallest):
                smallest = left
            if right < n and self._less(right, smallest):
                smallest = right
            if smallest == i:
                return
            self._data[i], self._data[smallest] = self._data[smallest], self._data[i]
            i = smallest


class Graph:
    def __init__(self):
        self.adj = {}

    def add_node(self, u):
        if u not in self.adj:
            self.adj[u] = []

    def add_edge(self, u, v, weight, directed=False):
        if weight < 0:
            raise ValueError("negative edge weight")
        self.add_node(u)
        self.add_node(v)
        self.adj[u].append((v, weight))
        if not directed:
            self.adj[v].append((u, weight))

    def nodes(self):
        return sorted(self.adj)

    def neighbors(self, u):
        if u not in self.adj:
            raise KeyError(u)
        return sorted(self.adj[u])


def _dijkstra(graph, src):
    dist = {src: 0}
    prev = {}
    done = set()
    heap = MinHeap()
    heap.push(0, src)
    while len(heap) > 0:
        d, u = heap.pop()
        if u in done:
            continue
        done.add(u)
        for v, w in graph.adj[u]:
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heap.push(nd, v)
    return dist, prev


def distances(graph, src):
    """Return {node: distance} for every node reachable from src."""
    if src not in graph.adj:
        raise KeyError(src)
    dist, _ = _dijkstra(graph, src)
    return dist


def shortest_path(graph, src, dst):
    """Return (distance, [src, ..., dst]) or (None, []) if unreachable."""
    if src not in graph.adj or dst not in graph.adj:
        raise KeyError("unknown node")
    dist, prev = _dijkstra(graph, src)
    if dst not in dist:
        return None, []
    path = []
    node = dst
    while node != src:
        path.append(node)
        node = prev[node]
    path.append(src)
    path.reverse()
    return dist[dst], path
