"""LRU cache with optional time-to-live. Time is passed in explicitly."""


class LRUCache:
    def __init__(self, capacity, ttl=None):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.ttl = ttl
        self._data = {}   # key -> (value, expires_at or None)
        self._order = []  # least recently used first
        self.hits = 0
        self.misses = 0

    def __len__(self):
        return len(self._data)

    def keys(self):
        return list(self._order)

    def _touch(self, key):
        self._order.remove(key)
        self._order.insert(0, key)

    def _remove(self, key):
        del self._data[key]
        self._order.remove(key)

    def _expired(self, key, now):
        expires_at = self._data[key][1]
        return expires_at is not None and now > expires_at

    def _expiry(self, now):
        return None if self.ttl is None else now + self.ttl

    def get(self, key, now=0, default=None):
        if key in self._data and self._expired(key, now):
            self._remove(key)
        if key not in self._data:
            self.hits += 1
            return default
        self.hits += 1
        self._touch(key)
        return self._data[key][0]

    def put(self, key, value, now=0):
        if key in self._data:
            self._data[key] = (value, self._data[key][1])
            self._touch(key)
            return
        self.purge(now)
        if len(self._data) > self.capacity:
            self._remove(self._order[-1])
        self._data[key] = (value, self._expiry(now))
        self._order.append(key)

    def purge(self, now):
        expired = [key for key in self._order if self._expired(key, now)]
        for key in expired:
            self._remove(key)
        return len(expired)

    def hit_rate(self):
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return self.hits // total
