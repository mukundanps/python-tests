import unittest

from calc import tokenize, to_rpn, eval_rpn, evaluate


class TestTokenize(unittest.TestCase):
    def test_single_digit(self):
        self.assertEqual(tokenize("7"), [7])

    def test_multi_digit(self):
        self.assertEqual(tokenize("120+35"), [120, "+", 35])

    def test_whitespace_ignored(self):
        self.assertEqual(tokenize("  4 *  ( 5 )"), [4, "*", "(", 5, ")"])

    def test_leading_minus_is_neg(self):
        self.assertEqual(tokenize("-4"), ["neg", 4])

    def test_minus_after_number_is_binary(self):
        self.assertEqual(tokenize("9-4"), [9, "-", 4])

    def test_minus_after_open_paren_is_neg(self):
        self.assertEqual(tokenize("(-4)"), ["(", "neg", 4, ")"])

    def test_minus_after_close_paren_is_binary(self):
        self.assertEqual(tokenize("(1)-4"), ["(", 1, ")", "-", 4])

    def test_minus_after_operator_is_neg(self):
        self.assertEqual(tokenize("2*-4"), [2, "*", "neg", 4])

    def test_double_neg(self):
        self.assertEqual(tokenize("--4"), ["neg", "neg", 4])

    def test_bad_character(self):
        with self.assertRaises(ValueError):
            tokenize("2 & 3")


class TestToRpn(unittest.TestCase):
    def test_precedence(self):
        self.assertEqual(to_rpn([1, "+", 2, "*", 3]), [1, 2, 3, "*", "+"])

    def test_left_assoc(self):
        self.assertEqual(to_rpn([8, "-", 3, "-", 2]), [8, 3, "-", 2, "-"])

    def test_power_right_assoc(self):
        self.assertEqual(to_rpn([2, "^", 3, "^", 2]), [2, 3, 2, "^", "^"])

    def test_parens(self):
        self.assertEqual(
            to_rpn(["(", 1, "+", 2, ")", "*", 3]), [1, 2, "+", 3, "*"]
        )

    def test_neg_binds_looser_than_power(self):
        self.assertEqual(to_rpn(["neg", 2, "^", 2]), [2, 2, "^", "neg"])

    def test_neg_binds_tighter_than_mul(self):
        self.assertEqual(to_rpn(["neg", 2, "*", 3]), [2, "neg", 3, "*"])

    def test_unbalanced_close(self):
        with self.assertRaises(ValueError):
            to_rpn([1, "+", 2, ")"])

    def test_unbalanced_open(self):
        with self.assertRaises(ValueError):
            to_rpn(["(", 1, "+", 2])


class TestEvalRpn(unittest.TestCase):
    def test_subtraction_order(self):
        self.assertEqual(eval_rpn([10, 4, "-"]), 6)

    def test_power_order(self):
        self.assertEqual(eval_rpn([2, 3, "^"]), 8)

    def test_division_truncates_toward_zero(self):
        self.assertEqual(eval_rpn([7, 2, "/"]), 3)
        self.assertEqual(eval_rpn([7, "neg", 2, "/"]), -3)
        self.assertEqual(eval_rpn([7, 2, "neg", "/"]), -3)

    def test_modulo_takes_sign_of_dividend(self):
        self.assertEqual(eval_rpn([7, 3, "%"]), 1)
        self.assertEqual(eval_rpn([7, "neg", 3, "%"]), -1)
        self.assertEqual(eval_rpn([7, 3, "neg", "%"]), 1)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            eval_rpn([1, 0, "/"])

    def test_modulo_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            eval_rpn([1, 0, "%"])

    def test_negative_exponent(self):
        with self.assertRaises(ValueError):
            eval_rpn([2, 1, "neg", "^"])

    def test_missing_operand(self):
        with self.assertRaises(ValueError):
            eval_rpn([1, "+"])

    def test_leftover_operands(self):
        with self.assertRaises(ValueError):
            eval_rpn([1, 2])

    def test_empty(self):
        with self.assertRaises(ValueError):
            eval_rpn([])


class TestEvaluate(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(evaluate("1 + 2 * 3"), 7)

    def test_big_numbers(self):
        self.assertEqual(evaluate("1000 - 250 * 3"), 250)

    def test_nested_parens(self):
        self.assertEqual(evaluate("((2 + 3) * (4 - 1)) - 5"), 10)

    def test_power_chain(self):
        self.assertEqual(evaluate("2 ^ 3 ^ 2"), 512)

    def test_neg_power(self):
        self.assertEqual(evaluate("-2 ^ 2"), -4)

    def test_paren_neg_power(self):
        self.assertEqual(evaluate("(-2) ^ 2"), 4)

    def test_mixed(self):
        self.assertEqual(evaluate("-(3 + 4) * 2 - -17 / 5 + 20 % 6"), -9)

    def test_empty_string(self):
        with self.assertRaises(ValueError):
            evaluate("   ")

    def test_adjacent_numbers(self):
        with self.assertRaises(ValueError):
            evaluate("3 4")

    def test_unbalanced(self):
        with self.assertRaises(ValueError):
            evaluate("(1 + 2")


if __name__ == "__main__":
    unittest.main()
