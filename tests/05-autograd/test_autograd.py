import unittest

from autograd import Value, zero_grad, sgd_step


class TestForward(unittest.TestCase):
    def test_add_mul(self):
        self.assertEqual((Value(2.0) + Value(3.0)).data, 5.0)
        self.assertEqual((Value(2.0) * Value(3.0)).data, 6.0)

    def test_constants_on_either_side(self):
        x = Value(4.0)
        self.assertEqual((x + 1).data, 5.0)
        self.assertEqual((1 + x).data, 5.0)
        self.assertEqual((x * 3).data, 12.0)
        self.assertEqual((3 * x).data, 12.0)

    def test_sub_and_neg(self):
        x = Value(4.0)
        self.assertEqual((x - 1).data, 3.0)
        self.assertEqual((-x).data, -4.0)

    def test_constant_minus_value(self):
        self.assertEqual((10 - Value(4.0)).data, 6.0)

    def test_pow_and_div(self):
        self.assertEqual((Value(3.0) ** 2).data, 9.0)
        self.assertEqual((Value(6.0) / Value(3.0)).data, 2.0)

    def test_relu(self):
        self.assertEqual(Value(2.5).relu().data, 2.5)
        self.assertEqual(Value(-2.5).relu().data, 0.0)


class TestSingleOpGradients(unittest.TestCase):
    def test_add(self):
        x, y = Value(2.0), Value(3.0)
        (x + y).backward()
        self.assertEqual((x.grad, y.grad), (1.0, 1.0))

    def test_mul(self):
        x, y = Value(3.0), Value(4.0)
        (x * y).backward()
        self.assertEqual((x.grad, y.grad), (4.0, 3.0))

    def test_pow(self):
        x = Value(2.0)
        (x ** 3).backward()
        self.assertEqual(x.grad, 12.0)

    def test_relu_positive(self):
        x = Value(2.0)
        x.relu().backward()
        self.assertEqual(x.grad, 1.0)

    def test_relu_negative(self):
        x = Value(-2.0)
        x.relu().backward()
        self.assertEqual(x.grad, 0.0)

    def test_output_grad_is_one(self):
        z = Value(2.0) * Value(5.0)
        z.backward()
        self.assertEqual(z.grad, 1.0)


class TestReuse(unittest.TestCase):
    def test_x_plus_x(self):
        x = Value(3.0)
        (x + x).backward()
        self.assertEqual(x.grad, 2.0)

    def test_x_times_x(self):
        x = Value(3.0)
        (x * x).backward()
        self.assertEqual(x.grad, 6.0)


class TestChains(unittest.TestCase):
    def test_two_layers(self):
        x, y = Value(2.0), Value(3.0)
        z = (x * y) * 5
        z.backward()
        self.assertEqual((x.grad, y.grad), (15.0, 10.0))

    def test_polynomial(self):
        x, y = Value(2.0), Value(3.0)
        z = (x * y + x) ** 2
        z.backward()
        self.assertEqual(z.data, 64.0)
        self.assertEqual((x.grad, y.grad), (64.0, 32.0))

    def test_subtraction_chain(self):
        x, y = Value(5.0), Value(2.0)
        z = (x - y) * (x - y)
        z.backward()
        self.assertEqual((x.grad, y.grad), (6.0, -6.0))

    def test_constant_minus_value(self):
        x = Value(4.0)
        z = (10 - x) * 2
        z.backward()
        self.assertEqual(x.grad, -2.0)

    def test_division(self):
        x, y = Value(6.0), Value(2.0)
        z = x / y
        z.backward()
        self.assertAlmostEqual(x.grad, 0.5)
        self.assertAlmostEqual(y.grad, -1.5)

    def test_diamond(self):
        x = Value(3.0)
        a = x * 2
        z = a * a + a
        z.backward()
        self.assertEqual(z.data, 42.0)
        self.assertEqual(x.grad, 26.0)

    def test_neuron(self):
        w, x, b = Value(-3.0), Value(2.0), Value(1.0)
        out = (w * x + b).relu()
        out.backward()
        self.assertEqual(out.data, 0.0)
        self.assertEqual((w.grad, x.grad, b.grad), (0.0, 0.0, 0.0))


class TestOptimiser(unittest.TestCase):
    def test_zero_grad(self):
        x = Value(1.0)
        (x * 3).backward()
        zero_grad([x])
        self.assertEqual(x.grad, 0.0)

    def test_sgd_step(self):
        x = Value(1.0)
        x.grad = 4.0
        sgd_step([x], 0.5)
        self.assertEqual(x.data, -1.0)

    def test_descent_reduces_loss(self):
        x = Value(5.0)
        for _ in range(3):
            zero_grad([x])
            loss = (x - 1) ** 2
            loss.backward()
            sgd_step([x], 0.25)
        self.assertEqual(x.data, 1.5)


if __name__ == "__main__":
    unittest.main()
