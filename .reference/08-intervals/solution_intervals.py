"""Operations on half-open integer intervals [start, end)."""


def merge(intervals):
    merged = []
    for start, end in sorted(intervals):
        if start >= end:
            continue
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


def insert(intervals, new):
    return merge(list(intervals) + [new])


def total_length(intervals):
    return sum(end - start for start, end in merge(intervals))


def intersect(a, b):
    a = merge(a)
    b = merge(b)
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        lo = max(a[i][0], b[j][0])
        hi = min(a[i][1], b[j][1])
        if lo < hi:
            out.append((lo, hi))
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return out


def contains(intervals, x):
    merged = merge(intervals)
    lo, hi = 0, len(merged)
    while lo < hi:
        mid = (lo + hi) // 2
        start, end = merged[mid]
        if x < start:
            hi = mid
        elif x >= end:
            lo = mid + 1
        else:
            return True
    return False


def gaps(intervals, lo, hi):
    out = []
    cursor = lo
    for start, end in merge(intervals):
        if end <= lo:
            continue
        if start >= hi:
            break
        if start > cursor:
            out.append((cursor, start))
        cursor = max(cursor, end)
    if cursor < hi:
        out.append((cursor, hi))
    return out
