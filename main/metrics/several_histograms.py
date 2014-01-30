import matplotlib.pyplot as plt
from main.util.common import simpleDocs, dataPath, figurePath, groupCount, writeJsonToData, readJsonFromData, formatHist
from matplotlib import ticker
from main.util.plotting import histDisc, hist, barPlot, pieData
import numpy
import itertools
from main.util.tex import simpleTabular, compileTex
import os
import math
import itertools

def publication_years():
    plt.figure()

    publicationYears = list(simpleDoc.publicationDatetime().timetuple()[0] for simpleDoc in simpleDocs())
    histDisc(plt, publicationYears)
    plt.savefig(figurePath("publication_years.png"))
    plt.show()

def distFirstTweetToDoc():
    diffs = []
    for doc in filter(lambda doc: len(doc.tweets) != 0 and len(doc.tweets) < 5, simpleDocs()):
        pubTimestamp = doc.publicationTimestamp
        # firstTweetTimestamp = max([tweet.timestamp for tweet in doc.tweets])
        diffs.extend([tweet.timestamp-pubTimestamp for tweet in doc.tweets])

    diffs = map(lambda x: x/60/60/24, diffs)

    """relBins1, labels1 = pieData([
        [lambda x: x<=7, "1W"],
        [lambda x: x>7 and x<=30, "1M"],
        [lambda x: x>30 and x<=160, "1/2Y"],
        [lambda x: x>160 and x<=365, "1Y"],
        [lambda x: x>365, ">1Y"],
    ], diffs1)"""
    
    relBins, labels = pieData([
        [lambda x: x<=1, "1T"],
        [lambda x: x>1 and x<=2, "2T"],
        [lambda x: x>2 and x<=3, "3T"],
        [lambda x: x>3 and x<=4, "4T"],
        [lambda x: x>4 and x<=5, "5T"],
        [lambda x: x>5 and x<=6, "6T"],
        [lambda x: x>6 and x<=7, "7T"],
        [lambda x: x>7 and x<=8, "8T"],
        [lambda x: x>8 and x<=9, "9T"],
        [lambda x: x>9 and x<=10, "10T"],
        [lambda x: x>10 and x<=11, "11T"],
        [lambda x: x>11 and x<=12, "12T"],
        [lambda x: x>12 and x<=13, "13T"],
        [lambda x: x>13 and x<=14, "14T"],
        [lambda x: x>14 and x<=15, "15T"],
        [lambda x: x>15 and x<=16, "16T"],
        [lambda x: x>16 and x<=17, "17T"],
        [lambda x: x>17 and x<=18, "18T"],
        [lambda x: x>18 and x<=19, "19T"],
        [lambda x: x>19 and x<=20, "20T"],
        [lambda x: x>20 and x<=21, "21T"],
        [lambda x: x>21 and x<=22, "22T"],
        [lambda x: x>22 and x<=23, "23T"],
        [lambda x: x>23 and x<=24, "24T"],
        [lambda x: x>24 and x<=25, "25T"],
        [lambda x: x>25 and x<=26, "26T"],
        [lambda x: x>26 and x<=27, "27T"],
        [lambda x: x>27 and x<=28, "28T"],
        [lambda x: x>28 and x<=29, "29T"],
        [lambda x: x>29 and x<=30, "30T"],
        [lambda x: x>30, ">30T"]
    ], diffs)


    plt.figure()
    plt.pie(relBins, autopct='%1.1f%%', 
        startangle=90, labels=labels)
    plt.show()


def numTweets():
    plt.figure()
    
    numTweets = list(len(simpleDoc.tweets) for simpleDoc in simpleDocs())
    labels, values = hist(numTweets, [1, 2, 5, 10, 20, 50, 100, 500, 1000])
    barPlot(plt, labels, values)
    plt.show()

def userHist():
    plt.figure()

    users = []
    for doc in simpleDocs():
        for tweet in doc.tweets:
            users.append(tweet.user)

    userGroupCounts = sorted(groupCount(users), key=lambda x: x[1], reverse=True)
    filteredUserGroupCounts = filter(lambda x: x[1]>=2, userGroupCounts)

    plt.plot(map(lambda x: x[1], filteredUserGroupCounts), range(1, len(filteredUserGroupCounts)+1))
    plt.title("Users sortiert nach Tweets (1er User abgeschnitten)")
    plt.xlabel("Rang des Users")
    plt.ylabel("#Tweets")
    plt.show()

def topUsers():
    plt.figure()

    users = []
    for doc in simpleDocs():
        for tweet in doc.tweets:
            users.append(tweet.user)

    userGroupCounts = sorted(groupCount(users), key=lambda x: x[1], reverse=True)
    topUsers = userGroupCounts[:10]

    users, values = zip(*topUsers)

    barPlot(plt, list(users), list(values))
    plt.title("Top 10 Users")
    plt.ylabel("#Tweets")
    plt.show()

def numRetweets():
    numNormalTweets = 0
    numRetweets = 0

    for doc in simpleDocs():
        for tweet in doc.tweets:
            if(tweet.isRetweet()):
                numRetweets += 1
            else:
                numNormalTweets += 1

    relNormalTweets, relRetweets = float(numNormalTweets)*100 / (numNormalTweets+numRetweets), float(numRetweets)*100 / (numNormalTweets+numRetweets)

    plt.figure()
    plt.pie([relNormalTweets, relRetweets], autopct='%1.1f%%', 
        startangle=90, labels=[
            'normale Tweets (' + str(numNormalTweets) + ')', 
            'Retweets (' + str(numRetweets) + ')'
        ], colors=['green', 'yellow'])

    plt.show()

def removeDoubleUsersAbsolute():
    l = [ ]

    for doc in simpleDocs():
        tweetUsers = map(lambda x: x.user, doc.tweets)
        if len(tweetUsers) >= 1:
            l.append([len(tweetUsers), len(set(tweetUsers))])

    diffs = map(lambda x: x[0]-x[1], l)

    """relBins, labels = pieData([
        [lambda x: x==0, "diff: 0"], 
        [lambda x: x==1, "diff: 1"],
        [lambda x: x>=2 and x <= 5, "diff: 2-5"],
        [lambda x: x>5, "diff: >5"]
    ], diffs)"""

    relBins, labels = pieData([
        [lambda x: x>=6 and x<=10, "diff: 5-10"],
        [lambda x: x>=11 and x<=50, "diff: 11-50"],
        [lambda x: x>=51 and x<=300, "diff: 51-300"]
    ], diffs)

    plt.figure()
    plt.pie(relBins, autopct='%1.1f%%', 
        startangle=90, labels=labels)

    plt.title("Differenzen in Anzahl Tweets zu Dokument, wenn doppelte Benutzer entfernt werden.")
    plt.show()

def removeDoubleUsersRelative():
    l = [ ]

    for doc in simpleDocs():
        tweetUsers = map(lambda x: x.user, doc.tweets)
        if len(tweetUsers) >= 1:
            l.append([len(tweetUsers), len(set(tweetUsers))])

    diffs = map(lambda x: float(x[0]-x[1])/x[0], l)

    relBins, labels = pieData([
        [lambda x: x==0.0, "0%"], 
        [lambda x: x>0.0 and x<=10.0, "0%<d<=10%"],
        [lambda x: x>0.1 and x<=0.3, "10%<d<=30%"],
        [lambda x: x>0.3, ">30%"]
    ], diffs)

    plt.figure()
    plt.pie(relBins, autopct='%1.1f%%', 
        startangle=90, labels=labels)

    plt.title("Differenzen in Anzahl Tweets zu Dokument, wenn doppelte Benutzer entfernt werden.")
    plt.show()

def removeRetweetsAbsolute():
    l = [ ]

    for doc in simpleDocs():
        if len(doc.tweets) >= 1:
            numNormalTweets = sum(1 for tweet in doc.tweets if not tweet.isRetweet())
            numRetweets = sum(1 for tweet in doc.tweets if tweet.isRetweet())

            l.append([numNormalTweets, numRetweets])

    diffs = map(lambda x: x[0]-x[1], l)

    """relBins, labels = pieData([
        [lambda x: x==0, "diff: 0"], 
        [lambda x: x==1, "diff: 1"],
        [lambda x: x>=2 and x <= 5, "diff: 2-5"],
        [lambda x: x>5, "diff: >5"]
    ], diffs)"""

    relBins, labels = pieData([
        [lambda x: x>=6 and x <=10, "diff: 6-10"],
        [lambda x: x>=11 and x <=50, "diff: 11-50"],
        [lambda x: x>51, "diff: >51"]
    ], diffs)

    plt.figure()
    plt.pie(relBins, autopct='%1.1f%%', 
        startangle=90, labels=labels)

    plt.title("Differenzen in Anzahl Tweets zu Dokument, wenn Retweets entfernt werden.")
    plt.show()

def removeRetweetsRelative():
    l = [ ]

    for doc in simpleDocs():
        if len(doc.tweets) >= 1:
            numNormalTweets = sum(1 for tweet in doc.tweets if not tweet.isRetweet())
            numRetweets = sum(1 for tweet in doc.tweets if tweet.isRetweet())

            l.append([numNormalTweets+numRetweets, numNormalTweets])

    diffs = map(lambda x: float(x[0]-x[1])/x[0], l)

    relBins, labels = pieData([
        [lambda x: x==0.0, "0%"], 
        [lambda x: x>0.0 and x<=0.3, "0%<d<=30%"],
        [lambda x: x>0.3 and x<=0.5, "30%<d<=50%"],
        [lambda x: x>0.5, ">50%"]
    ], diffs)

    plt.figure()
    plt.pie(relBins, autopct='%1.1f%%', 
        startangle=90, labels=labels)

    plt.title("Differenzen in Prozent, Retweets entfernt werden")
    plt.show()

def mendeleyDisciplines():
    l = [ ]

    totaldocs = 0
    for doc in simpleDocs():
        totaldocs += 1
        if doc.mendeleyDisciplines:
            for d in doc.mendeleyDisciplines:
                l.append(d)

    discSorted = sorted(groupCount(l), key=lambda x: x[1], reverse=True)
    discSorted2 = map(lambda x: [x[0], x[1], ("%2.2f" % (float(x[1])*100/totaldocs)) + "\\%"], discSorted)

    compileTex(
        simpleTabular(["Disziplin", "\\#Dokumente", "Anteil"], discSorted2, orientation="lrr"),
        figurePath("mendeleyDisciplines.pdf")
    )

def crossrefVsTwitter(yearBounds = [None, None], maxTweets = 300, maxCitations = 300):
    tweetVsCitationList = []

    totalDocs = 0
    for doc in filter(lambda doc: 
        (not yearBounds[0] or doc.publicationDatetime().year>=yearBounds[0]) and 
            (not yearBounds[1] or doc.publicationDatetime().year<=yearBounds[1]), 
        simpleDocs()
    ):
        tweetVsCitationList.append([len(doc.tweets), doc.citationTimeline[0].totalCitations])
        totalDocs += 1

    x, y = zip(*filter(lambda x: x[1]>0 and x[1]<maxCitations and x[0]>0 and x[0]<maxTweets, tweetVsCitationList))
    plt.figure()
    plt.scatter(x, y)
    plt.title("Korrelation zwischen Tweets und Zitationen (Papieren zwischen " + str(yearBounds[0]) + " und " + str(yearBounds[1]) + "; #Docs: " + str(totalDocs) + ")")
    plt.ylabel("#Tweets (1-" + str(maxTweets) + ")")
    plt.xlabel("#Citations (1-" + str(maxCitations) + ")")

    p = numpy.polyfit(x, y, 1)
    xTrend = range(min(x), max(x)+1)
    yTrend = map(lambda x: numpy.polyval(p, x), xTrend)
    plt.plot(xTrend, yTrend, color='r')

    plt.figtext(0.80, 0.05,  'korrelationskoeffizient: ' + str(korrelationskoeffizient(x, y)))

    plt.show()

def tweetVsMendeleyReaders(yearBounds = [None, None], maxTweets = 300, maxReaders = 300):
    tweetVsMendeleyReaderList = []

    totalDocs = 0
    for doc in filter(lambda doc: 
        (doc.mendeleyReaders != None and doc.mendeleyReaders<=maxReaders) and 
            (doc.tweets != None and len(doc.tweets)<=maxTweets) and
            (not yearBounds[0] or doc.publicationDatetime().year>=yearBounds[0]) and
            (not yearBounds[1] or doc.publicationDatetime().year<=yearBounds[1]), 
        simpleDocs()
    ):
        tweetVsMendeleyReaderList.append([len(doc.tweets), doc.mendeleyReaders])
        totalDocs += 1

    x, y = zip(*tweetVsMendeleyReaderList)
    

    plt.figure()

    plt.scatter(x, y)
    plt.title("Korrelation zwischen Tweets und Zitationen (Papieren zwischen " + str(yearBounds[0]) + " und " + str(yearBounds[1]) + "; #Docs: " + str(totalDocs) + ")")
    plt.ylabel("#Tweets (1-" + str(maxTweets) + ")")
    plt.xlabel("#Readers (1-" + str(maxReaders) + ")")

    p = numpy.polyfit(x, y, 1)
    xTrend = range(min(x), max(x)+1)
    yTrend = map(lambda x: numpy.polyval(p, x), xTrend)
    plt.plot(xTrend, yTrend, color='r')

    plt.figtext(0.80, 0.05,  'korrelationskoeffizient: ' + str(korrelationskoeffizient(x, y)))

    plt.show()

def userCorrelationToDiscipline():
    """
    zuerst user_disc_map erstellen:
    [ user1 : [ 
        [mendDisc1_1, mendDisc1_2, ...], // Liste von Disziplinen pro Tweet des Nutzers
        [mendDisc2_1, mendDisc2_2, ...]
    ], user2: [
        ...
    ] ]
    """
    if not os.path.isfile(dataPath("user_disc_map.json")):
        userDiscList = []

        for doc in simpleDocs():
            twitterUsers = [tweet.user for tweet in doc.tweets]
            disciplines = doc.mendeleyDisciplines
            if len(twitterUsers)!=0 and disciplines!=None and len(disciplines)!=0:
                for twitterUser in twitterUsers:
                    userDiscList.append([twitterUser, disciplines])
        
        userDiscMap = {}
        for item in userDiscList:
            discList = userDiscMap.get(item[0], [])
            discList.append(item[1])
            userDiscMap[item[0]] = discList

        writeJsonToData(userDiscMap, "user_disc_map.json")
    else:
        userDiscMap = readJsonFromData("user_disc_map.json")


    """
    dann "user_disc_count_map" erstellen:
    [ user1 : { 
        "total_posts" : n,
        "user_posts_in_desc" : {
            "disc1" : n_1,
            "disc2" : n_2, 
            ...
        }
    }, user2: {
        ...
    } ]
    """
    if not os.path.isfile(dataPath("user_disc_count_map.json")):
        userDiscCountMap = { }
        for user, descListList in userDiscMap.items():
            totalPosts = len(descListList)
            allUsersDesc = set()
            for descList in descListList:
                allUsersDesc |= set(descList)

            userPostsInDesc = { }
            for desc in allUsersDesc:
                postsInDesc = sum(1 for descList in descListList if desc in descList)
                userPostsInDesc[desc] = postsInDesc

            userDiscCountMap[user] = { "total_posts" : totalPosts, "user_posts_in_desc" : userPostsInDesc }

        writeJsonToData(userDiscCountMap, "user_disc_count_map.json")
    else:
        userDiscCountMap = readJsonFromData("user_disc_count_map.json")

    for user, userdata in userDiscCountMap.items():
        totalPosts = userdata['total_posts']

        relCounts = []
        for desc, count in userdata['user_posts_in_desc'].items():
            relCounts.append([desc, float(count)/totalPosts])

        relCounts = sorted(relCounts, key=lambda x: x[1], reverse=True)

        if totalPosts > 50:
            print user
            print relCounts
            print "\n\n"

def korrelationskoeffizient(x, y):
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

def correlationsForQuartals():
    quartals = [
        [3, 2008],
        [0, 2009], [1, 2009], [2, 2009], [3, 2009],
        [0, 2010], [1, 2010], [2, 2010], [3, 2010],
        [0, 2011], [1, 2011], [2, 2011], [3, 2011],
        [0, 2012], [1, 2012], [2, 2012], [3, 2012],
        [0, 2013], [1, 2013]
    ]

    def docInQuartal(doc, quartal):
        if quartal[1] != doc.publicationDatetime().year:
            return False
        elif quartal[0] == 0:
            return doc.publicationDatetime().month >=1 and doc.publicationDatetime().month<=3
        elif quartal[0] == 1:
            return doc.publicationDatetime().month >=4 and doc.publicationDatetime().month<=6
        elif quartal[0] == 2:
            return doc.publicationDatetime().month >=7 and doc.publicationDatetime().month<=9
        elif quartal[0] == 3:
            return doc.publicationDatetime().month >=10 and doc.publicationDatetime().month<=12
        else:
            raise ValueError("Argument quartal consists of a tuple [quartal, year] where quartal must be between 0 and 3")

    allDocs = list(simpleDocs())
    coefficients = []
    for quartal in quartals:
        docs = filter(lambda doc: docInQuartal(doc, quartal) and doc.mendeleyReaders != None, allDocs)
        print len(docs)
        x, y = zip(*map(lambda doc: [len(doc.tweets), doc.citationTimeline[0].totalCitations], docs))

        coefficients.append(korrelationskoeffizient(x, y))

    plt.figure()
    plt.plot(range(0, len(quartals)), coefficients)
    plt.show()

def correlationTimeTweets():
    x, y = zip(*map(lambda doc: [doc.publicationTimestamp, len(doc.tweets)], simpleDocs()))
    print korrelationskoeffizient(x, y) # 0.082


def alteringTweetStreamAfterFirstPeak():
    return False
    # return False

def cummulativeTwitterPlots():
    # twitterTimelines, publicationTimestamps = zip(*filter(lambda timelinePubTs: len(timelinePubTs[0]) != 0, map(lambda doc: [doc.cummulativeTwitterTimeline(), doc.publicationTimestamp], simpleDocs())))
    twitterTimelines = filter(lambda tl: len(tl) != 0, map(lambda doc: map(lambda point: [point[0]-doc.publicationTimestamp, point[1]], doc.cummulativeTwitterTimeline()), simpleDocs()))

    # twitterTimelines = filter(lambda tl: len(tl) < 20, twitterTimelines)
    # twitterTimelines = filter(lambda tl: len(tl) > 50, twitterTimelines)
    plt.figure()
    for timeline in twitterTimelines:
        x, y = zip(*timeline)
        plt.plot(x, y)
    
    plt.show()

