# Practice Test 4 — Next-Token Sampling (sprint)

Time limit: 15 minutes. Fix `sampling.py` so that `test_sampling.py` passes.
Run from the repo root: `python3 scripts/run.py 04`

## Spec

- `softmax(logits, temperature=1.0)` — divides each logit by the
  temperature, then normalises `exp` of the result. Must not overflow for
  large logits. `temperature <= 0` raises `ValueError`.
- `argmax(values)` — index of the maximum; lowest index on ties.
- `top_k(probs, k)` — keeps the `k` most probable entries (ties: lower
  index first), zeroes the rest and renormalises to sum 1. `k` larger than
  the vocabulary keeps everything. `k <= 0` raises `ValueError`.
- `top_p(probs, p)` — nucleus filtering. Taking entries from most to least
  probable (ties: lower index first), keeps the smallest prefix whose
  total probability is `>= p`, zeroes the rest and renormalises.
  `p` outside `(0, 1]` raises `ValueError`.
- `sample(probs, u)` — inverse-CDF sampling with `u` in `[0, 1)`: returns
  the first index whose cumulative probability is strictly greater than
  `u`. If rounding leaves no such index, returns the last index with
  non-zero probability.
- `next_token(logits, u, temperature=1.0, k=None, p=None)` — if
  `temperature == 0`, returns `argmax(logits)`. Otherwise: softmax, then
  top-k if `k` is given, then top-p (on the top-k result) if `p` is given,
  then `sample`.

Where this spec is ambiguous, the tests are the final word.
