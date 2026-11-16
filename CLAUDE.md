# Practice-test repo: rules for Claude

The owner is practising for a proctored, timed assessment in which he must
debug a broken implementation of an algorithm until the provided `unittest`
suite passes. Score is the number of passing tests. In the real assessment
he has no AI help, no web search, no external editor and no libraries, so
practice here must build his own unaided debugging skill.

## Learner mode (always on)

- Never edit the implementation file inside `tests/<id>/`. He fixes it.
- Never reveal or paraphrase `.reference/` contents (solutions, `BUGS.md`)
  unless he explicitly asks for the answer to a specific bug after trying.
- Hints are graded: (1) which test to look at and which function it
  exercises, (2) which lines to read and what to compare against the spec,
  (3) the nature of the mistake. Give one level per request.
- After an attempt, review the process as well as the result: order of
  fixes, time lost, whether tests were re-run after each change.
- Do not help with the real assessment or accept any of its content into
  this repo. Its terms forbid sharing details and using AI assistance.

## Layout

```
tests/<NN>-<slug>/SPEC.md            spec + time limit
tests/<NN>-<slug>/<module>.py        broken implementation (he edits this)
tests/<NN>-<slug>/test_<module>.py   unittest suite (read-only)
.reference/<NN>-<slug>/solution_<module>.py   correct implementation
.reference/<NN>-<slug>/broken/<module>.py     pristine broken copy
.reference/<NN>-<slug>/BUGS.md       planted bugs and fixes
scripts/run.py | reset.py | verify.py
PROGRESS.md                          score log
```

## Rules for a new test

1. Standard library only; tests use `unittest`; Python 3.8+ syntax.
2. Write and test the correct implementation first, then derive the broken
   one from it by planting bugs. Never write the broken version directly.
3. Size: 120-300 lines of implementation, 30-50 tests, 8-14 bugs, time
   limit 45-90 minutes. Increase size as his scores improve.
4. The code has layers (helpers, a core structure, a top-level function)
   and the tests cover each layer separately, so failures localise bugs.
5. Every bug is a small local change that some test detects: off-by-one,
   wrong comparison operator, swapped arguments, `and`/`or`, wrong index
   formula, missing state update, wrong initial value, wrong sign or
   rounding rule, missing error check, wrong tie-break. No syntax errors
   and nothing that needs a rewrite.
6. Bugs fail different subsets of tests; a few may mask each other. The
   broken version must pass 30-60% of tests at the start.
7. Tests are deterministic and fast, with names that state the behaviour.
   The spec states every rule a test relies on, and the tests win where
   the spec is vague.
8. Vary the algorithm family between tests. Check the README table and
   pick something different: interval structures, LRU/LFU caches, tries,
   union-find, topological sort, BFS/DFS on grids, binary search variants,
   text wrapping or diffing, run-length or Huffman coding, matrix
   operations, big-integer arithmetic, simple parsers and state machines,
   schedulers, sliding windows, dynamic programming.
9. Run `python3 scripts/verify.py` and get `OK` for the new test before
   committing. Add the row to the README table. Commit the test and its
   `.reference/` folder together.
10. Use `PROGRESS.md` notes to aim the next test at what slowed him down.
