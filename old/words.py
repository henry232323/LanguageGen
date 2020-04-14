import enum
import random
import re

from old import sounds

with open("words.txt") as wf:
    TOPWORDS = wf.read().split("\n")
    random.shuffle(TOPWORDS)

COMMONCHART = {
    "OBJ": [
        "time",
        "person",
        "year",
        "way",
        "day",
        "thing",
        "man",
        "world",
        "life",
        "hand",
        "part",
        "child",
        "eye",
        "woman",
        "place",
        "work",
        "week",
        "case",
        "point",
        "group",
    ],
    "ACT": [
        "be",
        "have",
        "do",
        "say",
        # "get",
        "make",
        "go",
        "know",
        "take",
        "see",
        "come",
        "think",
        "look",
        "want",
        "give",
        "use",
        "find",
        "tell",
        "ask",
        "work",
        "seem",
        "feel",
        "try",
        "leave",
    ],
    "POS": [
        "of",
        "with",
        "at",
        "from",
        "into",
        "against",
        "among",
        "to",
        "in",
        "for",
        "on",
        "by",
        "about",
        "through",
        "over",
        "before",
        "between",
        "after",
        "without",
        "under",
        "within",
        "across",
        "behind",
        "beyond",
        "up",
        "out",
        "around",
        "down",
        "off",
        "above",
        "near"
    ],
    "DESC": [
        "not",
        "quick"
    ]

}
preps = {'of': 5220, 'with': 1062, 'at': 624, 'from': 622, 'into': 301, 'during': 103, 'including': 58, 'until': 54,
         'against': 46, 'among': 37, 'throughout': 27, 'despite': 17, 'towards': 16, 'upon': 15, 'concerning': 3,
         'to': 4951, 'in': 2822, 'for': 1752, 'on': 1087, 'by': 706, 'about': 451, 'like': 324, 'through': 235,
         'over': 170, 'before': 141, 'between': 137, 'after': 110, 'since': 107, 'without': 89, 'under': 70,
         'within': 46, 'along': 45, 'following': 39, 'across': 36, 'behind': 22, 'beyond': 20, 'plus': 14, 'except': 6,
         'but': 626, 'up': 296, 'out': 294, 'around': 101, 'down': 94, 'off': 74, 'above': 40, 'near': 13}


class Parts(enum.Enum):
    ACT = "ACT"
    OBJ = "OBJ"
    DESC = "DESC"
    CONJ = "CONJ"
    POS = "POS"
    PRO = "PRO"


class Word:
    def __init__(self, lang, defn, part, mutchance=1e-4, syllables=None, sindex=0):
        self.language = lang
        self.part = part
        self.mutchance = mutchance
        self.syllables = syllables or []
        self.stressindex = sindex
        self.meaning = defn
        self.whole = "".join(syllables)

    def __repr__(self):
        return f"Word({self.whole}, defn={self.meaning}, sindex={self.stressindex}, mutchance={self.mutchance})"

    def __str__(self):
        return self.whole

    def mutate(self):
        s = self.whole
        if random.random() < self.mutchance:
            c = False
            for item in random.sample(sounds.c_changes, len(sounds.c_changes)):
                for j in range(len(item) - 1):
                    if item[j] in s:
                        f = s
                        s = re.sub(item[j], item[j + 1], s)
                        self.language.mutations.append((f, s))
                        c = True
                        if random.random() < 0.5:
                            break
                    if c:
                        break
                if c:
                    break
            else:
                changes = "unstressed"  # if i == self.stressindex else "unstressed"
                for item in random.sample(sounds.v_changes[changes], len(sounds.v_changes[changes])):
                    if re.match(item[0], s):
                        f = s
                        s = re.sub(item[0], item[1], s)
                        self.language.mutations.append((f, s))

            self.whole = s


class Verb(Word):  # 0 obj = intransitive, 1 obj = transitive, 2 indirect object
    def __init__(self, *args, nobjects=0, **kwargs, ):
        super().__init__(*args, **kwargs)
        self.nobjects = nobjects

    def __repr__(self):
        return f"Verb({self.whole}, defn={self.meaning}, sindex={self.stressindex}, mutchance={self.mutchance}), nobjects={self.nobjects}"
