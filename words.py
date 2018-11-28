import enum, random
import sounds
import re

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
    ]
}


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
        self.mutchance = mutchance
        self.syllables = syllables or []
        self.stressindex = sindex
        self.meaning = defn
        self.whole = "".join(syllables)

    def __repr__(self):
        return f"Word({self.whole}, defn={self.meaning}, sindex={self.stressindex}, mutchance={self.mutchance})"

    def mutate(self):
        s = self.whole
        if random.random() < self.mutchance:
            c = False
            for item in random.sample(sounds.c_changes, len(sounds.c_changes)):
                for j in range(len(item) - 1):
                    if item[j] in s:
                        f = s
                        s = s.replace(item[j], item[j + 1])
                        self.language.mutations.append((f, s))
                        c = True
                        if random.random() < 0.5:
                            break
                    if c:
                        break
                if c:
                    break
            else:
                changes = "unstressed"# if i == self.stressindex else "unstressed"
                for item in random.sample(sounds.v_changes[changes], len(sounds.v_changes[changes])):
                    if re.match(item[0], s):
                        f = s
                        s = re.sub(item[0], s, item[1])
                        self.language.mutations.append((f, s))

            self.whole = s

