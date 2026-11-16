import math
import unittest

from lm import (
    BOS_ID, EOS_ID, UNK_ID, tokenize, Vocab, BigramModel, greedy_generate, beam_search,
)

CORPUS = ["The cat sat.", "The cat ran!", "the dog sat", "A cat sat"]
# token counts: cat 3, sat 3, the 3, a 1, dog 1, ran 1
CAT, SAT, THE, A, DOG, RAN = 3, 4, 5, 6, 7, 8


def make(k=1.0):
    vocab = Vocab().build(CORPUS)
    return BigramModel(vocab, k).train(CORPUS)


class TestTokenize(unittest.TestCase):
    def test_lowercases(self):
        self.assertEqual(tokenize("The CAT"), ["the", "cat"])

    def test_strips_edge_punctuation(self):
        self.assertEqual(tokenize("Hello, world!"), ["hello", "world"])

    def test_keeps_inner_punctuation(self):
        self.assertEqual(tokenize("pi is 3.14"), ["pi", "is", "3.14"])

    def test_any_whitespace(self):
        self.assertEqual(tokenize("a\tb\nc  d"), ["a", "b", "c", "d"])

    def test_drops_punctuation_only(self):
        self.assertEqual(tokenize("wait ... what ?"), ["wait", "what"])

    def test_empty(self):
        self.assertEqual(tokenize("   "), [])


class TestVocab(unittest.TestCase):
    def test_specials(self):
        v = Vocab()
        self.assertEqual(v.id_to_token, ["<s>", "</s>", "<unk>"])
        self.assertEqual((BOS_ID, EOS_ID, UNK_ID), (0, 1, 2))

    def test_build_orders_by_count_then_token(self):
        v = Vocab().build(CORPUS)
        self.assertEqual(v.id_to_token[3:], ["cat", "sat", "the", "a", "dog", "ran"])

    def test_len(self):
        self.assertEqual(len(Vocab().build(CORPUS)), 9)

    def test_min_count_is_inclusive(self):
        v = Vocab(min_count=3).build(CORPUS)
        self.assertEqual(sorted(v.id_to_token[3:]), ["cat", "sat", "the"])

    def test_min_count_excludes_rare(self):
        v = Vocab(min_count=2).build(CORPUS)
        self.assertNotIn("dog", v.token_to_id)

    def test_encode_known(self):
        v = Vocab().build(CORPUS)
        self.assertEqual(v.encode(["the", "dog", "ran"]), [THE, DOG, RAN])

    def test_encode_unknown(self):
        v = Vocab().build(CORPUS)
        self.assertEqual(v.encode(["the", "zebra"]), [THE, UNK_ID])

    def test_decode_skips_sentence_markers(self):
        v = Vocab().build(CORPUS)
        self.assertEqual(v.decode([BOS_ID, THE, CAT, EOS_ID]), ["the", "cat"])

    def test_decode_keeps_unknown(self):
        v = Vocab().build(CORPUS)
        self.assertEqual(v.decode([THE, UNK_ID]), ["the", "<unk>"])


class TestCounts(unittest.TestCase):
    def test_start_counts(self):
        m = make()
        self.assertEqual(m.count(BOS_ID, THE), 3)
        self.assertEqual(m.count(BOS_ID, A), 1)

    def test_inner_counts(self):
        m = make()
        self.assertEqual(m.count(THE, CAT), 2)
        self.assertEqual(m.count(CAT, SAT), 2)

    def test_end_counts(self):
        m = make()
        self.assertEqual(m.count(SAT, EOS_ID), 3)
        self.assertEqual(m.count(RAN, EOS_ID), 1)

    def test_unseen_count(self):
        self.assertEqual(make().count(DOG, CAT), 0)

    def test_totals(self):
        m = make()
        self.assertEqual(m.totals[BOS_ID], 4)
        self.assertEqual(m.totals[THE], 3)
        self.assertEqual(m.totals[CAT], 3)

    def test_nothing_follows_end_marker(self):
        self.assertNotIn(EOS_ID, make().totals)


class TestProbabilities(unittest.TestCase):
    def test_k_must_be_positive(self):
        with self.assertRaises(ValueError):
            BigramModel(Vocab(), 0)

    def test_seen_bigram(self):
        self.assertAlmostEqual(make().prob(BOS_ID, THE), 4 / 13)
        self.assertAlmostEqual(make().prob(THE, CAT), 3 / 12)

    def test_unseen_bigram(self):
        self.assertAlmostEqual(make().prob(THE, RAN), 1 / 12)

    def test_unseen_context_is_uniform(self):
        self.assertAlmostEqual(make().prob(UNK_ID, CAT), 1 / 9)

    def test_smaller_k(self):
        self.assertAlmostEqual(make(0.5).prob(BOS_ID, THE), 3.5 / 8.5)

    def test_distribution_sums_to_one(self):
        m = make(0.3)
        for prev in range(len(m.vocab)):
            self.assertAlmostEqual(sum(m.next_distribution(prev)), 1.0)

    def test_log_prob(self):
        self.assertAlmostEqual(make().log_prob(THE, CAT), math.log(0.25))


class TestSentenceScores(unittest.TestCase):
    def test_sentence_log_prob(self):
        want = math.log((4 / 13) * (3 / 12) * (3 / 12) * (4 / 12))
        self.assertAlmostEqual(make().sentence_log_prob(["the", "cat", "sat"]), want)

    def test_empty_sentence(self):
        self.assertAlmostEqual(make().sentence_log_prob([]), math.log(1 / 13))

    def test_unknown_word(self):
        want = math.log((4 / 13) * (1 / 12) * (1 / 9))
        self.assertAlmostEqual(make().sentence_log_prob(["the", "zebra"]), want)

    def test_perplexity(self):
        p = (4 / 13) * (3 / 12) * (3 / 12) * (4 / 12)
        self.assertAlmostEqual(make().perplexity(["the", "cat", "sat"]), p ** (-1 / 4))

    def test_perplexity_empty_sentence(self):
        self.assertAlmostEqual(make().perplexity([]), 13.0)


class TestTopNext(unittest.TestCase):
    def test_best(self):
        self.assertEqual(make().top_next(BOS_ID, 1), [THE])

    def test_two_best(self):
        self.assertEqual(make().top_next(BOS_ID, 2), [THE, A])

    def test_ties_by_lower_id(self):
        self.assertEqual(make().top_next(RAN, 3), [EOS_ID, UNK_ID, CAT])

    def test_never_start_marker(self):
        ids = make().top_next(CAT, 100)
        self.assertEqual(len(ids), 8)
        self.assertNotIn(BOS_ID, ids)


class TestGreedy(unittest.TestCase):
    def test_runs_to_end_marker(self):
        self.assertEqual(greedy_generate(make(), 10), ["the", "cat", "sat"])

    def test_max_len(self):
        self.assertEqual(greedy_generate(make(), 2), ["the", "cat"])

    def test_max_len_zero(self):
        self.assertEqual(greedy_generate(make(), 0), [])

    def test_start_tokens(self):
        self.assertEqual(greedy_generate(make(), 10, ["a"]), ["a", "cat", "sat"])


def tiny():
    corpus = ["a a a a a a"]
    return BigramModel(Vocab().build(corpus), 0.1).train(corpus)


P_A = 1.1 / 1.4        # <s> -> a
P_END0 = 0.1 / 1.4     # <s> -> </s>
P_AA = 5.1 / 6.4       # a -> a
P_END = 1.1 / 6.4      # a -> </s>


class TestBeamSearch(unittest.TestCase):
    def test_width_must_be_positive(self):
        with self.assertRaises(ValueError):
            beam_search(make(), 0, 5)

    def test_width_one_matches_greedy(self):
        result = beam_search(make(0.1), 1, 5)
        self.assertEqual([tokens for tokens, _ in result], [["the", "cat", "sat"]])

    def test_score_is_sentence_log_prob(self):
        m = make(0.1)
        tokens, score = beam_search(m, 1, 5)[0]
        self.assertAlmostEqual(score, m.sentence_log_prob(tokens))
        want = math.log((3.1 / 4.9) * (2.1 / 3.9) * (2.1 / 3.9) * (3.1 / 3.9))
        self.assertAlmostEqual(score, want)

    def test_width_three(self):
        result = beam_search(make(0.1), 3, 5)
        self.assertEqual(
            [tokens for tokens, _ in result],
            [["the", "cat", "sat"], ["the", "dog", "sat"], ["the", "cat", "ran"]],
        )

    def test_scores_descend(self):
        scores = [score for _, score in beam_search(make(0.1), 3, 5)]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_max_len_zero(self):
        result = beam_search(tiny(), 1, 0)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], [])
        self.assertAlmostEqual(result[0][1], math.log(P_END0))

    def test_max_len_one(self):
        result = beam_search(tiny(), 2, 1)
        self.assertEqual([tokens for tokens, _ in result], [["a"], []])
        self.assertAlmostEqual(result[0][1], math.log(P_A * P_END))

    def test_cut_off_beam_pays_for_end_marker(self):
        result = beam_search(tiny(), 1, 3)
        self.assertEqual(result[0][0], ["a"])
        self.assertAlmostEqual(result[0][1], math.log(P_A * P_END))

    def test_cut_off_beams_ranked_with_finished(self):
        result = beam_search(tiny(), 3, 3)
        self.assertEqual(
            [tokens for tokens, _ in result], [["a"], ["a", "a"], ["a", "a", "a"]]
        )
        self.assertAlmostEqual(result[2][1], math.log(P_A * P_AA * P_AA * P_END))


if __name__ == "__main__":
    unittest.main()
