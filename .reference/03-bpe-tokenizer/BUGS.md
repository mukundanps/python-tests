# 03-bpe-tokenizer — planted bugs (6)

| # | Where | Bug | Fix |
|---|-------|-----|-----|
| 1 | get_pair_counts | loop stops one pair early | range(len(symbols) - 1) |
| 2 | get_pair_counts | adds 1 per word type, ignoring its frequency | + freq |
| 3 | best_pair | ties go to the lexicographically largest pair | min(..., key=(-count, pair)) |
| 4 | merge_symbols | advances by 1 after a merge, so the second symbol is emitted again | i += 2 |
| 5 | train | stops when the best count is 2 (should stop below 2) | counts[pair] < 2 |
| 6 | decode | end-of-word marker removed without leaving a space | replace(END, " ") |
