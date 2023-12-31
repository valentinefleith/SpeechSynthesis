import sys
import csv
from typing import List, Dict


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage : python3 diphones.py phrases.txt dictionnaire.txt")
    phrases = load_sentences(sys.argv[1])
    dict_conversion = load_dict_SAMPA(sys.argv[2])
    logatomes = []
    for phrase in phrases:
        phrase_phonetique = convert_SAMPA(phrase.split(), dict_conversion)
        print(phrase_phonetique)
        diphones = generate_bigrams(phrase_phonetique)
        print(diphones)
        logatomes += generate_logatoms(diphones)
    print_unique_logatoms(logatomes)


def print_unique_logatoms(logatomes):
    uniques = []
    for logatome in logatomes:
        if logatome not in uniques:
            uniques.append(logatome)
    for logatome in uniques:
        print(logatome)
    print(f"Nombre de logatomes : {len(uniques)}")


def convert_SAMPA(phrase: List[str], dict_conversion: Dict[str, str]) -> str:
    converted = []
    for mot in phrase:
        if mot in dict_conversion:
            converted.append(dict_conversion[mot])
        else:
            write_in_unknown_file(mot + "\n")
    return add_shwa(converted, phrase)


def add_shwa(phrase_phonetique: List[str], phrase_ortho: List[str]) -> str:
    consonnes = [
        "p",
        "t",
        "k",
        "f",
        "s",
        "S",
        "b",
        "d",
        "g",
        "v",
        "z",
        "j",
        "l",
        "R",
        "n",
        "N",
        "m",
        "w",
        "H",
        "Z",
    ]
    phrase_finale = ""
    for i, mot_phon in enumerate(phrase_phonetique):
        phrase_finale += phrase_phonetique[i]
        if (
            i < len(phrase_phonetique) - 1
            and phrase_ortho[i][-1] == "e"
            and phrase_phonetique[i + 1][0] in consonnes
            and mot_phon[-1] not in "@e"
        ):
            phrase_finale += "@"
        phrase_finale += " "
    return phrase_finale


def generate_bigrams(phrase_phonetique: str) -> List[str]:
    bigrams = []
    without_spaces = ""
    for char in phrase_phonetique:
        if char != " ":
            without_spaces += char
    if without_spaces:
        bigrams.append("_" + without_spaces[0])
    for i in range(len(without_spaces) - 1):
        bigrams.append(without_spaces[i] + without_spaces[i + 1])
    bigrams.append(without_spaces[-1] + "_")
    return bigrams


def generate_logatoms(diphones: List[str]) -> List[str]:
    logatomes = []
    missed = []
    voyelles = ["a", "@", "2", "9", "o", "O", "e", "E", "u", "y", "i", "e~", "A", "C"]
    consonnes = [
        "p",
        "t",
        "k",
        "f",
        "s",
        "S",
        "b",
        "d",
        "g",
        "v",
        "z",
        "j",
        "l",
        "R",
        "n",
        "N",
        "m",
        "w",
        "H",
        "Z",
    ]
    for diphone in diphones:
        if diphone[0] in consonnes and diphone[1] in voyelles:
            logatomes.append("pa" + diphone + "pa")
        elif diphone[0] in consonnes and diphone[1] in consonnes:
            logatomes.append("pa" + diphone + "apa")
        elif diphone[0] in voyelles and diphone[1] in consonnes:
            logatomes.append("p" + diphone + "apa")
        elif diphone[0] in voyelles and diphone[1] in voyelles:
            logatomes.append("p" + diphone + "pa")
        elif diphone[0] == "_" and diphone[1] in voyelles:
            logatomes.append(diphone[1] + "pa")
        elif diphone[0] == "_" and diphone[1] in consonnes:
            logatomes.append(diphone[1] + "apa")
        elif diphone[1] == "_" and diphone[0] in voyelles:
            logatomes.append("ap" + diphone[0])
        elif diphone[1] == "_" and diphone[0] in consonnes:
            logatomes.append("apa" + diphone[0])
        else:
            missed.append(diphone)
    return logatomes


def load_sentences(path: str) -> List[str]:
    with open(path, "r") as text:
        return text.readlines()


def load_dict_SAMPA(path: str) -> Dict[str, str]:
    dict_conversion = {}
    with open(path, "r") as dict_SAMPA:
        reader = csv.reader(dict_SAMPA, delimiter="\t")
        for row in reader:
            dict_conversion[row[0]] = row[1]
    return dict_conversion


def write_in_unknown_file(mot):
    with open("mots_inconnus.txt", "a") as inconnus:
        inconnus.write(mot)


if __name__ == "__main__":
    main()
