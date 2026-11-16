# Bug patterns

A cheat sheet of the small mistakes these tests plant. Claude Code adds to
it during `/walkthrough` and `/solve`. Re-read it before the assessment.

## How to read a failure

| What the test output shows | Likely pattern |
|---|---|
| Result off by exactly one item or one unit | Off-by-one in a range, slice or comparison |
| Right items, wrong order | Sort key sign, missing reverse, wrong tie-break |
| Only the tie or boundary case fails | `<` versus `<=`, or wrong tie-break |
| Simple cases pass, repeated or reused values fail | Assignment where accumulation is needed, or state not updated |
| `IndexError` on the last element | Bound uses `<=` where `<` is needed, or wrong index formula |
| Result is a mirror image of the expected one | Swapped arguments or operands |
| Value too small, as if only the last step counted | Running total not carried forward |
| Negative-number cases fail, positive pass | Floor versus truncation, sign of remainder |
| Expected exception not raised | Missing or inverted check, `and` versus `or` |
| Everything that depends on one helper fails | Fix the helper first: lowest layer wins |

## Patterns

| Pattern | Typical form | Where to look |
|---|---|---|
| Off-by-one in a loop bound | `range(n - 2)` for `range(n - 1)`, `[:k + 1]` for `[:k]` | Loops over adjacent pairs, slices that keep "the top k" |
| Wrong comparison at a boundary | `<` for `<=`, `>` for `>=` | Capacity checks, expiry times, interval ends, thresholds |
| Wrong tie-break | `>=` in an argmax, `-i` in a sort key, `max` for `min` | Any spec sentence containing "ties" |
| Sort direction | Missing `-` in a key, missing `reverse()` | Ranking, beam pruning, backtraced paths |
| Swapped operands or indices | `b ** a`, `table[len(b)][len(a)]`, `(new, old)` | Non-commutative operations, 2-D tables, result tuples |
| Wrong variable | `other.data` for `self.data`, `nxt` for `prev`, `lo` for `cursor` | Lines with two similar names |
| Assign versus accumulate | `x = y` for `x += y`, `+ 1` for `+ freq` | Counters, gradients, running sums |
| Running total dropped | `new = step` for `new = total + step` | Path costs, sequence scores |
| Wrong initial value | Table row filled with `0`, distances pre-filled with infinity | First row or column of a DP table, dictionaries of "seen" items |
| Wrong index formula | Heap parent `i // 2` for `(i - 1) // 2` | Array-backed trees, strides |
| State not updated | Counter never incremented, pointer advanced by 1 for 2 | Loops that consume input, tie-break counters |
| Wrong pointer advanced | Advancing the list that ends later | Two-pointer merges and intersections |
| Arithmetic rule | `//` for truncation, Python `%` sign, `/` versus `//`, `*` for `/` | Division, modulo, scaling by a temperature or rate |
| Wrong constant | Precedence value, smoothing term missing a factor | Tables of constants, denominators |
| Missing or inverted guard | No error raised, `and` for `or`, check on the wrong value | Input validation, end-of-loop checks |
| Wrong fallback or default | Unknown maps to the wrong id, default index is the last element | `dict.get` defaults, loop fall-through returns |
| Wrong order of traversal | Forward where reverse is needed | Backpropagation, backtracing, topological order |
| Stage reads stale input | A later step uses the original value, not the filtered one | Pipelines of several transformations |

## Routine for the assessment

1. Run the whole suite first. Note the pass count and which test classes fail.
2. Start with the lowest layer: the smallest helpers and their tests.
3. For one failing test, read the assertion diff, then the test, then the one function it calls.
4. Compare that function line by line with the spec sentence that covers it.
5. Make one change. Re-run. If the count drops, undo it.
6. If a bug resists for ten minutes, move to another failing test and return later.
7. Never edit the tests, and do not tidy code that works.
