import torch
from dataclasses import asdict
from model import ESPite
from prep import CFG

src = torch.load("espite.pt", map_location="cpu")["model"]
m = ESPite(CFG)
sd = m.state_dict()
for k, v in src.items():
    sd[k] = v
new = f"layers.{CFG.n_layers - 1}."
for k in sd:
    if k.startswith(new) and (k.endswith("wo.weight") or k.endswith("w2.weight")):
        sd[k] = torch.zeros_like(sd[k])
m.load_state_dict(sd)
torch.save({"cfg": asdict(CFG), "model": m.state_dict(), "step": 0, "val": 0.0}, "espite_v3_grown.pt")
print("grown to", m.n_params(), "params")
