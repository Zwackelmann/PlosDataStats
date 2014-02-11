import json
import os
from os import path
from datetime import datetime
import string 
import numpy

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
        raise BaseException

simpleDocsFilename = "relevant_document_data.json"
simpleDocsPath = path.join(dataBasePath, simpleDocsFilename)
def doForEachSimpleDoc(fun, maxDocs=None):
    """Document Structure:
        [[0]   [1]     [2]        [3]            [4]            [5]              [6]                  [7]        [8]    [9]    [10]     [11]      [12]   ]
        [doi, title, pubDate, twitterData, citationTimeline, citations, mendeleyDisciplineList, mendeleyReaders, issn, issue, volume, pdfViews, htmlViews]

        twitterData:
                     [      [0]      [1]                 [2]                         [3]    ]
            list of: [ "tweet text", user, retweetUser (None, wenn kein retweet), zeitpunkt ]

        citationTimeline:
                     [    [0]           [1]      ]
            list of: [ zeitpunkt, totalCitations ]

        citations:
                     [[0]   [1]         [2]      ]
            list of: [doi, issn, publication_type]
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

def readIssnData():
    issnToImpactRaw = readJsonFromData("issn_impact.json")
    
    issnToImpact = { }
    for key, value in issnToImpactRaw.items():
        issnToImpact[filter(lambda c: c in string.digits, key)] = value
    
    return issnToImpact

def filterDigits(s):
    return filter(lambda c: c in string.digits, s)

class SimpleDoc:
    maximumTimestampInDataset = 1379408980
    corpus = None

    def __init__(self, docData):
        self.doi = docData[0]
        self.title = docData[1]
        self.publicationTimestamp = docData[2]
        self.tweets = map(lambda tweetData: Tweet(tweetData), docData[3])
        # TODO check if tweets are sorted in time and sort if not
        self.citationTimeline = map(lambda citationData: CitationDataPoint(citationData), docData[4])
        # TODO check if citationTimeline are sorted in time and sort if not
        self.citations = map(lambda citationData: Citation(citationData), docData[5])
        self.mendeleyDisciplines = docData[6]
        self.mendeleyReaders = docData[7]
        self.issn = docData[8]
        self.issue = docData[9]
        self.volume = docData[10]
        self.pdfViews = docData[11]
        self.htmlViews = docData[12]

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

    def numCitations(self):
        return max(map(lambda c: c.totalCitations, self.citationTimeline))

    def timespan(self):
        timestamps = map(lambda tweet: tweet.timestamp, self.tweets)
        return max(timestamps) - min(timestamps)

    def age(self):
        return SimpleDoc.maximumTimestampInDataset-self.publicationTimestamp

    def year(self):
        return self.publicationDatetime().year

    def month(self):
        return self.publicationDatetime().month

    def totalViews(self):
        return self.htmlViews + self.pdfViews

    def citationWeight(self, method = "sum"):
        ifs = []
        for citation in self.citations:
            if type(citation.issn) is list:
                ifs.append(max(map(lambda issn: SimpleDoc.issnToImpact.get(filterDigits(issn), 0.0), citation.issn)))
            elif type(citation.issn) is unicode:
                ifs.append(SimpleDoc.issnToImpact.get(filterDigits(citation.issn), 0.0))
            elif citation.issn is None:
                ifs.append(None)
            else:
                raise ValueError("citation issns is neither a list nor a string but " + str(type(citation.issn)))

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
            raise ValueError(method + " is no valid method for citation weighting")

    issnToImpact = readIssnData()

    @staticmethod
    def getall():
        if SimpleDoc.corpus is None:
            SimpleDoc.corpus = SimpleDoc.readCorpus()
        return SimpleDoc.corpus

    @staticmethod
    def readCorpus():
        lines = open(simpleDocsPath)
        return [SimpleDoc(json.loads(line)) for line in lines]

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

class CitationDataPoint:
    def __init__(self, citationData):
        self.timestamp = citationData[0]
        self.totalCitations = citationData[1]

    def datetime(self):
        return datetime.fromtimestamp(self.timestamp)

class Citation:
    def __init__(self, citationData):
        self.doi = citationData[0]
        self.issn = citationData[1]
        self.publication_type = citationData[2]

def twitterHorizonDocs():
    return filter(
        lambda doc: 
            (doc.publicationDatetime().year==2012 and 
            doc.publicationDatetime().month>=6 and doc.publicationDatetime().month<=8),
        SimpleDoc.getall()
    )

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
