import math
from dataclasses import dataclass, asdict

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class Config:
    vocab: int = 1024
    dim: int = 128
    n_layers: int = 5
    n_heads: int = 4
    n_kv_heads: int = 2
    hidden: int = 352
    max_seq: int = 256
    rope_theta: float = 10000.0
    norm_eps: float = 1e-5


class RMSNorm(nn.Module):
    def __init__(self, dim, eps):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x):
        return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps) * self.weight


def rope_tables(head_dim, pos, theta):
    inv = 1.0 / (theta ** (torch.arange(0, head_dim, 2, dtype=torch.float32) / head_dim))
    ang = pos.float().unsqueeze(-1) * inv
    return torch.cos(ang), torch.sin(ang)


def apply_rope(x, cos, sin):
    x0, x1 = x[..., 0::2], x[..., 1::2]
    cos, sin = cos.unsqueeze(1), sin.unsqueeze(1)
    y0 = x0 * cos - x1 * sin
    y1 = x0 * sin + x1 * cos
    return torch.stack((y0, y1), dim=-1).flatten(-2)


class Block(nn.Module):
    def __init__(self, c: Config):
        super().__init__()
        self.c = c
        hd = c.dim // c.n_heads
        self.hd = hd
        self.attn_norm = RMSNorm(c.dim, c.norm_eps)
        self.wq = nn.Linear(c.dim, c.n_heads * hd, bias=False)
        self.wk = nn.Linear(c.dim, c.n_kv_heads * hd, bias=False)
        self.wv = nn.Linear(c.dim, c.n_kv_heads * hd, bias=False)
        self.wo = nn.Linear(c.n_heads * hd, c.dim, bias=False)
        self.ffn_norm = RMSNorm(c.dim, c.norm_eps)
        self.w1 = nn.Linear(c.dim, c.hidden, bias=False)
        self.w3 = nn.Linear(c.dim, c.hidden, bias=False)
        self.w2 = nn.Linear(c.hidden, c.dim, bias=False)

    def forward(self, x, cos, sin, mask):
        B, T, _ = x.shape
        c = self.c
        h = self.attn_norm(x)
        q = self.wq(h).view(B, T, c.n_heads, self.hd).transpose(1, 2)
        k = self.wk(h).view(B, T, c.n_kv_heads, self.hd).transpose(1, 2)
        v = self.wv(h).view(B, T, c.n_kv_heads, self.hd).transpose(1, 2)
        q, k = apply_rope(q, cos, sin), apply_rope(k, cos, sin)
        rep = c.n_heads // c.n_kv_heads
        k = k.repeat_interleave(rep, dim=1)
        v = v.repeat_interleave(rep, dim=1)
        a = F.scaled_dot_product_attention(q, k, v, attn_mask=mask)
        x = x + self.wo(a.transpose(1, 2).reshape(B, T, -1))
        h = self.ffn_norm(x)
        x = x + self.w2(F.silu(self.w1(h)) * self.w3(h))
        return x


class ESPite(nn.Module):
    def __init__(self, c: Config):
        super().__init__()
        self.c = c
        self.embed = nn.Embedding(c.vocab, c.dim)
        self.layers = nn.ModuleList(Block(c) for _ in range(c.n_layers))
        self.norm = RMSNorm(c.dim, c.norm_eps)
        self.apply(self._init)
        for n, p in self.named_parameters():
            if n.endswith("wo.weight") or n.endswith("w2.weight"):
                nn.init.normal_(p, 0.0, 0.02 / math.sqrt(2 * c.n_layers))

    @staticmethod
    def _init(m):
        if isinstance(m, (nn.Linear, nn.Embedding)):
            nn.init.normal_(m.weight, 0.0, 0.02)

    def forward(self, idx, pos, mask):
        cos, sin = rope_tables(self.c.dim // self.c.n_heads, pos, self.c.rope_theta)
        x = self.embed(idx)
        for l in self.layers:
            x = l(x, cos, sin, mask)
        x = self.norm(x)
        return x @ self.embed.weight.t()

    def n_params(self):
        return sum(p.numel() for p in self.parameters())
