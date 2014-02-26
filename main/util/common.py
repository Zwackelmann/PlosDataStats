import json
import os
from os import path
from datetime import datetime
import string 
import numpy
import time
import calendar
from scipy import stats
import math
from dateutil.parser import parse

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

def timestr2timestamp(timestr):
    return calendar.timegm(parse(timestr).timetuple())

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

simpleDocsFilename = "relevant_document_data.json"
simpleDocsPath = path.join(dataBasePath, simpleDocsFilename)
def doForEachSimpleDoc(fun, maxDocs=None):
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

def readIssnData():
    issnToImpactRaw = readJsonFromData("issn_impact.json")
    
    issnToImpact = { }
    for key, value in issnToImpactRaw.items():
        issnToImpact[filter(lambda c: c in string.digits, key)] = value
    
    return issnToImpact

def filterDigits(s):
    return filter(lambda c: c in string.digits, s)

def yearMonthDay2Timestamp(year, month=1, day=1):
    dt = datetime(year=year, month=month, day=day)
    return time.mktime(dt.timetuple())

class SimpleDoc:
    maximumTimestampInDataset = 1379408980 #  Sep 17 2013
    corpus = None

    def __init__(self, docData):
        """Document Structure:
        [[0]   [1]     [2]        [3]            [4]            [5]              [6]                  [7]        [8]    [9]    [10]     [11]      [12]           [13]            [14]              [15]             [16]            [17]           [18]               [19]               [20]             [21]           [22]           [23]           [24]       [25]    [26]        [27]              [28]            [29]           [30]           [31]             [32]           [33]            [34]         ]
        [doi, title, pubDate, twitterData, crossrefTimeline, crossrefs, mendeleyDisciplineList, mendeleyReaders, issn, issue, volume, pdfViews, htmlViews, citeULikeShares, citeULikeTotal, connoteaCitations, connoteaTotal, natureCitations, natureTotal, postgenomicCitations, postgenomicTotal, pubmedCitations, pubmedTotal, scopusCitations, scopusTotal, pmcPdf, pmcHtml, facebookShares, facebookComments, facebookLikes, facebookTotal, mendeleyGroups, mendeleyShares, mendeleyTotal, relativemetricTotal]

        twitterData:
                     [      [0]      [1]                 [2]                         [3]    ]
            list of: [ "tweet text", user, retweetUser (None, wenn kein retweet), zeitpunkt ]

        crossrefTimeline:
                     [    [0]           [1]      ]
            list of: [ zeitpunkt, totalCitations ]

        crossrefs:
                     [[0]   [1]         [2]      ]
            list of: [doi, issn, publication_type]
        mendeleyDisciplineList: list of strings
        """
        if len(docData) != 35:
            raise ValueError("The docData array for initializing a SimpleDoc must have exactly 35 elements")

        self.doi = docData[0]
        self.title = docData[1]
        self.publicationTimestamp = docData[2]
        self.tweets = map(lambda tweetData: Tweet(tweetData), docData[3])
        # TODO check if tweets are sorted in time and sort if not
        self.crossrefTimeline = map(lambda crossrefData: CrossrefDataPoint(crossrefData), docData[4])
        # TODO check if crossrefTimeline are sorted in time and sort if not
        self.crossrefs = map(lambda crossrefData: Crossref(crossrefData), docData[5])
        self.mendeleyDisciplines = docData[6]
        self.mendeleyReaders = docData[7]
        self.issn = docData[8]
        self.issue = docData[9]
        self.volume = docData[10]
        self.pdfViews = docData[11]
        self.htmlViews = docData[12]
        self.citeULikeShares = docData[13]
        self.citeULikeTotal = docData[14]
        self.connoteaCitations = docData[15]
        self.connoteaTotal = docData[16]
        self.natureCitations = docData[17]
        self.natureTotal = docData[18]
        self.postgenomicCitations = docData[19]
        self.postgenomicTotal = docData[20]
        self.pubmedCitations = docData[21]
        self.pubmedTotal = docData[22]
        self.scopusCitations = docData[23]
        self.scopusTotal = docData[24]
        self.pmcPdf = docData[25]
        self.pmcHtml = docData[26]
        self.facebookShares = docData[27]
        self.facebookComments = docData[28]
        self.facebookLikes = docData[29]
        self.facebookTotal = docData[30]
        self.mendeleyGroups = docData[31]
        self.mendeleyShares = docData[32]
        self.mendeleyTotal = docData[33]
        self.relativemetricTotal = docData[34]

    def publicationDatetime(self):
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
            timelinePoints.append([SimpleDoc.maximumTimestampInDataset, totalTweets])

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

    def numCrossrefs(self):
        return max(map(lambda c: c.totalCitations, self.crossrefTimeline))

    def averageCrossref(self):
        return numpy.mean([self.numCrossrefs(), self.scopusCitations, self.pubmedCitations])

    def tweetTimespan(self):
        timestamps = map(lambda tweet: tweet.timestamp, self.tweets)
        return max(timestamps) - min(timestamps)

    def age(self):
        return SimpleDoc.maximumTimestampInDataset-self.publicationTimestamp

    def year(self):
        return self.publicationDatetime().year

    def month(self):
        return self.publicationDatetime().month

    def totalViews(self):
        if self.htmlViews is None or self.pdfViews is None:
            return None
        else:
            return self.htmlViews + self.pdfViews

    def crossrefWeight(self, method = "sum"):
        ifs = []
        for crossref in self.crossref:
            if type(crossref.issn) is list:
                ifs.append(max(map(lambda issn: SimpleDoc.issnToImpact.get(filterDigits(issn), 0.0), crossref.issn)))
            elif type(crossref.issn) is unicode:
                ifs.append(SimpleDoc.issnToImpact.get(filterDigits(crossref.issn), 0.0))
            elif crossref.issn is None:
                ifs.append(None)
            else:
                raise ValueError("crossref issns is neither a list nor a string but " + str(type(crossref.issn)))

        if method == "sum":
            nonNones = filter(lambda x: x!= None, ifs)
            if len(nonNones) != 0:
                return sum(nonNones)
            else:
                return None
        elif method == "avg":
            nonNones = filter(lambda x: x!= None, ifs)
            if len(nonNones) != 0:
                return numpy.mean(nonNones)
            else:
                return None
        elif method == "max":
            nonNones = filter(lambda x: x!= None, ifs)
            if len(nonNones) != 0:
                return max(nonNones)
            else:
                return None
        else:
            raise ValueError(method + " is no valid method for crossref weighting")

    issnToImpact = readIssnData() if not onTbdb else None

    @classmethod
    def getall(cls, filterFunction = None):
        if SimpleDoc.corpus is None:
            SimpleDoc.corpus = SimpleDoc.readCorpus()

        if filterFunction == None:
            return SimpleDoc.corpus
        else:
            return filter(filterFunction, SimpleDoc.corpus)

    @classmethod
    def readCorpus(cls):
        lines = open(simpleDocsPath)
        return [SimpleDoc(json.loads(line)) for line in lines]

    @classmethod
    def getallBetween(cls, lowerBound = None, upperBound = None):
        if type(lowerBound) is int:
            lowerBoundTimestamp = yearMonthDay2Timestamp(year=lowerBound)
        elif lowerBound is None:
            lowerBoundTimestamp = None
        else:
            lowerBoundTimestamp = yearMonthDay2Timestamp(*lowerBound)
        
        if upperBound == None:
            upperBoundTimestamp = None
        elif type(upperBound) is int:
            upperBoundTimestamp = yearMonthDay2Timestamp(year=upperBound+1, month=1, day=1)
        elif len(upperBound) == 1 or (len(upperBound) == 2 and upperBound[1] == 12):
            # get the timestamp of the first day in next year
            upperBoundTimestamp = yearMonthDay2Timestamp(year=upperBound[0]+1, month=1, day=1)
        elif len(upperBound) == 2:
            # get the timestamp of the first day in next month
            year = upperBound[0]
            month = upperBound[1]
            upperBoundTimestamp = yearMonthDay2Timestamp(year=year, month=month+1, day=1)
        elif len(upperBound) == 3:
            year = upperBound[0]
            month = upperBound[1]
            day = upperBound[2]

            upperBoundTimestamp = yearMonthDay2Timestamp(year=year, month=month, day=day)
        else:
            raise ValueError("Submitted an invalid upperBound: " + str(upperBound))

        return filter(
            lambda doc: 
                (not lowerBoundTimestamp or doc.publicationTimestamp >= lowerBoundTimestamp) and
                (not upperBoundTimestamp or doc.publicationTimestamp < upperBoundTimestamp),
            SimpleDoc.getall()
        )

    @classmethod
    def findByDoi(cls, doi):
        if SimpleDoc.doi2DocMap is None:
            SimpleDoc.doi2DocMap = { }
            for doc in SimpleDoc.getall():
                SimpleDoc.doi2DocMap[doc.doi] = doc

        return SimpleDoc.doi2DocMap.get(doi, None)

SimpleDoc.doi2DocMap = None

class Tweet:
    def __init__(self, tweetData):
        self.text = tweetData[0]
        self.username = tweetData[1]
        self.retweetUser = tweetData[2]
        self.timestamp = tweetData[3]

    def user(self):
        return User.findByTwitterName(self.username)

    def isRetweet(self):
        return self.retweetUser != None

    def datetime(self):
        return datetime.fromtimestamp(self.timestamp)

class CrossrefDataPoint:
    def __init__(self, crossrefData):
        self.timestamp = crossrefData[0]
        self.totalCitations = crossrefData[1]

    def datetime(self):
        return datetime.fromtimestamp(self.timestamp)

class Crossref:
    def __init__(self, crossrefData):
        self.doi = crossrefData[0]
        self.issn = crossrefData[1]
        self.publication_type = crossrefData[2]

"""
    User data structure:
        [  [0]             [1]         [2]        [3]             [4]            [5]           [6]   ]
        [twitterId, twitterScreenname, name, followersCount, statusesCount, friendsCount, listedCount]
"""
class User:
    usersFilename = "twitterUsers.json"
    usersPath = path.join(dataBasePath, usersFilename)
    userdata = None
    twitterName2UserMap = None
    twitterName2NumTweetsInCorpus = None
    usernamesInCorpus = None

    def __init__(self, userdata):
        self.twitterId = userdata[0]
        self.twitterName = userdata[1]
        self.verboseName = userdata[2]
        self.numFollowers = userdata[3]
        self.numTweetsPosted = userdata[4]
        self.numFriends = userdata[5]
        self.listedCount = userdata[6]

    def numTweetsInCorpus(self):
        if User.twitterName2NumTweetsInCorpus is None:
            User.twitterName2NumTweetsInCorpus = { }
            for doc in SimpleDoc.getall():
                for tweet in doc.tweets:
                    User.twitterName2NumTweetsInCorpus[tweet.username] = User.twitterName2NumTweetsInCorpus.get(tweet.username, 0) + 1

        return User.twitterName2NumTweetsInCorpus[self.twitterName]

    def weight(self, method = "followers"):
        if method == "followers":
            return self.numFollowers
        else:
            raise ValueError("Method " + method + " for user weighting is not valid")

    @staticmethod
    def getall():
        if User.userdata is None:
            User.userdata = User.readUserdata()
        return User.userdata

    @staticmethod
    def allUsernamesInCorpus():
        if User.usernamesInCorpus is None:
            User.usernamesInCorpus = set()
            for doc in SimpleDoc.getall():
                for tweet in doc.tweets:
                    User.usernamesInCorpus.add(tweet.username)

        return User.usernamesInCorpus

    @staticmethod
    def readUserdata():
        lines = open(User.usersPath)
        users = [User(json.loads(line)) for line in lines]
        return users

    @staticmethod
    def findByTwitterName(username):
        if User.twitterName2UserMap is None:
            User.twitterName2UserMap = {}

            for user in User.getall():
                User.twitterName2UserMap[user.twitterName] = user

        return User.twitterName2UserMap.get(username, None)

class Sentiment:
    def __init__(self, ident, classification):
        self.id_tweetTimestamp = ident[0]
        self.id_tweetUser = ident[1]
        self.id_docDoi = ident[2]
        self.classification = classification

    def ident(self):
        return (self.id_tweetTimestamp, self.id_tweetUser, self.id_docDoi)

    def asJsonString(self):
        return json.dumps([self.id_tweetTimestamp, self.id_tweetUser, self.id_docDoi, self.classification])

    def doc(self):
        return SimpleDoc.findByDoi(self.id_docDoi)

    @classmethod
    def openFile(cls, filename):
        l = cls.fromFile(filename)
        Sentiment.openFilename = filename
        Sentiments.allSentiments = l

    @classmethod
    def fromFile(cls, filename):
        l = [ ]
        lines = open(filename, "r")

        for line in lines:
            jsonArray = json.loads(line)

            ident = (jsonArray[0], jsonArray[1], jsonArray[2])
            classification = jsonArray[3]

            l.append(Sentiment(ident, classification))

        lines.close()
        return l

    @classmethod
    def append(cls, ident, classification):
        s = Sentiment(ident, classification)
        Sentiment.allSentiments.append(s)

        if Sentiment.openFilename != None:
            f = open(Sentiment.openFilename, "a")
            f.write(s.asJsonString()+"\n")
            f.close()

    @classmethod
    def sentimentAvailable(ident):
        for Sentiment.availableSentiment in Sentiment.availableSentiments:
            if availableSentiment.ident() == ident:
                return True

        return False

Sentiment.openFilename = None
Sentiment.allSentiments = [ ]

class DocumentTimelines:
    """[ doi, citeULikeTimeline, pubmedTimeline, scopusTimeline, pmcTimeline, pmcEvents, facebookTimeline, 
    mendeleyTimeline, crossrefTimeline, counterTimeline, counterEvents, relativemetricTimeline ]"""

    def __init__(self, doi, publicationTimestamp, citeULikeTimeline, pubmedTimeline, scopusTimeline, pmcTimeline, pmcEvents, facebookTimeline,
        mendeleyTimeline, crossrefTimeline, counterTimeline, counterEvents, relativemetricTimeline):
        self.doi = doi
        self.publicationTimestamp = publicationTimestamp
        self.citeULikeTimeline = citeULikeTimeline
        self.pubmedTimeline = pubmedTimeline
        self.scopusTimeline = scopusTimeline
        self.pmcTimeline = pmcTimeline
        self.pmcEvents = pmcEvents
        self.facebookTimeline = DocumentTimelines.repairTwitterTimeline(facebookTimeline) # facebookTimeline
        self.mendeleyTimeline = mendeleyTimeline
        self.crossrefTimeline = crossrefTimeline
        self.counterTimeline = counterTimeline
        self.counterEvents = counterEvents
        self.relativemetricTimeline = relativemetricTimeline

    @classmethod
    def fromJsonArr(cls, data, trimmed=False, sort=True):
        if trimmed:
            if sort:
                return cls(data[0], data[1], sorted(data[2], key=lambda x: x[0]), 
                    sorted(data[3], key=lambda x: x[0]), sorted(data[4], key=lambda x: x[0]), 
                    sorted(data[5], key=lambda x: x[0]), None, sorted(data[6], key=lambda x: x[0]), 
                    sorted(data[7], key=lambda x: x[0]), sorted(data[8], key=lambda x: x[0]), 
                    sorted(data[9], key=lambda x: x[0]), None, sorted(data[10], key=lambda x: x[0]))
            else:
                return cls(data[0], data[1], data[2], data[3], data[4], data[5], None,
                    data[6], data[7], data[8], data[9], None, data[10])
        else:
            if sort:
                return cls(data[0], data[1], sorted(data[2], key=lambda x: x[0]), 
                    sorted(data[3], key=lambda x: x[0]), sorted(data[4], key=lambda x: x[0]),
                    sorted(data[5], key=lambda x: x[0]), data[6], sorted(data[7], key=lambda x: x[0]), 
                    sorted(data[8], key=lambda x: x[0]), sorted(data[9], key=lambda x: x[0]), 
                    sorted(data[10], key=lambda x: x[0]), data[11], sorted(data[12], key=lambda x: x[0]))
            else:
                return cls(*data)

    @classmethod
    def fromFile(cls, filename, trimmed=False, sort=True):
        lines = open(filename, "r")
        return [ DocumentTimelines.fromJsonArr(json.loads(line), trimmed, sort) for line in lines ]

    @classmethod
    def trimTimeline(cls, timeline):
        newTimeline = []

        if len(timeline) != 0:
            newTimeline.append(timeline[0])
            for i in range(1, len(timeline)-1):
                if not (timeline[i-1][1] == timeline[i][1] and timeline[i][1] == timeline[i+1][1]):
                    newTimeline.append(timeline[i])
            if len(timeline) != 1:
                newTimeline.append(timeline[-1])

        return newTimeline

    @classmethod
    def valueAtTime(cls, sortedTimeline, time, tolerance):
        # cant say anything if timeline is empty
        if len(sortedTimeline) == 0:
            return None, 0

        # if one point happens to match exactly, return that value
        for point in sortedTimeline:
            if point[0] == time:
                return point[1], 1

        firstTimestamp = sortedTimeline[0][0]
        lastTimestamp = sortedTimeline[-1][0]

        if time < firstTimestamp:
            if time+tolerance >= firstTimestamp:
                return sortedTimeline[0][1], 2
            elif sortedTimeline[0][1] == 0:
                return 0, 3
            else:
                return None, 4
        elif time > lastTimestamp:
            if time-tolerance <= firstTimestamp:
                return sortedTimeline[-1][1], 5
            else:
                return None, 6
        else:
            ind = 0
            while sortedTimeline[ind][0]<time: # cannot go out of bounds because time must be smaller than the last point in time
                ind += 1

            pointBeforeTime = sortedTimeline[ind-1]
            pointAfterTime = sortedTimeline[ind]

            if pointBeforeTime[1] == pointAfterTime[1]:
                return pointBeforeTime[1], 7
            else:
                diffToBefore = time-pointBeforeTime[0]
                diffToAfter = pointAfterTime[0]-time

                if diffToBefore <= diffToAfter: # and diffToBefore <= tolerance:
                    return pointBeforeTime[1], 8
                elif diffToAfter < diffToBefore: # and diffToAfter <= tolerance:
                    return pointAfterTime[1], 9
                # elif pointBeforeTime[1] == 0 and pointAfterTime[1] < 5:
                #     return pointAfterTime[1] / 2, 10
                else:
                    # f = interpolate.interp1d(map(lambda x: x[0], timeline), map(lambda x: x[1], timeline))

                    # if pointBeforeTime[1] == 0 and pointAfterTime[1] >= 5:
                    #     return None, 11

                    # diff = float(pointAfterTime[1]) / pointBeforeTime[1]
                    return None, 13
                    #return (float(pointAfterTime[1]) + pointBeforeTime[1])/2, 12
                    """if diff < 1.1:
                        return (float(pointBeforeTime[1]) + pointAfterTime[1]) / 2, 12
                    else:
                        return None, 13"""

    @classmethod
    def repairTwitterTimeline(cls, timeline):
        decreaseIndex = None

        for ind in range(0, len(timeline)-1):
            if timeline[ind][1] >= 1.5*timeline[ind+1][1]:
                decreaseIndex = ind
                break

        if decreaseIndex != None:
            lastHighIncreaseIndex = None
            for ind in range(0, decreaseIndex):
                if timeline[ind][1]*3 <= timeline[ind+1][1]:
                    lastHighIncreaseIndex = ind+1

            newTimeline = []
            for ind in range(0, len(timeline)):
                decrease = ((not decreaseIndex or ind <= decreaseIndex) and (not lastHighIncreaseIndex or ind >= lastHighIncreaseIndex))
                if decrease:
                    newTimeline.append([timeline[ind][0], timeline[ind][1]/3])
                else:
                    newTimeline.append(timeline[ind])
            return newTimeline
        return timeline

    def trimmed(self):
        return DocumentTimelines(
            self.doi,
            self.publicationTimestamp,
            DocumentTimelines.trimTimeline(self.citeULikeTimeline), 
            DocumentTimelines.trimTimeline(self.pubmedTimeline), 
            DocumentTimelines.trimTimeline(self.scopusTimeline), 
            DocumentTimelines.trimTimeline(self.pmcTimeline), 
            self.pmcEvents, 
            DocumentTimelines.trimTimeline(self.facebookTimeline),
            DocumentTimelines.trimTimeline(self.mendeleyTimeline), 
            DocumentTimelines.trimTimeline(self.crossrefTimeline), 
            DocumentTimelines.trimTimeline(self.counterTimeline), 
            self.counterEvents, 
            DocumentTimelines.trimTimeline(self.relativemetricTimeline)
        )

    def toJson(self, trimmed=False):
        if trimmed:
            return json.dumps([ self.doi, self.publicationTimestamp, self.citeULikeTimeline, 
                self.pubmedTimeline, self.scopusTimeline, self.pmcTimeline, 
                self.facebookTimeline, self.mendeleyTimeline, self.crossrefTimeline, 
                self.counterTimeline, self.relativemetricTimeline ])
        else:
            return json.dumps([ self.doi, self.publicationTimestamp, self.citeULikeTimeline, 
                self.pubmedTimeline, self.scopusTimeline, self.pmcTimeline, self.pmcEvents, 
                self.facebookTimeline, self.mendeleyTimeline, self.crossrefTimeline, 
                self.counterTimeline, self.counterEvents, self.relativemetricTimeline ])

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

    tau, pValue1 = stats.kendalltau(identsByX2, identsByY2)
    r, pValue2 = stats.spearmanr(identsByX2, identsByY2)

    return tau, pValue1, r, pValue2

def pearsonCorrelation(x, y):
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

    return sumErrorProducts / math.sqrt(xSquareError*ySquareError)

def allCorrelations(x, y):
    kendall, p1, spearman, p2 = rankCorrelation(x, y)
    pearson = pearsonCorrelation(x, y)

    return pearson, kendall, spearman

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