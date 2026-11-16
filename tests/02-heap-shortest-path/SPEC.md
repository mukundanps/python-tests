# Practice Test 2 — Min-Heap and Shortest Paths

Time limit: 60 minutes. Fix `routes.py` so that `test_routes.py` passes.
Score = number of passing tests.

Run from the repo root: `python3 scripts/run.py 02`
(or, inside this folder: `python3 -m unittest -v test_routes`)

## Spec

### `MinHeap`
A binary min-heap stored in a list, holding `(priority, item)` pairs.

- `push(priority, item)` adds an entry.
- `pop()` removes and returns the `(priority, item)` with the smallest
  priority. `peek()` returns it without removing it.
- Entries with **equal priority come out in the order they were pushed**
  (FIFO). Items are never compared with each other, so they may be of any
  type (including unorderable ones such as dicts).
- `pop()` / `peek()` on an empty heap raise `IndexError`.
- `len(heap)` is the number of entries.
- Array layout: children of index `i` are `2i + 1` and `2i + 2`.

### `Graph`
- `add_node(u)` adds an isolated node (no-op if present).
- `add_edge(u, v, weight, directed=False)` adds both nodes if needed and an
  edge `u -> v`. When `directed` is false it also adds `v -> u` with the
  same weight.
- Weights must be `>= 0`; a negative weight raises `ValueError`.
- `nodes()` returns the sorted node list.
- `neighbors(u)` returns the sorted list of `(neighbor, weight)` pairs;
  unknown `u` raises `KeyError`.

### `distances(graph, src) -> dict`
Shortest distance from `src` to every node **reachable** from it
(including `src` itself at distance 0). Unreachable nodes do not appear.
Unknown `src` raises `KeyError`.

### `shortest_path(graph, src, dst) -> (distance, path)`
- `path` is the node list from `src` to `dst` inclusive.
- `src == dst` gives `(0, [src])`.
- Unreachable `dst` gives `(None, [])`.
- If **either** `src` or `dst` is not in the graph, raises `KeyError`.

Where this spec is ambiguous, the tests are the final word.
