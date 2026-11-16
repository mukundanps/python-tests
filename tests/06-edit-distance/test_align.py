import unittest

from align import edit_table, edit_distance, edit_ops, similarity, closest


class TestEditTable(unittest.TestCase):
    def test_shape(self):
        t = edit_table("ab", "xyz")
        self.assertEqual(len(t), 3)
        self.assertEqual(len(t[0]), 4)

    def test_first_column(self):
        self.assertEqual([row[0] for row in edit_table("abc", "x")], [0, 1, 2, 3])

    def test_first_row(self):
        self.assertEqual(edit_table("x", "abc")[0], [0, 1, 2, 3])

    def test_small_table(self):
        self.assertEqual(edit_table("ab", "b"), [[0, 1], [1, 1], [2, 1]])

    def test_insert_only_table(self):
        self.assertEqual(edit_table("a", "ab"), [[0, 1, 2], [1, 0, 1]])


class TestEditDistance(unittest.TestCase):
    def test_identical(self):
        self.assertEqual(edit_distance("same", "same"), 0)

    def test_both_empty(self):
        self.assertEqual(edit_distance("", ""), 0)

    def test_from_empty(self):
        self.assertEqual(edit_distance("", "abc"), 3)

    def test_to_empty(self):
        self.assertEqual(edit_distance("abc", ""), 3)

    def test_substitution(self):
        self.assertEqual(edit_distance("cat", "cut"), 1)

    def test_insertion(self):
        self.assertEqual(edit_distance("cat", "cart"), 1)

    def test_deletion(self):
        self.assertEqual(edit_distance("cart", "cat"), 1)

    def test_kitten_sitting(self):
        self.assertEqual(edit_distance("kitten", "sitting"), 3)

    def test_different_lengths(self):
        self.assertEqual(edit_distance("flaw", "lawn"), 2)
        self.assertEqual(edit_distance("intention", "execution"), 5)


class TestEditOps(unittest.TestCase):
    def test_identical(self):
        self.assertEqual(edit_ops("ab", "ab"), [("keep", "a"), ("keep", "b")])

    def test_substitution_is_old_then_new(self):
        self.assertEqual(
            edit_ops("cat", "cut"),
            [("keep", "c"), ("sub", "a", "u"), ("keep", "t")],
        )

    def test_insert_at_end(self):
        self.assertEqual(
            edit_ops("ab", "abc"), [("keep", "a"), ("keep", "b"), ("ins", "c")]
        )

    def test_delete_at_end(self):
        self.assertEqual(
            edit_ops("abc", "ab"), [("keep", "a"), ("keep", "b"), ("del", "c")]
        )

    def test_from_empty(self):
        self.assertEqual(edit_ops("", "hi"), [("ins", "h"), ("ins", "i")])

    def test_to_empty(self):
        self.assertEqual(edit_ops("hi", ""), [("del", "h"), ("del", "i")])

    def test_op_count_matches_distance(self):
        ops = edit_ops("kitten", "sitting")
        self.assertEqual(sum(1 for op in ops if op[0] != "keep"), 3)


class TestSimilarity(unittest.TestCase):
    def test_identical(self):
        self.assertEqual(similarity("abc", "abc"), 1.0)

    def test_both_empty(self):
        self.assertEqual(similarity("", ""), 1.0)

    def test_nothing_in_common(self):
        self.assertEqual(similarity("abc", "xyz"), 0.0)

    def test_uses_longer_length(self):
        self.assertEqual(similarity("abc", "abcd"), 0.75)

    def test_one_empty(self):
        self.assertEqual(similarity("", "abcd"), 0.0)


class TestClosest(unittest.TestCase):
    def test_no_candidates(self):
        self.assertIsNone(closest("word", []))

    def test_exact_match(self):
        self.assertEqual(closest("cat", ["dog", "cat", "cow"]), "cat")

    def test_nearest(self):
        self.assertEqual(closest("helo", ["world", "hello", "help"]), "hello")

    def test_tie_goes_to_first(self):
        self.assertEqual(closest("cat", ["bat", "rat", "hat"]), "bat")


if __name__ == "__main__":
    unittest.main()
