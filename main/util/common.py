import json
import os
from os import path

relativeDataPath = "data"
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

def dataPath(filename):
    return path.join(dataBasePath, filename)

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

simpleDocsFilename = "relevant_document_data.json"
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
        doc = json.loads(line)
        fun(doc)

def formatHist(bins, bounds, formatHint = 5):
    print (' ' * formatHint) + str(map(lambda x: ("%" + str(formatHint) + "d") % x, bins))
    print map(lambda x: ("%" + str(formatHint) + "d") % x, bounds)