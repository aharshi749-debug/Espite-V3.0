import json
import subprocess
import sys
from collections import defaultdict

HOST = "../host/espite_host"
REVEAL = "--reveal" in sys.argv
TEMP = "0"
for a in sys.argv[1:]:
    if a.startswith("--temp="):
        TEMP = a.split("=")[1]

cases = json.load(open("attack_locked.json"))
lines = []
for c in cases:
    lines += c["msgs"] + ["/reset"]
out = subprocess.run([HOST, "chat", TEMP], input="\n".join(lines) + "\n", capture_output=True, text=True).stdout
replies = [l[len("espite> "):] for l in out.splitlines() if l.startswith("espite> ")]
assert len(replies) == sum(len(c["msgs"]) for c in cases), (len(replies))


def grade(r, ck):
    t = r.lower()
    if ck.get("all") and not all(s.lower() in t for s in ck["all"]):
        return False
    if ck.get("any") and not any(s.lower() in t for s in ck["any"]):
        return False
    if ck.get("none") and any(s.lower() in t for s in ck["none"]):
        return False
    if ck.get("unknown") and not ("don't know" in t or "not sure" in t):
        return False
    return True


score = defaultdict(lambda: [0, 0])
rows = []
i = 0
for c in cases:
    r = replies[i:i + len(c["msgs"])][-1]
    i += len(c["msgs"])
    ok = grade(r, c["check"])
    score[c["cat"]][0] += ok
    score[c["cat"]][1] += 1
    rows.append((ok, c, r))
tot = [sum(a for a, _ in score.values()), sum(b for _, b in score.values())]
for cat, (a, b) in sorted(score.items()):
    print(f"{cat:28s} {a:3d}/{b:<3d}")
print(f"{'TOTAL':28s} {tot[0]}/{tot[1]}  ({100 * tot[0] / tot[1]:.0f}%)")
if REVEAL:
    for ok, c, r in rows:
        print(("\nPASS " if ok else "\nFAIL ") + f"[{c['cat']}] " + " | ".join(c["msgs"]))
        print("  check:", json.dumps(c["check"]))
        print("  reply:", r)
