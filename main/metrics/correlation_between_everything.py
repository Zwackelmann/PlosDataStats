from main.util.common import SimpleDoc, rankCorrelation
import math
import json
import numpy as np
import itertools

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

def correlationBetweenEverything(matrix, filename):
    f = open(filename, "w")
    pairs = [(x, y) for x in range(0, numAttributes) for y in range(0, numAttributes)]

    for pair in pairs:
        pearson, tau, r, p1, numPairs, leftZeroPairs, rightZeroPairs, bothZeroPairs = correlationBetweenAttributes(matrix, pair[0], pair[1])

        corr = CorrelationItem(
            corrFrom = attributeNames[pair[0]], 
            corrTo = attributeNames[pair[1]], 
            numValidPairs = numPairs, 
            leftZeroPairs = leftZeroPairs,
            rightZeroPairs = rightZeroPairs, 
            bothZeroPairs = bothZeroPairs, 
            kendall = tau, 
            spearman = r, 
            pearson = pearson, 
            pValue = p1
        )
        f.write(corr.toJson() + "\n")
        print corr.prettyPrint() + "\n\n"

    f.close()


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

# mendeleyShares = mendeleyReaders => removed ("mendeleyShares", None)
# mendeleyTotal = mendeleyReaders => removed ("mendeleyTotal", None)
# citeULikeShares = citeULikeTotal => removed ("citeULikeTotal", None)
# scopusCitations = scopusTotal => removed ("scopusTotal", None)
# pubmedTotal = pubmedCitations => removed ("pubmedTotal", None)
# natureTotal = natureCitations => removed ("natureTotal", None)
# postgenomicTotal = postgenomicCitations => removed ("postgenomicTotal", None)
# connoteaTotal = connoteaCitations => removed ("connoteaTotal", None)
# ("facebookTotal", None) removed
callList = [
    ("mendeleyReaders", None), ("pdfViews", None), ("htmlViews", None), ("citeULikeShares", None),
    ("connoteaCitations", None), ("natureCitations", None), ("postgenomicCitations", None), 
    ("pubmedCitations", None), ("scopusCitations", None), ("pmcPdf", None), ("pmcHtml", None), 
    ("facebookShares", None), ("facebookComments", None), ("facebookLikes", None), 
    ("mendeleyGroups", None), ("relativemetricTotal", None), ("numTweets", ()), 
    ("numCitations", ()), ("totalViews", ())
]

attributeNames = map(lambda call: call[0], callList)

"""matrix = map(lambda doc: map(lambda call: applyCall(doc, call), callList), SimpleDoc.getallBetween((2012,6), (2012,8)))
numAttributes = len(attributeNames)
correlationBetweenEverything(matrix, "pairwise_corr_2012-6_2012-8.json")"""

"""corrAll = CorrelationItem.fromFile("pairwise_corr_all_documents.json")
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

corrs = CorrelationItem.fromFile("pairwise_corr_2012-6_2012-8.json")
filteredCorrs = removeReflexiveCorrs(removeAllMirrorPairs(corrs))

def findCorr(corrs, corrFrom, corrTo):
    reverse = False
    targetIndex = next( (i for i in xrange(0, len(corrs)) if corrs[i].corrFrom==corrFrom and corrs[i].corrTo==corrTo), None)
    
    if targetIndex == None:
        targetIndex = next( (i for i in xrange(0, len(corrs)) if corrs[i].corrFrom==corrTo and corrs[i].corrTo==corrFrom), None)
        if targetIndex != None:
            reverse = True
            return corrs[targetIndex].correlation()
        else:
            return None
    else:
        return corrs[targetIndex].correlation()

f = open("foo", "w")
for corr1 in attributeNames:
    corrsForAttribute = []
    for corr2 in attributeNames:
        c = findCorr(corrs, corr1, corr2)
        corrsForAttribute.append(str(c) if not c is None else "None")

    f.write("\t".join(corrsForAttribute) + "\n")
f.close()

"""for attr, corrGroup in itertools.groupby(corrs, lambda corr: corr.corrFrom):
    sortedCorrGroup = sorted( corrGroup, key=lambda corr: corr.correlation(), reverse=True )

    print "Correlations to " + attr + ":\n======================================="
    for corr in sortedCorrGroup:
        print corr.prettyPrint() + "\n\n"""

"""for corr in filteredCorrs:
    if corr.correlation() > 0.4:
        print "  " + json.dumps({ "source" : corr.corrFrom, "target" : corr.corrTo, "weight" : corr.correlation()}) + ","


v = [ ]
for corr in filteredCorrs:
    v.append(corr.numValidPairs)
numDocuments = max(v)

weight = { }
for corr in filteredCorrs:
    weight[corr.corrFrom] = numDocuments-corr.leftZeroPairs

print json.dumps(dict([(k, float(v)/numDocuments) for k, v in weight.items()]))"""
