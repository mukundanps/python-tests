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
Do not open `.reference/` until you are done: it holds the solutions.

## Tests

| ID | Topic | Tests | Starts at | Time |
|----|-------|------:|----------:|-----:|
| 01 | Expression calculator (tokenizer, shunting-yard, RPN evaluator) | 38 | 18 | 45 min |
| 02 | Min-heap and Dijkstra shortest paths | 36 | 16 | 60 min |

## Adding tests with Claude Code

Open the repo in Claude Code and use:

- `/new-test [topic]` — generate, verify and register a new practice test
- `/hint <id> [test name]` — a graded hint, without the answer
- `/review <id>` — score the attempt and walk through what is still failing

`CLAUDE.md` holds the rules these follow.
