import lang

consonants = {
    "nasal": {
        "bilabial": ["m"],
        "alveolar": ["n̥","n"],
        "velar": ["ŋ"],
    },
    "stop": {
        "bilabial": ["p", "b"],
        "alveolar": ["t", "d"],
        "velar": ["k", "g"],
    },
    "sibilant fricative": {
        "alveolar": ["s", "z"],
        "post-alveolar": ["ʃ","tʃ", "dʒ"],
    },
    "non-sibilant fricative": {
        "labio-dental": ["f", "v"],
        "dental": ["θ", "ð"],
        "palatal":["ç"],
        "velar": ["x", "ɣ"],
        "glottal": ["h"]
    },
    "approximant": {
        "alveolar": ["l̥","l"],
        "palatal": ["j"],
        "velar": ["ʍ", "w"]
    },
    # "tap/flap": { },
     "trill": {
        "alveolar": ["r̥", "r"]
    },
}

vowels = {
    "close": {
        "front": ["i", "y", "iː", "yː"],
        "back": ["u", "uː"],
    },
    "mid": {
        "front": ["e", "eː", "ø", "øː"],
        "back": ["o", "oː"]
    },
    "open": {
        "front": ["a", "aː", "æ", "æː"],
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
        ("iu̯",),
        ("iːu̯",),
        ("eo̯",),
        ("eːo̯",),
        ("æɑ̯",),
        ("æːɑ̯̯",)
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
