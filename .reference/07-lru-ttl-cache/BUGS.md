# 07-lru-ttl-cache — planted bugs (7)

| # | Where | Bug | Fix |
|---|-------|-----|-----|
| 1 | _touch | moves the key to the least-recent end | self._order.append(key) |
| 2 | _expired | `>` keeps an entry alive at exactly its expiry time | now >= expires_at |
| 3 | get | a missing or expired lookup increments hits instead of misses | self.misses += 1 |
| 4 | put, existing key | keeps the old expiry instead of refreshing it | (value, self._expiry(now)) |
| 5 | put, eviction check | `>` lets the cache grow to capacity + 1 | len(self._data) >= self.capacity |
| 6 | put, eviction | evicts the most recently used key | self._order[0] |
| 7 | hit_rate | integer division | self.hits / total |
