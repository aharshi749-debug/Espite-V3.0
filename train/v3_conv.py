import random

import gen
import v3_base as base
import v3_animals as A
import v3_misc as M
from v3_base import first_sentence, ref_of


def _attr_tuple(fn):
    def f(state, rng):
        out = fn(state, rng)
        k = state.get("attr")
        if isinstance(k, str):
            state["attr"] = (k,)
        return out
    return f


def t_compound(state, rng):
    if rng.random() < 0.7:
        e = rng.choice(gen.ANIMALS); tpl, parts = rng.choice(gen.COMP_1["animal"])
    else:
        e = rng.choice(gen.OBJECTS); tpl, parts = rng.choice(gen.COMP_1["object"])
    state["last"] = ("kb", e, 0)
    state["attr"] = (parts[-1],) if parts[-1] != "ans" else None
    q = tpl.format(ref=ref_of(e), pl=gen.pl_of(e))
    ans = " ".join(first_sentence(e.answer) if k == "ans" else M.part(e, k) for k in parts)
    return gen.style_user(q, rng), ans


GENERIC = [
    (gen.t_kb, 18), (_attr_tuple(gen.t_attr), 12), (t_compound, 6), (M.t_multi, 6), (gen.t_cause, 8),
    (M.t_math, 12), (A.t_ability, 7), (A.t_food, 5), (A.t_diet, 3), (A.t_class, 6), (A.t_legs, 3),
    (A.t_compare, 6), (M.t_unknown, 17), (M.t_multi_attr, 4), (gen.t_repeat, 3), (gen.t_count, 1), (gen.t_calendar, 4),
    (gen.t_color, 2), (gen.t_sound, 2), (gen.t_capital, 3), (gen.t_opposite, 2), (gen.t_joke, 3),
    (gen.t_story, 1.5), (gen.t_fact, 2), (gen.t_like, 2), (gen.t_cant, 2), (gen.t_statement, 1),
    (gen.t_fav, 1.5), (gen.t_ai, 4), (gen.simple(gen.ID_Q, gen.ID_A), 3), (gen.simple(gen.MAKER_Q, gen.MAKER_A), 1.5),
    (gen.simple(gen.AMRIO_Q, gen.AMRIO_A), 1.2), (gen.t_old_name, 0.4), (gen.simple(gen.HOW_Q, gen.HOW_A), 2),
    (gen.t_feel, 2), (gen.simple(gen.THANKS_Q, gen.THANKS_A), 1.5), (gen.simple(gen.NICE_Q, gen.NICE_A), 1),
    (gen.simple(gen.MEAN_Q, gen.MEAN_A), 1), (gen.simple(gen.YESNO_Q, gen.YESNO_A), 1), (gen.t_ask_name, 0.6),
    (gen.t_more, 0.4),
]
FN = [g for g, _ in GENERIC]
W = [w for _, w in GENERIC]


def conversation(rng):
    state = {}
    turns = []
    n = rng.choices(range(1, 13), weights=[14, 15, 14, 12, 10, 9, 7, 6, 5, 4, 3, 3])[0]
    name_at = rng.randrange(n) if (n >= 2 and rng.random() < 0.4) else -1
    for i in range(n):
        if i == 0 and rng.random() < 0.25:
            f = gen.simple(gen.GREET_Q, gen.GREET_A)
        elif i == name_at:
            f = gen.t_set_name
        elif state.get("name") and rng.random() < 0.06:
            f = M.t_change_name
        elif state.get("name") and rng.random() < 0.28:
            f = gen.t_ask_name
        elif state.get("last") and state["last"][0] == "kb" and rng.random() < 0.55:
            f = rng.choices([gen.t_more, M.t_what_about, gen.t_react, M.t_pronoun], weights=[4, 3, 1, 5])[0]
        elif state.get("last") and state["last"][0] in ("joke", "story") and rng.random() < 0.3:
            f = gen.t_more
        elif i == n - 1 and n > 1 and rng.random() < 0.12:
            f = gen.simple(gen.BYE_Q, gen.BYE_A)
        else:
            f = rng.choices(FN, weights=W)[0]
        turns.append(f(state, rng))
    return turns


def coverage(rng):
    out = []
    for e in gen.ENTRIES:
        st = {"last": ("kb", e, 0)}
        out.append([(gen.style_user(gen.kb_question(e, rng), rng), e.answer), gen.t_more(st, rng)])
    for e in gen.ANIMALS:
        for k in ("eat", "live", "likes"):
            q = rng.choice(gen.ATTR_Q[k]).format(ref=ref_of(e), pl=gen.pl_of(e), name=e.name)
            out.append([(gen.style_user(q, rng), e.attrs[k])])
        st = {}
        out.append([(gen.style_user(f"what kind of animal is {ref_of(e)}", rng), A.class_ans(e))])
        if A.legs_ans(e):
            out.append([(gen.style_user(f"how many legs does {ref_of(e)} have", rng), A.legs_ans(e))])
    for e in gen.OBJECTS:
        q = rng.choice(gen.ATTR_Q["used"]).format(ref=ref_of(e), pl=gen.pl_of(e), name=e.name)
        out.append([(gen.style_user(q, rng), e.used)])
    for phs, ans, d in gen.CAUSES:
        for ph in phs:
            q = rng.choice(gen.CAUSE_YOU).format(p=ph, pi=gen.cause_forms(ph)[0])
            out.append([(gen.style_user(q, rng), ans)])
    return out


def generate(n, seed, params_str="2.0 million", vocab_str="1024"):
    base.init(params_str)
    rng = random.Random(seed)
    convs = []
    for _ in range(max(1, n // 40000)):
        convs += coverage(rng)
    while len(convs) < n:
        convs.append(conversation(rng))
    rng.shuffle(convs)
    return convs
