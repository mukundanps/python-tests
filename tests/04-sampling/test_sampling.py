import math
import unittest

from sampling import softmax, argmax, top_k, top_p, sample, next_token

P = [0.5, 0.25, 0.125, 0.125]
LOGITS = [math.log(x) for x in P]


class Base(unittest.TestCase):
    def assertProbs(self, got, want):
        self.assertEqual(len(got), len(want))
        for g, w in zip(got, want):
            self.assertAlmostEqual(g, w, places=9)


class TestSoftmax(Base):
    def test_uniform(self):
        self.assertProbs(softmax([2.0, 2.0]), [0.5, 0.5])

    def test_recovers_distribution(self):
        self.assertProbs(softmax(LOGITS), P)

    def test_sums_to_one(self):
        self.assertAlmostEqual(sum(softmax([3.0, -1.0, 0.5])), 1.0)

    def test_large_logits_do_not_overflow(self):
        self.assertProbs(softmax([1000.0, 1000.0]), [0.5, 0.5])

    def test_high_temperature_flattens(self):
        self.assertProbs(softmax([0.0, math.log(4.0)], 2.0), [1 / 3, 2 / 3])

    def test_low_temperature_sharpens(self):
        self.assertProbs(softmax([0.0, math.log(2.0)], 0.5), [0.2, 0.8])

    def test_zero_temperature_rejected(self):
        with self.assertRaises(ValueError):
            softmax([1.0, 2.0], 0)


class TestArgmax(Base):
    def test_simple(self):
        self.assertEqual(argmax([1, 9, 3]), 1)

    def test_tie_lowest_index(self):
        self.assertEqual(argmax([4, 7, 7, 2]), 1)


class TestTopK(Base):
    def test_k_one(self):
        self.assertProbs(top_k(P, 1), [1.0, 0.0, 0.0, 0.0])

    def test_k_two(self):
        self.assertProbs(top_k(P, 2), [2 / 3, 1 / 3, 0.0, 0.0])

    def test_tie_keeps_lower_index(self):
        self.assertProbs(top_k(P, 3), [4 / 7, 2 / 7, 1 / 7, 0.0])

    def test_k_larger_than_vocab(self):
        self.assertProbs(top_k(P, 10), P)

    def test_unsorted_input(self):
        self.assertProbs(top_k([0.125, 0.5, 0.125, 0.25], 2), [0.0, 2 / 3, 0.0, 1 / 3])

    def test_k_zero_rejected(self):
        with self.assertRaises(ValueError):
            top_k(P, 0)


class TestTopP(Base):
    def test_small_p_keeps_top_token(self):
        self.assertProbs(top_p(P, 0.3), [1.0, 0.0, 0.0, 0.0])

    def test_exact_boundary(self):
        self.assertProbs(top_p(P, 0.75), [2 / 3, 1 / 3, 0.0, 0.0])

    def test_between_boundaries(self):
        self.assertProbs(top_p(P, 0.8), [4 / 7, 2 / 7, 1 / 7, 0.0])

    def test_p_one_keeps_all(self):
        self.assertProbs(top_p(P, 1.0), P)

    def test_p_out_of_range(self):
        with self.assertRaises(ValueError):
            top_p(P, 0)


class TestSample(Base):
    def test_first_bucket(self):
        self.assertEqual(sample(P, 0.0), 0)
        self.assertEqual(sample(P, 0.49), 0)

    def test_boundary_belongs_to_next_bucket(self):
        self.assertEqual(sample(P, 0.5), 1)
        self.assertEqual(sample(P, 0.75), 2)

    def test_last_bucket(self):
        self.assertEqual(sample(P, 0.99), 3)

    def test_skips_zero_probability(self):
        self.assertEqual(sample([0.0, 1.0, 0.0], 0.0), 1)

    def test_overflow_returns_last_nonzero(self):
        self.assertEqual(sample([0.25, 0.25, 0.0], 0.9), 1)


class TestNextToken(Base):
    def test_zero_temperature_is_greedy(self):
        self.assertEqual(next_token([0.1, 2.0, 2.0], 0.99, temperature=0), 1)

    def test_plain_sampling(self):
        self.assertEqual(next_token(LOGITS, 0.6), 1)
        self.assertEqual(next_token(LOGITS, 0.9), 3)

    def test_top_k_limits_choices(self):
        self.assertEqual(next_token(LOGITS, 0.9, k=2), 1)

    def test_top_p_limits_choices(self):
        self.assertEqual(next_token(LOGITS, 0.9, p=0.5), 0)

    def test_top_k_then_top_p(self):
        # after k=2 the distribution is [2/3, 1/3]; p=0.9 keeps both
        self.assertEqual(next_token(LOGITS, 0.95, k=2, p=0.9), 1)


if __name__ == "__main__":
    unittest.main()
