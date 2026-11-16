# 05-autograd — planted bugs (7)

| # | Where | Bug | Fix |
|---|-------|-----|-----|
| 1 | Value.__add__ | assigns the gradient instead of accumulating, so a value used twice loses a contribution | self.grad += out.grad |
| 2 | Value.__mul__ | second operand's gradient uses its own data | other.grad += self.data * out.grad |
| 3 | Value.__pow__ | derivative keeps exponent n | n * x ** (n - 1) |
| 4 | Value.relu | tests `out.data >= 0`, which is always true, so the gradient passes through for negative inputs | 1.0 only if self.data > 0 |
| 5 | Value.__rsub__ | computes self - other | (-self) + other |
| 6 | Value.backward | walks the topological order forwards, so inputs run before outputs | reversed(order) |
| 7 | sgd_step | steps up the gradient | p.data -= lr * p.grad |
