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
    phrase_ortho = "tout les travaux sur la ligne quatorze sont ratés"
    #phrase_ortho = "j' ai raté le RER A tous les jours pendant quatorze semaines"
    #phrase_ortho = "j' ai raté le RER A à cause des travaux sur la ligne quatorze du métro"
    #phrase_ortho = "les travaux interrompent le trafic sur la ligne quatorze"
    #phrase_ortho = "le trafic du RER A sera interrompu pendant deux semaines"
    #phrase_ortho = "la ligne de métro quatorze sera fermée pour cause de travaux pendant deux semaines"
    extracts = get_extracts(phrase_ortho, sound, phonemes)
    synthetise(sound, extracts)


def synthetise(sound, extracts):
    synthese = sound.extract_part(0, 0.01, pm.WindowShape.RECTANGULAR, 1, False)
    synthese = synthese.concatenate(extracts, overlap=0.03)
    synthese.save('wav-files/synthese.wav', "WAV")


def get_extracts(phrase_ortho, sound, phonemes):
    extracts = []
    phrase_phon = convert_sentence_SAMPA(phrase_ortho)
    print(phrase_phon)
    for i in range(len(phrase_phon) - 1):
        extraction = extract_diphone(phrase_phon[i] + phrase_phon[i + 1], sound, phonemes)
        if extraction:
            extracts.append(extraction)
    return extracts


def extract_diphone(diphone, sound, phonemes):
    phoneme1 = diphone[0]
    phoneme2 = diphone[1]
    for p1_index in range(len(phonemes) - 1):
        p2_index = p1_index + 1
        if phonemes[p1_index].text.strip() == phoneme1 and phonemes[p2_index].text.strip() == phoneme2:
            milieu_p1 = find_middle_phoneme(sound, phonemes, p1_index)
            milieu_p2 = find_middle_phoneme(sound, phonemes, p2_index)
            extract = sound.extract_part(milieu_p1, milieu_p2, pm.WindowShape.RECTANGULAR, 1, False,)
            extract = modif_duree(extract)
            return extract
    #return f"DIPHONE NOT FOUND : {diphone}"


def modif_duree(extraction):
    """
    Il faut que l'extrait ait une f0 donc verifier nb value > 0
    """
    allongement = 0.85
    modif = call(extraction, "To Manipulation", 0.01, 75, 600)
    duration_tier = call(modif, "Extract duration tier")
    call(duration_tier, "Remove points between", 0, extraction.duration)
    call(duration_tier, "Add point", extraction.duration / 2, allongement)
    call([modif, duration_tier], "Replace duration tier")
    return call(modif, "Get resynthesis (overlap-add)")


def find_middle_phoneme(sound, phonemes, index):
    milieu = (phonemes[index].xmax + phonemes[index].xmin) / 2
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


if __name__ == "__main__":
    main()
