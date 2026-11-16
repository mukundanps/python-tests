"""Scalar reverse-mode automatic differentiation."""


class Value:
    def __init__(self, data, parents=(), op=""):
        self.data = data
        self.grad = 0.0
        self.op = op
        self._parents = parents
        self._backward = lambda: None

    def __repr__(self):
        return "Value(data=%r, grad=%r)" % (self.data, self.grad)

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), "+")

        def _backward():
            self.grad = out.grad
            other.grad = out.grad

        out._backward = _backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), "*")

        def _backward():
            self.grad += other.data * out.grad
            other.grad += other.data * out.grad

        out._backward = _backward
        return out

    def __pow__(self, n):
        out = Value(self.data ** n, (self,), "**")

        def _backward():
            self.grad += n * self.data ** n * out.grad

        out._backward = _backward
        return out

    def relu(self):
        out = Value(self.data if self.data > 0 else 0.0, (self,), "relu")

        def _backward():
            self.grad += (1.0 if out.data >= 0 else 0.0) * out.grad

        out._backward = _backward
        return out

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + (-other)

    def __truediv__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return self * other ** -1

    def __radd__(self, other):
        return self + other

    def __rmul__(self, other):
        return self * other

    def __rsub__(self, other):
        return self + (-other)

    def backward(self):
        order = []
        seen = set()

        def visit(node):
            if id(node) in seen:
                return
            seen.add(id(node))
            for parent in node._parents:
                visit(parent)
            order.append(node)

        visit(self)
        self.grad = 1.0
        for node in order:
            node._backward()


def zero_grad(params):
    for p in params:
        p.grad = 0.0


def sgd_step(params, lr):
    for p in params:
        p.data += lr * p.grad
