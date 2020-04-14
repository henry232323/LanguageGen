from old import lang

consonants = {
    "nasal": {
        "bilabial": ["m"],
        "alveolar": ["n"],
    },
    "stop": {
        "bilabial": ["p", "b"],
        "alveolar": ["t", "d"],
        "velar": ["k", "g"],
    },
    "sibilant fricative": {
        "alveolar": ["s", "z"],
        "post-alveolar": ["ʃ", "ʒ"],
    },
    "non-sibilant fricative": {
        "labio-dental": ["f", "v"],
        "dental": ["θ", "ð"],
        "velar": ["x"],
        "uvular": ["ʁ"],
        "pharyngeal": ["ħ"],
    },
    # "approximant": { },
    # "tap/flap": { },
    # "trill": { },
}

vowels = {
    "close": {
        "front": ["i", "y"],
        "back": ["u"],
    },
    "near-close": {
        "front": ["ɪ"],
        "back": ["ʊ"]
    },
    # "close-mid": {
    # "front": ["e"],
    # "back": ["o"]
    # },
    "mid": {
        "central": ["ə"],
    },
    "open-mid": {
        "front": ["ɛ"],
        "central": ["ʌ"],
        "back": ["ɔ"]
    },
    "near-open": {
        "front": ["æ"],
    },
    "open": {
        "front": ["a"],
    }

}

patterns = {
    "consonants": [
        ("*",),
        ("stop", "sibilant fricative"),
        ("sibilant fricative", "stop"),
        ("nasal", "*"),
    ],
    "vowels": [
        ("*",), ("*",), ("*",), ("*",), ("*",),
        ("*",), ("*",), ("*",), ("*",), ("*",),
        ("eɪ",),
        ("oʊ",),
        ("aɪ",),
        ("aʊ",),
        ("oɪ",)
    ],
    "syllable": [
        ("cc", "vc"),
        ("cc", "vc"),
        ("cc", "vc"),
        ("cc", "vc"),
        #("cc", "vc", "cc"),
        #("vc", "cc"),
        ("vc",)
    ]
}

f = lang.Lang(patterns=patterns, inventory=(consonants, vowels))

f.create_random("me", "OBJ")
f.create_random("tree", "OBJ")
f.create_random("rock", "OBJ")
f.create_random("be", "ACT", nobj=0)
f.create_random("be", "ACT", nobj=1)
f.create_random("see", "ACT", nobj=1)
f.create_random("give", "ACT", nobj=2)
f.create_random("run", "ACT", nobj=0)
f.create_random("in", "POS")
f.create_random("of", "POS")
f.create_random("fast", "DESC")
f.create_random("not", "DESC")

print(f.corpus)
f.mutate(1000)
print(f.corpus)
for i in range(10):
    s = f.create_sentence()
    print(s)
    print(repr(s))

#import pickle
#pickle.dump(f, open("mylang", 'w'))
