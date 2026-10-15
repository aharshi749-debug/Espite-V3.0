import gen
import kb3
from gen import cap, pl_of, as_typed, article_for
from v3_base import STRUCT, UNKNOWN, ALL_FOODS, first_sentence, ref_of, disp_pl
from v3_animals import answer_for, VERB, CLASS_A, ASKABLE

NUMW = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]
TOO_BIG = "That's too big for my tiny brain. I can add and subtract up to 20, and multiply and divide up to 10."
ASK = ["what is {x}", "what's {x}", "{x}", "how much is {x}", "calculate {x}", "whats {x}", "{x} =",
       "can you do {x}", "quick math: {x}", "what does {x} equal", "solve {x}"]


def _num(n, rng):
    return NUMW[n] if n <= 20 and rng.random() < 0.25 else str(n)


def t_math(state, rng):
    state["last"] = ("other",); state["attr"] = None
    x = rng.random()
    if x < 0.09:
        a, b, c = (rng.randint(0, 10) for _ in range(3))
        e = f"{_num(a, rng)} plus {_num(b, rng)} plus {_num(c, rng)}"
        return gen.style_user(rng.choice(ASK).format(x=e), rng, typo=False), f"{a} plus {b} plus {c} is {a + b + c}."
    if x < 0.19:
        op = rng.choice(["plus", "minus", "times", "divided by"])
        a, b = rng.randint(21, 999), rng.randint(2, 999)
        if op in ("times", "divided by"):
            a, b = rng.randint(11, 999), rng.randint(0, 99)
        if rng.random() < 0.5:
            a, b = b, a
        return gen.style_user(rng.choice(ASK).format(x=f"{a} {op} {b}"), rng, typo=False), TOO_BIG
    op = rng.choices(["plus", "minus", "times", "div"], weights=[34, 26, 24, 16])[0]
    if op in ("plus", "minus"):
        a, b = rng.randint(0, 20), rng.randint(0, 20)
        if op == "minus" and b > a:
            a, b = b, a
        sym = rng.choice([op, op, "+" if op == "plus" else "-"])
        r = a + b if op == "plus" else a - b
    elif op == "times":
        a, b = rng.randint(0, 10), rng.randint(0, 10)
        sym, r = rng.choice(["times", "times", "*", "x", "multiplied by"]), a * b
    else:
        b, k = rng.randint(1, 10), rng.randint(0, 10)
        a = b * k + (rng.randint(0, b - 1) if rng.random() < 0.15 else 0)
        sym, r = rng.choice(["divided by", "divided by", "/"]), None
    sp = "" if sym in "+-*/" and rng.random() < 0.4 else " "
    expr = f"{_num(a, rng)}{sp}{sym}{sp}{_num(b, rng)}"
    q = rng.choice(ASK).format(x=expr)
    if op == "plus" and rng.random() < 0.12:
        q = f"add {_num(a, rng)} and {_num(b, rng)}"
    if op == "div":
        k, rem = divmod(a, b)
        ans = f"{a} divided by {b} is {k}." if rem == 0 else f"{a} divided by {b} is {k} with {rem} left over."
    else:
        word = {"plus": "plus", "minus": "minus", "times": "times"}[op]
        ans = f"{a} {word} {b} is {r}."
    return gen.style_user(q, rng, typo=False), ans


M2 = ["what is {r1} and what is {r2}", "what's {r1} and what's {r2}", "tell me about {r1} and {r2}",
      "what are {p1} and {p2}", "explain {r1} and {r2}", "describe {r1} and {r2}", "what is {r1}? what is {r2}?",
      "i want to know about {r1} and {r2}", "define {r1} and {r2}", "what are {r1} and {r2}"]
M3 = ["what are {p1}, {p2}, and {p3}", "what are {p1}, {p2} and {p3}", "tell me about {r1}, {r2}, and {r3}",
      "explain {r1}, {r2} and {r3}", "what is {r1}, {r2}, and {r3}", "describe {p1}, {p2}, and {p3}",
      "{p1}, {p2}, {p3}: what are they"]


def t_multi(state, rng):
    k = 3 if rng.random() < 0.4 else 2
    es = rng.sample(gen.ENTRIES, k)
    f = {}
    for i, e in enumerate(es, 1):
        f[f"r{i}"], f[f"p{i}"] = ref_of(e), pl_of(e)
    q = rng.choice(M3 if k == 3 else M2).format(**f)
    state["last"] = ("kb", es[-1], 0); state["attr"] = None
    return gen.style_user(q, rng), " ".join(first_sentence(e.answer) for e in es)


UNK_WHAT = ["I'm not sure what {x} is. I'm a tiny model, so I only know about simple things.",
            "Hmm, I don't know about {x}. My memory is very small!",
            "I don't know what {x} is. Try asking me about animals, food, science, or tech."]
UNK_ANIMALISH = ["I'm not sure. I don't know about {x}, so I can't answer that.",
                 "I don't know much about {x}. I only know some animals and simple things.",
                 "Hmm, I'm not sure about {x}. My memory is small!"]
UNK_QS = ["what is {ref} for", "what does {ref} do", "describe {ref}", "tell me about {pl}", "{ref}?",
          "where can i find {ref}", "is {ref} dangerous", "what color is {ref}", "how big is {ref}",
          "what does {ref} eat", "where do {pl} live", "what do {pl} like to do", "can {pl} fly", "can {ref} swim",
          "do {pl} eat meat", "is {ref} a mammal", "how many legs does {ref} have", "what is {ref} used for",
          "is {ref} bigger than a cat", "where does {ref} live", "what do {pl} eat", "do {pl} eat fish",
          "is {ref} a bird", "what kind of animal is {ref}"]


def _unk_word(rng):
    return rng.choice(UNKNOWN) if rng.random() < 0.6 else gen.pseudo_word(rng)


def _lookalike(rng):
    singles = [e for e in gen.ENTRIES if " " not in e.name and "-" not in e.name and 2 < len(e.name) < 8]
    for _ in range(50):
        if rng.random() < 0.5:
            a, b = rng.sample(singles, 2)
            w = a.name + b.name
            if w not in gen.KNOWN_WORDS:
                return w, a, b
        else:
            b = rng.choice(singles)
            w = rng.choice(kb3.LOOKALIKE_PREFIX) + b.name
            if w not in gen.KNOWN_WORDS and w not in UNKNOWN:
                return w, None, b
    return "zorbfish", None, None


def t_unknown(state, rng):
    state["last"] = ("other",); state["attr"] = None
    x = rng.random()
    if x < 0.3:
        w, a, b = _lookalike(rng)
        ref = f"{article_for(w)} {w}"
        q = gen.style_user(rng.choice(["what is {r}", "what's {r}", "tell me about {r}", "what does {r} eat",
                                       "do you know what {r} is", "explain {r}"]).format(r=ref), rng, typo=False)
        t = as_typed(q, w)
        if a and b:
            return q, f"I don't know what {article_for(t)} {t} is, but I know about {disp_pl(a)} and {disp_pl(b)}!"
        return q, f"I'm not sure what {article_for(t)} {t} is. I'm a tiny model, so I only know about simple things."
    w = _unk_word(rng)
    ref = f"{article_for(w)} {w}"
    if x < 0.65:
        q = gen.style_user(rng.choice(UNK_QS).format(ref=ref, pl=w + "s"), rng, typo=False)
        return q, rng.choice(UNK_ANIMALISH).format(x=as_typed(q, w))
    ref2 = ref if rng.random() < 0.75 else w
    q = gen.style_user(rng.choice(["what is {r}", "what's {r}", "tell me about {r}", "explain {r}", "define {w}",
                                   "what even is {r}", "{r}? what's that", "do you know what {r} is"]).format(r=ref2, w=w),
                       rng, typo=False)
    return q, rng.choice(UNK_WHAT).format(x=as_typed(q, ref2))


def t_change_name(state, rng):
    n = gen.random_name(rng)
    q = gen.style_user(rng.choice(["actually my name is {n}", "actually call me {n}", "call me {n} instead",
                                   "no wait, i'm {n}", "my name is actually {n}", "change my name to {n}",
                                   "i changed my mind, call me {n}", "wait, my real name is {n}"]).format(n=n),
                       rng, typo=False)
    n = as_typed(q, n)
    state["name"] = n; state["last"] = ("other",)
    return q, rng.choice([f"Okay, I'll call you {n}!", f"Got it, {n}!", f"Sure thing, {n}!"])


PRON_EXTRA = {"ab": ["can it {v}", "can they {v}", "does it {v}", "is it able to {v}"],
              "class": ["what kind of animal is it", "is it a mammal", "what type of animal is that"],
              "legs": ["how many legs does it have", "how many legs do they have"],
              "diet": ["does it eat meat", "do they eat plants"]}


def t_pronoun(state, rng):
    e = state["last"][1]
    if e.name in STRUCT and rng.random() < 0.45:
        kind = rng.choice(["ab", "class", "legs", "diet"])
        if kind == "ab":
            abil = [a[1:] for a in STRUCT[e.name]["abil"]]
            if abil:
                ab = rng.choice(abil)
                state["attr"] = ("ab", ab)
                return gen.style_user(rng.choice(PRON_EXTRA["ab"]).format(v=VERB[ab]), rng, typo=False), answer_for(e, ("ab", ab))
        elif kind == "class":
            q = rng.choice(PRON_EXTRA["class"])
            if q == "is it a mammal":
                c = STRUCT[e.name]["cls"]
                a = f"Yes, {ref_of(e)} is a mammal." if c == "mammal" else f"No, {ref_of(e)} is {CLASS_A[c]}, not a mammal."
                return gen.style_user(q, rng, typo=False), a
            state["attr"] = ("class",)
            return gen.style_user(q, rng, typo=False), answer_for(e, ("class",))
        elif kind == "legs" and STRUCT[e.name]["legs"] >= 0:
            state["attr"] = ("legs",)
            return gen.style_user(rng.choice(PRON_EXTRA["legs"]), rng, typo=False), answer_for(e, ("legs",))
        elif kind == "diet":
            q = rng.choice(PRON_EXTRA["diet"])
            k = ("diet", "meat" if "meat" in q else "plants")
            state["attr"] = k
            return gen.style_user(q, rng, typo=False), answer_for(e, k)
    if e.attrs:
        k = rng.choice(["eat", "live", "likes"])
    elif e.used:
        k = "used"
    else:
        return t_more(state, rng)
    state["attr"] = (k,)
    return gen.style_user(rng.choice(gen.PRON_Q[k]), rng, typo=False), part(e, k)


def part(e, k):
    return e.used if k == "used" else e.attrs[k]


def t_more(state, rng):
    return gen.t_more(state, rng)


def t_what_about(state, rng):
    last, k = state.get("last"), state.get("attr")
    if last and last[0] == "kb" and k:
        pool = gen.OBJECTS if k[0] == "used" else gen.ANIMALS
        for _ in range(30):
            e = rng.choice(pool)
            a = answer_for(e, k)
            if a and e is not last[1]:
                state["last"] = ("kb", e, 0)
                return gen.style_user(gen.what_about(e, rng), rng), a
    if last and last[0] == "kb":
        e = rng.choice(gen.ENTRIES)
        state["last"] = ("kb", e, 0); state["attr"] = None
        return gen.style_user(gen.what_about(e, rng), rng), e.answer
    return gen.t_kb(state, rng)


def t_multi_attr(state, rng):
    e1, e2 = rng.sample(gen.ANIMALS, 2)
    k = rng.choice(["eat", "live", "likes"])
    tpl = {"eat": ["what do {p1} and {p2} eat", "what does {r1} eat and what does {r2} eat", "what do {p1} and {p2} like to eat"],
           "live": ["where do {p1} and {p2} live", "where does {r1} live and where does {r2} live"],
           "likes": ["what do {p1} and {p2} like to do", "what do {p1} and {p2} do for fun"]}[k]
    q = rng.choice(tpl).format(p1=pl_of(e1), p2=pl_of(e2), r1=ref_of(e1), r2=ref_of(e2))
    state["last"] = ("kb", e2, 0); state["attr"] = (k,)
    return gen.style_user(q, rng), e1.attrs[k] + " " + e2.attrs[k]
