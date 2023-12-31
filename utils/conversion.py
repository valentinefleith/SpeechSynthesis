
def convert_sentence_SAMPA(phrase_ortho):
    dictionary = create_dictionary()
    converted = []
    for mot in phrase_ortho.split():
        converted.append(dictionary[mot])
    return add_shwa(converted, phrase_ortho.split())


def add_shwa(phrase_phonetique, phrase_ortho):
    consonnes = "ptkfsSbdgvzjlRnNmwHZ"
    phrase_finale = "_"
    for i, mot_phon in enumerate(phrase_phonetique):
        phrase_finale += phrase_phonetique[i]
        if (
            i < len(phrase_phonetique) - 1
            and (phrase_ortho[i][-1] == "e" or phrase_ortho[i][-3:] == "ent")
            and phrase_phonetique[i + 1][0] in consonnes
            and mot_phon[-1] not in "@e"
        ):
            phrase_finale += "@"
    phrase_finale += "_"
    return phrase_finale


def create_dictionary(path="aux/dico_UTF8.txt"):
    dictionary = {}
    with open(path, "r") as dico:
        for ligne in dico:
            orth, sampa = ligne.strip().split("\t")
            if "a~" in sampa:
                sampa = sampa.replace("a~", "A")
            if "e~" in sampa:
                sampa = sampa.replace("e~", "1")
            if "o~" in sampa:
                sampa = sampa.replace("o~", "C")
            dictionary[orth] = sampa
    return dictionary

