import json

PAD, USER, BOT, END = 0, 1, 2, 3
N_SPECIAL = 4
BASE = N_SPECIAL + 95


def is_alpha(c):
    return ("a" <= c <= "z") or ("A" <= c <= "Z") or c == "'"


def clean(s):
    out = []
    for c in s:
        if c in "\t\n\r":
            c = " "
        out.append(c if 32 <= ord(c) <= 126 else "?")
    return "".join(out)


def pretokenize(s):
    s = clean(s)
    i, n = 0, len(s)
    out = []
    while i < n:
        c = s[i]
        if c == " " and i + 1 < n and is_alpha(s[i + 1]):
            j = i + 1
            while j < n and is_alpha(s[j]):
                j += 1
            out.append(s[i:j]); i = j
        elif is_alpha(c):
            j = i
            while j < n and is_alpha(s[j]):
                j += 1
            out.append(s[i:j]); i = j
        else:
            out.append(c); i += 1
    return out


def char_id(c):
    return N_SPECIAL + ord(c) - 32


class Tokenizer:
    def __init__(self, merges):
        self.merges = [tuple(m) for m in merges]
        self.rank = {m: i for i, m in enumerate(self.merges)}
        self.vocab = ["<pad>", "<user>", "<bot>", "<end>"] + [chr(i) for i in range(32, 127)]
        for a, b in self.merges:
            self.vocab.append(self.vocab[a] + self.vocab[b])
        self.cache = {}

    @property
    def size(self):
        return len(self.vocab)

    def encode_piece(self, p):
        if p in self.cache:
            return self.cache[p]
        ids = [char_id(c) for c in p]
        while len(ids) > 1:
            best, bi = None, -1
            for i in range(len(ids) - 1):
                r = self.rank.get((ids[i], ids[i + 1]))
                if r is not None and (best is None or r < best):
                    best, bi = r, i
            if best is None:
                break
            ids = ids[:bi] + [BASE + best] + ids[bi + 2:]
        self.cache[p] = ids
        return ids

    def encode(self, s):
        out = []
        for p in pretokenize(s):
            out.extend(self.encode_piece(p))
        return out

    def decode(self, ids):
        return "".join(self.vocab[i] for i in ids if i >= N_SPECIAL)

    def save(self, path):
        json.dump({"merges": self.merges}, open(path, "w"))

    @staticmethod
    def load(path):
        return Tokenizer(json.load(open(path))["merges"])


def train_bpe(texts, vocab_size):
    from collections import Counter
    words = Counter()
    for t in texts:
        words.update(pretokenize(t))
    seqs = {w: [char_id(c) for c in w] for w in words}
    merges = []
    n_merges = vocab_size - BASE
    for m in range(n_merges):
        pairs = Counter()
        for w, s in seqs.items():
            c = words[w]
            for i in range(len(s) - 1):
                pairs[(s[i], s[i + 1])] += c
        if not pairs:
            break
        best = max(pairs, key=lambda p: (pairs[p], -p[0], -p[1]))
        new_id = BASE + m
        merges.append(best)
        a, b = best
        for w, s in seqs.items():
            if len(s) < 2:
                continue
            i, out = 0, []
            while i < len(s):
                if i < len(s) - 1 and s[i] == a and s[i + 1] == b:
                    out.append(new_id); i += 2
                else:
                    out.append(s[i]); i += 1
            seqs[w] = out
    return Tokenizer(merges)
