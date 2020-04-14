import changes
import simulator

rules = []
changes.parse(rules, "t tʃ k kw → d dʒ ɡ gw / _{V,R}")
changes.parse(rules, "C[+voice] → C[-voice] / _{V,R}")
print(rules)

corpus = {"talaxak": ["t͡salaxak"]}

print(simulator.runchanges(corpus, debug=True, rules=rules))