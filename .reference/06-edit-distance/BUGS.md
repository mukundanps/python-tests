# 06-edit-distance — planted bugs (7)

| # | Where | Bug | Fix |
|---|-------|-----|-----|
| 1 | edit_table, first row | first row initialised to 0 instead of j | table[0][j] = j |
| 2 | edit_table, inner loop | insertion reads the diagonal cell | table[i][j - 1] + 1 |
| 3 | edit_distance | row and column indices swapped | [len(a)][len(b)] |
| 4 | edit_ops | substitution tuple has old and new swapped | ("sub", a[i - 1], b[j - 1]) |
| 5 | edit_ops | script never reversed, so it reads end to start | ops.reverse() |
| 6 | similarity | normalises by the shorter length | max(len(a), len(b)) |
| 7 | closest | `<=` lets a later candidate win a tie | d < best_distance |
