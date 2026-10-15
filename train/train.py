import math
import sys
import time
from dataclasses import asdict

import numpy as np
import torch
import torch.nn.functional as F

from model import ESPite
from prep import CFG

torch.manual_seed(1337)
torch.set_num_threads(2)

STEPS = int(sys.argv[1]) if len(sys.argv) > 1 else 3600
INIT = sys.argv[2] if len(sys.argv) > 2 else None
B = 32
LR, LR_MIN, WARM = (2e-3, 1e-4, 150) if not INIT else (float(sys.argv[3]) if len(sys.argv) > 3 else 1e-3, 3e-5, 50)


def load(name):
    z = np.load(f"{name}.npz")
    return [torch.from_numpy(z[k].astype(np.int64)) for k in ("tok", "mask", "doc", "pos")]


tr = load("train")
va = load("val")


def batch(data, idx):
    tok, msk, doc, pos = (d[idx] for d in data)
    x, y = tok[:, :-1], tok[:, 1:]
    lm = msk[:, 1:].bool() & (doc[:, 1:] == doc[:, :-1])
    d = doc[:, :-1]
    T = x.shape[1]
    causal = torch.ones(T, T, dtype=torch.bool).tril()
    am = (d[:, :, None] == d[:, None, :]) & causal
    return x, y, lm, pos[:, :-1], am.unsqueeze(1)


def loss_fn(m, x, y, lm, p, am):
    lo = m(x, p, am)
    l = F.cross_entropy(lo.reshape(-1, lo.shape[-1]), y.reshape(-1), reduction="none")
    lmf = lm.reshape(-1).float()
    return (l * lmf).sum() / lmf.sum()


@torch.no_grad()
def evaluate(m):
    m.eval()
    tot, n = 0.0, 0
    for i in range(0, min(len(va[0]), 512), 64):
        idx = torch.arange(i, min(i + 64, len(va[0])))
        x, y, lm, p, am = batch(va, idx)
        lo = m(x, p, am)
        l = F.cross_entropy(lo.reshape(-1, lo.shape[-1]), y.reshape(-1), reduction="none")
        tot += (l * lm.reshape(-1).float()).sum().item(); n += lm.sum().item()
    m.train()
    return tot / n


m = ESPite(CFG)
if INIT:
    m.load_state_dict(torch.load(INIT)["model"])
    print("resumed from", INIT, flush=True)
print("params", m.n_params(), flush=True)
decay = [p for n, p in m.named_parameters() if p.dim() >= 2]
nodecay = [p for n, p in m.named_parameters() if p.dim() < 2]
opt = torch.optim.AdamW([{"params": decay, "weight_decay": 0.1},
                         {"params": nodecay, "weight_decay": 0.0}], lr=LR, betas=(0.9, 0.95))
N = len(tr[0])
perm = torch.randperm(N)
ptr = 0
t0 = time.time()
ema = None
for step in range(1, STEPS + 1):
    lr = LR * step / WARM if step < WARM else LR_MIN + 0.5 * (LR - LR_MIN) * (1 + math.cos(math.pi * (step - WARM) / (STEPS - WARM)))
    for g in opt.param_groups:
        g["lr"] = lr
    if ptr + B > N:
        perm = torch.randperm(N); ptr = 0
    idx = perm[ptr:ptr + B]; ptr += B
    loss = loss_fn(m, *batch(tr, idx))
    opt.zero_grad(set_to_none=True)
    loss.backward()
    torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
    opt.step()
    ema = loss.item() if ema is None else 0.98 * ema + 0.02 * loss.item()
    if step % 50 == 0:
        el = time.time() - t0
        print(f"step {step}/{STEPS} loss {ema:.4f} lr {lr:.2e} {el / 60:.1f}min eta {(STEPS - step) * el / step / 60:.1f}min", flush=True)
    if step % 100 == 0 and step % 300 != 0 and step != STEPS:
        torch.save({"cfg": asdict(CFG), "model": m.state_dict(), "step": step, "val": -1.0}, "ckpt.pt")
    if step % 300 == 0 or step == STEPS:
        v = evaluate(m)
        print(f"  val {v:.4f}", flush=True)
        torch.save({"cfg": asdict(CFG), "model": m.state_dict(), "step": step, "val": v}, "ckpt.pt")
print("done", flush=True)
