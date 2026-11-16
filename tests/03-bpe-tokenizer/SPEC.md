# Practice Test 3 — Byte-Pair Encoding (sprint)

Time limit: 15 minutes. Fix `bpe.py` so that `test_bpe.py` passes.
Run from the repo root: `python3 scripts/run.py 03`

## Spec

A word is a tuple of symbols. Each word starts as its characters followed
by the end-of-word marker `"</w>"`.

- `get_pair_counts(words)` — `words` maps symbol tuples to frequencies.
  Returns how often each adjacent pair occurs, weighted by frequency.
- `best_pair(counts)` — the pair with the highest count; ties go to the
  smallest pair in tuple order. `None` when `counts` is empty.
- `merge_symbols(symbols, pair)` — scanning left to right, replaces each
  non-overlapping occurrence of `pair` with the concatenated symbol.
- `train(text, num_merges)` — splits `text` on whitespace, then repeatedly
  merges the best pair, returning the merges in order. Stops early when
  the best pair occurs fewer than 2 times.
- `encode_word(word, merges)` — applies the merges in order to one word.
- `encode(text, merges)` — encodes every word and concatenates the tokens.
- `decode(tokens)` — joins tokens, turning each `"</w>"` into a space
  between words (no trailing space).

Where this spec is ambiguous, the tests are the final word.
