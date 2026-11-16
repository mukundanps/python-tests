---
description: Score an attempt and review what is still failing
argument-hint: <id>
---
Review his attempt at test $ARGUMENTS.

Run `python3 scripts/run.py $ARGUMENTS -v`. Report the score. For each test
still failing, say which behaviour in the spec it checks and where to look,
at hint level 1-2. Compare his file with `.reference/<id>/broken/` to see
which bugs he fixed and whether any fix is wider than needed; do not reveal
the remaining bugs. Ask how long it took and what slowed him down, then
offer to log it with `python3 scripts/run.py <id> --log` and add his notes
to PROGRESS.md.
