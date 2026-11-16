# Practice-test repo: rules for Claude

The owner is practising for a proctored, timed assessment in which he must
debug a broken implementation of an algorithm until the provided `unittest`
suite passes. Score is the number of passing tests. In the real assessment
he has no AI help, no web search, no external editor and no libraries. His
practice time is short, so most tests are done as guided walkthroughs, not
full solo attempts.

## Modes

He picks the mode by command. With no command, assume **walkthrough**.

- **Solo** (`/hint`, `/review`). He fixes the file himself. Do not edit the
  implementation in `tests/<id>/` and do not reveal `.reference/` contents.
  Hints are graded, one level per request: (1) which test to look at and
  which function it exercises, (2) which lines to read and what to compare
  against the spec, (3) the nature of the mistake.
- **Walkthrough** (`/walkthrough <id>`). Go through the bugs one at a time
  in the order a good debugger would meet them (lowest layer first). For
  each: show the failing test name and assertion output, name the function
  to read, and ask him to spot the bug. If he answers, confirm or correct.
  If he says "show" or has no answer, reveal it. Then apply that one fix
  to `tests/<id>/`, re-run, report the new score, and add the pattern to
  `PATTERNS.md` if it is not already there. Never reveal more than one bug
  ahead.
- **Solve** (`/solve <id>`). Apply every fix, run the tests, and print one
  entry per bug: failing test that exposed it, the before and after line,
  and the pattern name. Update `PATTERNS.md`.

In every mode:

- Never edit `test_*.py` or weaken a test to make it pass.
- After a test is finished, say which patterns cost the most time and
  suggest what to practise next.
- Do not help with the real assessment or accept any of its content into
  this repo. Its terms forbid sharing details and using AI assistance.

## Layout

```
tests/<NN>-<slug>/SPEC.md            spec + time limit
tests/<NN>-<slug>/<module>.py        broken implementation (the file to fix)
tests/<NN>-<slug>/test_<module>.py   unittest suite (read-only)
.reference/<NN>-<slug>/solution_<module>.py   correct implementation
.reference/<NN>-<slug>/bugs.py       planted bugs as find/replace pairs
.reference/<NN>-<slug>/broken/<module>.py     pristine broken copy (generated)
.reference/<NN>-<slug>/BUGS.md       bug table (generated)
scripts/run.py      run a test and print the score
scripts/reset.py    restore the broken file
scripts/plant.py    build broken file and BUGS.md from solution + bugs.py
scripts/verify.py   check solution, broken version and every single bug
PATTERNS.md         bug-pattern cheat sheet
PROGRESS.md         score log
```

Tests 01 and 02 predate `plant.py` and have a hand-written `BUGS.md` and
no `bugs.py`.

## Rules for a new test

1. Standard library only; tests use `unittest`; Python 3.8+ syntax.
2. Write and test the correct implementation first as
   `.reference/<name>/solution_<module>.py`. Write the bugs as find/replace
   pairs in `bugs.py` and run `python3 scripts/plant.py <NN>`. Never write
   the broken version by hand.
3. Sizes:

   | Size | Implementation | Tests | Bugs | Time limit |
   |------|---------------:|------:|-----:|-----------:|
   | sprint | 60-120 lines | 20-30 | 5-7 | 15 min |
   | full | 120-300 lines | 30-50 | 8-14 | 45-90 min |
   | rehearsal | 150-400 lines | 45-70 | 14-20 | 75-120 min |

   Default to sprint. Offer a rehearsal after every five or six sprints.
4. The code has layers (helpers, a core structure, a top-level function)
   and the tests cover each layer separately, so failures localise bugs.
5. Every bug is a small local change that some test detects: off-by-one,
   wrong comparison operator, swapped arguments, `and`/`or`, wrong index
   formula, missing state update, wrong initial value, wrong sign or
   rounding rule, missing error check, wrong tie-break, assignment where
   accumulation is needed, wrong iteration order. No syntax errors and
   nothing that needs a rewrite.
6. Bugs fail different subsets of tests; a few may mask each other. The
   broken version passes roughly 30-65% of tests at the start.
7. Tests are deterministic and fast, with names that state the behaviour.
   The spec states every rule a test relies on, and the tests win where
   the spec is vague. Compare floats with `assertAlmostEqual`, and never
   depend on the order of mathematically equal floats computed two ways.
8. Topics. The assessment is for an AI company, so favour algorithms from
   that work, and vary the family from test to test (check the README
   table):
   - tokenization and text: BPE, WordPiece-style longest match, tries,
     chunking with overlap, n-gram counting
   - decoding and sampling: top-k, top-p, beam search, repetition penalty,
     constrained decoding, stop sequences
   - numerical core: matrix multiply, broadcasting, autograd, optimisers
     (SGD with momentum, Adam), cross-entropy, layer norm, attention
     scores in plain lists
   - classic ML: k-means, k-nearest neighbours, Viterbi, naive Bayes,
     decision-tree split, edit distance, TF-IDF, cosine similarity search
   - serving and infrastructure: LRU/LFU caches, token-bucket or sliding
     window rate limiters, request batching, priority schedulers,
     consistent hashing, retry with backoff
   - data handling: streaming parsers and state machines, deduplication,
     reservoir sampling, top-k with a heap, interval structures, run-length
     coding, topological sort, union-find
9. Run `python3 scripts/verify.py <NN>` and get `OK` before committing: it
   checks the solution passes everything, the broken version passes only
   part, and each bug alone fails at least one test. Add the row to the
   README table. Commit the test and its `.reference/` folder together.
10. Use `PROGRESS.md` and `PATTERNS.md` to aim the next test at the
    patterns that slowed him down.
