import json
import re
from random import sample, shuffle

import eng_to_ipa as ipa

from changes import default_rules


def runchanges(corpus, nchanges=25, debug=False, rules=default_rules):
    frules = []
    for rule in rules:
        try:
            if any(re.findall(rule[0], word[0]) for word in corpus.values()):
                frules.append(rule)
        except:
            print(rule[0])

    if debug:
        print(f"{len(frules)} rules available for corpus")
    apply = sample(list(set(frules)), min(nchanges, len(frules)))
    if debug:
        print("Rules:", apply)
    for rule in apply:
        for word in corpus:
            lword = corpus[word][-1]
            nword = re.sub(rule[0], rule[1], lword)
            if nword != lword:
                if len(nword) >= 2 * (len(lword) - 1) and len(lword) > 4:
                    raise Exception(
                        "\nNew Word: {0}\nOld Word: {1}\nRule Match: {2}\nRule Sub: {3}".format(nword, lword, rule[0],
                                                                                                rule[1]))
                corpus[word].append(nword)
                # print(nword)

    return corpus


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def convert(text):
    vals = ""
    for chunk in chunks(text.split(), 499):
        vals += " " + ipa.convert(" ".join(chunk))

    return vals


if __name__ == "__main__":
    with open("old\\words.txt", 'r') as wf:
        text = wf.read()
        lwords = text.split('\n')
        shuffle(lwords)
        words = {x: [y] for x, y in zip(lwords, convert(" ".join(lwords)).split())}

    nwords = runchanges(words)
    print(json.dumps(list(nwords.items())[:15], indent=4, ensure_ascii=False))
