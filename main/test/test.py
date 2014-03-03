import json
import matplotlib.pyplot as plt
from main.util.common import SimpleDoc
import numpy as np
from scipy import stats

def rankCorrelation(x, y):
    numPairs = len(x)
    pairs = zip(range(0, numPairs), x, y)

    identsByX = map( lambda pair: pair[0],
        sorted(pairs, key=lambda pair: pair[1], reverse=True)
    )

    identsByY = map( lambda pair: pair[0],
        sorted(pairs, key=lambda pair: pair[2], reverse=True)
    )

    identsByXRank = { }
    rank = 0
    for ident in identsByX:
        identsByXRank[ident] = rank
        rank += 1

    identsByX2 = range(0, numPairs)
    identsByY2 = []

    for ident in identsByY:
        identsByY2.append(identsByXRank[ident])

    r, pValue2 = stats.spearmanr(identsByX2, identsByY2)

    return r, pValue2


def rankCorrelation2(x, y):
    return stats.spearmanr(x, y)

x = [ 2.0, 3.0, 3.0, 5.0, 5.5, 8.0, 10.0, 10.0 ]
y = [ 1.5, 1.5, 4.0, 3.0, 1.0, 5.0, 5.0, 9.5 ]

print rankCorrelation2(x, y)
print rankCorrelation(x, y)