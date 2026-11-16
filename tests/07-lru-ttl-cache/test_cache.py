import unittest

from cache import LRUCache


class TestBasics(unittest.TestCase):
    def test_capacity_must_be_positive(self):
        with self.assertRaises(ValueError):
            LRUCache(0)

    def test_put_get(self):
        c = LRUCache(2)
        c.put("a", 1)
        self.assertEqual(c.get("a"), 1)

    def test_missing_returns_default(self):
        c = LRUCache(2)
        self.assertIsNone(c.get("a"))
        self.assertEqual(c.get("a", default=-1), -1)

    def test_len(self):
        c = LRUCache(3)
        c.put("a", 1)
        c.put("b", 2)
        self.assertEqual(len(c), 2)

    def test_overwrite_value(self):
        c = LRUCache(2)
        c.put("a", 1)
        c.put("a", 9)
        self.assertEqual(c.get("a"), 9)
        self.assertEqual(len(c), 1)


class TestRecency(unittest.TestCase):
    def test_keys_in_insertion_order(self):
        c = LRUCache(3)
        for k in "abc":
            c.put(k, k)
        self.assertEqual(c.keys(), ["a", "b", "c"])

    def test_get_makes_most_recent(self):
        c = LRUCache(3)
        for k in "abc":
            c.put(k, k)
        c.get("a")
        self.assertEqual(c.keys(), ["b", "c", "a"])

    def test_overwrite_makes_most_recent(self):
        c = LRUCache(3)
        for k in "abc":
            c.put(k, k)
        c.put("b", "B")
        self.assertEqual(c.keys(), ["a", "c", "b"])


class TestEviction(unittest.TestCase):
    def test_never_exceeds_capacity(self):
        c = LRUCache(2)
        for k in "abcd":
            c.put(k, k)
        self.assertEqual(len(c), 2)

    def test_evicts_least_recent(self):
        c = LRUCache(2)
        c.put("a", 1)
        c.put("b", 2)
        c.put("c", 3)
        self.assertEqual(c.keys(), ["b", "c"])
        self.assertIsNone(c.get("a"))

    def test_get_protects_from_eviction(self):
        c = LRUCache(2)
        c.put("a", 1)
        c.put("b", 2)
        c.get("a")
        c.put("c", 3)
        self.assertEqual(c.keys(), ["a", "c"])

    def test_capacity_one(self):
        c = LRUCache(1)
        c.put("a", 1)
        c.put("b", 2)
        self.assertEqual(c.keys(), ["b"])


class TestTTL(unittest.TestCase):
    def test_no_ttl_never_expires(self):
        c = LRUCache(2)
        c.put("a", 1, now=0)
        self.assertEqual(c.get("a", now=10 ** 9), 1)

    def test_alive_before_expiry(self):
        c = LRUCache(2, ttl=10)
        c.put("a", 1, now=5)
        self.assertEqual(c.get("a", now=14), 1)

    def test_expired_at_exact_time(self):
        c = LRUCache(2, ttl=10)
        c.put("a", 1, now=5)
        self.assertIsNone(c.get("a", now=15))

    def test_expired_entry_is_removed(self):
        c = LRUCache(2, ttl=10)
        c.put("a", 1, now=0)
        c.get("a", now=50)
        self.assertEqual(len(c), 0)

    def test_overwrite_refreshes_expiry(self):
        c = LRUCache(2, ttl=10)
        c.put("a", 1, now=0)
        c.put("a", 2, now=8)
        self.assertEqual(c.get("a", now=12), 2)

    def test_get_does_not_refresh_expiry(self):
        c = LRUCache(2, ttl=10)
        c.put("a", 1, now=0)
        c.get("a", now=8)
        self.assertIsNone(c.get("a", now=12))

    def test_purge_returns_count(self):
        c = LRUCache(5, ttl=10)
        c.put("a", 1, now=0)
        c.put("b", 2, now=3)
        c.put("c", 3, now=9)
        self.assertEqual(c.purge(now=13), 2)
        self.assertEqual(c.keys(), ["c"])

    def test_put_purges_expired_before_evicting(self):
        c = LRUCache(2, ttl=10)
        c.put("old", 1, now=0)
        c.put("live", 2, now=9)
        c.get("old", now=9)
        c.put("new", 3, now=12)
        self.assertEqual(c.keys(), ["live", "new"])


class TestStats(unittest.TestCase):
    def test_empty_hit_rate(self):
        self.assertEqual(LRUCache(1).hit_rate(), 0.0)

    def test_counts(self):
        c = LRUCache(2)
        c.put("a", 1)
        c.get("a")
        c.get("a")
        c.get("zzz")
        self.assertEqual((c.hits, c.misses), (2, 1))

    def test_hit_rate(self):
        c = LRUCache(2)
        c.put("a", 1)
        c.get("a")
        c.get("b")
        c.get("c")
        c.get("d")
        self.assertEqual(c.hit_rate(), 0.25)

    def test_expired_lookup_is_a_miss(self):
        c = LRUCache(2, ttl=5)
        c.put("a", 1, now=0)
        c.get("a", now=99)
        self.assertEqual((c.hits, c.misses), (0, 1))


if __name__ == "__main__":
    unittest.main()
