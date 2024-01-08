VERBS = ["sera", "interrompent", "ai", "sont"]


class Sentence:
    def __init__(self, nb, mots, phonemes, modalite):
        self.nb = nb
        self.mots = mots
        self.phonemes = phonemes
        self.modalite = modalite

    def get_verb_index(self):
        for i, mot in enumerate(self.mots):
            if mot.text in VERBS:
                return i
        return -1

    def get_stressed_phoneme_index(self, verb_index):
        mot_a_allonger = self.mots[verb_index - 1]
        for i, phoneme in enumerate(self.phonemes):
            if self.phonemes[i].xmin >= mot_a_allonger.xmin and self.phonemes[i].xmax <= mot_a_allonger.xmax:
                if self.is_stressed(self.phonemes[i].text):
                    return i
        return -1

    def is_stressed(self, phoneme):
        if self.nb == 0 or self.nb == 5:
            return phoneme == "O"
        if self.nb == 1 or self.nb == 4:
            return phoneme == "a"
        if self.nb == 2:
            return phoneme == "o"
        if self.nb == 3 or self.nb == 6 or self.nb == 7:
            return phoneme == "E"
        return False
