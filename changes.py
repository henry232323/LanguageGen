import re

import ipapy
from ipapy.ipastring import IPAString

with open("index-diachronica.txt", 'r') as text:
    data = text.read()

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

rules = {}

optpat = re.compile(r"(\(.+?\))")
anypat = re.compile(r"({(.*?,)*?(.*?)})")

for line in data.split():
    try:
        if '→' not in line:
            continue
        l, r = line.split("→")
        r = re.sub("(.*?)/.*$", r"\1", r)
        for subl, subr in zip(l.split(), r.split()):
            subl = subl.strip()
            result = re.sub(",", "|", anypat.sub(r"(\2\3)", optpat.sub(r"\1?", subl)))
            subr = subr.strip()
            print(result)
            subr = [anypat.sub(r"\2\3", x) for x in anypat.findall(optpat.sub(r"\1?", subr))]


    except:
        continue





