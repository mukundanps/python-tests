# 09-bigram-beam-search — planted bugs (15)

| # | Where | Bug | Fix |
|---|-------|-----|-----|
| 1 | tokenize | splits on single spaces only, so tabs and newlines stay inside tokens | text.split() |
| 2 | Vocab.build | orders tokens by ascending count | key=(-count, token) |
| 3 | Vocab.build | `>` drops tokens whose count equals min_count | counts[token] >= self.min_count |
| 4 | Vocab.encode | unknown tokens map to BOS_ID | UNK_ID |
| 5 | Vocab.decode | also drops <unk> | i > EOS_ID |
| 6 | BigramModel.train | loop stops one bigram early, so the transition into </s> is never counted | range(len(ids) - 1) |
| 7 | BigramModel.train | totals are keyed by the next token | self.totals[prev] |
| 8 | BigramModel.prob | smoothing denominator adds k once instead of k * vocabulary size | total + self.k * len(self.vocab) |
| 9 | BigramModel.sentence_log_prob | skips the first transition (<s> to the first token) | range(len(ids) - 1) |
| 10 | BigramModel.perplexity | divides by the token count, omitting the </s> transition | len(tokens) + 1 |
| 11 | BigramModel.top_next | ties go to the higher id | key=(-prob, id) |
| 12 | greedy_generate | `<=` produces one token more than max_len | len(out) < max_len |
| 13 | beam_search, expansion | score is the last step's log-probability only, not the running sum | score + model.log_prob(...) |
| 14 | beam_search, pruning | sorts candidates ascending, keeping the worst beams | key=(-score, ids) |
| 15 | beam_search, length limit | beams cut off at max_len are finished without the </s> log-probability | score + model.log_prob(ids[-1], EOS_ID) |
