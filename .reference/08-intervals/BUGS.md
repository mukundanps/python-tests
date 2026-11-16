# 08-intervals — planted bugs (7)

| # | Where | Bug | Fix |
|---|-------|-----|-----|
| 1 | merge | `<` leaves touching intervals unmerged | start <= merged[-1][1] |
| 2 | merge | takes the new end even when the new interval is nested inside the current one | max(merged[-1][1], end) |
| 3 | intersect | `<=` emits empty intervals where the inputs only touch | lo < hi |
| 4 | intersect | advances the list whose interval ends later | advance the one that ends first |
| 5 | contains | `>` treats the end point as inside | x >= end |
| 6 | gaps | each gap starts at the window start instead of the cursor | (cursor, start) |
| 7 | gaps | `<=` appends an empty trailing gap | cursor < hi |
