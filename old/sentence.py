class Sentence():
    def __init__(self, struct, bstruct, words):
        self.eng = " ".join(f"{n.meaning}.{t}.{b}" for t, b, n in zip(struct, bstruct, words))
        self.whole = " ".join(str(n) for n in words)
        
    def __str__(self):
        return self.whole

    def __repr__(self):
        return f"Sentence('{self.eng}')"
