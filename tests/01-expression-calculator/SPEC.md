# Practice Test 1 — Integer Expression Calculator

Time limit: 45 minutes. Fix `calc.py` so that `test_calc.py` passes.
Score = number of passing tests. Run from the repo root: `python3 scripts/run.py 01`
(or, inside this folder: `python3 -m unittest -v test_calc`)

## Spec

`calc.py` evaluates integer arithmetic expressions in three stages.

### 1. `tokenize(text) -> list`
- Non-negative integer literals become Python `int`s (multi-digit allowed).
- Operators `+ - * / % ^` and parentheses `( )` become one-character strings.
- Whitespace is ignored.
- A `-` is **unary** (emitted as the string `"neg"`) when it is the first
  token, or directly follows `(`, a binary operator, or another `"neg"`.
  Otherwise it is the binary `"-"`.
- Any other character raises `ValueError`.

### 2. `to_rpn(tokens) -> list`
Converts infix tokens to Reverse Polish Notation (shunting-yard).

| Operator        | Precedence | Associativity |
|-----------------|-----------:|---------------|
| `^`             | 4          | right         |
| `neg` (unary)   | 3          | prefix        |
| `*` `/` `%`     | 2          | left          |
| `+` `-`         | 1          | left          |

- So `-2 ^ 2` means `-(2 ^ 2)`, and `2 ^ 3 ^ 2` means `2 ^ (3 ^ 2)`.
- Unbalanced parentheses (either direction) raise `ValueError`.

### 3. `eval_rpn(rpn) -> int`
- `/` is integer division truncating **toward zero** (`-7 / 2 == -3`).
- `%` is the matching remainder: result has the sign of the **dividend**
  (`-7 % 3 == -1`, `7 % -3 == 1`).
- Division or modulo by zero raises `ZeroDivisionError`.
- `^` is exponentiation; a negative exponent raises `ValueError`.
- An operator without enough operands raises `ValueError`.
- After evaluation exactly one value must remain; otherwise `ValueError`
  (this includes empty input).

### `evaluate(text) -> int`
`eval_rpn(to_rpn(tokenize(text)))`.

Where this spec is ambiguous, the tests are the final word.
