# 04-sampling — planted bugs (7)

| # | Where | Bug | Fix |
|---|-------|-----|-----|
| 1 | softmax | multiplies logits by temperature | x / temperature |
| 2 | argmax | `>=` returns the last of tied maxima | `>` so the lowest index wins |
| 3 | top_k | keeps k + 1 entries | [:k] |
| 4 | top_p | `>` keeps one token too many when the mass equals p exactly | cumulative >= p |
| 5 | sample | `<=` selects a token when u equals its lower boundary | u < cumulative |
| 6 | sample | fallback tracks the last index, not the last index with non-zero probability | update `last` only when p > 0 |
| 7 | next_token | top-p is applied to the unfiltered distribution, discarding top-k | top_p(probs, p) |
