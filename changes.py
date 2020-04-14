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

import dill as dill
import ipapy

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
    R={x for x in ipapy.IPA_CHARS if x.is_consonant and x.manner in ("approximant", "nasal", "flap", "tap", "trill")},
    S={x for x in ipapy.IPA_CHARS if x.is_consonant and x.manner == "plosive"},
    T={x for x in ipapy.IPA_CHARS if x.is_consonant and x.manner == "plosive" and x.voicing == "voiceless"},
    V={x for x in ipapy.IPA_CHARS if x.is_vowel},
    W={x for x in ipapy.IPA_CHARS if x.is_consonant and x.manner == "glide"},
)

optpat = re.compile(r"(\(.+?\))")
anypat = re.compile(r"({(.*?,)*?(.*?)})")


def format_group(letter):
    group = codes[letter]
    return "({})".format("|".join(str(x) for x in group))


def getvoiced(x):
    try:
        ochar = ipapy.UNICODE_TO_IPA[x]
    except:
        return x

    for char in ipapy.IPA_CHARS:
        if not char.is_consonant:
            continue
        if (char.voicing != ochar.voicing and
                char.manner == ochar.manner and
                char.place == ochar.place and
                char.modifiers == ochar.modifiers
        ):
            return str(char)


def finalize(subl, subr):
    i = 0
    subr = subr.replace("Ø", "")
    while i < len(subl):
        code = subl[i]
        if code in codes:
            ncode = rf"{code}\[.*?\]"
            fg = format_group(code)
            subl = re.sub(ncode, fg, subl, 1)
            tc = subl[:i].count('(')
            subr = subr.replace(code, rf"\{tc + 1}", 1)
            i += len(fg)
        else:
            i += 1

    print(subl, subr)

    def nsubr(outer):
        def subannotation(inner):
            g1 = inner.group(1)
            g2 = inner.group(2)

            if g2.endswith("voice"):
                return getvoiced(outer.group(int(g1.strip("\\"))))
            else:
                return inner.group(0)


        nsub = re.sub(r"(\\\d)\[(.*?)\]", subannotation, subr)
        return re.sub(subl, nsub, outer.string)

    return subl, nsubr


# TODO: Manage voice -> unvoice etc
# TODO: Manage matching for things like _# and #_, so no more weird disappearing vowels

def parse(RULES, line):
    line = line.replace("*", "").replace("!", "")
    if '→' not in line:
        return
    l, r = line.split("→")
    r = re.sub("(.*?)/.*$", r"\1", r)
    for subl, subr in zip(l.split(), r.split()):
        subl = subl.strip()
        subl = re.sub(",", "|", anypat.sub(r"(\2\3)", optpat.sub(r"\1?", subl)))
        if subl.startswith("-"):
            subl = subl.strip("-")
            subl += "$"
            subr = subr.strip("-")

        # for code in codes:
        #     if code in subr and code not in subl:
        #         continue

        subr = subr.strip()
        # print(optpat.findall(subr))

        allsubs = [
                      [(x[0], y) for y in x[0].strip("{").strip("}").split(",")]
                      for x in anypat.findall(subr)
                  ] + [[(x, ""), (x, x.strip("(").strip(")"))] for x in optpat.findall(subr)]
        # print(allsubs)
        try:
            re.compile(subl)
        except:
            continue

        if not allsubs:
            RULES.append(finalize(subl, subr))
        else:
            for prod in itertools.product(*allsubs):
                psubr = subr
                # print(list(prod))
                for full, choice in prod:
                    psubr = psubr.replace(full, choice)

                RULES.append(finalize(subl, subr))

    return RULES


def get_defaults():
    with open("index-fixed.txt", 'r', encoding="UTF-8") as text:
        data = text.read()

    rules = []
    for i, line in enumerate(data.split("\n")):
        try:
            parse(rules, line)
        except Exception as e:
            pass
            # print(e)

    with open("rules.dat", "wb") as rfile:
        print(rules[:30])
        dill.dump(rules, rfile)

    return rules


if __name__ == "__main__":
    default_rules = get_defaults()

else:
    with open("rules.dat", "rb") as rfile:
        default_rules = dill.load(rfile)
