import parselmouth as pm
import textgrids
import matplotlib.pyplot as plt
from parselmouth.praat import call 
from sys import argv, exit


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


def modif_f0(extraction):
    """
    Il faut que l'extrait ait une f0 donc verifier nb value > 0
    """
    # allongement = 0.85
    modif = call(extraction, "To Manipulation", 0.01, 75, 600)
    pitch_tier = call(modif, "Extract pitch tier")
    call(pitch_tier, "Remove points between", 0, extraction.duration)
    call(pitch_tier, "Add point", extraction.duration / 2, 99)
    call(pitch_tier, "Add point", 3 * extraction.duration / 4, 233)
    call([modif, pitch_tier], "Replace pitch tier")
    return call(modif, "Get resynthesis (overlap-add)")
