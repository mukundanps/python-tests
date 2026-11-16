import unittest

from intervals import merge, insert, total_length, intersect, contains, gaps


class TestMerge(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(merge([]), [])

    def test_disjoint_sorted(self):
        self.assertEqual(merge([(5, 7), (1, 3)]), [(1, 3), (5, 7)])

    def test_overlap(self):
        self.assertEqual(merge([(1, 4), (3, 6)]), [(1, 6)])

    def test_touching(self):
        self.assertEqual(merge([(1, 3), (3, 5)]), [(1, 5)])

    def test_nested(self):
        self.assertEqual(merge([(1, 10), (2, 3)]), [(1, 10)])

    def test_chain(self):
        self.assertEqual(merge([(1, 3), (2, 6), (5, 9), (20, 21)]), [(1, 9), (20, 21)])

    def test_empty_intervals_dropped(self):
        self.assertEqual(merge([(4, 4), (1, 2)]), [(1, 2)])


class TestInsertAndLength(unittest.TestCase):
    def test_insert_between(self):
        self.assertEqual(insert([(1, 2), (8, 9)], (4, 5)), [(1, 2), (4, 5), (8, 9)])

    def test_insert_bridges(self):
        self.assertEqual(insert([(1, 3), (6, 9)], (2, 7)), [(1, 9)])

    def test_insert_does_not_mutate(self):
        original = [(1, 3)]
        insert(original, (5, 6))
        self.assertEqual(original, [(1, 3)])

    def test_total_length(self):
        self.assertEqual(total_length([(1, 4), (2, 6), (10, 11)]), 6)

    def test_total_length_nested(self):
        self.assertEqual(total_length([(0, 10), (2, 3), (4, 5)]), 10)


class TestIntersect(unittest.TestCase):
    def test_no_overlap(self):
        self.assertEqual(intersect([(1, 2)], [(5, 6)]), [])

    def test_simple(self):
        self.assertEqual(intersect([(1, 5)], [(3, 8)]), [(3, 5)])

    def test_touching_is_empty(self):
        self.assertEqual(intersect([(1, 3)], [(3, 5)]), [])

    def test_one_spans_many(self):
        self.assertEqual(
            intersect([(0, 10)], [(1, 2), (4, 6), (9, 12)]),
            [(1, 2), (4, 6), (9, 10)],
        )

    def test_interleaved(self):
        self.assertEqual(
            intersect([(0, 3), (5, 9), (12, 14)], [(2, 6), (8, 13)]),
            [(2, 3), (5, 6), (8, 9), (12, 13)],
        )

    def test_empty_input(self):
        self.assertEqual(intersect([], [(1, 2)]), [])


class TestContains(unittest.TestCase):
    DATA = [(1, 3), (5, 8), (10, 11), (20, 30)]

    def test_inside(self):
        self.assertTrue(contains(self.DATA, 6))
        self.assertTrue(contains(self.DATA, 25))

    def test_start_is_inside(self):
        self.assertTrue(contains(self.DATA, 5))
        self.assertTrue(contains(self.DATA, 1))

    def test_end_is_outside(self):
        self.assertFalse(contains(self.DATA, 8))
        self.assertFalse(contains(self.DATA, 30))

    def test_between(self):
        self.assertFalse(contains(self.DATA, 4))
        self.assertFalse(contains(self.DATA, 15))

    def test_outside_range(self):
        self.assertFalse(contains(self.DATA, 0))
        self.assertFalse(contains(self.DATA, 99))

    def test_empty(self):
        self.assertFalse(contains([], 1))


class TestGaps(unittest.TestCase):
    def test_nothing_covered(self):
        self.assertEqual(gaps([], 0, 10), [(0, 10)])

    def test_fully_covered(self):
        self.assertEqual(gaps([(0, 10)], 0, 10), [])

    def test_gap_in_middle(self):
        self.assertEqual(gaps([(0, 3), (6, 10)], 0, 10), [(3, 6)])

    def test_several_gaps(self):
        self.assertEqual(
            gaps([(2, 3), (5, 6)], 0, 10), [(0, 2), (3, 5), (6, 10)]
        )

    def test_intervals_outside_window(self):
        self.assertEqual(gaps([(0, 2), (4, 5), (50, 60)], 3, 9), [(3, 4), (5, 9)])

    def test_interval_overhangs_window(self):
        self.assertEqual(gaps([(0, 4), (8, 20)], 2, 10), [(4, 8)])


if __name__ == "__main__":
    unittest.main()
