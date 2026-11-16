import unittest

from bpe import (
    get_pair_counts, best_pair, merge_symbols, train, encode_word, encode, decode,
)

LOW = [("l", "o"), ("lo", "w"), ("low", "</w>")]


class TestPairCounts(unittest.TestCase):
    def test_two_symbols(self):
        self.assertEqual(get_pair_counts({("a", "b"): 1}), {("a", "b"): 1})

    def test_last_pair_counted(self):
        self.assertEqual(
            get_pair_counts({("a", "b", "c"): 1}), {("a", "b"): 1, ("b", "c"): 1}
        )

    def test_frequency_weighted(self):
        self.assertEqual(
            get_pair_counts({("a", "b", "c"): 2, ("b", "c"): 3}),
            {("a", "b"): 2, ("b", "c"): 5},
        )

    def test_single_symbol_has_no_pairs(self):
        self.assertEqual(get_pair_counts({("a",): 4}), {})


class TestBestPair(unittest.TestCase):
    def test_empty(self):
        self.assertIsNone(best_pair({}))

    def test_highest_count(self):
        self.assertEqual(best_pair({("a", "b"): 3, ("b", "c"): 5}), ("b", "c"))

    def test_tie_goes_to_smallest_pair(self):
        self.assertEqual(
            best_pair({("b", "c"): 2, ("a", "z"): 2, ("a", "b"): 2}), ("a", "b")
        )


class TestMergeSymbols(unittest.TestCase):
    def test_no_match(self):
        self.assertEqual(merge_symbols(("a", "b"), ("x", "y")), ("a", "b"))

    def test_merge_at_start(self):
        self.assertEqual(merge_symbols(("a", "b", "c"), ("a", "b")), ("ab", "c"))

    def test_merge_at_end(self):
        self.assertEqual(merge_symbols(("c", "a", "b"), ("a", "b")), ("c", "ab"))

    def test_merge_twice(self):
        self.assertEqual(
            merge_symbols(("a", "b", "a", "b"), ("a", "b")), ("ab", "ab")
        )

    def test_no_overlap(self):
        self.assertEqual(merge_symbols(("a", "a", "a"), ("a", "a")), ("aa", "a"))


class TestTrain(unittest.TestCase):
    def test_no_repeats_no_merges(self):
        self.assertEqual(train("abc", 5), [])

    def test_zero_merges(self):
        self.assertEqual(train("low low low lower", 0), [])

    def test_first_merge(self):
        self.assertEqual(train("low low low lower", 1), [("l", "o")])

    def test_stops_when_no_pair_repeats(self):
        self.assertEqual(train("low low low lower", 10), LOW)

    def test_count_of_two_still_merges(self):
        self.assertEqual(train("ab ab", 5), [("a", "b"), ("ab", "</w>")])


class TestEncodeDecode(unittest.TestCase):
    def test_encode_word_no_merges(self):
        self.assertEqual(encode_word("ab", []), ["a", "b", "</w>"])

    def test_encode_known_word(self):
        self.assertEqual(encode_word("low", LOW), ["low</w>"])

    def test_encode_longer_word(self):
        self.assertEqual(encode_word("lower", LOW), ["low", "e", "r", "</w>"])

    def test_encode_text(self):
        self.assertEqual(
            encode("low lower", LOW), ["low</w>", "low", "e", "r", "</w>"]
        )

    def test_decode(self):
        self.assertEqual(
            decode(["low</w>", "low", "e", "r", "</w>"]), "low lower"
        )

    def test_round_trip(self):
        text = "the lower slow low flow"
        merges = train(text, 20)
        self.assertEqual(decode(encode(text, merges)), text)


if __name__ == "__main__":
    unittest.main()
