"""A small bigram language model: tokenizer, vocabulary, add-k smoothed
probabilities, perplexity, greedy generation and beam search."""
import math

BOS = "<s>"
EOS = "</s>"
UNK = "<unk>"
BOS_ID = 0
EOS_ID = 1
UNK_ID = 2
PUNCTUATION = ".,!?"


# ---------------------------------------------------------------- tokenizer

def tokenize(text):
    tokens = []
    for raw in text.split(" "):
        word = raw.strip(PUNCTUATION).lower()
        if word:
            tokens.append(word)
    return tokens


# --------------------------------------------------------------- vocabulary

class Vocab:
    def __init__(self, min_count=1):
        self.min_count = min_count
        self.id_to_token = [BOS, EOS, UNK]
        self.token_to_id = {BOS: BOS_ID, EOS: EOS_ID, UNK: UNK_ID}

    def __len__(self):
        return len(self.id_to_token)

    def build(self, sentences):
        counts = {}
        for sentence in sentences:
            for token in tokenize(sentence):
                counts[token] = counts.get(token, 0) + 1
        for token in sorted(counts, key=lambda t: (counts[t], t)):
            if counts[token] > self.min_count and token not in self.token_to_id:
                self.token_to_id[token] = len(self.id_to_token)
                self.id_to_token.append(token)
        return self

    def encode(self, tokens):
        return [self.token_to_id.get(token, BOS_ID) for token in tokens]

    def decode(self, ids):
        return [self.id_to_token[i] for i in ids if i > UNK_ID]


# -------------------------------------------------------------------- model

class BigramModel:
    def __init__(self, vocab, k=1.0):
        if k <= 0:
            raise ValueError("k must be positive")
        self.vocab = vocab
        self.k = k
        self.counts = {}   # prev id -> {next id: count}
        self.totals = {}   # prev id -> number of bigrams starting with it

    def _ids(self, tokens):
        return [BOS_ID] + self.vocab.encode(tokens) + [EOS_ID]

    def train(self, sentences):
        for sentence in sentences:
            ids = self._ids(tokenize(sentence))
            for i in range(len(ids) - 2):
                prev, nxt = ids[i], ids[i + 1]
                row = self.counts.setdefault(prev, {})
                row[nxt] = row.get(nxt, 0) + 1
                self.totals[nxt] = self.totals.get(nxt, 0) + 1
        return self

    def count(self, prev, nxt):
        return self.counts.get(prev, {}).get(nxt, 0)

    def prob(self, prev, nxt):
        total = self.totals.get(prev, 0)
        return (self.count(prev, nxt) + self.k) / (total + self.k)

    def log_prob(self, prev, nxt):
        return math.log(self.prob(prev, nxt))

    def sentence_log_prob(self, tokens):
        ids = self._ids(tokens)
        total = 0.0
        for i in range(1, len(ids) - 1):
            total += self.log_prob(ids[i], ids[i + 1])
        return total

    def perplexity(self, tokens):
        transitions = len(tokens)
        return math.exp(-self.sentence_log_prob(tokens) / transitions)

    def next_distribution(self, prev):
        return [self.prob(prev, nxt) for nxt in range(len(self.vocab))]

    def top_next(self, prev, n):
        probs = self.next_distribution(prev)
        ids = [i for i in range(len(probs)) if i != BOS_ID]
        ids.sort(key=lambda i: (-probs[i], -i))
        return ids[:n]


# --------------------------------------------------------------- generation

def greedy_generate(model, max_len, start=()):
    ids = [BOS_ID] + model.vocab.encode(list(start))
    out = list(start)
    while len(out) <= max_len:
        nxt = model.top_next(ids[-1], 1)[0]
        if nxt == EOS_ID:
            break
        ids.append(nxt)
        out.append(model.vocab.id_to_token[nxt])
    return out


def beam_search(model, beam_width, max_len):
    if beam_width <= 0:
        raise ValueError("beam_width must be positive")
    live = [(0.0, [BOS_ID])]
    finished = []
    for _ in range(max_len):
        candidates = []
        for score, ids in live:
            for nxt in range(len(model.vocab)):
                if nxt == BOS_ID:
                    continue
                new_score = model.log_prob(ids[-1], nxt)
                if nxt == EOS_ID:
                    finished.append((new_score, ids[1:]))
                else:
                    candidates.append((new_score, ids + [nxt]))
        candidates.sort(key=lambda c: (c[0], c[1]))
        live = candidates[:beam_width]
    for score, ids in live:
        finished.append((score, ids[1:]))
    finished.sort(key=lambda c: (-c[0], c[1]))
    return [(model.vocab.decode(ids), score) for score, ids in finished[:beam_width]]
