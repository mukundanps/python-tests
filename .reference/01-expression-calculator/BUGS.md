# 01 — planted bugs (9)

| # | Where | Bug | Fix |
|---|-------|-----|-----|
| 1 | `NEG_PREC` | set to 5, so `neg` binds tighter than `^` | 3 |
| 2 | `tokenize`, digits | `num + int(...)` sums digits | `num * 10 + int(...)` |
| 3 | `tokenize`, `-` | unary after `")"` instead of after `"("` | `prev == "("` |
| 4 | `to_rpn`, operator loop | pops on `>=` for every operator, so `^` is left-associative | pop on `>`, or `==` when the incoming operator is left-associative |
| 5 | `to_rpn`, final drain | silently drops a leftover `"("` | raise `ValueError` |
| 6 | `_apply`, `/` | `a // b` floors | truncate toward zero |
| 7 | `_apply`, `%` | Python `%` (sign of divisor) | sign of dividend |
| 8 | `_apply`, `^` | `b ** a`, no negative-exponent check | `a ** b`, raise `ValueError` if `b < 0` |
| 9 | `eval_rpn`, end | returns `stack[-1]` without checking | require exactly one value |
