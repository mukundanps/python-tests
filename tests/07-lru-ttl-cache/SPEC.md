# Practice Test 7 — LRU Cache with TTL (sprint)

Time limit: 15 minutes. Fix `cache.py` so that `test_cache.py` passes.
Run from the repo root: `python3 scripts/run.py 07`

## Spec

`LRUCache(capacity, ttl=None)` holds at most `capacity` entries
(`capacity <= 0` raises `ValueError`). The current time is passed to each
call as `now`; the cache never reads a clock.

- `put(key, value, now=0)` stores the value and makes the key the most
  recently used. With a `ttl`, the entry expires at `now + ttl`; storing
  an existing key again **refreshes** its expiry. When a new key would
  exceed capacity, expired entries are purged first, and if the cache is
  still full the **least** recently used key is evicted.
- `get(key, now=0, default=None)` returns the value and makes the key the
  most recently used, counting a hit. A missing key returns `default` and
  counts a miss. An entry is expired when `now >= expiry`; an expired
  entry is removed and treated as missing. `get` does not change expiry.
- `purge(now)` removes every expired entry and returns how many.
- `keys()` lists keys from least to most recently used. `len(cache)` is
  the number of stored entries.
- `hits`, `misses` count `get` results; `hit_rate()` is
  `hits / (hits + misses)`, or `0.0` before any `get`.

Where this spec is ambiguous, the tests are the final word.
