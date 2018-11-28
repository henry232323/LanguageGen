import lang

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
        ("eɪ",),
        ("oʊ",),
        ("aɪ",),
        ("aʊ",),
        ("oɪ",)
    ],
    "syllable": [
        ("cc", "vc"),
        ("cc", "vc", "cc"),
        ("vc", "cc"),
        ("vc",)
    ]
}

f = lang.Lang(patterns=patterns, inventory=(consonants, vowels))
f.create_corpus(100)
#print(f.corpus)
f.mutate(1000)
#print(f.corpus)
