import parselmouth as pm
import textgrids
import sys

from synthese import get_extracts, synthetise
from prosody import modif_duree, modif_f0


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage : python3 synthese.py fichier_wav fichier_textgrid")
    sound = pm.Sound(sys.argv[1])
    segmentation = textgrids.TextGrid(sys.argv[2])
    phonemes = segmentation["diphones"]
    with open("aux/phrases.txt", "r") as phrases:
        phrases_ortho = phrases.readlines()
    extracts = get_extracts(phrases_ortho[0].strip(), sound, phonemes)
    synthese = synthetise(sound, extracts)
    synthese.save("wav-files/synthese.wav", "WAV")


if __name__ == "__main__":
    main()
