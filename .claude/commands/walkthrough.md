---
description: Guided bug-by-bug walkthrough of a practice test
argument-hint: <id>
---
Run walkthrough mode (see CLAUDE.md) for test $ARGUMENTS.

Start with `python3 scripts/run.py $ARGUMENTS -v` and show the score and
the list of failing tests grouped by test class. Read
`.reference/<name>/BUGS.md` privately to plan the order, lowest layer
first. Then handle one bug per turn: failing test and its assertion
output, the function to read, and a prompt for him to name the bug. Wait
for his answer or "show". Then explain, apply that single fix, re-run,
report the score, and record the pattern in PATTERNS.md. When all tests
pass, summarise which patterns he spotted himself and which he did not,
and offer to log the result with `python3 scripts/run.py <id> --log`.
