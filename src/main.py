import parselmouth as pm
import textgrids
import matplotlib.pyplot as plt
from parselmouth.praat import call
import sys

sys.path.insert(0, "utils")

from prosody import modif_duree, modif_f0
from conversion import convert_sentence_SAMPA


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage : python3 synthese.py fichier_wav fichier_textgrid")
    sound = pm.Sound(sys.argv[1])
    segmentation = textgrids.TextGrid(sys.argv[2])
    phonemes = segmentation["diphones"]
    with open("../aux/phrases.txt", "r") as phrases:
        phrases_ortho = phrases.readlines()
    # phrases_ortho = [
    #     "tout les travaux sur la ligne quatorze sont ratés",
    #     "j' ai raté le RER A tous les jours pendant quatorze semaines",
    #     "j' ai raté le RER A à cause des travaux sur la ligne quatorze du métro",
    #     "les travaux interrompent le trafic sur la ligne quatorze",
    #     "le trafic du RER A sera interrompu pendant deux semaines",
    #     "la ligne de métro quatorze sera fermée pour cause de travaux pendant deux semaines",
    # ]
    extracts = get_extracts(phrases_ortho[5], sound, phonemes)
    synthetise(sound, extracts)


def synthetise(sound, extracts):
    synthese = sound.extract_part(0, 0.01, pm.WindowShape.RECTANGULAR, 1, False)
    synthese = synthese.concatenate(extracts, overlap=0.03)
    #synthese = modif_f0(synthese)
    synthese.save("wav-files/synthese.wav", "WAV")


def get_extracts(phrase_ortho, sound, phonemes):
    extracts = []
    phrase_phon = convert_sentence_SAMPA(phrase_ortho)
    print(phrase_phon)
    for i in range(len(phrase_phon) - 1):
        extraction = extract_diphone(
            phrase_phon[i] + phrase_phon[i + 1], sound, phonemes
        )
        if extraction:
            extracts.append(extraction)
    return extracts


def extract_diphone(diphone, sound, phonemes):
    phoneme1 = diphone[0]
    phoneme2 = diphone[1]
    for p1_index in range(len(phonemes) - 1):
        p2_index = p1_index + 1
        if (
            phonemes[p1_index].text.strip() == phoneme1
            and phonemes[p2_index].text.strip() == phoneme2
        ):
            milieu_p1 = find_middle_phoneme(sound, phonemes, p1_index)
            milieu_p2 = find_middle_phoneme(sound, phonemes, p2_index)
            extract = sound.extract_part(
                milieu_p1,
                milieu_p2,
                pm.WindowShape.RECTANGULAR,
                1,
                False,
            )
            extract = modif_duree(extract)
            return extract
    return f"DIPHONE NOT FOUND : {diphone}"


def find_middle_phoneme(sound, phonemes, index):
    milieu = (phonemes[index].xmax + phonemes[index].xmin) / 2
    milieu = sound.get_nearest_zero_crossing(milieu, 1)
    return milieu


if __name__ == "__main__":
    main()
