import random
import subprocess
import sys

import gen
import v3_base
from v3_base import first_sentence, STRUCT
from kb import CAPITALS

HOST = "../host/espite_host"
v3_base.init(open("params.txt").read().split("\n")[1])
E = gen.ENTRIES
rng = random.Random(42)

convs = []


def add(cat, msgs, check):
    convs.append((cat, msgs, check))


for e in E:
    add("facts (trained phrasing)", [f"what is {e.ref()}"], lambda r, e=e: r[-1] == e.answer)
    held = rng.choice([f"i was wondering what {e.ref()} is", f"do you happen to know what {e.ref()} is",
                       f"so like, what is {e.ref()}", f"could you explain what {e.ref()} is to me"])
    add("facts (NEW phrasing)", [held], lambda r, e=e: r[-1] == e.answer)
    add("tell me more follow-up", [f"what is {e.ref()}", "tell me more"], lambda r, e=e: r[-1] == e.more)

for a in range(11):
    for b in range(11):
        add("math", [f"what is {a} plus {b}"], lambda r, a=a, b=b: r[-1] == f"{a} plus {b} is {a + b}.")
        add("math", [f"{a}*{b}"], lambda r, a=a, b=b: r[-1] == f"{a} times {b} is {a * b}.")
        if a >= b:
            add("math", [f"what's {a} minus {b}"], lambda r, a=a, b=b: r[-1] == f"{a} minus {b} is {a - b}.")

NEW_NAMES = ["Bartholomew", "Zelda", "Kwame", "Ingo", "Priyanka", "Thaddeus", "Fern", "Ozzy",
             "Marisol", "Quentin", "Delphine", "Yusuf", "Brick", "Wanda", "Lorenzo", "Tilly"]
fillers = ["what is a cat", "tell me a joke", "what is 2 plus 2", "how are you", "what is wifi",
           "what color is the sky", "who made you", "what is a resistor"]
for n in NEW_NAMES:
    for k in range(3):
        msgs = [f"my name is {n}"] + rng.sample(fillers, k) + ["what's my name?"]
        add("remembers NEW name", msgs, lambda r, n=n: n in r[-1])

NEW_UNKNOWN = ["trampoline", "kazoo", "igloo", "anvil", "kayak", "marmoset", "harpsichord",
               "zucchini", "gazebo", "periscope", "sundial", "bagpipe", "tofu", "wizard", "yodel"]
for w in NEW_UNKNOWN:
    add("admits not knowing (NEW words)", [f"what is a {w}"],
        lambda r: any(s in r[-1] for s in ("not sure", "don't know")))

for c, v in CAPITALS.items():
    add("capitals", [f"what is the capital of {c}"], lambda r, v=v: v in r[-1])

for q, must in [("hi", "Hi"), ("who are you", "ESPite"), ("who made you", "Elias"),
                ("are you chatgpt", "No"), ("what time is it", "clock"), ("thanks", "!"),
                ("what sound does a cat make", "meow"), ("what day comes after friday", "Saturday"),
                ("what is the opposite of hot", "cold"), ("count to 5", "1, 2, 3, 4, 5.")]:
    add("chat basics", [q], lambda r, m=must: m in r[-1])


if getattr(gen, "ANIMALS", None):
    from gen import pl_of, cause_forms
    for e in gen.ANIMALS:
        add("attributes (trained phrasing)", [f"what does {e.ref()} eat"], lambda r, e=e: r[-1] == e.attrs["eat"])
        add("attributes (trained phrasing)", [f"where do {pl_of(e)} live"], lambda r, e=e: r[-1] == e.attrs["live"])
        add("attributes (NEW phrasing)", [f"i want to know what {pl_of(e)} like to eat"], lambda r, e=e: r[-1] == e.attrs["eat"])
        add("attributes (NEW phrasing)", [f"so how does {e.ref()} like to spend its time"], lambda r, e=e: r[-1] == e.attrs["likes"])
        add("compound question (NEW phrasing)", [f"tell me what {e.ref()} is and where it lives"],
            lambda r, e=e: r[-1] == first_sentence(e.answer) + " " + e.attrs["live"])
        add("compound question (trained phrasing)", [f"what's {e.ref()} and what's its favorite activity"],
            lambda r, e=e: r[-1] == first_sentence(e.answer) + " " + e.attrs["likes"])
        add("pronoun follow-up", [f"what is {e.ref()}", "ok and what does it eat"], lambda r, e=e: r[-1] == e.attrs["eat"])
    animals = list(gen.ANIMALS)
    for i, e in enumerate(animals):
        e2 = animals[(i * 7 + 3) % len(animals)]
        if e2 is e:
            continue
        add("'what about X' keeps the question", [f"where does {e.ref()} live", f"what about {pl_of(e2)}"],
            lambda r, e2=e2: r[-1] == e2.attrs["live"])
    for e in gen.OBJECTS:
        add("used for (NEW phrasing)", [f"what would someone use {e.ref()} for"], lambda r, e=e: r[-1] == e.used)
    ents = list(gen.ENTRIES)
    for i in range(60):
        e1, e2 = ents[(i * 13) % len(ents)], ents[(i * 29 + 5) % len(ents)]
        if e1 is e2:
            continue
        add("two topics in one question", [f"can you explain {e1.ref()} and also {e2.ref()}"],
            lambda r, e1=e1, e2=e2: r[-1] == first_sentence(e1.answer) + " " + first_sentence(e2.answer))
    for phs, ans, d in gen.CAUSES:
        ph = phs[0]
        add("what happens if (trained phrasing)", [f"what happens if you {ph}"], lambda r, a=ans: r[-1] == a)
        add("what happens if (NEW phrasing)", [f"what would happen if you {ph}"], lambda r, a=ans: r[-1] == a)

    import v3_animals as A
    from v3_base import ref_of
    for i, e in enumerate(gen.ANIMALS):
        add("v3 class (NEW phrasing)", [f"which animal group does {ref_of(e)} belong to"], lambda r, e=e: r[-1] == A.class_ans(e))
        if A.legs_ans(e):
            add("v3 legs", [f"how many legs does {ref_of(e)} have"], lambda r, e=e: r[-1] == A.legs_ans(e))
        ab = [a[1:] for a in STRUCT[e.name]["abil"]]
        if ab:
            add("v3 yes/no ability (NEW phrasing)", [f"is it possible for {gen.pl_of(e)} to {A.VERB[ab[0]]}"], lambda r, e=e, ab=ab[0]: r[-1].split(",")[0] == A.ab_ans(e, ab).split(",")[0])
        e2 = gen.ANIMALS[(i * 11 + 7) % len(gen.ANIMALS)]
        if STRUCT[e2.name]["size"] != STRUCT[e.name]["size"]:
            big = e if STRUCT[e.name]["size"] > STRUCT[e2.name]["size"] else e2
            add("v3 compare (NEW phrasing)", [f"out of {ref_of(e)} and {ref_of(e2)}, which one is bigger"], lambda r, big=big: r[-1].lower().startswith(ref_of(big).lower()))
    for a_, b_ in [(13, 6), (20, 7), (15, 15), (19, 1)]:
        add("v3 math 11-20", [f"what is {a_} plus {b_}"], lambda r, a_=a_, b_=b_: r[-1] == f"{a_} plus {b_} is {a_ + b_}.")
        add("v3 math 11-20", [f"what is {a_} minus {b_ % 10}"], lambda r, a_=a_, b_=b_: r[-1] == f"{a_} minus {b_ % 10} is {a_ - b_ % 10}.")
    for a_, b_ in [(12, 3), (20, 4), (9, 3), (100, 10), (7, 7)]:
        add("v3 math divide", [f"what is {a_} divided by {b_}"], lambda r, a_=a_, b_=b_: r[-1] == f"{a_} divided by {b_} is {a_ // b_}.")


lines = []
for _, msgs, _ in convs:
    lines += msgs + ["/reset"]
out = subprocess.run([HOST, "chat", "0"], input="\n".join(lines) + "\n", capture_output=True, text=True).stdout
replies = [l[len("espite> "):] for l in out.splitlines() if l.startswith("espite> ")]
assert len(replies) == sum(len(m) for _, m, _ in convs), (len(replies))

from collections import defaultdict
score = defaultdict(lambda: [0, 0])
fails = defaultdict(list)
i = 0
for cat, msgs, check in convs:
    r = replies[i:i + len(msgs)]; i += len(msgs)
    ok = check(r)
    score[cat][0] += ok; score[cat][1] += 1
    if not ok:
        fails[cat].append((msgs[-1], r[-1]))
tot = [0, 0]
for cat, (a, b) in score.items():
    print(f"{cat:32s} {a:4d}/{b:<4d} {100 * a / b:5.1f}%")
    tot[0] += a; tot[1] += b
print(f"{'TOTAL':32s} {tot[0]:4d}/{tot[1]:<4d} {100 * tot[0] / tot[1]:5.1f}%")
if "-v" in sys.argv:
    for cat, fl in fails.items():
        print(f"\n## {cat}")
        for q, r in fl[:8]:
            print(f"  {q!r} -> {r!r}")
