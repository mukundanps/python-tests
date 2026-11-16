import unittest

from routes import MinHeap, Graph, distances, shortest_path


class TestMinHeap(unittest.TestCase):
    def test_empty_len(self):
        self.assertEqual(len(MinHeap()), 0)

    def test_push_pop_single(self):
        h = MinHeap()
        h.push(5, "a")
        self.assertEqual(h.pop(), (5, "a"))
        self.assertEqual(len(h), 0)

    def test_pop_empty(self):
        with self.assertRaises(IndexError):
            MinHeap().pop()

    def test_peek_empty(self):
        with self.assertRaises(IndexError):
            MinHeap().peek()

    def test_peek_does_not_remove(self):
        h = MinHeap()
        h.push(2, "x")
        h.push(1, "y")
        self.assertEqual(h.peek(), (1, "y"))
        self.assertEqual(len(h), 2)

    def test_two_items(self):
        h = MinHeap()
        h.push(2, "x")
        h.push(1, "y")
        self.assertEqual([h.pop(), h.pop()], [(1, "y"), (2, "x")])

    def test_ascending_input(self):
        h = MinHeap()
        for p in [1, 2, 3, 4, 5, 6, 7]:
            h.push(p, str(p))
        self.assertEqual([h.pop()[0] for _ in range(7)], [1, 2, 3, 4, 5, 6, 7])

    def test_descending_input(self):
        h = MinHeap()
        for p in [7, 6, 5, 4, 3, 2, 1]:
            h.push(p, str(p))
        self.assertEqual([h.pop()[0] for _ in range(7)], [1, 2, 3, 4, 5, 6, 7])

    def test_mixed_input(self):
        h = MinHeap()
        values = [9, 4, 7, 1, 8, 2, 6, 3, 5, 0]
        for p in values:
            h.push(p, p)
        self.assertEqual([h.pop()[0] for _ in values], sorted(values))

    def test_interleaved(self):
        h = MinHeap()
        h.push(5, "e")
        h.push(3, "c")
        self.assertEqual(h.pop(), (3, "c"))
        h.push(1, "a")
        h.push(4, "d")
        self.assertEqual(h.pop(), (1, "a"))
        self.assertEqual(h.pop(), (4, "d"))
        self.assertEqual(h.pop(), (5, "e"))

    def test_ties_fifo(self):
        h = MinHeap()
        for name in ["zed", "amy", "bob", "kim"]:
            h.push(1, name)
        self.assertEqual(
            [h.pop()[1] for _ in range(4)], ["zed", "amy", "bob", "kim"]
        )

    def test_ties_unorderable_items(self):
        h = MinHeap()
        h.push(1, {"id": 1})
        h.push(1, {"id": 2})
        self.assertEqual(h.pop(), (1, {"id": 1}))
        self.assertEqual(h.pop(), (1, {"id": 2}))


class TestGraph(unittest.TestCase):
    def test_add_node(self):
        g = Graph()
        g.add_node("a")
        self.assertEqual(g.nodes(), ["a"])
        self.assertEqual(g.neighbors("a"), [])

    def test_undirected_edge(self):
        g = Graph()
        g.add_edge("a", "b", 3)
        self.assertEqual(g.neighbors("a"), [("b", 3)])
        self.assertEqual(g.neighbors("b"), [("a", 3)])

    def test_directed_edge(self):
        g = Graph()
        g.add_edge("a", "b", 3, directed=True)
        self.assertEqual(g.neighbors("a"), [("b", 3)])
        self.assertEqual(g.neighbors("b"), [])

    def test_zero_weight_allowed(self):
        g = Graph()
        g.add_edge("a", "b", 0)
        self.assertEqual(g.neighbors("a"), [("b", 0)])

    def test_negative_weight_rejected(self):
        g = Graph()
        with self.assertRaises(ValueError):
            g.add_edge("a", "b", -1)

    def test_neighbors_unknown(self):
        with self.assertRaises(KeyError):
            Graph().neighbors("nope")

    def test_nodes_sorted(self):
        g = Graph()
        g.add_edge("c", "a", 1)
        g.add_edge("b", "c", 1)
        self.assertEqual(g.nodes(), ["a", "b", "c"])


def build_city():
    g = Graph()
    g.add_edge("A", "B", 4)
    g.add_edge("A", "C", 1)
    g.add_edge("C", "B", 2)
    g.add_edge("B", "D", 5)
    g.add_edge("C", "D", 8)
    g.add_edge("D", "E", 3)
    g.add_node("Z")
    return g


class TestDistances(unittest.TestCase):
    def test_single_node(self):
        g = Graph()
        g.add_node("a")
        self.assertEqual(distances(g, "a"), {"a": 0})

    def test_one_edge(self):
        g = Graph()
        g.add_edge("a", "b", 7)
        self.assertEqual(distances(g, "a"), {"a": 0, "b": 7})

    def test_chain_accumulates(self):
        g = Graph()
        g.add_edge("a", "b", 2)
        g.add_edge("b", "c", 3)
        g.add_edge("c", "d", 4)
        self.assertEqual(distances(g, "a"), {"a": 0, "b": 2, "c": 5, "d": 9})

    def test_city(self):
        self.assertEqual(
            distances(build_city(), "A"),
            {"A": 0, "B": 3, "C": 1, "D": 8, "E": 11},
        )

    def test_unreachable_omitted(self):
        self.assertNotIn("Z", distances(build_city(), "A"))

    def test_directed_respected(self):
        g = Graph()
        g.add_edge("a", "b", 1, directed=True)
        self.assertEqual(distances(g, "b"), {"b": 0})

    def test_unknown_source(self):
        with self.assertRaises(KeyError):
            distances(build_city(), "Q")


class TestShortestPath(unittest.TestCase):
    def test_same_node(self):
        self.assertEqual(shortest_path(build_city(), "A", "A"), (0, ["A"]))

    def test_direct_edge(self):
        self.assertEqual(shortest_path(build_city(), "A", "C"), (1, ["A", "C"]))

    def test_detour_beats_direct(self):
        self.assertEqual(
            shortest_path(build_city(), "A", "B"), (3, ["A", "C", "B"])
        )

    def test_long_path(self):
        self.assertEqual(
            shortest_path(build_city(), "A", "E"),
            (11, ["A", "C", "B", "D", "E"]),
        )

    def test_reverse_direction(self):
        self.assertEqual(
            shortest_path(build_city(), "E", "A"),
            (11, ["E", "D", "B", "C", "A"]),
        )

    def test_unreachable(self):
        self.assertEqual(shortest_path(build_city(), "A", "Z"), (None, []))

    def test_unknown_destination(self):
        with self.assertRaises(KeyError):
            shortest_path(build_city(), "A", "Q")

    def test_unknown_source(self):
        with self.assertRaises(KeyError):
            shortest_path(build_city(), "Q", "A")

    def test_zero_weight_path(self):
        g = Graph()
        g.add_edge("a", "b", 0)
        g.add_edge("b", "c", 0)
        g.add_edge("a", "c", 1)
        self.assertEqual(shortest_path(g, "a", "c"), (0, ["a", "b", "c"]))

    def test_grid(self):
        g = Graph()
        for r in range(4):
            for c in range(4):
                if c < 3:
                    g.add_edge((r, c), (r, c + 1), 1 + r)
                if r < 3:
                    g.add_edge((r, c), (r + 1, c), 1 + c)
        dist, path = shortest_path(g, (3, 3), (0, 0))
        self.assertEqual(dist, 15)
        self.assertEqual(path[0], (3, 3))
        self.assertEqual(path[-1], (0, 0))
        self.assertEqual(len(path), 7)


if __name__ == "__main__":
    unittest.main()
