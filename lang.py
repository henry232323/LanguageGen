import random
import enum
import words, sounds, sentence

choice = random.choice


def dchoice(d):
    return d[random.choice(list(d.keys()))]


SOV = 0
SVO = 1


class Lang:
    def __init__(self, order=None,
                 inventory=(sounds.consonants, sounds.vowels),
                 patterns=None
                 ):
        self.corpus = {}
        self.order = order if order else choice([SOV, SVO])
        self.patterns = patterns or {}
        self.consonants = inventory[0]
        self.vowels = inventory[1]
        self.mutations = []
        self.wordpattern = {
            1: {
                "W":[["S", "V"]],
                "S":[[0, 3, 1, 1.5],["N"],["O"], ["N", "D"]],
                "O":[[0, 3, 1, 1.2],["N"],["N", "P", "O"], ["D", "N"]],
                "IO":[[0, 1], ["P", "O"]],
                "V":[[0,1,1,1,1], ["V0"],["V0", "IO"],["V1", "O"],["V2", "O", "IO"]]
            },
            0: {
                "W":[["S", "V"]],
                "S":[[0, .75, .25, .325],["N"],["O"], ["N", "D"]],
                "O":[[0, .75, .25, 0.325],["N"],["O", "P", "N"], ["N", "D"]],
                "IO":[[0, 1],["O", "P"]],
                "V":[[0,.75,.25,1,1],["V0"],["IO", "V0"],["O", "V1"],["O", "IO", "V2"]]
            },
            "V0": lambda: self.get_type("ACT", lambda x: x.nobjects == 0),
            "V1": lambda: self.get_type("ACT", lambda x: x.nobjects == 1),
            "V2": lambda: self.get_type("ACT", lambda x: x.nobjects == 2),
            "N": lambda: self.get_type("OBJ"),
            "P": lambda: self.get_type("POS"),
            "D": lambda: self.get_type("DESC"),
        }

    def create_random(self, defn=None, part=None, nobj=None):
        nsylla = random.choice([1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3])
        syllables = []
        part = part or random.choice(list(words.COMMONCHART.keys()))
        defn = defn or random.choice(words.COMMONCHART[part])
        sindex = 0#random.randint(0, nsylla - 1)
        for i in range(nsylla):
            syllables.append(self.rand_sylla())
        if defn in words.TOPWORDS:
            mutchance = 100 / (words.TOPWORDS.index(defn) + 1)
        else:
            mutchance = 1e-4
        if part == "ACT":
            nobj = nobj if nobj is not None else random.randint(0, 2)
            self.corpus[defn] = word = words.Verb(self, defn, part, mutchance, syllables, sindex, nobjects=nobj)
        else:
            self.corpus[defn] = word = words.Word(self, defn, part, mutchance, syllables, sindex)
        return word

    def rand_sylla(self):
        template = choice(self.patterns["syllable"])
        #print(template)
        fin = ""
        for item in template:
            #print(fin, 1)
            if item == "c":
                fin += choice(dchoice(dchoice(self.consonants)))
            elif item == "cc":
                ctemp = choice(self.patterns["consonants"])
                for citem in ctemp:
                    if citem == "*":
                        fin += choice(dchoice(dchoice(self.consonants)))
                    elif citem in self.consonants:
                        fin += choice(dchoice(self.consonants[citem]))
                    else:
                        fin += citem
            elif item == "v":
                fin += choice(dchoice(dchoice(self.vowels)))
            elif item == "vc":
                vtemp = choice(self.patterns["vowels"])
                for vitem in vtemp:
                    if vitem == "*":
                        fin += choice(dchoice(dchoice(self.vowels)))
                    elif vitem in self.vowels:
                        fin += choice(dchoice(self.vowels[vitem]))
                    else:
                        fin += vitem
            else:
                fin += item
        return fin

    def create_corpus(self, n):
        for x in range(n):
            self.create_random()

    def mutate(self, n=1):
        for i in range(n):
            for w in self.corpus.values():
                w.mutate()

    def __repr__(self):
        return f"Lang(corpus={len(self.corpus)} words)"

    def get_type(self, type, check=lambda x: True):
        return choice(list(filter(lambda x: x.part == type and check(x), self.corpus.values())))

    def create_sentence(self):
        final = []
        pattern = self.wordpattern[self.order]
        stype = choice(pattern["W"])
        final.extend(self.create_part(stype, "W", pattern))
        return sentence.Sentence(*zip(*final))

    def create_part(self, chunk, nitem, pattern):
        for item in chunk:
            if item in pattern:
                yield from self.create_part(random.choices(pattern[item], weights=pattern[item][0])[0], item, pattern)
            else:
                yield (item, nitem, self.wordpattern[item]())
                

    """
    def rand_sylla(self):
        start = ""
        if random.randint(0, 1):
            start = self.rand_chunk()

        vowel = choice(dchoice(dchoice(self.vowels)))
        end = ""
        if random.randint(0, 1):
            end = self.rand_chunk()
        #print(start, vowel, end)
        return start + vowel + end

    """
