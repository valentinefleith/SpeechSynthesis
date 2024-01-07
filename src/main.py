import parselmouth as pm
import textgrids
import sys

from synthese import get_extracts, synthetise
from prosody import modif_f0


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage : python3 synthese.py fichier_wav fichier_textgrid")
    sound = pm.Sound(sys.argv[1])
    segmentation = textgrids.TextGrid(sys.argv[2])
    phonemes = segmentation["diphones"]
    with open("aux/phrases.txt", "r") as phrases:
        phrases_ortho = phrases.readlines()
    sentence_nb = get_sentence_to_synthetise(phrases_ortho)
    extracts = get_extracts(phrases_ortho[sentence_nb].strip(), sound, phonemes)
    synthese = synthetise(sound, extracts)
    #text = parse_phrase(phrase_ortho[0], synthese)
    #synthese = modif_f0(synthese)
    synthese.save("wav-files/synthese.wav", "WAV")


def get_sentence_to_synthetise(phrases_ortho):
    print("Quelle phrase voulez-vous synthétiser ? Vous avez le choix entre les phrases suivantes :\n")
    for i, phrase in enumerate(phrases_ortho):
        print(f"{i}) {phrase.replace('tout', 'tous')}")
    for i in range(3):
        nb = input("Entrez le numéro correspondant à la phrase : ")
        if not nb.isdigit() or int(nb) < 0 or int(nb) > 7:
            continue
        return int(nb)
    print("Vous avez entré trois numéros incorrects à la suite.")
    print("Par défaut, nous prendrons la première phrase.")
    return 0
        

if __name__ == "__main__":
    main()
