import json
import os
from os import path
from datetime import datetime

relativeDataPath = "data"
relativeFigurePath = "figures"
baseDirName = "PlosDataStats"
plosDataBaseDir = "/home/toennies/plosALM/data/"

onTbdb = False
if path.isfile(plosDataBaseDir):
    plosDataFiles = [ f for f in os.listdir(plosDataBaseDir) if path.isfile(path.join(plosDataBaseDir,f)) ]
    onTbdb = True

currentDir = path.dirname(path.realpath(__file__))

basedir = currentDir
while not (path.basename(basedir) == baseDirName or basedir == "/"):
    basedir = path.abspath(path.join(basedir, path.pardir))

dataBasePath = path.join(basedir, relativeDataPath)
figureBasePath = path.join(basedir, relativeFigurePath)

def dataPath(filename):
    return path.join(dataBasePath, filename)

def figurePath(filename):
    return path.join(figureBasePath, filename)

def writeJsonToData(obj, filename):
    targetFilePath = path.join(dataBasePath, filename)
    writeAsJson(obj, targetFilePath)

def readJsonFromData(filename):
    targetFilePath = path.join(dataBasePath, filename)
    jsonObject = readAsJson(targetFilePath)
    return jsonObject

def readAsJson(path):
    s = open(path)
    jsonObject = json.load(s)
    s.close()
    return jsonObject

def writeAsJson(obj, path):
    file = open(path, "w")
    file.write(json.dumps(obj))
    file.close()

def doForEachPlosDoc(fun):
    if onTbdb:
        for plosFile in plosDataFiles:
            fullPath = path.join(plosDataBaseDir, plosFile)
            docMetadataList = readAsJson(fullPath)
            for docMetadata in docMetadataList:
                fun(docMetadata)
    else:
        raise

simpleDocsFilename = "relevant_document_data2.json"
simpleDocsPath = path.join(dataBasePath, simpleDocsFilename)
def doForEachSimpleDoc(fun):
    """
    Document Structure:
        [ [0]    [1]        [2]         [3]                [4]         ]
        [ doi, pubDate, twitterData, citations, mendeleyDisciplineList ]

        twitterData:
                     [      [0]      [1]                 [2]                         [3]    ]
            list of: [ "tweet text", user, retweetUser (None, wenn kein retweet), zeitpunkt ]

        citations:
                     [    [0]           [1]      ]
            list of: [ zeitpunkt, totalCitations ]
    """
    lines = open(simpleDocsPath)
    for line in lines:
        docData = json.loads(line)
        fun(SimpleDoc(docData))

def formatHist(bins, bounds, formatHint = 5):
    print (' ' * formatHint) + str(map(lambda x: ("%" + str(formatHint) + "d") % x, bins))
    print map(lambda x: ("%" + str(formatHint) + "d") % x, bounds)

class SimpleDoc:
    def __init__(self, docData):
        self.doi = docData[0]
        self.publicationTimestamp = docData[1]
        self.tweets = map(lambda tweetData: Tweet(tweetData), docData[2])
        self.citationTimeline = map(lambda citationData: CitationDataPoint(citationData), docData[3])
        self.mendeleyDisciplines = docData[4]
    
    def publicationDatetime(self):
        return datetime.fromtimestamp(self.publicationTimestamp)

class Tweet:
    def __init__(self, tweetData):
        self.text = tweetData[0]
        self.user = tweetData[1]
        self.retweetUser = tweetData[2]
        self.timestamp = tweetData[3]

    def isRetweet(self):
        return self.retweetUser != None

    def datetime(self):
        return datetime.fromtimestamp(self.timestamp)

class CitationDataPoint:
    def __init__(self, citationData):
        self.timestamp = citationData[0]
        self.totalCitations = citationData[1]

    def datetime(self):
        return datetime.fromtimestamp(self.timestamp)

def simpleDocs():
    lines = open(simpleDocsPath)
    return (SimpleDoc(json.loads(line)) for line in lines)

def groupCount(l):
    d = { }

    for x in l:
        d[x] = d.get(x, 0) + 1

    return list(d.items())