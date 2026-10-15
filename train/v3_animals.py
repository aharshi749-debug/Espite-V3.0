import gen
from gen import cap, pl_of
from v3_base import STRUCT, ALL_FOODS, ref_of, disp_pl

CLASS_A = {"mammal": "a mammal", "bird": "a bird", "reptile": "a reptile", "fish": "a fish",
           "amphibian": "an amphibian", "insect": "an insect", "arachnid": "an arachnid", "mollusk": "a mollusk",
           "crustacean": "a crustacean", "invertebrate": "an invertebrate"}
CLASS_PL = {"mammal": "mammals", "bird": "birds", "reptile": "reptiles", "fish": "fish", "amphibian": "amphibians",
            "insect": "insects"}
ASKABLE = ["mammal", "bird", "reptile", "fish", "amphibian", "insect"]
VERB = {"fly": "fly", "swim": "swim", "climb": "climb", "run": "run fast", "jump": "jump", "dig": "dig"}


def ab_ans(e, ab):
    s = STRUCT[e.name]["abil"]
    if "+" + ab in s:
        return f"Yes, {disp_pl(e)} can {VERB[ab]}."
    if "-" + ab in s:
        other = [a[1:] for a in s if a[0] == "+" and a[1:] != ab]
        tail = f" But they can {VERB[other[0]]}." if other else ""
        return f"No, {disp_pl(e)} can't {VERB[ab]}.{tail}"
    return None


ALL_AB = ["fly", "swim", "climb", "run", "jump", "dig"]


def unsure_ab_ans(e, ab):
    s = STRUCT[e.name]["abil"]
    known = [a[1:] for a in s if a[0] == "+"]
    tail = f" But I know they can {VERB[known[0]]}." if known else ""
    return f"I'm not sure if {disp_pl(e)} can {VERB[ab]}.{tail}"


def class_ans(e):
    return f"{cap(ref_of(e))} is {CLASS_A[STRUCT[e.name]['cls']]}."


def legs_ans(e):
    n = STRUCT[e.name]["legs"]
    if n < 0:
        return None
    if n == 0:
        return f"{cap(ref_of(e))} has no legs."
    unit = "arms" if STRUCT[e.name]["cls"] == "mollusk" else "legs"
    return f"{cap(ref_of(e))} has {n} {unit}."


def food_ans(e, f):
    return ("Yes! " if f in STRUCT[e.name]["foods"] else "No. ") + e.attrs["eat"]


def diet_ans(e, kind):
    d = STRUCT[e.name]["diet"]
    ok = d in ("meat", "both") if kind == "meat" else d in ("plant", "both")
    return ("Yes! " if ok else "No. ") + e.attrs["eat"]


def answer_for(e, k):
    if not k:
        return None
    if k[0] in ("eat", "live", "likes"):
        return e.attrs[k[0]] if e.attrs else None
    if k[0] == "used":
        return e.used
    if e.name not in STRUCT:
        return None
    return {"ab": lambda: ab_ans(e, k[1]), "food": lambda: food_ans(e, k[1]), "diet": lambda: diet_ans(e, k[1]),
            "class": lambda: class_ans(e), "legs": lambda: legs_ans(e)}[k[0]]()


Q_AB = ["can {pl} {v}", "can {ref} {v}", "do {pl} {v}", "is {ref} able to {v}", "are {pl} able to {v}",
        "does {ref} {v}", "{pl} can {v} right", "do {pl} know how to {v}"]
Q_FOOD = ["do {pl} eat {f}", "does {ref} eat {f}", "can {pl} eat {f}", "do {pl} like {f}", "does {ref} like {f}",
          "would {ref} eat {f}", "is it true {pl} eat {f}"]
Q_DIET = {"meat": ["do {pl} eat meat", "does {ref} eat meat", "are {pl} meat eaters", "is {ref} a meat eater"],
          "plants": ["do {pl} eat plants", "does {ref} eat plants", "are {pl} plant eaters", "is {ref} a plant eater",
                     "do {pl} eat veggies"]}
Q_CLASS_YN = ["is {ref} {ac}", "are {pl} {cp}", "{ref}, is it {ac}", "is {ref} considered {ac}"]
Q_CLASS_WHAT = ["what kind of animal is {ref}", "what type of animal is {ref}", "what class of animal is {ref}",
                "is {ref} {ac} or {ac2}", "what animal group are {pl} in", "what group of animals is {ref} in"]
Q_LEGS = ["how many legs does {ref} have", "how many legs do {pl} have", "how many legs has {ref} got",
          "how many feet does {ref} have", "{pl} have how many legs"]
Q_WHICH = ["which is bigger {r1} or {r2}", "what's bigger {r1} or {r2}", "is {r1} or {r2} bigger",
           "who's bigger {r1} or {r2}", "which is bigger out of {r1} and {r2}", "{r1} vs {r2}, which is bigger",
           "which is bigger, {r1} or {r2}", "what's bigger, {r1} or {r2}", "which is larger, {r1} or {r2}",
           "{r1} or {r2}, which is bigger", "which one is bigger, {r1} or {r2}", "which is heavier, {r1} or {r2}"]
Q_WHICH_S = ["which is smaller {r1} or {r2}", "is {r1} or {r2} smaller", "which is smaller, {r1} or {r2}", "what's smaller, {r1} or {r2}", "which one is smaller, {r1} or {r2}"]
Q_YN_BIG = ["is {r1} bigger than {r2}", "is {r1} larger than {r2}"]
Q_YN_SMALL = ["is {r1} smaller than {r2}"]


def _mark(state, e, k):
    state["last"] = ("kb", e, 0)
    state["attr"] = k


def _fmt(e):
    return dict(pl=pl_of(e), ref=ref_of(e))


def t_ability(state, rng):
    if rng.random() < 0.2:
        e = rng.choice(gen.ANIMALS)
        marked = {a[1:] for a in STRUCT[e.name]["abil"]}
        free = [a for a in ALL_AB if a not in marked]
        if free:
            ab = rng.choice(free)
            _mark(state, e, None)
            return gen.style_user(rng.choice(Q_AB).format(v=VERB[ab], **_fmt(e)), rng), unsure_ab_ans(e, ab)
    while True:
        e = rng.choice(gen.ANIMALS)
        abil = [a[1:] for a in STRUCT[e.name]["abil"]]
        if abil:
            break
    ab = rng.choice(abil)
    q = rng.choice(Q_AB).format(v=VERB[ab], **_fmt(e))
    _mark(state, e, ("ab", ab))
    return gen.style_user(q, rng), ab_ans(e, ab)


def t_food(state, rng):
    e = rng.choice(gen.ANIMALS)
    foods = STRUCT[e.name]["foods"]
    f = rng.choice(foods) if rng.random() < 0.5 else rng.choice([x for x in ALL_FOODS if x not in foods])
    _mark(state, e, ("food", f))
    return gen.style_user(rng.choice(Q_FOOD).format(f=f, **_fmt(e)), rng), food_ans(e, f)


def t_diet(state, rng):
    e = rng.choice(gen.ANIMALS)
    kind = rng.choice(["meat", "plants"])
    _mark(state, e, ("diet", kind))
    return gen.style_user(rng.choice(Q_DIET[kind]).format(**_fmt(e)), rng), diet_ans(e, kind)


def t_class(state, rng):
    e = rng.choice(gen.ANIMALS)
    c = STRUCT[e.name]["cls"]
    _mark(state, e, ("class",))
    if rng.random() < 0.6:
        asked = c if (c in ASKABLE and rng.random() < 0.4) else rng.choice([x for x in ASKABLE if x != c])
        q = rng.choice(Q_CLASS_YN).format(ac=CLASS_A[asked], cp=CLASS_PL[asked], **_fmt(e))
        a = (f"Yes, {ref_of(e)} is {CLASS_A[c]}." if asked == c
             else f"No, {ref_of(e)} is {CLASS_A[c]}, not {CLASS_A[asked]}.")
        return gen.style_user(q, rng), a
    pair = [CLASS_A[c], CLASS_A[rng.choice([x for x in ASKABLE if x != c])]]
    rng.shuffle(pair)
    q = rng.choice(Q_CLASS_WHAT).format(ac=pair[0], ac2=pair[1], **_fmt(e))
    return gen.style_user(q, rng), class_ans(e)


def t_legs(state, rng):
    while True:
        e = rng.choice(gen.ANIMALS)
        if STRUCT[e.name]["legs"] >= 0:
            break
    _mark(state, e, ("legs",))
    return gen.style_user(rng.choice(Q_LEGS).format(**_fmt(e)), rng), legs_ans(e)


def t_compare(state, rng):
    while True:
        e1, e2 = rng.sample(gen.ANIMALS, 2)
        s1, s2 = STRUCT[e1.name]["size"], STRUCT[e2.name]["size"]
        if s1 != s2:
            break
    state["last"] = ("other",); state["attr"] = None
    r1, r2 = ref_of(e1), ref_of(e2)
    big, small = (r1, r2) if s1 > s2 else (r2, r1)
    f = dict(r1=r1, r2=r2)
    x = rng.random()
    if x < 0.45:
        return gen.style_user(rng.choice(Q_WHICH).format(**f), rng), f"{cap(big)} is bigger than {small}."
    if x < 0.65:
        return gen.style_user(rng.choice(Q_WHICH_S).format(**f), rng), f"{cap(small)} is smaller than {big}."
    if x < 0.85:
        a = f"Yes, {r1} is bigger than {r2}." if s1 > s2 else f"No, {r1} is smaller than {r2}."
        return gen.style_user(rng.choice(Q_YN_BIG).format(**f), rng), a
    a = f"Yes, {r1} is smaller than {r2}." if s1 < s2 else f"No, {r1} is bigger than {r2}."
    return gen.style_user(rng.choice(Q_YN_SMALL).format(**f), rng), a
