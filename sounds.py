from enum import Enum

consonants = {
    "nasal": {
        "bilabial": ["m̥", "m"],
        "labio-dental": ["ɱ"],
        "linguo-labial": ["n̼"],
        "alveolar": ["n̥", "n"],
        "retro-flex": ["ɳ̊", "ɳ"],
        "palatal": ["ɲ̊", "ɲ"],
        "velar": ["ŋ̊", "ŋ"],
        "uvular": ["ɴ"],
    },
    "stop": {
        "bilabial": ["p", "b"],
        "labiodental": ["p̪", "b̪"],
        "linguo-labial": ["t̼", "d̼"],
        "alveolar": ["t", "d"],
        "palatal": ["c", "ɟ"],
        "velar": ["k", "g"],
        "uvular": ["q", "ɢ"],
        "glottal": ["ʔ"]
    },
    "sibilant fricative": {
        "alveolar": ["s", "z"],
        "post-alveolar": ["ʃ", "ʒ"],
        "palatal": ["ɕ", "ʑ"],
    },
    "non-sibilant fricative": {
        "bilabial": ["ɸ", "β"],
        "labio-dental": ["f", "v"],
        "linguo-labial": ["θ̼", "ð̼"],
        "dental": ["θ", "ð"],
        "velar": ["x", "ɣ"],
        "uvular": ["χ", "ʁ"],
        "pharyngeal": ["ħ", "ʕ"],
        "glottal": ["h", "ɦ"]
    },
    # "approximant": { },
    # "tap/flap": { },
    # "trill": { },
}

vowels = {
    "close": {
        "front": ["i", "y"],
        "central": ["ɨ", "ʉ"],
        "back": ["ɯ", "u"],
    },
    "near-close": {
        "front": ["ɪ", "ʏ"],
        "central": ["ɨ̞", "ʉ̞"],
        "back": ["ɯ̞", "ʊ"]
    },
    "close-mid": {
        "front": ["e", "ø"],
        "central": ["ɘ", "ɵ"],
        "back": ["ɤ", "o"]
    },
    "mid": {
        "front": ["e̞", "ø̞"],
        "central": ["ə"],
        "back": ["ɤ̞", "o̞"]
    },
    "open-mid": {
        "front": ["ɛ", "œ"],
        "central": ["ɜ", "ɞ"],
        "back": ["ʌ", "ɔ"]
    },
    "near-open": {
        "front": ["æ"],
        "central": ["ɐ"],
        # "back": []
    },
    "open": {
        "front": ["a", "ɶ"],
        "central": ["ä", "ɒ̈"],
        "back": ["ɑ", "ɒ"]
    }

}

VOWEL = "0"
CONS = "1"
NASAL = "2"
STOP = "3"
SIBIL = "4"
NONSIBIL = "5"
APPROX = "6"
TAP = "7"
TRILL = "8"



def flatten(d: dict):
    fin = []
    for k, v in d.items():
        if isinstance(v, dict):
            fin.extend(flatten(v))
        if isinstance(v, (list, tuple)):
            fin.extend(v)
    return "".join(fin)

flatvowels = flatten(vowels)
flatcons = flatten(consonants)
flatnasals = flatten(consonants["nasal"])
flatstops: str = flatten(consonants["stop"])
flatsibil: str = flatten(consonants["sibilant fricative"])
flatnonsibil: str = flatten(consonants["non-sibilant fricative"])


ctypes = list(consonants.keys())
ptypes = list(consonants[ctypes[0]].keys())
vtypes = list(vowels.keys())


class CTypes:
    nasal = ctypes[0]
    stop = ctypes[1]
    sfric = ctypes[2]
    nsfric = ctypes[3]
    # approx = ctypes[4]
    # tap = ctypes[5]
    # trill = ctypes[6]


class VTypes:
    close = vtypes[0]
    nclose = vtypes[1]
    cmid = vtypes[2]
    mid = vtypes[3]
    omid = vtypes[4]
    nopen = vtypes[5]
    open = vtypes[6]


c_changes = [
    ["b", "p", "ɸ", "f"],
    ["d", "t", "θ"],
    ["g", "k", "x", "h", ""],
    ["g", "g", "g"],
    ["p", "f", "v"],
    ["t", "ð", "d"],
    ["ð", "θ"],
    ["θ", "f"],
    [rf"([{flatvowels}])n", r"\1\u0303n"],
    ["ka", "ʃa"],
    ["ke", "se"],
    ["ke", "tʃe"],
    ["ge", "ʒe"],
    ["je", "ʒe"],
    ["np", "mp"],
    ["ti", "tʃi"],
    ["ti", "ʃi"],
    ["ti", "ɕ"],
    ["ti", "tɕ"],
    ["di", "ʑi"],
    ["dr", "ʒr"],
    ["tr", "tʃ"],
    ["tu", "tʃu"],
    ["ox", "ax"],
    ["oħ", "aħ"],
    ["mθ", "mf"],
    [rf"[{flatnonsibil}]([{flatnonsibil}])", r"\1"],
    [rf"([{flatsibil}])[{flatnonsibil}]", r"\1"],
    [rf"(([{flatcons}])\1)", r"\1"],
    [r"s+is", r"ris"]
]

v_changes = {
    "unstressed": [
        [r"a", r"ə"],
        [r"i", r"ə"],
        [r"(a)(.*?[i])", r"e\2"],
        [r"(a)([^ɪ].*?[ɪ])", r"e\2"],
        [r"aʊ", r"o"],
        [r"au", r"o"],
        [r"ʊ", r"ɪʊ"],
        [r"ʌæ", r"ʌ"]
    ]
}

english_con = {'n': 7.11, 'r': 6.94, 't': 6.91, 's': 4.75, 'd': 4.21, 'l': 3.96,
               'k': 3.18, 'ð': 2.95, 'm': 2.76, 'z': 2.76, 'p': 2.15, 'v': 2.01, 'w': 1.95,
               'b': 1.8, 'ʌ': 1.74, 'f': 1.71, 'h': 1.4, 'ŋ': 0.99, 'ʃ': 0.97, 'j': 0.81,
               'g': 0.8, 'dʒ': 0.59, 'tʃ': 0.56, 'θ': 0.41, 'ʒ': 0.07}

english_vow = {'ə': 11.49, 'ɪ': 6.32, 'i': 3.61, 'ɛ': 2.86, 'æ': 2.1, 'u': 1.93, 'e': 1.79, 'aɪ': 1.5, 'ɑ': 1.45,
               'o': 1.25, 'ɒ': 1.18, 'aʊ': 0.5, 'ʊ': 0.43, 'ɔɪ': 0.1, }
