import parselmouth as pm
import textgrids
import sys
import subprocess

from synthese import get_extracts, synthetise
from prosody import modif_prosody


def main():
    if len(sys.argv) != 3:
        sound = pm.Sound("wav-files/Logatomes.wav")
        segmentation = textgrids.TextGrid("wav-files/Logatomes.TextGrid")
    else:
        sound = pm.Sound(sys.argv[1])
        segmentation = textgrids.TextGrid(sys.argv[2])
    phonemes = segmentation["diphones"]
    with open("aux/phrases.txt", "r") as phrases:
        phrases_ortho = phrases.readlines()
    sentence_nb = get_sentence_to_synthetise(phrases_ortho)
    extracts = get_extracts(phrases_ortho[sentence_nb].strip(), sound, phonemes)
    synthese = synthetise(sound, extracts)
    synthese_modifiee = modif_prosody(synthese, sentence_nb, get_modalite())
    synthese_modifiee.save(f"wav-files/synthese_phrase{sentence_nb}.wav", "WAV")
    subprocess.run(["open", f"wav-files/synthese_phrase{sentence_nb}.wav"])


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


def get_modalite():
    modalites = ["Assertive", "Interrogative", "Exclamative"]
    print("\nQuelle modalité voulez-vous pour la phrase ?")
    for i, modalite in enumerate(modalites):
        print(f"{i} : {modalite}\n")
    nb = input("Entrez le numéro correspondant :")
    if not nb.isdigit() or int(nb) < 0 or int(nb) > 2:
        print("Vous avez entré un mauvais chiffre. Par défaut, nous prendrons la modalité assertive.")
        return 0
    return int(nb)


if __name__ == "__main__":
    main()
