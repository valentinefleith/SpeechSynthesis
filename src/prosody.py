import parselmouth as pm
import textgrids
from parselmouth.praat import call
from Sentence import Sentence

VERBS = ["sera", "interrompent", "ai", "sont"]


def modif_prosody(synthese, sentence_nb, modalite):
    segmentation = textgrids.TextGrid(f"wav-files/synthese_phrase{sentence_nb}.TextGrid")
    sentence = Sentence(sentence_nb, segmentation["mots"], segmentation["phonemes"], modalite)
    verb_index = sentence.get_verb_index()
    synthese = modif_f0(synthese, sentence, verb_index)
    synthese = modif_duration_phrase(synthese, sentence, verb_index)
    return synthese


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


def modif_f0(synthese, sentence, verb_index):
    modif = call(synthese, "To Manipulation", 0.01, 75, 600)
    pitch_tier = call(modif, "Extract pitch tier")
    call(pitch_tier, "Remove points between", 0, synthese.duration)
    call(pitch_tier, "Add point", 0.01, 190)
    if sentence.modalite == 0:
        call(pitch_tier, "Add point", synthese.duration - 0.0001, 180)
    elif sentence.modalite == 1:
        call(pitch_tier, "Add point", synthese.duration - 0.0001, 250)
    elif sentence.modalite == "exclamative":
        call(pitch_tier, "Add point", synthese.duration - 0.0001, 180)
    call(pitch_tier, "Add point", sentence.mots[verb_index].xmax, 230)
    call([modif, pitch_tier], "Replace pitch tier")
    return call(modif, "Get resynthesis (overlap-add)")


def modif_duration_phrase(synthese, sentence, verb_index):
    allongement = 1.5
    modif = call(synthese, "To Manipulation", 0.01, 75, 600)
    duration_tier = call(modif, "Extract duration tier")
    call(duration_tier, "Remove points between", 0, synthese.duration)
    stressed_index = sentence.get_stressed_phoneme_index(verb_index)
    call(duration_tier, "Add point", sentence.phonemes[stressed_index].xmin - 0.5, 1)
    call(duration_tier, "Add point", sentence.phonemes[stressed_index].xmin - 0.5 + 0.001, allongement)
    call(duration_tier, "Add point", sentence.phonemes[stressed_index].xmax - 0.5 - 0.001, allongement)
    call(duration_tier, "Add point", sentence.phonemes[stressed_index].xmax - 0.5, 1)
    call([modif, duration_tier], "Replace duration tier")
    return call(modif, "Get resynthesis (overlap-add)")
