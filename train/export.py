import sys

import numpy as np
import torch

from model import Config, ESPite
from tok import Tokenizer

OUT = sys.argv[1] if len(sys.argv) > 1 else "../firmware/ESPite/espite_model.h"


def q8(w):
    w = w.astype(np.float32)
    s = np.abs(w).max(axis=1) / 127.0
    s[s == 0] = 1.0
    q = np.clip(np.round(w / s[:, None]), -127, 127).astype(np.int8)
    return q, s.astype(np.float32)


def dequant_model(m):
    with torch.no_grad():
        for n, p in m.named_parameters():
            if p.dim() == 2:
                q, s = q8(p.numpy())
                p.copy_(torch.from_numpy(q.astype(np.float32) * s[:, None]))
    return m


def load(path=None):
    ck = torch.load(path or (sys.argv[2] if len(sys.argv) > 2 else "espite.pt"), map_location="cpu")
    c = Config(**ck["cfg"])
    m = ESPite(c)
    m.load_state_dict(ck["model"])
    m.eval()
    return m, c, ck


def c_array(ctype, name, arr, per_line=32):
    flat = arr.reshape(-1)
    if ctype == "float":
        items = [f"{float(v):.9g}f" for v in flat]
    else:
        items = [str(int(v)) for v in flat]
    lines = [",".join(items[i:i + per_line]) for i in range(0, len(items), per_line)]
    return f"static const {ctype} {name}[{len(flat)}] = {{\n" + ",\n".join(lines) + "\n};\n"


def main():
    m, c, ck = load()
    tk = Tokenizer.load("tokenizer.json")
    sd = {k: v.numpy() for k, v in m.state_dict().items()}
    L = c.n_layers
    out = []
    out.append("#pragma once\n#include <stdint.h>\n\n")
    hd = c.dim // c.n_heads
    for k, v in (("DIM", c.dim), ("LAYERS", L), ("HEADS", c.n_heads), ("KV_HEADS", c.n_kv_heads),
                 ("HIDDEN", c.hidden), ("VOCAB", c.vocab), ("CTX", c.max_seq),
                 ("N_MERGES", len(tk.merges)), ("N_PARAMS", m.n_params())):
        out.append(f"#define ESPITE_{k} {v}\n")
    out.append(f"#define ESPITE_ROPE_THETA {c.rope_theta}f\n#define ESPITE_NORM_EPS {c.norm_eps}f\n\n")

    q, s = q8(sd["embed.weight"])
    out.append(c_array("int8_t", "ESPITE_W_EMB", q))
    out.append(c_array("float", "ESPITE_S_EMB", s))

    def stack(key):
        qs, ss = zip(*(q8(sd[f"layers.{i}.{key}.weight"]) for i in range(L)))
        return np.stack(qs), np.stack(ss)

    for key in ("wq", "wk", "wv", "wo", "w1", "w3", "w2"):
        qa, sa = stack(key)
        out.append(c_array("int8_t", f"ESPITE_W_{key.upper()}", qa))
        out.append(c_array("float", f"ESPITE_S_{key.upper()}", sa))
    out.append(c_array("float", "ESPITE_ATTN_NORM", np.stack([sd[f"layers.{i}.attn_norm.weight"] for i in range(L)])))
    out.append(c_array("float", "ESPITE_FFN_NORM", np.stack([sd[f"layers.{i}.ffn_norm.weight"] for i in range(L)])))
    out.append(c_array("float", "ESPITE_FINAL_NORM", sd["norm.weight"]))


    blob, offs = bytearray(), [0]
    for i, t in enumerate(tk.vocab):
        blob += t.encode("ascii") if i >= 4 else b""
        offs.append(len(blob))
    out.append(c_array("char", "ESPITE_VOCAB_BLOB", np.frombuffer(bytes(blob) + b"\0", dtype=np.uint8).astype(np.int32)))
    out.append(c_array("uint16_t", "ESPITE_VOCAB_OFF", np.array(offs)))
    keys = sorted(((a << 16) | b, r) for r, (a, b) in enumerate(tk.merges))
    out.append(c_array("uint32_t", "ESPITE_MERGE_KEY", np.array([k for k, _ in keys], dtype=np.uint64)))
    out.append(c_array("uint16_t", "ESPITE_MERGE_RANK", np.array([r for _, r in keys])))
    open(OUT, "w").write("".join(out))
    nbytes = sum(sd[k].size for k in sd if sd[k].ndim == 2)
    print(f"wrote {OUT}: {m.n_params()} params, ~{nbytes / 1024:.0f} KB int8 weights")


if __name__ == "__main__":
    main()
