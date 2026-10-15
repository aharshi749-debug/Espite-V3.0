import re

import gen
import kb
import kb2
import kb3

gen.PROPER |= {"komodo dragon"}
STRUCT = {}
UNKNOWN = []
ALL_FOODS = []


def first_sentence(text):
    m = re.search(r"[.!?](\s|$)", text)
    return text[:m.end()].strip() if m else text


def ref_of(e):
    return e.ref() if e.article else e.name


def disp_pl(e):
    return e.display_pl or e.display


def init(params_str):
    gen.PARAMS_STR = params_str
    for k in gen.AI_Q:
        qs, a = gen.AI_Q[k]
        gen.AI_Q[k] = (qs, re.sub(r"\d\.\d million", params_str, a))
    na, nattr, nstruct = kb3.parse_new_animals()
    nt, nused = kb3.parse_new_topics()
    ents = [gen.Entry(d) for d in kb.parse_kb() + na + nt]
    attrs = kb2.parse_attrs(); attrs.update(nattr)
    used = kb2.parse_used(); used.update(nused)
    for e in ents:
        e.attrs = attrs.get(e.name)
        e.used = used.get(e.name)
    gen.ENTRIES = ents
    gen.BY_NAME = {e.name: e for e in ents}
    gen.ANIMALS = [e for e in ents if e.attrs]
    gen.OBJECTS = [e for e in ents if e.used]
    gen.CAUSES = kb2.parse_cause()
    known = {e.name for e in ents} | {e.plural for e in ents if e.plural}
    gen.KNOWN_WORDS = known
    STRUCT.clear(); STRUCT.update(kb3.parse_struct()); STRUCT.update(nstruct)
    assert {e.name for e in gen.ANIMALS} == set(STRUCT)
    UNKNOWN[:] = sorted({w for w in kb.UNKNOWN_NOUNS + kb3.EXTRA_UNKNOWN if w not in known})
    gen.UNKNOWN_NOUNS = UNKNOWN
    ALL_FOODS[:] = sorted({f for s in STRUCT.values() for f in s["foods"]})


SLANG = [(r"\bwhat is\b", ["wat is", "wut is", "whats"]), (r"\byou\b", ["u"]), (r"\bare\b", ["r"]),
         (r"\bplease\b", ["pls", "plz"]), (r"\bdo you\b", ["do u"]), (r"\bwhat\b", ["wat", "wut"]),
         (r"\bthe\b", ["da"])]
_style_v2 = gen.style_user


def style_user(text, rng, typo=True, wrap=True):
    if typo and rng.random() < 0.08:
        for pat, reps in SLANG:
            if re.search(pat, text) and rng.random() < 0.6:
                text = re.sub(pat, rng.choice(reps), text, count=1)
    t = _style_v2(text, rng, typo=False, wrap=wrap)
    if rng.random() < 0.04:
        t = t.title()
    if typo and rng.random() < 0.06:
        words = t.split(" ")
        idx = [i for i, w in enumerate(words) if len(w) >= 4 and w.isalpha()]
        if idx:
            i = max(idx, key=lambda j: len(words[j]))
            words[i] = gen.add_typo(words[i], rng)
            t = " ".join(words)
    if typo and rng.random() < 0.11:
        t = gen.add_typo(t, rng)
        if rng.random() < 0.3:
            t = gen.add_typo(t, rng)
    return t


gen.style_user = style_user

EXTRA_WHAT = ["{bare} definition", "definition of {bare}", "explain {ref} to a kid", "explain {ref} like i'm five",
              "what even is {ref}", "the thing called {ref}, what is it", "{ref}? what's that",
              "i've never heard of {ref}, what is it", "what in the world is {ref}", "so what is {ref} really",
              "what does {bare} mean", "what can you tell me about {ref}", "ok but what is {ref}",
              "{bare}, what's that", "wait what is {ref}", "remind me what {ref} is", "info on {bare}",
              "tell me what {ref} is", "what is this {bare} thing", "what's {ref} all about"]
EXTRA_WHAT_PL = ["{pl}. what are they", "what's the deal with {pl}", "tell me something about {pl}",
                 "what are {pl} anyway", "what even are {pl}", "explain {pl} to me"]
_kbq_v2 = gen.kb_question


def kb_question(e, rng):
    if rng.random() < 0.35:
        forms = list(EXTRA_WHAT)
        if e.plural and e.plural != e.name:
            forms += EXTRA_WHAT_PL
        return rng.choice(forms).format(ref=ref_of(e), bare=e.name, pl=gen.pl_of(e))
    return _kbq_v2(e, rng)


gen.kb_question = kb_question
