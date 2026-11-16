---
description: Generate a new practice test (optional topic)
argument-hint: [topic]
---
Create the next practice test following every rule in CLAUDE.md.

Topic requested: $ARGUMENTS (if empty, read the README table and
PROGRESS.md, then choose an algorithm family not yet used that targets his
weak spots).

Steps: pick the next number; write the reference solution and tests in a
scratch location and make them pass; plant the bugs; create
`tests/<NN>-<slug>/` and `.reference/<NN>-<slug>/` (solution, `broken/`,
`BUGS.md`); run `python3 scripts/verify.py <NN>` until OK; update the README
table; commit. Then tell him only the topic, test count, starting score
and time limit. Do not describe the bugs.
