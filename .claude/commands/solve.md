---
description: Fix every bug in a practice test and explain each one
argument-hint: <id>
---
Run solve mode (see CLAUDE.md) for test $ARGUMENTS.

Run `python3 scripts/run.py $ARGUMENTS -v`, apply every fix to the file in
`tests/<name>/`, and re-run until all tests pass. Then print one entry per
bug, lowest layer first: the test that exposed it, the line before and
after, and the pattern name from PATTERNS.md (add the pattern if it is
new). Finish with the three patterns most worth remembering from this
test. He can redo it later with `python3 scripts/reset.py <id>`.
