# Practice Test 6 — Edit Distance (sprint)

Time limit: 15 minutes. Fix `align.py` so that `test_align.py` passes.
Run from the repo root: `python3 scripts/run.py 06`

## Spec

- `edit_table(a, b)` — the Levenshtein table with `len(a) + 1` rows and
  `len(b) + 1` columns. `table[i][j]` is the minimum number of single
  character insertions, deletions and substitutions that turn `a[:i]` into
  `b[:j]`. So `table[i][0] == i` and `table[0][j] == j`.
- `edit_distance(a, b)` — the bottom-right cell of that table.
- `edit_ops(a, b)` — one optimal edit script, **in order from the start of
  the strings**, as a list of tuples:
  `("keep", ch)`, `("sub", old_ch, new_ch)`, `("del", ch)`, `("ins", ch)`.
- `similarity(a, b)` — `1 - distance / max(len(a), len(b))`; `1.0` when
  both strings are empty.
- `closest(word, candidates)` — the candidate with the smallest distance
  to `word`; the earliest one on ties; `None` for an empty list.

Where this spec is ambiguous, the tests are the final word.
