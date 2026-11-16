# python-tests

Practice for a timed "debug a broken implementation until the unit tests
pass" assessment: plain Python, built-in `unittest`, no libraries.

Each folder under `tests/` is one practice test:

- `SPEC.md` — what the code is supposed to do, and the time limit
- one broken implementation file — the only file you edit
- `test_*.py` — the tests; read them, never edit them

## Taking a test

```
python3 scripts/run.py 02          # run test 02 and print the score
python3 scripts/run.py 02 -v       # same, listing every test
python3 scripts/run.py 02 --log    # also record the score in PROGRESS.md
python3 scripts/reset.py 02        # put the broken file back to redo it
```

Start a timer, run the tests first, fix one thing at a time, re-run.
`.reference/` holds the solutions; leave it closed during a solo attempt.
`PATTERNS.md` is the cheat sheet of bug patterns and the debugging routine.

## Tests

| ID | Size | Topic | Tests | Starts at | Time |
|----|------|-------|------:|----------:|-----:|
| 01 | full | Expression calculator (tokenizer, shunting-yard, RPN evaluator) | 38 | 18 | 45 min |
| 02 | full | Min-heap and Dijkstra shortest paths | 36 | 16 | 60 min |
| 03 | sprint | Byte-pair encoding tokenizer | 23 | 7 | 15 min |
| 04 | sprint | Next-token sampling (softmax, top-k, top-p) | 30 | 15 | 15 min |
| 05 | sprint | Scalar autograd and SGD | 24 | 11 | 15 min |
| 06 | sprint | Edit distance and edit script | 30 | 10 | 15 min |
| 07 | sprint | LRU cache with TTL | 24 | 12 | 15 min |
| 08 | sprint | Interval merge, intersect, gaps | 30 | 19 | 15 min |
| 09 | rehearsal | Bigram language model and beam search | 50 | 15 | 75 min |

## Working with Claude Code

Open the repo in Claude Code and use:

- `/walkthrough <id>` — bug by bug: you get a moment to spot each one, then
  Claude explains it, applies the fix and re-runs (the quick way to learn)
- `/solve <id>` — Claude fixes everything and explains each bug
- `/hint <id> [test name]` — a graded hint during a solo attempt
- `/review <id>` — score a solo attempt and point at what is still failing
- `/new-test [sprint|full|rehearsal] [topic]` — generate, verify and
  register a new practice test

`CLAUDE.md` holds the rules these follow.
