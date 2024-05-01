import time
import serial
import time as t
import numpy as np
import pyttsx3
from maestro import Controller
import math


# 2D Multilateration with N platforms.
# Input is list of platform objects with x,y position and range to target
def multilatNPlat(Refs, alt=np.nan):
    solList = []
    # Get list solution pair for all reference platform pairs
    for platCombo in itertools.combinations(Refs,2):
        solList.append(multilat2Plat(platCombo[0],platCombo[1],alt))
    minError = np.inf
    for solCombo in itertools.product(*solList):
        solution = np.asarray(solCombo)
        meanSol = np.mean(solution, axis=0)
        meanError = meanError = np.sum(np.abs(solution-meanSol))
        if meanError < minError:
            position = meanSol
            minError = meanError
    return position