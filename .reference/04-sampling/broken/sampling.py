"""Next-token selection: softmax, greedy, top-k, top-p, inverse-CDF sampling."""
import math


def softmax(logits, temperature=1.0):
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    scaled = [x * temperature for x in logits]
    m = max(scaled)
    exps = [math.exp(x - m) for x in scaled]
    total = sum(exps)
    return [e / total for e in exps]


def argmax(values):
    best = 0
    for i in range(1, len(values)):
        if values[i] >= values[best]:
            best = i
    return best


def _ranked(probs):
    return sorted(range(len(probs)), key=lambda i: (-probs[i], i))


def _renormalise(probs, keep):
    kept = [p if i in keep else 0.0 for i, p in enumerate(probs)]
    total = sum(kept)
    return [p / total for p in kept]


def top_k(probs, k):
    if k <= 0:
        raise ValueError("k must be positive")
    keep = set(_ranked(probs)[:k + 1])
    return _renormalise(probs, keep)


def top_p(probs, p):
    if not 0 < p <= 1:
        raise ValueError("p must be in (0, 1]")
    keep = set()
    cumulative = 0.0
    for i in _ranked(probs):
        keep.add(i)
        cumulative += probs[i]
        if cumulative > p:
            break
    return _renormalise(probs, keep)


def sample(probs, u):
    cumulative = 0.0
    last = 0
    for i, p in enumerate(probs):
        last = i
        cumulative += p
        if u <= cumulative:
            return i
    return last


def next_token(logits, u, temperature=1.0, k=None, p=None):
    if temperature == 0:
        return argmax(logits)
    probs = softmax(logits, temperature)
    if k is not None:
        probs = top_k(probs, k)
    if p is not None:
        probs = top_p(softmax(logits, temperature), p)
    return sample(probs, u)
