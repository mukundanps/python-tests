# Practice Test 5 — Scalar Autograd (sprint)

Time limit: 15 minutes. Fix `autograd.py` so that `test_autograd.py` passes.
Run from the repo root: `python3 scripts/run.py 05`

## Spec

`Value` wraps a number (`.data`) and records how it was computed so that
`.backward()` can fill in `.grad` (the derivative of the output with
respect to that value) for every value that contributed.

- Supported: `+`, `-`, `*`, `/`, unary `-`, `** n` (constant `n`),
  `.relu()`. Plain numbers may appear on either side of `+`, `-`, `*`.
- Derivatives: `d(a+b) = 1, 1`; `d(a*b) = b, a`; `d(a**n) = n * a**(n-1)`;
  `relu` passes the gradient only where its input is `> 0`.
- A value used more than once receives the **sum** of the gradients from
  every use.
- `backward()` sets the output's own `.grad` to `1.0` and propagates from
  the output back towards the inputs, visiting each value after everything
  that depends on it.
- `zero_grad(params)` resets `.grad` to `0.0`.
- `sgd_step(params, lr)` moves each parameter **against** its gradient:
  `data = data - lr * grad`.

Where this spec is ambiguous, the tests are the final word.
