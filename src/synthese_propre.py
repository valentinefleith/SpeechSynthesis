import parselmouth as pm
import textgrids
import matplotlib.pyplot as plt
from parselmouth.praat import call
from sys import argv, exit


def main():
    if len(argv) != 3:
        exit("Usage : python3 synthese.py fichier_wav fichier_textgrid")
    sound = pm.Sound(argv[1])
    segmentation = textgrids.TextGrid(argv[2])
    phonemes = segmentation["diphones"]
    phrase_ortho = "la ligne de métro quatorze"
    synthese = synthetise(phrase_ortho, sound, phonemes)
    synthese.save('synthese.wav', "WAV")


def synthetise(phrase_ortho, sound, phonemes):
    phrase_phon = convert_sentence_SAMPA(phrase_ortho)
    print(phrase_phon)
    debut = sound.extract_part(0, 0.01, pm.WindowShape.RECTANGULAR, 1, False)
    for i in range(len(phrase_phon) - 1):
        extraction = extract_diphone(phrase_phon[i] + phrase_phon[i + 1], sound, phonemes)
        debut = debut.concatenate([debut, extraction])
    return debut


def extract_diphone(diphone, sound, phonemes):
    phoneme1 = diphone[0]
    phoneme2 = diphone[1]
    for p1_index in range(len(phonemes) - 1):  # on peut peut etre enlever le moins 1
        p2_index = p1_index + 1
        if phonemes[p1_index].text == phoneme1 and phonemes[p2_index].text == phoneme2:
            milieu_p1 = trouver_milieu_phoneme(sound, phonemes, p1_index)
            milieu_p2 = trouver_milieu_phoneme(sound, phonemes, p2_index)
            extract = sound.extract_part(milieu_p1, milieu_p2, pm.WindowShape.RECTANGULAR, 1, False,)
            extract = modif_duree(extract)
            return extract
    return "DIPHONE NOT FOUND"


def modif_duree(extraction):
    """
    Il faut que l'extrait ait une f0 donc verifier nb value > 0
    """
    allongement = 2
    modif = call(extraction, "To Manipulation", 0.01, 75, 600)
    duration_tier = call(modif, "Extract duration tier")
    call(duration_tier, "Remove points between", 0, extraction.duration)
    call(duration_tier, "Add point", extraction.duration / 2, allongement)
    call([modif, duration_tier], "Replace duration tier")
    return call(modif, "Get resynthesis (overlap-add)")


def trouver_milieu_phoneme(sound, phonemes, index):
    milieu = phonemes[index].xmin + (phonemes[index].xmax - phonemes[index].xmin) / 2
    milieu = sound.get_nearest_zero_crossing(milieu, 1)
    return milieu


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
    # phrase_finale += "_"
    return phrase_finale


def create_dictionary(path="dico_UTF8.txt"):
    dictionary = {}
    with open(path, "r") as dico:
        for ligne in dico:
            orth, sampa = ligne.strip().split("\t")
            dictionary[orth] = sampa
    return dictionary


if __name__ == "__main__":
    main()
