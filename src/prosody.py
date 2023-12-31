import parselmouth as pm
import textgrids
import matplotlib.pyplot as plt
from parselmouth.praat import call 
import spacy


def parse_text(synthese, phrase_nb, phrase):
    sound = pm.Sound(synthese)
    segmentation = textgrids.TextGrid(f'wav-files/{phrase_nb}.TextGrid')
    nlp = spacy.load("fr_core_news_sm")
    tokens = nlp(phrase)
    return tokens


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


def modif_f0(synthese, tokens, segmentation):
    """
    Il faut que l'extrait ait une f0 donc verifier nb value > 0
    """
    # allongement = 0.85
    modif = call(synthese, "To Manipulation", 0.01, 75, 600)
    pitch_tier = call(modif, "Extract pitch tier")
    call(pitch_tier, "Remove points between", 0, synthese.duration)
    call(pitch_tier, "Add point", 1 * synthese.duration / 10, 100)
    for token in tokens:
        if token.pos_ == "VERB":
            call(pitch_tier, "Add point", get_token_endtime(token.text, segmentation), 233)
    call(pitch_tier, "Add point", 9 * synthese.duration / 10, 100)
    call([modif, pitch_tier], "Replace pitch tier")
    return call(modif, "Get resynthesis (overlap-add)")


def get_token_endtime(token, segmentation):
    mots = segmentation["mots"]
    for mot in mots:
        if mot == token:
            return mot.xmax
