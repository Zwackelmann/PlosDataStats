from main.util.common import SimpleDoc, rankCorrelation
import math
import json
import numpy as np
import itertools
from main.util.graph import writeGraphToFile

def applyCall(obj, call):
    x = getattr(obj, call[0])

    if call[1] == None:
        return x
    elif type(call[1]) is tuple:
        return x(*call[1])
    else:
        raise ValueError("apply call with call: " + repr(call) + " failed")

def getAttributeStats(matrix):
    attributeStats = { }

    for row in matrix:
        for colInd in range(0, len(callList)):
            colValue = row[colInd]
            attributeStatsTuple = attributeStats.get(colInd, (0, 0, 0))

            if colValue == None:
                attributeStatsTuple = (attributeStatsTuple[0]+1, attributeStatsTuple[1], attributeStatsTuple[2])
            elif colValue == 0:
                attributeStatsTuple = (attributeStatsTuple[0], attributeStatsTuple[1]+1, attributeStatsTuple[2])
            else:
                attributeStatsTuple = (attributeStatsTuple[0], attributeStatsTuple[1], attributeStatsTuple[2]+1)

            attributeStats[colInd] = attributeStatsTuple

    print zip(attributeStats.items(), map(lambda call: call[0], callList))

def corrcoeff(x, y):
    avgX = float(sum(x)) / len(x)
    avgY = float(sum(y)) / len(y)

    sumErrorProducts = 0
    for i in range(0, len(x)):
        sumErrorProducts += (x[i]-avgX)*(y[i]-avgY)

    xSquareError = 0
    for xi in x:
        xSquareError += math.pow(xi-avgX, 2)

    ySquareError = 0
    for yi in y:
        ySquareError += math.pow(yi-avgY, 2)

    if xSquareError*ySquareError == 0.0:
        return None
    else:
        return sumErrorProducts / math.sqrt(xSquareError*ySquareError)

def correlationBetweenEverything(matrix, attributeNames):
    numAttributes = len(attributeNames)
    pairs = [(x, y) for x in range(0, numAttributes) for y in range(x+1, numAttributes)]

    correlationItems = [ ]
    for corrFrom, corrTo in pairs:
        pearson, tau, r, p1, numPairs, leftZeroPairs, rightZeroPairs, bothZeroPairs = correlationBetweenAttributes(matrix, corrFrom, corrTo)

        correlationItems.append(CorrelationItem(
            corrFrom = attributeNames[corrFrom], 
            corrTo = attributeNames[corrTo], 
            numValidPairs = numPairs, 
            leftZeroPairs = leftZeroPairs,
            rightZeroPairs = rightZeroPairs, 
            bothZeroPairs = bothZeroPairs, 
            kendall = tau, 
            spearman = r, 
            pearson = pearson, 
            pValue = p1
        ))

    return correlationItems


def correlationBetweenAttributes(matrix, i, j):
    pairs = filter(lambda row: not row[0] is None and not row[1] is None, map(lambda row: [row[i], row[j]], matrix))
    numPairs = len(pairs)
    bothZeroPairs = len(filter(lambda row: row[0]==0 and row[1]==0, pairs))
    leftZeroPairs = len(filter(lambda row: row[0]==0, pairs))
    rightZeroPairs = len(filter(lambda row: row[1]==0, pairs))

    if len(pairs) != 0:
        x, y = zip(*pairs)

        pearson = corrcoeff(x, y)
        tau, p1, r, p2 = rankCorrelation(x, y)
        return pearson, tau, r, p1, numPairs, leftZeroPairs, rightZeroPairs, bothZeroPairs
    else:
        return None, None

class CorrelationItem:
    def __init__(self, corrFrom, corrTo, numValidPairs, leftZeroPairs, 
        rightZeroPairs, bothZeroPairs, kendall, spearman, pearson, pValue
        ):
        self.corrFrom = corrFrom
        self.corrTo = corrTo
        self.numValidPairs = numValidPairs
        self.leftZeroPairs = leftZeroPairs
        self.rightZeroPairs = rightZeroPairs
        self.bothZeroPairs = bothZeroPairs
        self.kendall = kendall
        self.spearman = spearman
        self.pearson = pearson
        self.pValue = pValue

    def prettyPrint(self):
        return self.corrFrom + " ~ " + self.corrTo + ":\n" + (
            "#Valid Pairs: " + str(self.numValidPairs) + "\n" + 
            "#Zero Pairs: (left: " + str(self.leftZeroPairs) + ", right: " + str(self.rightZeroPairs) + ", both: " + str(self.bothZeroPairs) + ")\n" + 
            "p-value: " + str(self.pValue) + "\n" + 
            "Kendall tau: " + str(self.kendall) + "\n" +
            "Spearman r: " + str(self.spearman) + "\n" +
            "Pearson corr: " + str(self.pearson))

    def toJson(self):
        jsonObj = {
            "corr-from" : self.corrFrom, "corr-to" : self.corrTo, "num-valid-pairs" : self.numValidPairs,
            "left-zero-pairs" : self.leftZeroPairs, "right-zero-pairs" : self.rightZeroPairs, 
            "both-zero-pairs" : self.bothZeroPairs, "kendall" : self.kendall, "spearman" : self.spearman, 
            "pearson" : self.pearson, "p-value" : self.pValue
        }
        return json.dumps(jsonObj)

    def correlation(self):
        l = filter(lambda x: x != None, [self.kendall, self.spearman, self.pearson])
        if len(l) == 0:
            return None
        else:
            return np.mean(l)

    @classmethod
    def fromJson(cls, jsonString):
        jsonObj = json.loads(jsonString)
        return cls(
            jsonObj['corr-from'], jsonObj['corr-to'], jsonObj['num-valid-pairs'], 
            jsonObj['left-zero-pairs'], jsonObj['right-zero-pairs'], 
            jsonObj['both-zero-pairs'], jsonObj['kendall'], jsonObj['spearman'], 
            jsonObj['pearson'], jsonObj['p-value']
        )

    @classmethod
    def fromFile(cls, filename):
        lines = open(filename)
        return [ cls.fromJson(line) for line in lines ]

def getAttributeValueMatrix(docs, callList):
    return map(lambda doc: map(lambda call: applyCall(doc, call), callList), docs)

def findMirrorPairIndex(corrs, ind):
    corr1 = corrs[ind]
    for i in (i for i in range(0, len(corrs)) if i != ind):
        corr2 = corrs[i]
        if ((corr1.corrFrom == corr2.corrFrom and corr1.corrTo == corr2.corrTo) or 
            (corr1.corrFrom == corr2.corrTo and corr1.corrTo == corr2.corrFrom)):
            return i

    return None

def isReflexive(corr):
    return corr.corrFrom == corr.corrTo

def removeAllMirrorPairs(corrs):
    delIndex = next( (findMirrorPairIndex(corrs, i) for i in xrange(0, len(corrs)) if findMirrorPairIndex(corrs, i) != None), None)

    if delIndex == None:
        return corrs
    else:
        del corrs[delIndex]
        return removeAllMirrorPairs(corrs)

def removeReflexiveCorrs(corrs):
    delIndex = next( (i for i in xrange(0, len(corrs)) if isReflexive(corrs[i])), None )
    if delIndex == None:
        return corrs
    else:
        del corrs[delIndex]
        return removeReflexiveCorrs(corrs)

def findCorr(corrs, corrFrom, corrTo, method="spearman"):
    if corrFrom == corrTo:
        return 1.0

    reverse = False
    targetIndex = next( (i for i in xrange(0, len(corrs)) if corrs[i].corrFrom==corrFrom and corrs[i].corrTo==corrTo), None)
    targetCorr = None

    if targetIndex == None:
        targetIndex = next( (i for i in xrange(0, len(corrs)) if corrs[i].corrFrom==corrTo and corrs[i].corrTo==corrFrom), None)
        if targetIndex != None:
            reverse = True
            targetCorr = corrs[targetIndex]
    else:
        targetCorr = corrs[targetIndex]

    if targetCorr != None:
        if method=="spearman":
            return targetCorr.spearman
        elif method=="kendall":
            return targetCorr.kendall
        elif method=="pearson":
            return targetCorr.pearson
        elif method=="avg":
            return targetCorr.correlation()
        else:
            raise ValueError( "Unknown correlation method " + method + ". (Try \"spearman\", \"kendall\", \"pearson\" or \"avg\")" )
    else:
        return None



def biggestDifferencesBetweenCorrelations():
    corrAll = CorrelationItem.fromFile("pairwise_corr_all_documents.json")
    corrNew = CorrelationItem.fromFile("pairwise_corr_2012-6_2012-8.json")

    corrPairs = [ [corr1, corr2] for corr1 in corrAll for corr2 in corrNew if corr1.corrFrom==corr2.corrFrom and corr1.corrTo==corr2.corrTo ]    

    corrDiffs = []
    for corrPair in corrPairs:
        attFrom = corrPair[0].corrFrom
        attTo = corrPair[0].corrTo

        diff = abs(corrPair[0].correlation()-corrPair[1].correlation())
        corrDiffs.append([diff, corrPair])

    sortedCorrDiffs = map(lambda x: x[1], sorted(corrDiffs, key=lambda x: x[0], reverse=True))

    for corrPair in sortedCorrDiffs[:50]:
        print corrPair[0].prettyPrint()
        print ""
        print corrPair[1].prettyPrint()
        print "\n\n"""

def printCorrelations(corrs, attributeNames):
    filteredCorrs = removeReflexiveCorrs(removeAllMirrorPairs(corrs))

    f = open("foo", "w")
    for corr1 in attributeNames:
        corrsForAttribute = []
        for corr2 in attributeNames:
            c = findCorr(corrs, corr1, corr2)
            corrsForAttribute.append(str(c) if not c is None else "None")

        f.write("\t".join(corrsForAttribute) + "\n")
    f.close()

def corrGraphData(corrs, threshold=0.4, method="spearman", attributeNameTranslation = {}):
    corrsOut = []

    for corr in corrs:
        corrValue = None
        if method=="spearman":
            if corr.spearman > threshold:
                corrValue = corr.spearman
        elif method=="kendall":
            if corr.kendall > threshold:
                corrValue = corr.kendall
        elif method=="pearson":
            if corr.pearson > threshold:
                corrValue = corr.pearson
        elif method=="avg":
            if corr.correlation() > threshold:
                corrValue = corr.correlation()
        else:
            raise ValueError( "Unknown method " + method + " for correlation graph creation. (Try \"spearman\", \"kendall\", \"pearson\" or \"avg\")" )
        corrsOut.append({ 
            "source" : attributeNameTranslation.get(corr.corrFrom, corr.corrFrom), 
            "target" : attributeNameTranslation.get(corr.corrTo, corr.corrTo),
            "weight" : corrValue
        })

    numDocuments = max(map(lambda corr: corr.numValidPairs, corrs))

    weight = { }
    for corr in corrs:
        weight[corr.corrFrom] = numDocuments-corr.leftZeroPairs
        weight[corr.corrTo] = numDocuments-corr.rightZeroPairs

    weightsOut = dict([(attributeNameTranslation.get(k, k), float(v)/numDocuments) for k, v in weight.items()])

    return corrsOut, weightsOut

# mendeleyShares = mendeleyReaders => removed ("mendeleyShares", None)
# mendeleyTotal = mendeleyReaders => removed ("mendeleyTotal", None)
# citeULikeShares = citeULikeTotal => removed ("citeULikeTotal", None)
# scopusCitations = scopusTotal => removed ("scopusTotal", None)
# pubmedTotal = pubmedCitations => removed ("pubmedTotal", None)
# natureTotal = natureCitations => removed ("natureTotal", None)
# postgenomicTotal = postgenomicCitations => removed ("postgenomicTotal", None)
# connoteaTotal = connoteaCitations => removed ("connoteaTotal", None)
# ("facebookTotal", None) removed

# (("natureCitations", None), None), (("connoteaCitations", None), None), (("postgenomicCitations", None), None), , (("mendeleyGroups", None), (2012,1))
attributeList = [
    (("numTweets", ()), (2012, 5), "Tweets"), 
    (("facebookShares", None), (2011, 12), "Facebook shares"), 
    (("facebookComments", None), (2011, 12), "Facebook comments"), 
    (("facebookLikes", None), (2011, 12), "Facebook Likes"), 
    (("mendeleyReaders", None), (2012, 1), "Mendeley readers"), 
    (("citeULikeShares", None), (2009, 3), "CiteULike shares"), 
    (("htmlViews", None), (2009, 9), "PLOS HTML views"), 
    (("pdfViews", None), (2009, 9), "PLOS PDF views"), 
    (("pmcHtml", None), (2011, 6), "PMC HTML views"), 
    (("pmcPdf", None), (2011, 6), "PMC PDF views"), 
    (("numCrossrefs", ()), (2009, 3), "CrossRef citations"),
    (("pubmedCitations", None), (2009, 3), "PubMed citations"), 
    (("scopusCitations", None), (2009, 3), "Scopus citations")
]

attributeNames = map(lambda x: x[0][0], attributeList)
attributePrintNames = map(lambda x: x[2], attributeList)
calls = map(lambda x: x[0], attributeList)

# statistical values for each metric:
"""
for ind, attr in zip(range(0, len(attributeList)), attributeList):
    call = attr[0]
    lowerBound = attr[1]
    attName = attr[0][0]

    valuesForMetric = filter(lambda x: x != None, map(lambda doc: applyCall(doc, call),
        SimpleDoc.getallBetween(lowerBound, None)
    ))

    minV, maxV, meanV, std = min(valuesForMetric), max(valuesForMetric), np.mean(valuesForMetric), np.std(valuesForMetric)
    print attName + "\t" + "\t".join(map(lambda x: str(x), [minV, maxV, meanV, std]))
"""


# docs = SimpleDoc.getallBetween((2012, 6), (2012, 8))

"""
matrix = getAttributeValueMatrix(docs, calls)
corrs = correlationBetweenEverything(matrix, attributeNames)

f = open("foo", "w")
for corr in corrs:
    f.write(corr.toJson() + "\n")
f.close()
"""


# corrs = CorrelationItem.fromFile("stuff/pairwise_corr_2012-6_2012-8.json")

"""
f = open("foo", "w")
m = []
for a1 in attributeNames:
    row = []
    for a2 in attributeNames:
        row.append(findCorr(corrs, a1, a2, method="spearman"))
    m.append(row)

f.write("\t" + "\t".join(attributePrintNames) + "\n")
for row, att in zip(m, attributePrintNames):
    f.write(att + "\t" + ("\t".join(map(lambda x: "%2.3f" % x, row))) + "\n")
f.close()
"""

attributeNameTranslation = dict(zip(attributeNames, attributePrintNames))
corrData, weightData = corrGraphData(corrs, method = "spearman", threshold=0.385, attributeNameTranslation=attributeNameTranslation)
writeGraphToFile(corrData, weightData, animated=True)