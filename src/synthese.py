import parselmouth as pm
from parselmouth.praat import call

import sys

sys.path.insert(0, "utils")

from prosody import accelerate_extract
from conversion import convert_sentence_SAMPA


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
            extract = accelerate_extract(extract)
            return extract
    return f"DIPHONE NOT FOUND : {diphone}"


def find_middle_phoneme(sound, phonemes, index):
    milieu = (phonemes[index].xmax + phonemes[index].xmin) / 2
    milieu = sound.get_nearest_zero_crossing(milieu, 1)
    return milieu


def synthetise(sound, extracts):
    synthese = sound.extract_part(0, 0.01, pm.WindowShape.RECTANGULAR, 1, False)
    synthese = synthese.concatenate(extracts, overlap=0.03)
    return synthese
