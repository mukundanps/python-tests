# Practice Test 8 — Intervals (sprint)

Time limit: 15 minutes. Fix `intervals.py` so that `test_intervals.py` passes.
Run from the repo root: `python3 scripts/run.py 08`

## Spec

An interval is a tuple `(start, end)` of integers and is **half-open**: it
contains `start` but not `end`. Intervals with `start >= end` are empty
and ignored. Input lists may be unsorted and overlapping; functions do not
modify their inputs.

- `merge(intervals)` — sorted list of disjoint intervals covering the same
  points. Overlapping **and touching** intervals (`(1, 3)` and `(3, 5)`)
  are joined.
- `insert(intervals, new)` — `merge` of the list plus one more interval.
- `total_length(intervals)` — number of covered points (each counted once).
- `intersect(a, b)` — merged list of the points covered by both lists.
  Intervals that only touch have no points in common.
- `contains(intervals, x)` — whether `x` lies in any interval.
- `gaps(intervals, lo, hi)` — the parts of the window `[lo, hi)` not
  covered by any interval, in order.

Where this spec is ambiguous, the tests are the final word.
