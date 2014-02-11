import json
import os
from os import path
from datetime import datetime

relativeDataPath = "data"
relativeFigurePath = "figures"
baseDirName = "PlosDataStats"
plosDataBaseDir = "/home/toennies/plosALM/data/"

onTbdb = False
if path.isdir(plosDataBaseDir):
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

def doForEachPlosDoc(fun, maxDocs=None, verbose=False):
    if onTbdb:
        count = 0
        for plosFile in plosDataFiles:
            fullPath = path.join(plosDataBaseDir, plosFile)
            docMetadataList = readAsJson(fullPath)
            for docMetadata in docMetadataList:
                count += 1
                if verbose and count%100 == 0:
                    print count
                if maxDocs and count >= maxDocs:
                    return

                fun(docMetadata)
    else:
        raise BaseException("not running on TBDB")

simpleDocsFilename = "relevant_data_dtptcmriiv.json"
simpleDocsPath = path.join(dataBasePath, simpleDocsFilename)
def doForEachSimpleDoc(fun, maxDocs=None):
    """Document Structure:
        [ [0]  [1]     [2]        [3]         [4]               [5]                 [6]         [7]   [8]     [9] ]
        [doi, title, pubDate, twitterData, citations, mendeleyDisciplineList, mendeleyReaders, issn, issue, volume]

        twitterData:
                     [      [0]      [1]                 [2]                         [3]    ]
            list of: [ "tweet text", user, retweetUser (None, wenn kein retweet), zeitpunkt ]

        citations:
                     [    [0]           [1]      ]
            list of: [ zeitpunkt, totalCitations ]

        mendeleyDisciplineList: list of strings
"""
    lines = open(simpleDocsPath)
    count = 0
    for line in lines:
        count += 1
        if maxDocs and count<=maxDocs:
            break

        docData = json.loads(line)
        fun(SimpleDoc(docData))

def formatHist(bins, bounds, formatHint = 5):
    print (' ' * formatHint) + str(map(lambda x: ("%" + str(formatHint) + "d") % x, bins))
    print map(lambda x: ("%" + str(formatHint) + "d") % x, bounds)

# from dateutil.parser import parse
# import calendar

class SimpleDoc:
    maximumTimestampInDataset = 1379408980

    def __init__(self, docData):
        self.doi = docData[0]
        self.title = docData[1]
        self.publicationTimestamp = docData[2]
        self.tweets = map(lambda tweetData: Tweet(tweetData), docData[3])
        # TODO check if tweets are sorted in time and sort if not
        self.citationTimeline = map(lambda citationData: CitationDataPoint(citationData), docData[4])
        # TODO check if citationTimeline are sorted in time and sort if not
        self.mendeleyDisciplines = docData[5]
        self.mendeleyReaders = None
        self.mendeleyReaders = docData[6]
        self.issn = docData[7]
        self.issue = docData[8]
        self.volume = docData[9]

    def publicationDatetime(self):
        # return calendar.timegm(parse(self.publicationTimestamp).timetuple())
        return datetime.fromtimestamp(self.publicationTimestamp)

    def cummulativeTwitterTimeline(self, padding=True):
        totalTweets = 0
        timelinePoints = []

        if padding and len(self.tweets) != 0:
            firstTweet = min(map(lambda tweet: tweet.timestamp, self.tweets))
            if firstTweet > self.publicationTimestamp:
                timelinePoints.append([self.publicationTimestamp, 0])
                
        for tweet in self.tweets:
            totalTweets += 1
            timelinePoints.append([tweet.timestamp, totalTweets])

        if padding: 
            maximumTimestampInDataset = 1379408980
            timelinePoints.append([maximumTimestampInDataset, totalTweets])

        return timelinePoints

    def numTweets(self):
        return len(self.tweets)

    def numTweetsBetweenRelative(self, lower=None, upper=None):
        return len(filter(lambda tweet: 
            (not lower or tweet.timestamp-self.publicationTimestamp>=lower) and
            (not upper or tweet.timestamp-self.publicationTimestamp<=upper)
        , self.tweets))

    def numTweetsBetweenAbsolute(self, lower=None, upper=None):
        return len(filter(lambda tweet: 
            (not lower or tweet.timestamp>=lower) and
            (not upper or tweet.timestamp<=upper)
        , self.tweets))

    def numCitations(self):
        return max(map(lambda c: c.totalCitations, self.citationTimeline))

    def timespan(self):
        timestamps = map(lambda tweet: tweet.timestamp, self.tweets)
        return max(timestamps) - min(timestamps)

    def age(self):
        maximumTimestampInDataset = 1379408980
        return maximumTimestampInDataset-self.publicationTimestamp

    def year(self):
        return self.publicationDatetime().year

class Tweet:
    def __init__(self, tweetData):
        self.text = tweetData[0]
        self.user = tweetData[1]
        self.retweetUser = tweetData[2]
        self.timestamp = tweetData[3]

    def isRetweet(self):
        return self.retweetUser != None

    def datetime(self):
        # return calendar.timegm(parse(self.timestamp).timetuple())
        return datetime.fromtimestamp(self.timestamp)

class CitationDataPoint:
    def __init__(self, citationData):
        self.timestamp = citationData[0]
        self.totalCitations = citationData[1]

    def datetime(self):
        # return calendar.timegm(parse(self.timestamp).timetuple())
        return datetime.fromtimestamp(self.timestamp)

def simpleDocs():
    lines = open(simpleDocsPath)
    return (SimpleDoc(json.loads(line)) for line in lines)

mendeleyDisciplines = [
    'Linguistics', 'Economics', 'Psychology', 'Humanities', 'Materials Science', 
    'Earth Sciences', 'Environmental Sciences', 'Biological Sciences', 'Medicine', 
    'Mathematics', 'Chemistry', 'Physics', 'Social Sciences', 'Electrical and Electronic Engineering', 
    'Astronomy / Astrophysics / Space Science', 'Sports and Recreation', 
    'Management Science / Operations Research', 'Philosophy', 'Law', 
    'Business Administration', 'Engineering', 'Design', 'Arts and Literature', 
    'Education', 'Computer and Information Science'
]

def groupCount(l):
    d = { }

    for x in l:
        d[x] = d.get(x, 0) + 1

    return list(d.items())
