import random
import enum
import words, sounds

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

    def create_random(self, defn=None, part=None):
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
