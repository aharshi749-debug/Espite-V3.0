import sys
import time

import numpy as np

import v3_conv as gen
from model import Config, ESPite
from tok import BOT, END, PAD, USER, Tokenizer, train_bpe

CFG = Config(vocab=1024, dim=160, n_layers=7, n_heads=5, n_kv_heads=1, hidden=432, max_seq=384)
WIN = CFG.max_seq + 1


def params_string():
    import torch
    n = ESPite(CFG).n_params()
    return n, f"{n / 1e6:.1f} million"


def encode_conv(tk, conv):
    ids, mask = [], []
    for u, b in conv:
        t = [USER] + tk.encode(u) + [BOT]
        r = tk.encode(b) + [END]
        if len(ids) + len(t) + len(r) > WIN:
            break
        ids += t + r
        mask += [0] * len(t) + [1] * len(r)
    return ids, mask


def pack(tk, convs):
    toks, msk, doc, pos = [], [], [], []
    cur_t, cur_m, cur_d, cur_p = [], [], [], []
    d = 0

    def flush():
        pad = WIN - len(cur_t)
        toks.append(cur_t + [PAD] * pad)
        msk.append(cur_m + [0] * pad)
        doc.append(cur_d + [-1] * pad)
        pos.append(cur_p + [0] * pad)

    for c in convs:
        ids, m = encode_conv(tk, c)
        if not ids:
            continue
        if len(cur_t) + len(ids) > WIN:
            flush()
            cur_t, cur_m, cur_d, cur_p = [], [], [], []
        cur_t += ids; cur_m += m; cur_d += [d] * len(ids); cur_p += list(range(len(ids)))
        d += 1
    if cur_t:
        flush()
    return (np.array(toks, np.int16), np.array(msk, np.int8),
            np.array(doc, np.int32), np.array(pos, np.int16))


if __name__ == "__main__":
    n_train = int(sys.argv[1]) if len(sys.argv) > 1 else 300000
    n, ps = params_string()
    print("params", n, ps)
    t0 = time.time()
    train = gen.generate(n_train, seed=int(sys.argv[2]) if len(sys.argv) > 2 else 1, params_str=ps, vocab_str=str(CFG.vocab))
    val = gen.generate(4000, seed=999, params_str=ps, vocab_str=str(CFG.vocab))
    print(f"generated {len(train)} convs in {time.time() - t0:.0f}s")
    import os
    if os.path.exists("tokenizer.json"):
        tk = Tokenizer.load("tokenizer.json")
    else:
        texts = [t for c in train[:60000] for turn in c for t in turn]
        tk = train_bpe(texts, CFG.vocab)
        tk.save("tokenizer.json")
    print("vocab", tk.size, "sample merges:", tk.vocab[99:140])
    for name, convs in (("train", train), ("val", val)):
        T, M, D, P = pack(tk, convs)
        np.savez_compressed(f"{name}.npz", tok=T, mask=M, doc=D, pos=P)
        real = int((D >= 0).sum())
        print(name, T.shape, "real tokens", real, "target tokens", int(M.sum()), f"fill {real / T.size:.2f}")
    open("params.txt", "w").write(f"{n}\n{ps}\n")
