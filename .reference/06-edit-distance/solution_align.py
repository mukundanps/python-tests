"""Levenshtein edit distance, edit script, similarity and nearest match."""


def edit_table(a, b):
    rows, cols = len(a) + 1, len(b) + 1
    table = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        table[i][0] = i
    for j in range(cols):
        table[0][j] = j
    for i in range(1, rows):
        for j in range(1, cols):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            table[i][j] = min(
                table[i - 1][j] + 1,
                table[i][j - 1] + 1,
                table[i - 1][j - 1] + cost,
            )
    return table


def edit_distance(a, b):
    return edit_table(a, b)[len(a)][len(b)]


def edit_ops(a, b):
    table = edit_table(a, b)
    i, j = len(a), len(b)
    ops = []
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            same = a[i - 1] == b[j - 1]
            if table[i][j] == table[i - 1][j - 1] + (0 if same else 1):
                if same:
                    ops.append(("keep", a[i - 1]))
                else:
                    ops.append(("sub", a[i - 1], b[j - 1]))
                i -= 1
                j -= 1
                continue
        if i > 0 and table[i][j] == table[i - 1][j] + 1:
            ops.append(("del", a[i - 1]))
            i -= 1
        else:
            ops.append(("ins", b[j - 1]))
            j -= 1
    ops.reverse()
    return ops


def similarity(a, b):
    longest = max(len(a), len(b))
    if longest == 0:
        return 1.0
    return 1.0 - edit_distance(a, b) / longest


def closest(word, candidates):
    best = None
    best_distance = None
    for candidate in candidates:
        d = edit_distance(word, candidate)
        if best_distance is None or d < best_distance:
            best = candidate
            best_distance = d
    return best
