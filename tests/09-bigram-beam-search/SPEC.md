# Practice Test 9 — Bigram Language Model and Beam Search (dress rehearsal)

Time limit: 75 minutes. Fix `lm.py` so that `test_lm.py` passes.
Run from the repo root: `python3 scripts/run.py 09`

This one is larger than the sprints: about 150 lines in four layers.
Work from the bottom layer up.

## Spec

Special tokens and their fixed ids: `<s>` = 0 (start of sentence, BOS),
`</s>` = 1 (end of sentence, EOS), `<unk>` = 2 (unknown word).

### `tokenize(text)`
Splits on any whitespace, strips the characters `.,!?` from both ends of
each piece, lowercases it, and drops pieces that end up empty.

### `Vocab(min_count=1)`
- Starts with the three special tokens.
- `build(sentences)` tokenizes every sentence, counts tokens, and adds
  each token whose count is `>= min_count`. Tokens are added in order of
  **descending count, then alphabetically**. Returns the vocab.
- `encode(tokens)` maps tokens to ids; unknown tokens become `<unk>`.
- `decode(ids)` maps ids to tokens, omitting `<s>` and `</s>` (but
  keeping `<unk>`).
- `len(vocab)` is the number of tokens including the specials.

### `BigramModel(vocab, k=1.0)`
`k` is the add-k smoothing constant and must be `> 0` (`ValueError`).

- `train(sentences)` — each sentence becomes
  `<s> tok1 ... tokN </s>` and every adjacent pair is counted.
  `count(prev, nxt)` is the pair count; `totals[prev]` is the number of
  pairs that start with `prev`. Returns the model.
- `prob(prev, nxt) = (count(prev, nxt) + k) / (totals[prev] + k * V)`
  where `V = len(vocab)`. A context never seen in training has total 0,
  so its distribution is uniform.
- `log_prob` is the natural log of `prob`.
- `sentence_log_prob(tokens)` — sum of `log_prob` over every transition of
  `<s> tokens </s>`, i.e. `len(tokens) + 1` transitions.
- `perplexity(tokens) = exp(-sentence_log_prob / (len(tokens) + 1))`.
- `next_distribution(prev)` — list of `prob(prev, i)` for every id `i`.
- `top_next(prev, n)` — the `n` most probable next ids, never `<s>`;
  ties go to the lower id.

### `greedy_generate(model, max_len, start=())`
Starting after `<s>` and the `start` tokens, repeatedly appends the single
most probable next token. Stops when that token is `</s>` (not included)
or when the output has `max_len` tokens. Returns the token list, including
the `start` tokens.

### `beam_search(model, beam_width, max_len)`
Returns up to `beam_width` complete sentences as `(tokens, score)` pairs,
best first. `beam_width <= 0` raises `ValueError`.

- A hypothesis is a sequence of ids starting with `<s>`; its score is the
  **sum** of the log-probabilities of all its transitions.
- Each step extends every live hypothesis with every id except `<s>`.
  Extensions ending in `</s>` are complete and move to the finished pool.
  Of the rest, the `beam_width` highest-scoring stay live (ties: the
  smaller id sequence first).
- After `max_len` steps, each hypothesis still live is completed by adding
  the log-probability of moving from its last token to `</s>`.
- The finished pool is ranked by score, highest first (ties: smaller id
  sequence), and the top `beam_width` are returned with tokens decoded.
  A complete hypothesis's score therefore equals `sentence_log_prob` of
  its tokens.

Where this spec is ambiguous, the tests are the final word.
