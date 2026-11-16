"""Byte-pair encoding: learn merges from text, then encode and decode."""

END = "</w>"


def get_pair_counts(words):
    """words maps a tuple of symbols to its frequency."""
    counts = {}
    for symbols, freq in words.items():
        for i in range(len(symbols) - 2):
            pair = (symbols[i], symbols[i + 1])
            counts[pair] = counts.get(pair, 0) + 1
    return counts


def best_pair(counts):
    if not counts:
        return None
    return max(counts, key=lambda p: (counts[p], p))


def merge_symbols(symbols, pair):
    out = []
    i = 0
    while i < len(symbols):
        if i < len(symbols) - 1 and (symbols[i], symbols[i + 1]) == pair:
            out.append(symbols[i] + symbols[i + 1])
            i += 1
        else:
            out.append(symbols[i])
            i += 1
    return tuple(out)


def train(text, num_merges):
    words = {}
    for word in text.split():
        key = tuple(word) + (END,)
        words[key] = words.get(key, 0) + 1
    merges = []
    for _ in range(num_merges):
        counts = get_pair_counts(words)
        pair = best_pair(counts)
        if pair is None or counts[pair] <= 2:
            break
        merges.append(pair)
        new_words = {}
        for symbols, freq in words.items():
            merged = merge_symbols(symbols, pair)
            new_words[merged] = new_words.get(merged, 0) + freq
        words = new_words
    return merges


def encode_word(word, merges):
    symbols = tuple(word) + (END,)
    for pair in merges:
        symbols = merge_symbols(symbols, pair)
    return list(symbols)


def encode(text, merges):
    tokens = []
    for word in text.split():
        tokens.extend(encode_word(word, merges))
    return tokens


def decode(tokens):
    return "".join(tokens).replace(END, "").strip()
