# 02 — planted bugs (9)

| # | Where | Bug | Fix |
|---|-------|-----|-----|
| 1 | `MinHeap.push` | counter never incremented, so ties are not FIFO | `self._counter += 1` |
| 2 | `_sift_up` | parent is `i // 2` | `(i - 1) // 2` |
| 3 | `_sift_down` | `right <= n` reads past the end | `right < n` |
| 4 | `Graph.add_edge` | `weight <= 0` rejects zero | `weight < 0` |
| 5 | `Graph.add_edge` | reverse edge stored as `(v, weight)` | `(u, weight)` |
| 6 | `_dijkstra` | `dist` pre-filled with `inf` for all nodes, so unreachable nodes look reached | start with `{src: 0}` and test `v not in dist` |
| 7 | `_dijkstra` | `nd = w` ignores the distance so far | `nd = d + w` |
| 8 | `shortest_path` | `and` in the unknown-node check | `or` |
| 9 | `shortest_path` | source never appended to the path | `path.append(src)` before reversing |
