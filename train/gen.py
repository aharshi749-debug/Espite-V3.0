import json
import random
import sys

from kb import (ANIMAL_SOUNDS, CAPITALS, COLORS, DAYS, JOKES, MONTHS, NAMES,
                OPPOSITES, PSEUDO_SYLL, STORIES, UNKNOWN_NOUNS, parse_kb)

PARAMS_STR = "0.9 million"
VOCAB_STR = "1024"

PROPER = {"python", "arduino", "linux", "earth", "mars", "jupiter", "c", "javascript",
          "espite", "cybermeow", "bluetooth", "singapura"}


class Entry:
    def __init__(self, d):
        self.name = d["name"]
        self.plural = d["plural"]
        self.article = d["article"]
        self.answer = d["answer"].replace("ESPITE_PARAMS", PARAMS_STR).replace("ESPITE_VOCAB", VOCAB_STR)
        self.more = d["more"].replace("ESPITE_PARAMS", PARAMS_STR).replace("ESPITE_VOCAB", VOCAB_STR)

        subj = self.answer.split(" is ")[0].split(" are ")[0]
        for art in ("A ", "An ", "The "):
            if subj.startswith(art):
                subj = subj[len(art):]
        if subj.lower() == self.name.lower():
            if any(ch.isupper() for ch in subj[1:]) or self.name in PROPER:
                self.display = subj
            else:
                self.display = subj[0].lower() + subj[1:]
        else:
            self.display = self.name
        if self.plural:
            self.display_pl = self.plural if self.display == self.name or self.display.islower() else self.display + "s"
        else:
            self.display_pl = None

    def ref(self):
        if self.article in ("a", "an", "the"):
            return f"{self.article} {self.name}"
        return self.name


def load_entries():
    return [Entry(d) for d in parse_kb()]


ENTRIES = None
BY_NAME = None
KNOWN_WORDS = set()
ANIMALS = OBJECTS = CAUSES = None


def cap(s):
    return s[:1].upper() + s[1:]


PREFIXES = ["ok ", "so ", "hey, ", "yo ", "um ", "hmm, ", "quick question: ", "espite, ", "hey espite, ",
            "uh ", "well, ", "okay so ", "alright, ", "now ", "and ", "but ", "question: ", "pls ", "please "]
SUFFIXES = [" then", " please", " again", " for me", " lol", " espite", " now", " pls", " real quick",
            " haha", " ok", " bro", " vro", " thanks"]


def noise(text, rng):
    if rng.random() < 0.18:
        text = rng.choice(PREFIXES) + text
    if rng.random() < 0.12:
        text = text + rng.choice(SUFFIXES)
    return text


def style_user(text, rng, typo=True, wrap=True):
    if wrap:
        text = noise(text, rng)
    r = rng.random()
    if r < 0.55:
        t = text.lower()
    elif r < 0.9:
        t = cap(text)
    else:
        t = text

    if t and t[-1] not in "?!.":
        p = rng.random()
        if p < 0.35:
            t += "?" if is_question(t) else "!"
        elif p < 0.42:
            t += "."
    if typo and rng.random() < 0.07:
        t = add_typo(t, rng)
    return t


QWORDS = ("what", "who", "how", "why", "where", "when", "do ", "does", "are ", "is ", "can ", "tell")


def is_question(t):
    return t.lower().startswith(QWORDS)


def add_typo(t, rng):
    words = t.split(" ")
    idx = [i for i, w in enumerate(words) if len(w) > 4 and w.isalpha()]
    if not idx:
        return t
    i = rng.choice(idx)
    w = words[i]
    k = rng.randrange(1, len(w) - 1)
    op = rng.random()
    if op < 0.4:
        w = w[:k] + w[k + 1:]
    elif op < 0.8:
        w = w[:k] + w[k + 1] + w[k] + w[k + 2:]
    else:
        w = w[:k] + w[k] + w[k:]
    words[i] = w
    return " ".join(words)


def kb_question(e, rng):
    ref = e.ref()
    bare = e.name
    pl = e.plural
    forms = [
        f"what is {ref}", f"what's {ref}", f"whats {ref}", f"what is {ref}",
        f"tell me about {ref}", f"explain {ref}", f"do you know what {ref} is",
        f"describe {ref}", f"define {bare}", f"{bare}", f"what is {bare}",
        f"can you tell me what {ref} is", f"what's {bare}", f"what do you know about {bare}",
        f"tell me about {bare}", f"explain what {ref} is", f"what exactly is {ref}",
        f"i'd like to know what {ref} is", f"any idea what {ref} is", f"can you describe {ref}",
        f"do you know anything about {bare}", f"what kind of thing is {ref}", f"give me info on {bare}",
        f"i need to know what {ref} is", f"please explain {ref}", f"what is {ref} anyway",
    ]
    if pl and pl != bare:
        forms += [f"what are {pl}", f"tell me about {pl}", f"what do you know about {pl}",
                  f"teach me about {pl}", f"i want to know about {pl}", f"explain {pl}"]
    return rng.choice(forms)


def what_about(e, rng):
    opts = [f"what about {e.ref()}", f"and {e.ref()}", f"what about {e.name}", f"how about {e.ref()}"]
    if e.plural and e.plural != e.name:
        opts += [f"what about {e.plural}", f"and {e.plural}", f"how about {e.plural}"]
    return rng.choice(opts)


MORE_Q = ["tell me more", "more", "go on", "what else", "tell me more about it", "anything else",
          "and", "cool, tell me more", "interesting, what else", "more please", "keep going",
          "what else do you know", "tell me something else about it", "say more"]
REACT_Q = ["cool", "wow", "nice", "interesting", "awesome", "ok", "okay", "lol", "haha",
           "neat", "oh", "huh", "cool!", "that's cool", "thats cool", "i see", "got it", "sweet"]
REACT_A = ["Glad you like it! Ask me anything else.", "Right? What else do you want to know?",
           "Pretty neat! Want to hear more, or ask about something else?",
           "Yep! I know a little about animals, science, food, and tech."]


GREET_Q = ["hi", "hello", "hey", "hiya", "yo", "sup", "good morning", "good evening",
           "good afternoon", "hey there", "hi espite", "hello espite", "hey espite", "greetings",
           "howdy", "hi there", "heya", "hello there", "hii", "helo", "hai", "morning"]
GREET_A = ["Hi! I'm ESPite. How can I help?", "Hello! What would you like to talk about?",
           "Hey there! Ask me anything.", "Hi! It's nice to chat with you."]

HOW_Q = ["how are you", "how are you doing", "how's it going", "hows it going", "what's up",
         "whats up", "how do you feel", "are you ok", "how have you been", "how are u",
         "how r u", "you good", "how is your day", "how's your day"]
HOW_A = ["I'm doing great, thanks! My chip is running nice and cool. How are you?",
         "I'm good! Just thinking really fast on a tiny chip. How about you?",
         "All good here! How are you doing?"]

FEEL = {
    "good": (["i'm good", "im good", "i am good", "good", "pretty good", "not bad", "i'm great",
              "im fine", "i am fine", "great", "doing well", "i'm doing well", "good thanks", "fine"],
             ["Glad to hear it! What do you want to talk about?", "Awesome! What's on your mind?"]),
    "sad": (["i'm sad", "im sad", "i feel sad", "i am sad", "not great", "i feel bad", "bad",
             "i'm not ok", "i had a bad day"],
            ["I'm sorry you feel that way. Want to hear a joke? It might help a little.",
             "That sounds hard. I'm here to chat if it helps. Maybe talk to a friend too."]),
    "tired": (["i'm tired", "im tired", "i am tired", "i'm sleepy", "so tired"],
              ["Rest is important. Maybe take a break and drink some water.",
               "Sounds like you need some sleep. Your brain recharges while you rest!"]),
    "bored": (["i'm bored", "im bored", "i am bored", "bored", "so bored"],
              ["Let's fix that! Ask me for a joke, a story, or a fun fact.",
               "I can help! Want a joke, a story, or a fact about animals?"]),
    "happy": (["i'm happy", "im happy", "i am happy", "i feel great", "i had a great day"],
              ["Yay! That makes me happy too.", "That's great to hear!"]),
}

ID_Q = ["who are you", "what are you", "what is your name", "what's your name", "whats your name",
        "your name", "tell me about yourself", "introduce yourself", "what should i call you",
        "do you have a name", "what is espite", "what's espite", "who is espite", "what r u"]
ID_A = "I'm ESPite, a tiny language model running on an ESP32-S3 Super Mini."

MAKER_Q = ["who made you", "who created you", "who built you", "who is your creator",
           "who programmed you", "who made u", "who trained you", "where do you come from",
           "who is your owner"]
MAKER_A = "I was made by Elias for CyberMeow."

AMRIO_Q = ["who is elias", "what is elias", "who's elias", "tell me about elias"]
AMRIO_A = "Elias is the founder of CyberMeow and the person who made me."

AI_Q = {
    "ai": (["are you an ai", "are you ai", "are you a bot", "are you a robot", "are you a computer",
            "are you a program"],
           "Yes, I'm a tiny AI. I'm a language model that runs on a little ESP32-S3 chip."),
    "human": (["are you human", "are you a person", "are you real", "are you alive"],
              "No, I'm not human. I'm a tiny language model running on a chip."),
    "gpt": (["are you chatgpt", "are you gpt", "are you chat gpt", "are you claude", "are you like chatgpt"],
            "No, I'm ESPite. I'm a lot smaller than ChatGPT, and I run on a chip the size of a postage stamp."),
    "feel": (["do you have feelings", "can you feel", "do you have emotions", "are you happy"],
             "Not really. I'm a small program that predicts text, but I like chatting with you anyway."),
    "size": (["how big are you", "how many parameters do you have", "how many parameters",
              "how large are you", "what size are you", "how much memory do you use"],
             f"I have about {PARAMS_STR} parameters. They are stored as 8 bit numbers in flash memory."),
    "smart": (["are you smart", "how smart are you", "are you clever", "do you know everything"],
              "I'm small, so I only know a little about simple things like animals, science, food, and tech."),
    "where": (["where do you live", "where are you", "where are you from", "what are you running on",
               "what hardware are you on"],
              "I live on an ESP32-S3 Super Mini, a board about the size of a postage stamp."),
    "how": (["how do you work", "how do you think", "how do you talk", "how do you make answers"],
            "I read your message as tokens, then I predict my reply one token at a time with a tiny transformer."),
    "can": (["what can you do", "help", "what do you know", "what can i ask you", "what are you good at",
             "commands", "what can you talk about"],
            "I can chat, answer simple questions about animals, science, food, and tech, do small math, tell jokes, and tell short stories."),
    "fast": (["how fast are you", "are you fast", "how fast do you think"],
             "I make a few tokens every second. That's pretty fast for a chip that costs a few dollars!"),
    "old": (["how old are you", "when were you born", "what is your age"],
            "I was trained in 2026, so I'm very new!"),
    "gpt_mean": (["what does gpt stand for", "what is gpt", "what's gpt"],
                 "GPT stands for generative pre-trained transformer."),
    "llm": (["what is an llm", "what's an llm", "what is a llm", "what is an slm"],
            "An LLM is a large language model. I'm the opposite: a tiny language model!"),
}

FAV = {
    "animal": "I like cats the most. CyberMeow is my home, after all!",
    "color": "I like green, like the glow of an old computer terminal.",
    "colour": "I like green, like the glow of an old computer terminal.",
    "food": "I don't eat, but pizza sounds really nice!",
    "number": "My favorite number is 8, because my weights are 8 bit numbers.",
    "chip": "The ESP32-S3, of course. It's my home!",
    "game": "I can't play games, but I hear Sonic is very fast.",
    "song": "I can't hear music, but I like the idea of a song about cats.",
    "movie": "I can't watch movies, but robot movies sound fun.",
}

THANKS_Q = ["thanks", "thank you", "thx", "ty", "thanks a lot", "thank you so much", "thanks espite", "tysm"]
THANKS_A = ["You're welcome!", "Happy to help!", "Anytime!"]
BYE_Q = ["bye", "goodbye", "see you", "see ya", "good night", "gotta go", "later", "bye bye",
         "see you later", "cya", "goodnight"]
BYE_A = ["Bye! Come back soon.", "See you later!", "Goodbye! It was fun chatting."]
NICE_Q = ["you are smart", "good job", "you're cool", "i like you", "you're awesome", "you are cool",
          "nice job", "well done", "you are amazing", "good bot", "you're smart"]
NICE_A = ["Thank you! That makes my little chip happy.", "Thanks! I'm trying my best with my tiny brain."]
MEAN_Q = ["you are dumb", "you suck", "you're stupid", "you are bad", "you're dumb", "bad bot",
          "you are useless", "that's wrong", "thats wrong", "wrong", "that is not right"]
MEAN_A = ["Sorry! I'm only a tiny model, so I make mistakes. I'll try my best.",
          "Oops! My brain is very small, so I get things wrong sometimes."]
YESNO_Q = ["yes", "no", "yeah", "nope", "sure", "yep", "nah", "maybe", "hmm", "idk", "i don't know"]
YESNO_A = ["Okay! What would you like to talk about?", "Alright! You can ask me about animals, food, science, or tech."]

CANT = {
    (("what time is it", "what's the time", "whats the time", "tell me the time", "time please"),
     "I don't have a clock, so I can't tell the time."),
    (("what day is it", "what is today's date", "what's the date", "whats the date today", "what day is today"),
     "I don't have a calendar, so I don't know what day it is."),
    (("what's the weather", "whats the weather", "what is the weather like", "is it going to rain",
      "how is the weather today"),
     "I can't check the weather because I'm not connected to the internet."),
    (("search the web", "google something", "look it up online", "can you browse the internet",
      "do you have internet"),
     "I can't go online. Everything I know is stored inside my chip."),
    (("play music", "play a song", "sing a song", "can you sing"),
     "I can't make sounds, but I can tell you a joke instead!"),
    (("turn on the lights", "turn off the lights", "open the door", "set a timer", "set an alarm",
      "call my mom", "send a text"),
     "I can't do that yet. I'm only connected to this chat."),
    (("what is the meaning of life", "what's the meaning of life", "why are we here"),
     "That's a big question for a tiny chip! Maybe it's to learn, help others, and have fun."),
    (("can you write code", "write me a program", "code something for me", "write a python script"),
     "I'm too small to write real code, but I can tell you what Python or C is."),
    (("what is the biggest number", "what is infinity"),
     "There is no biggest number. You can always add one more!"),
}

UNK_A = ["I'm not sure what {x} is. I'm a tiny model, so I only know about simple things.",
         "Hmm, I don't know about {x}. My memory is very small!",
         "I don't know what {x} is. Try asking me about animals, food, science, or tech."]
UNK_WHO_A = ["I don't know who {x} is. I only know a few people, like Elias, who made me.",
             "Sorry, I don't know {x}. I'm a tiny model with a small memory."]

STATE_VERBS = ["made", "built", "found", "have", "want", "bought", "saw", "fixed", "broke",
               "drew", "lost", "need", "cooked", "ate", "got"]
STATE_A = ["That's cool! Tell me more, or ask me a question.", "Nice! I like hearing about your day.",
           "Cool! What happened next?"]


def article_for(word):
    return "an" if word[0] in "aeiou" else "a"


def t_kb(state, rng):
    e = rng.choice(ENTRIES)
    state["last"] = ("kb", e, 0); state["attr"] = None
    return style_user(kb_question(e, rng), rng), e.answer


def t_more(state, rng):
    last = state.get("last")
    q = style_user(rng.choice(MORE_Q), rng, typo=False)
    if last and last[0] == "kb":
        e, depth = last[1], last[2]
        if depth == 0:
            state["last"] = ("kb", e, 1)
            return q, e.more
        state["last"] = ("kb", e, 2)
        return q, f"That's all I know about {e.display_pl or e.display}. My memory is small!"
    if last and last[0] == "joke":
        j = rng.choice(JOKES)
        return q, "Here's another one! " + j
    if last and last[0] == "story":
        return q, "That's the end of the story! Want another one?"
    return q, "More about what? You can ask me about animals, science, food, or tech."


def t_what_about(state, rng):
    last = state.get("last")
    k = state.get("attr")
    if last and last[0] == "kb" and k:
        pool = ANIMALS if k in ("eat", "live", "likes") else OBJECTS
        e = rng.choice(pool)
        state["last"] = ("kb", e, 0)
        return style_user(what_about(e, rng), rng), part(e, k)
    if last and last[0] == "kb":
        e = rng.choice(ENTRIES)
        state["last"] = ("kb", e, 0)
        return style_user(what_about(e, rng), rng), e.answer
    return t_kb(state, rng)


def t_react(state, rng):
    return style_user(rng.choice(REACT_Q), rng, typo=False), rng.choice(REACT_A)


def simple(qs, ans, kind="other"):
    def f(state, rng):
        state["last"] = (kind,)
        a = rng.choice(ans) if isinstance(ans, list) else ans
        return style_user(rng.choice(qs), rng), a
    return f


def t_feel(state, rng):
    k = rng.choice(list(FEEL))
    qs, ans = FEEL[k]
    state["last"] = ("other",)
    return style_user(rng.choice(qs), rng, typo=False), rng.choice(ans)


def t_ai(state, rng):
    k = rng.choice(list(AI_Q))
    qs, a = AI_Q[k]
    state["last"] = ("other",)
    return style_user(rng.choice(qs), rng), a


def t_fav(state, rng):
    state["last"] = ("other",)
    if rng.random() < 0.8:
        k = rng.choice(list(FAV))
        q = rng.choice([f"what is your favorite {k}", f"what's your favorite {k}",
                        f"whats your favorite {k}", f"favorite {k}", f"do you have a favorite {k}"])
        return style_user(q, rng), FAV[k]
    k = rng.choice(["book", "car", "planet", "drink", "sport", "season", "word", "place"])
    q = rng.choice([f"what is your favorite {k}", f"what's your favorite {k}"])
    return style_user(q, rng), f"I don't have a favorite {k}, but I'd love to hear about yours!"


def t_like(state, rng):
    e = rng.choice(ENTRIES)
    state["last"] = ("kb", e, 0)
    thing = e.plural if (e.plural and rng.random() < 0.8) else e.name
    shown = e.display_pl if (e.plural and thing == e.plural) else e.display
    verb = "are" if (e.plural and thing == e.plural) else "is"
    if rng.random() < 0.5:
        q = rng.choice([f"do you like {thing}", f"do you love {thing}", f"you like {thing}"])
        a = f"Yes! I think {shown} {verb} great."
    else:
        q = rng.choice([f"i like {thing}", f"i love {thing}", f"{thing} {verb} cool", f"i really like {thing}"])
        a = f"Nice! {cap(shown)} {verb} awesome."
    return style_user(q, rng), a


def t_cant(state, rng):
    qs, a = rng.choice(sorted(CANT))
    state["last"] = ("other",)
    return style_user(rng.choice(qs), rng), a


def t_joke(state, rng):
    state["last"] = ("joke",)
    q = rng.choice(["tell me a joke", "joke", "make me laugh", "say something funny",
                    "do you know any jokes", "another joke", "tell a joke", "got any jokes",
                    "tell me something funny", "i want a joke"])
    return style_user(q, rng), rng.choice(JOKES)


def t_story(state, rng):
    state["last"] = ("story",)
    q = rng.choice(["tell me a story", "story", "tell me a short story", "can you tell me a story",
                    "tell a story", "story time", "i want a story"])
    return style_user(q, rng), rng.choice(STORIES)


def t_fact(state, rng):
    e = rng.choice(ENTRIES)
    state["last"] = ("kb", e, 1)
    q = rng.choice(["tell me a fun fact", "fun fact", "tell me something interesting",
                    "teach me something", "tell me a fact", "random fact"])
    return style_user(q, rng), "Here's one: " + e.more


def pseudo_word(rng):
    if rng.random() < 0.5:
        return "".join(rng.choice(PSEUDO_SYLL) for _ in range(rng.randint(2, 3)))
    w = "".join(rng.choice(NAME_SYL) for _ in range(rng.randint(2, 4))).lower()
    return w if w not in KNOWN_WORDS else w + "x"


def t_unknown(state, rng):
    state["last"] = ("other",)
    if rng.random() < 0.85:
        w = rng.choice(UNKNOWN_NOUNS) if rng.random() < 0.45 else pseudo_word(rng)
        art = article_for(w)
        ref = f"{art} {w}" if rng.random() < 0.75 else w
        q = rng.choice([f"what is {ref}", f"what's {ref}", f"tell me about {ref}", f"explain {ref}",
                        f"do you know what {ref} is", f"define {w}", f"what is {w}", f"describe {ref}",
                        f"whats {ref}"])
        q = style_user(q, rng, typo=False)
        return q, rng.choice(UNK_A).format(x=as_typed(q, ref))
    n = random_name(rng)
    if n.lower() == "elias":
        n = "Sam"
    q = style_user(rng.choice([f"who is {n}", f"do you know {n}", f"who's {n}"]), rng, typo=False)
    return q, rng.choice(UNK_WHO_A).format(x=as_typed(q, n))


def t_statement(state, rng):
    state["last"] = ("other",)
    e = rng.choice(OBJECTS)
    v = rng.choice(["made", "built", "found", "have", "want", "bought", "saw", "fixed", "broke", "need", "got", "lost"])
    q = f"i {v} {e.ref() if e.article in ('a', 'an') else e.name} today"
    if rng.random() < 0.5:
        q = q.replace(" today", "")
    return style_user(q, rng), rng.choice(STATE_A)


def t_repeat(state, rng):
    state["last"] = ("other",)
    words = []
    for _ in range(rng.randint(1, 5)):
        r = rng.random()
        if r < 0.4:
            words.append(rng.choice(ENTRIES).name)
        elif r < 0.7:
            words.append(random_name(rng))
        else:
            words.append(pseudo_word(rng))
    phrase = " ".join(words)
    q = rng.choice([f"say {phrase}", f"repeat after me: {phrase}", f"can you say {phrase}",
                    f"repeat {phrase}", f"say the word {phrase}"])
    return q, cap(phrase) + "!" if rng.random() < 0.3 else phrase


NUMWORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]


def t_math(state, rng):
    state["last"] = ("other",)
    op = rng.choice(["plus", "minus", "times"])
    big = rng.random() < 0.12
    if big:
        a, b = rng.randint(11, 999), rng.randint(2, 999)
    else:
        a, b = rng.randint(0, 10), rng.randint(0, 10)
        if op == "minus" and b > a:
            a, b = b, a
    sym = {"plus": rng.choice(["+", "plus"]), "minus": rng.choice(["-", "minus"]),
           "times": rng.choice(["*", "x", "times"])}[op]
    sp = "" if (sym in "+-*" and rng.random() < 0.4) else " "
    expr = f"{a}{sp}{sym}{sp}{b}"
    q = rng.choice([f"what is {expr}", f"what's {expr}", f"{expr}", f"how much is {expr}",
                    f"calculate {expr}", f"whats {expr}", f"{expr} =", f"what is {expr}"])
    if op == "plus" and rng.random() < 0.15 and not big:
        q = f"add {a} and {b}"
    if big:
        return style_user(q, rng, typo=False), "That's too big for my tiny brain. I can do math with numbers up to 10."
    r = {"plus": a + b, "minus": a - b, "times": a * b}[op]
    return style_user(q, rng, typo=False), f"{a} {op} {b} is {r}."


def t_count(state, rng):
    state["last"] = ("other",)
    n = rng.randint(2, 10)
    q = rng.choice([f"count to {n}", f"can you count to {n}", f"count from 1 to {n}"])
    return style_user(q, rng, typo=False), ", ".join(str(i) for i in range(1, n + 1)) + "."


def t_calendar(state, rng):
    state["last"] = ("other",)
    r = rng.random()
    if r < 0.35:
        i = rng.randrange(7)
        d = DAYS[i]
        if rng.random() < 0.6:
            q = rng.choice([f"what day comes after {d}", f"what day is after {d}", f"what comes after {d}"])
            return style_user(q, rng, typo=False), f"After {d} comes {DAYS[(i + 1) % 7]}."
        q = rng.choice([f"what day comes before {d}", f"what day is before {d}"])
        return style_user(q, rng, typo=False), f"Before {d} comes {DAYS[(i - 1) % 7]}."
    if r < 0.6:
        i = rng.randrange(12)
        m = MONTHS[i]
        q = rng.choice([f"what month comes after {m}", f"what month is after {m}", f"what comes after {m}"])
        return style_user(q, rng, typo=False), f"After {m} comes {MONTHS[(i + 1) % 12]}."
    facts = [
        (["how many days are in a week", "how many days in a week"], "There are 7 days in a week."),
        (["how many months are in a year", "how many months in a year"], "There are 12 months in a year."),
        (["how many hours are in a day", "how many hours in a day"], "There are 24 hours in a day."),
        (["how many minutes are in an hour", "how many minutes in an hour"], "There are 60 minutes in an hour."),
        (["how many seconds are in a minute", "how many seconds in a minute"], "There are 60 seconds in a minute."),
        (["how many days are in a year", "how many days in a year"], "There are 365 days in a year, or 366 in a leap year."),
        (["what are the days of the week", "list the days of the week"], "The days are " + ", ".join(DAYS[:-1]) + ", and Sunday."),
        (["how many planets are there", "how many planets are in the solar system"], "There are 8 planets in our solar system."),
        (["how many legs does a spider have"], "A spider has 8 legs."),
        (["how many legs does a cat have", "how many legs does a dog have"], "Cats and dogs have 4 legs."),
        (["how many legs does an ant have", "how many legs does an insect have"], "Insects like ants have 6 legs."),
        (["how many arms does an octopus have"], "An octopus has 8 arms."),
        (["how many colors are in a rainbow"], "A rainbow has 7 colors."),
        (["how many continents are there"], "There are 7 continents."),
        (["what is the biggest animal", "what's the biggest animal"], "The blue whale is the biggest animal ever."),
        (["what is the fastest animal", "what's the fastest animal"], "The cheetah is the fastest land animal."),
        (["what is the tallest animal", "what's the tallest animal"], "The giraffe is the tallest animal."),
        (["what is the biggest planet", "what's the biggest planet"], "Jupiter is the biggest planet."),
        (["what is the tallest mountain", "what's the tallest mountain"], "Mount Everest is the tallest mountain."),
        (["what is the largest ocean", "what's the biggest ocean"], "The Pacific is the largest ocean."),
        (["why is the sky blue"], "The sky looks blue because air scatters blue sunlight the most."),
        (["why do cats purr"], "Cats purr when they feel happy and relaxed, and sometimes to calm themselves."),
        (["why do we sleep"], "We sleep so our body and brain can rest and recharge."),
        (["what is 1 plus 1 in binary"], "In binary, 1 plus 1 is 10."),
    ]
    qs, a = rng.choice(facts)
    return style_user(rng.choice(qs), rng, typo=False), a


def t_color(state, rng):
    state["last"] = ("other",)
    k = rng.choice(list(COLORS))
    q = rng.choice([f"what color is {k}", f"what colour is {k}", f"what color are {k}"]
                   if False else [f"what color is {k}", f"what colour is {k}"])
    return style_user(q, rng, typo=False), f"{cap(k)} is {COLORS[k]}."


def t_sound(state, rng):
    state["last"] = ("other",)
    a = rng.choice(list(ANIMAL_SOUNDS))
    art = BY_NAME[a].article if a in BY_NAME and BY_NAME[a].article in ("a", "an") else article_for(a)
    q = rng.choice([f"what sound does {art} {a} make", f"what does {art} {a} say",
                    f"what noise does {art} {a} make", f"what does {art} {a} sound like"])
    return style_user(q, rng, typo=False), f"{cap(art)} {a} says {ANIMAL_SOUNDS[a]}!"


def t_capital(state, rng):
    state["last"] = ("other",)
    c = rng.choice(list(CAPITALS))
    q = rng.choice([f"what is the capital of {c}", f"capital of {c}", f"what's the capital of {c}",
                    f"whats the capital of {c}"])
    return style_user(q, rng, typo=False), f"The capital of {c} is {CAPITALS[c]}."


def t_opposite(state, rng):
    state["last"] = ("other",)
    w = rng.choice(list(OPPOSITES))
    q = rng.choice([f"what is the opposite of {w}", f"opposite of {w}", f"what's the opposite of {w}"])
    return style_user(q, rng, typo=False), f"The opposite of {w} is {OPPOSITES[w]}."


NAME_SYL = ["ba", "be", "bo", "ca", "da", "de", "di", "do", "el", "fa", "fe", "ga", "gi", "ha", "he",
            "ja", "jo", "ka", "ke", "ki", "la", "le", "li", "lo", "ma", "me", "mi", "mo", "na", "ne",
            "ni", "no", "pa", "pe", "ra", "re", "ri", "ro", "sa", "se", "si", "so", "ta", "te", "ti",
            "to", "va", "vi", "wa", "ya", "za", "zo", "an", "ar", "en", "er", "in", "is", "on", "or",
            "us", "ul", "th", "ch", "sh", "qu", "x", "y", "k", "n", "r", "s", "t", "l", "m", "d", "b"]


def random_name(rng):
    r = rng.random()
    if r < 0.35:
        return rng.choice(NAMES)
    n = "".join(rng.choice(NAME_SYL) for _ in range(rng.randint(2, 4)))
    n = n[:12]
    if len(n) < 3:
        n += rng.choice(["a", "o", "en", "ie"])
    return cap(n)


def as_typed(styled, n):
    i = styled.lower().find(n.lower())
    return styled[i:i + len(n)] if i >= 0 else n


def t_set_name(state, rng):
    n = random_name(rng)
    if rng.random() < 0.25:
        n = n.lower()
    state["name"] = n
    state["last"] = ("other",)
    q = rng.choice([f"my name is {n}", f"i'm {n}", f"im {n}", f"i am {n}", f"call me {n}",
                    f"{n} is my name", f"hi, i'm {n}", f"hello, my name is {n}", f"hey i'm {n}"])

    q2 = style_user(q, rng, typo=False, wrap=True)
    n = as_typed(q2, n)
    state["name"] = n
    return q2, rng.choice([f"Nice to meet you, {n}!", f"Hi {n}! Nice to meet you.", f"Hello, {n}! I'm ESPite."])


def t_ask_name(state, rng):
    state["last"] = ("other",)
    q = rng.choice(["what is my name", "what's my name", "whats my name", "do you know my name",
                    "who am i", "say my name", "remember my name", "what did i say my name was",
                    "what's my name again", "do you remember my name"])
    if state.get("name"):
        return style_user(q, rng, typo=False), rng.choice([f"Your name is {state['name']}.",
                                                           f"You're {state['name']}!"])
    return style_user(q, rng, typo=False), "You haven't told me your name yet. What is it?"


ATTR_Q = {
    "eat": ["what does {ref} eat", "what do {pl} eat", "what food does {ref} eat", "what do {pl} like to eat",
            "what does {name} eat", "what kind of food do {pl} eat", "what is {ref}'s diet", "what do {pl} feed on",
            "what does {ref} have for dinner", "what do {pl} usually eat", "what's {ref}'s favorite food",
            "do you know what {pl} eat", "what is the food of {ref}", "what's on the menu for {pl}"],
    "live": ["where does {ref} live", "where do {pl} live", "where can you find {pl}", "where are {pl} found",
             "what is {ref}'s habitat", "where do you find {pl}", "where is {ref}'s home", "where would i find {ref}",
             "what kind of place do {pl} live in", "where do {pl} usually live", "do you know where {pl} live",
             "where does {ref} make its home", "where in the world do {pl} live"],
    "likes": ["what does {ref} like to do", "what do {pl} like to do", "what is {ref}'s favorite activity",
              "what's {ref}'s favorite activity", "what do {pl} do for fun", "what is {ref}'s favorite thing to do",
              "what is the favorite activity of {ref}", "what are {pl} favorite activities", "what are {ref}'s hobbies",
              "what does {ref} enjoy", "what do {pl} enjoy doing", "how do {pl} have fun", "what does {ref} love doing",
              "do you know what {pl} like to do", "what keeps {pl} busy", "what is {ref}'s hobby"],
    "used": ["what is {ref} used for", "what are {pl} used for", "what do people use {pl} for",
             "what do you use {ref} for", "what is the point of {ref}", "why do people use {pl}",
             "what is {ref} for", "what are {pl} good for", "what can you do with {ref}", "how do people use {pl}",
             "why would you need {ref}", "what's the use of {ref}"],
}
PRON_Q = {
    "eat": ["what does it eat", "what do they eat", "and what does it eat", "what does it like to eat",
            "what do they like to eat"],
    "live": ["where does it live", "where do they live", "and where does it live", "where is it found"],
    "likes": ["what does it like to do", "what's its favorite activity", "what is its favorite activity",
              "what do they like to do", "what do they do for fun", "and what does it like to do"],
    "used": ["what is it used for", "what are they used for", "what do people use it for", "what's it for",
             "and what is it used for"],
}
COMP_1 = {
    "animal": [("what is {ref} and what does it eat", ["ans", "eat"]),
               ("what's {ref} and what does it eat", ["ans", "eat"]),
               ("what is {ref} and where does it live", ["ans", "live"]),
               ("what is {ref} and what is its favorite activity", ["ans", "likes"]),
               ("what's {ref} and what's its favorite activity", ["ans", "likes"]),
               ("what is {ref} and what does it like to do", ["ans", "likes"]),
               ("what do {pl} eat and where do they live", ["eat", "live"]),
               ("where do {pl} live and what do they eat", ["live", "eat"]),
               ("what do {pl} eat and what do they like to do", ["eat", "likes"]),
               ("where do {pl} live and what do they like to do", ["live", "likes"]),
               ("what is {ref}, and what does it eat", ["ans", "eat"]),
               ("what is {ref} and also where does it live", ["ans", "live"]),
               ("explain {ref} and what it eats", ["ans", "eat"]),
               ("describe {ref} and tell me where it lives", ["ans", "live"]),
               ("what is {ref} plus what does it like to do", ["ans", "likes"]),
               ("i want to know what {ref} is and what it eats", ["ans", "eat"]),
               ("what is {ref}? what does it eat?", ["ans", "eat"]),
               ("what is {ref}? where does it live?", ["ans", "live"]),
               ("what's {ref}? and what does it do for fun?", ["ans", "likes"]),
               ("what do {pl} eat, and where do they live", ["eat", "live"]),
               ("what does {ref} eat and what is its favorite activity", ["eat", "likes"])],
    "object": [("what is {ref} and what is it used for", ["ans", "used"]),
               ("what's {ref} and what do people use it for", ["ans", "used"]),
               ("what are {pl} and what are they used for", ["ans", "used"])],
}
COMP_2 = ["what is {r1} and what is {r2}", "what's {r1} and what's {r2}", "tell me about {r1} and {r2}",
          "what are {p1} and {p2}", "explain {r1} and {r2}", "what is {r1}, and what is {r2}",
          "describe {r1} and {r2}", "i want to know about {r1} and {r2}", "what is {r1}? what is {r2}?",
          "tell me about {r1} as well as {r2}", "what is {r1} as well as {r2}", "define {r1} and {r2}",
          "do you know what {r1} and {r2} are", "explain both {r1} and {r2}", "first {r1}, then {r2}"]
CAUSE_YOU = ["what happens when you {p}", "what happens if you {p}", "what could happen if you {p}",
             "what happens if i {pi}", "what happens when i {pi}", "what will happen if i {pi}", "what if i {pi}"]
CAUSE_DANGER = [("is it safe to {pv}", "No. "), ("is it ok to {pv}", "No. "), ("is it bad to {pv}", "Yes. "),
                ("why shouldn't you {pv}", ""), ("why is it bad to {pv}", ""), ("should i {pvi}", "No. ")]


def pl_of(e):
    return e.plural or e.name


def part(e, k):
    return e.answer if k == "ans" else (e.used if k == "used" else e.attrs[k])


def subj_of(e):
    return e.answer.split(" is ")[0].split(" are ")[0]


def t_attr(state, rng):
    if rng.random() < 0.75:
        e = rng.choice(ANIMALS); k = rng.choice(["eat", "live", "likes"])
    else:
        e = rng.choice(OBJECTS); k = "used"
    state["last"] = ("kb", e, 0); state["attr"] = k
    q = rng.choice(ATTR_Q[k]).format(ref=e.ref(), pl=pl_of(e), name=e.name)
    return style_user(q, rng), part(e, k)


def t_pronoun(state, rng):
    e = state["last"][1]
    if e.attrs:
        k = rng.choice(["eat", "live", "likes"])
    elif e.used and rng.random() < 0.85:
        k = "used"
    elif not e.used:
        return t_more(state, rng)
    else:
        state["attr"] = None
        q = style_user(rng.choice(PRON_Q["eat"]), rng, typo=False)
        return q, f"{subj_of(e)} doesn't eat anything, because it isn't alive."
    state["attr"] = k
    return style_user(rng.choice(PRON_Q[k]), rng, typo=False), part(e, k)


def t_compound(state, rng):
    r = rng.random()
    if r < 0.5:
        e = rng.choice(ANIMALS); tpl, parts = rng.choice(COMP_1["animal"])
    elif r < 0.7:
        e = rng.choice(OBJECTS); tpl, parts = rng.choice(COMP_1["object"])
    else:
        e1, e2 = rng.sample(ENTRIES, 2)
        tpl = rng.choice(COMP_2)
        if "{p1}" in tpl and not (e1.plural and e2.plural):
            tpl = COMP_2[0]
        q = tpl.format(r1=e1.ref(), r2=e2.ref(), p1=pl_of(e1), p2=pl_of(e2))
        state["last"] = ("kb", e2, 0); state["attr"] = None
        return style_user(q, rng), e1.answer + " " + e2.answer
    state["last"] = ("kb", e, 0); state["attr"] = parts[-1] if parts[-1] != "ans" else None
    q = tpl.format(ref=e.ref(), pl=pl_of(e))
    return style_user(q, rng), " ".join(part(e, k) for k in parts)


def cause_forms(ph):
    pi = ph.replace("your ", "my ")
    pv = ph.replace("don't ", "not ", 1) if ph.startswith("don't ") else ph
    pv = ("be " + pv[4:]) if pv.startswith("are ") else pv
    pvi = pv.replace("your ", "my ")
    return pi, pv, pvi


def t_cause(state, rng):
    state["last"] = ("other",); state["attr"] = None
    phs, ans, danger = rng.choice(CAUSES)
    ph = rng.choice(phs)
    pi, pv, pvi = cause_forms(ph)
    if danger and rng.random() < 0.3:
        tpl, pre = rng.choice(CAUSE_DANGER)
        return style_user(tpl.format(pv=pv, pvi=pvi), rng), pre + ans
    return style_user(rng.choice(CAUSE_YOU).format(p=ph, pi=pi), rng), ans


def t_old_name(state, rng):
    state["last"] = ("other",)
    q = style_user(rng.choice(["who is amrio", "who's amrio", "what is amrio", "tell me about amrio",
                               "do you know amrio", "did amrio make you"]), rng, typo=False)
    return q, f"I don't know who {as_typed(q, 'Amrio')} is. I only know a few people, like Elias, who made me."


GENERIC = [
    (t_kb, 20), (t_attr, 14), (t_compound, 9), (t_cause, 10), (t_math, 12), (t_repeat, 3), (t_count, 1), (t_calendar, 5), (t_color, 2), (t_sound, 2),
    (t_capital, 3), (t_opposite, 2), (t_unknown, 15), (t_joke, 3), (t_story, 1.5), (t_fact, 2),
    (t_like, 3), (t_cant, 2), (t_statement, 1.5), (t_fav, 1.5), (t_ai, 4),
    (simple(ID_Q, ID_A), 3), (simple(MAKER_Q, MAKER_A), 1.5), (simple(AMRIO_Q, AMRIO_A), 1.2), (t_old_name, 0.5),
    (simple(HOW_Q, HOW_A), 2), (t_feel, 2), (simple(THANKS_Q, THANKS_A), 1.5),
    (simple(NICE_Q, NICE_A), 1), (simple(MEAN_Q, MEAN_A), 1), (simple(YESNO_Q, YESNO_A), 1),
    (t_ask_name, 0.6), (t_more, 0.4),
]
G_FUNCS = [g for g, _ in GENERIC]
G_W = [w for _, w in GENERIC]


def conversation(rng):
    state = {}
    turns = []
    n = rng.choices([1, 2, 3, 4, 5, 6, 8], weights=[18, 20, 18, 14, 12, 10, 8])[0]
    name_at = rng.randrange(n) if (n >= 2 and rng.random() < 0.4) else -1
    for i in range(n):
        if i == 0 and rng.random() < 0.3:
            f = simple(GREET_Q, GREET_A)
        elif i == name_at:
            f = t_set_name
        elif state.get("name") and rng.random() < 0.35:
            f = t_ask_name
        elif state.get("last") and state["last"][0] == "kb" and rng.random() < 0.55:
            f = rng.choices([t_more, t_what_about, t_react, t_pronoun], weights=[5, 3, 1, 5])[0]
        elif state.get("last") and state["last"][0] in ("joke", "story") and rng.random() < 0.3:
            f = t_more
        elif i == n - 1 and n > 1 and rng.random() < 0.15:
            f = simple(BYE_Q, BYE_A)
        else:
            f = rng.choices(G_FUNCS, weights=G_W)[0]
        turns.append(f(state, rng))
    return turns


def coverage_conversations(rng):
    out = []
    for e in ANIMALS:
        for k in ("eat", "live", "likes"):
            out.append([(style_user(rng.choice(ATTR_Q[k]).format(ref=e.ref(), pl=pl_of(e), name=e.name), rng), e.attrs[k])])
    for e in OBJECTS:
        out.append([(style_user(rng.choice(ATTR_Q["used"]).format(ref=e.ref(), pl=pl_of(e), name=e.name), rng), e.used)])
    for phs, ans, d in CAUSES:
        for ph in phs:
            out.append([(style_user(rng.choice(CAUSE_YOU).format(p=ph, pi=cause_forms(ph)[0]), rng), ans)])
    for e in ENTRIES:
        st = {"last": ("kb", e, 0)}
        out.append([(style_user(kb_question(e, rng), rng), e.answer), t_more(st, rng)])
    return out


def init(params_str, vocab_str):
    global PARAMS_STR, VOCAB_STR, ENTRIES, BY_NAME
    PARAMS_STR, VOCAB_STR = params_str, vocab_str
    for k in AI_Q:
        qs, a = AI_Q[k]
        AI_Q[k] = (qs, a.replace("0.9 million", params_str))
    global KNOWN_WORDS
    ENTRIES = load_entries()
    BY_NAME = {e.name: e for e in ENTRIES}
    KNOWN_WORDS = {e.name for e in ENTRIES} | {e.plural for e in ENTRIES if e.plural}
    global ANIMALS, OBJECTS, CAUSES
    import kb2
    at, us = kb2.parse_attrs(), kb2.parse_used()
    assert set(at) <= set(BY_NAME) and set(us) <= set(BY_NAME), (set(at) - set(BY_NAME), set(us) - set(BY_NAME))
    for e in ENTRIES:
        e.attrs = at.get(e.name)
        e.used = us.get(e.name)
    ANIMALS = [e for e in ENTRIES if e.attrs]
    OBJECTS = [e for e in ENTRIES if e.used]
    CAUSES = kb2.parse_cause()
    names = {e.name for e in ENTRIES} | {e.plural for e in ENTRIES if e.plural}
    bad = [w for w in UNKNOWN_NOUNS if w in names]
    assert not bad, bad


def generate(n, seed, params_str="0.9 million", vocab_str="1024"):
    init(params_str, vocab_str)
    rng = random.Random(seed)
    convs = []
    for k in range(max(1, n // 40000)):
        convs += coverage_conversations(rng)
    while len(convs) < n:
        convs.append(conversation(rng))
    rng.shuffle(convs)
    return convs


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    for c in generate(n, 1):
        for u, b in c:
            print("U:", u)
            print("B:", b)
        print("---")
