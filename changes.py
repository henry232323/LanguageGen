"""
    Ø = Nothing/Null/Zero
    A = Affricate
    B = Back vowel
    C = Consonant
    D = Voiced plosive
    E = Front vowel
    F = Fricative
    H = Laryngeal
    J = Approximant
    K = Velar
    Ḱ = Palatovelar
    L = Liquid
    M = Diphthong
    N = Nasal
    O = Obstruent
    P = Labial/Bilabial
    Q = Uvular consonant; click consonant (Khoisan)
    R = Resonant/Sonorant
    S = Plosive
    T = Voiceless plosive
    U = Syllable
    V = Vowel
    W = Semivowel
    Z = Continuant
    """

import itertools
import re

import ipapy
from ipapy.ipastring import IPAString

codes = dict(
    A={x for x in ipapy.IPA_CHARS if x.is_consonant and x.manner == "affricate"},
    C={x for x in ipapy.IPA_CHARS if x.is_consonant},
    B={x for x in ipapy.IPA_CHARS if x.is_vowel and x.backness == "back"},
    D={x for x in ipapy.IPA_CHARS if x.is_consonant and x.manner == "plosive" and x.voicing == "voiced"},
    E={x for x in ipapy.IPA_CHARS if x.is_vowel and x.backness == "front"},
    F={x for x in ipapy.IPA_CHARS if x.is_consonant and x.manner == "fricative"},
    H={x for x in ipapy.IPA_CHARS if x.is_consonant and x.place in ("pharyngeal", "glottal")},
    J={x for x in ipapy.IPA_CHARS if x.is_consonant and x.manner == "approximant"},
    K={x for x in ipapy.IPA_CHARS if x.is_consonant and x.place == "velar"},
    Ḱ={x for x in ipapy.IPA_CHARS if x.is_consonant and x.place == "palatovelar"},
    # liquids={x for x in ipapy.IPA_CHARS if x.manner == "liquid"},
    # diphthongs={x for x in ipapy.IPA_CHARS if x.is_vowel and x.is_dip}
    N={x for x in ipapy.IPA_CHARS if x.is_consonant and x.manner == "nasal"},
    # obstruent={x for x in ipapy.IPA_CHARS if x.is_consonant and x.manner == "nasal"},
    P={x for x in ipapy.IPA_CHARS if x.is_consonant and x.place == "bilabial"},
    Q={x for x in ipapy.IPA_CHARS if x.is_consonant and x.place == "uvular"},
    R={x for x in ipapy.IPA_CHARS if x.is_consonant and x.manner == ("approximant", "nasal", "flap", "tap", "trill")},
    S={x for x in ipapy.IPA_CHARS if x.is_consonant and x.manner == "plosive"},
    T={x for x in ipapy.IPA_CHARS if x.is_consonant and x.manner == "plosive" and x.voicing == "voiceless"},
    V={x for x in ipapy.IPA_CHARS if x.is_vowel},
    W={x for x in ipapy.IPA_CHARS if x.is_consonant and x.manner == "glide"},
)

rules = []

optpat = re.compile(r"(\(.+?\))")
anypat = re.compile(r"({(.*?,)*?(.*?)})")


def format_group(letter):
    group = codes[letter]
    return "({})".format("|".join(str(x) for x in group))


def parse(line):
    if '→' not in line:
        return
    l, r = line.split("→")
    r = re.sub("(.*?)/.*$", r"\1", r)
    for subl, subr in zip(l.split(), r.split()):
        subl = subl.strip()
        result = re.sub(",", "|", anypat.sub(r"(\2\3)", optpat.sub(r"\1?", subl)))

        codecount = 0
        for code in codes:
            while code in subl:
                subl = subl.replace(code, format_group(code), 1)
                subr = subr.replace(code, rf"\{codecount + 1}", 1)
                codecount += 1

        subr = subr.strip()
        # print(optpat.findall(subr))
        allsubs = [
                      [(x[0], y) for y in x[0].strip("{").strip("}").split(",")]
                      for x in anypat.findall(subr)
                  ] + [[(x, ""), (x, x.strip("(").strip(")"))] for x in optpat.findall(subr)]
        # print(allsubs)
        if not allsubs:
            rules.append((result, subr))
        else:
            for prod in itertools.product(*allsubs):
                psubr = subr
                # print(list(prod))
                for full, choice in prod:
                    psubr = psubr.replace(full, choice)

                rules.append((result, psubr))

    return rules


with open("index-diachronica.txt", 'r') as text:
    data = text.read()

for line in data.split():
    try:
        parse(line)
    except:
        continue

print(len(rules))
import json

with open("rules.json", "w") as rfile:
    rfile.write(json.dumps(rules, indent=4))
