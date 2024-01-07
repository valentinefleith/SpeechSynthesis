import parselmouth as pm
import textgrids
from parselmouth.praat import call

VERBS = ["sera", "interrompent", "ai", "sont"]


def modif_duration(extraction, allongement):
    """
    Il faut que l'extrait ait une f0 donc verifier nb value > 0
    """
    allongement = 0.70
    modif = call(extraction, "To Manipulation", 0.01, 75, 600)
    duration_tier = call(modif, "Extract duration tier")
    call(duration_tier, "Remove points between", 0, extraction.duration)
    call(duration_tier, "Add point", extraction.duration / 2, allongement)
    call([modif, duration_tier], "Replace duration tier")
    return call(modif, "Get resynthesis (overlap-add)")


def modif_f0(synthese, modalite):
    modalite = "declarative"
    segmentation = textgrids.TextGrid("wav-files/synthese.TextGrid")
    phrase = segmentation["mots"]
    modif = call(synthese, "To Manipulation", 0.01, 75, 600)
    pitch_tier = call(modif, "Extract pitch tier")
    call(pitch_tier, "Remove points between", 0, synthese.duration)
    call(pitch_tier, "Add point", 0.01, 190)
    if modalite == "declarative":
        call(pitch_tier, "Add point", synthese.duration - 0.0001, 180)
    elif modalite == "interrogative":
        call(pitch_tier, "Add point", synthese.duration - 0.0001, 180)
    elif modalite == "exclamative":
        call(pitch_tier, "Add point", synthese.duration - 0.0001, 180)
    for i, mot in enumerate(phrase):
        if mot.text in VERBS:
            call(pitch_tier, "Add point", phrase[i].xmax, 230)
    call([modif, pitch_tier], "Replace pitch tier")
    return call(modif, "Get resynthesis (overlap-add)")


def find_phoneme_to_lengthen(synthese):
    segmentation = textgrids.TextGrid("wav-files/synthese.TextGrid")
    phrase = segmentation["mots"]
    phonemes = segmentation["phonemes"]
    mot_a_allonger = phrase[0]
    for i, mot in enumerate(phrase):
        if mot.text in VERBS:
            mot_a_allonger = phrase[i - 1]
    if mot_a_allonger == phrase[0]:
        return
    print("je suis ici")
    for i, phoneme in enumerate(phonemes):
        if phonemes[i].xmin >= mot_a_allonger.xmin and phonemes[i].xmax <= mot_a_allonger.xmax:
            #if (is_stressed(phoneme)):
            if phoneme.text == "O":
                return modif_duration_phrase(synthese, phoneme)


def modif_duration_phrase(synthese, phoneme):
    allongement = 2
    modif = call(synthese, "To Manipulation", 0.01, 75, 600)
    duration_tier = call(modif, "Extract duration tier")
    call(duration_tier, "Remove points between", 0, synthese.duration)
    call(duration_tier, "Add point", 0, 1)
    call(duration_tier, "Add point", synthese.duration, 1)
    call(duration_tier, "Add point", phoneme.xmin, 1)
    call(duration_tier, "Add point", phoneme.xmax, 1)
    call(duration_tier, "Add point", (phoneme.xmax + phoneme.xmin) / 2, allongement)
    call([modif, duration_tier], "Replace duration tier")
    return call(modif, "Get resynthesis (overlap-add)")
