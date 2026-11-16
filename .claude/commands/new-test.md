---
description: Generate a new practice test (optional size and topic)
argument-hint: [sprint|full|rehearsal] [topic]
---
Create the next practice test following every rule in CLAUDE.md.

Requested: $ARGUMENTS (size defaults to sprint; if no topic is given, read
the README table, PROGRESS.md and PATTERNS.md, then choose a family not
yet used that targets his weak patterns).

Steps: pick the next number; write `.reference/<NN>-<slug>/solution_*.py`
and `tests/<NN>-<slug>/test_*.py` and make the tests pass against the
solution; write `bugs.py`; run `python3 scripts/plant.py <NN>`; write
`SPEC.md`; run `python3 scripts/verify.py <NN>` until OK; update the README
table; commit. Then tell him only the topic, size, test count, starting
score and time limit. Do not describe the bugs.
