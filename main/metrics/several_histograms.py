import matplotlib.pyplot as plt
from main.util.common import dataPath, figurePath, groupCount, writeJsonToData, readJsonFromData, formatHist, twitterHorizonDocs, User, SimpleDoc, allCorrelations
from matplotlib import ticker
from main.util.plotting import histDisc, hist, barPlot, pieData, paperFigure
import numpy
import scipy as sp
import itertools
from main.util.tex import simpleTabular, compileTex
import os
import math
import itertools
import random
import json

def publication_years():
    plt.figure(num=None, figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')
    publicationYears = list(simpleDoc.publicationDatetime().year for simpleDoc in SimpleDoc.getallBetween(None, None))
    histDisc(plt, publicationYears, width = 0.5)
    # plt.savefig(figurePath("publication_years.png"))
    plt.tight_layout()
    plt.show()

def distFirstTweetToDoc():
    allDocs = list(SimpleDoc.getall())

    for param in range(20, 100):
        diffs = []

        maximumTweetAge = 60*60*24*param
        minimumTweetAge = 60*60*24*10
        for doc in filter(lambda doc: len(doc.tweets) != 0 and doc.age() >= maximumTweetAge, allDocs):
            pubTimestamp = doc.publicationTimestamp
            # firstTweetTimestamp = max([tweet.timestamp for tweet in doc.tweets])
            diffs.extend([tweet.timestamp-pubTimestamp for tweet in 
                filter(
                    lambda tweet: (tweet.timestamp-doc.publicationTimestamp) < maximumTweetAge and (tweet.timestamp-doc.publicationTimestamp) > minimumTweetAge,
                    doc.tweets
                )
            ])

        maxBins = 30
        timeslot = (float(maximumTweetAge)-float(minimumTweetAge))/maxBins

        def binNr2Bound(binNr):
            return minimumTweetAge+(binNr*timeslot)

        binConditions = map(
            lambda binNr: [lambda x: x>binNr2Bound(binNr) and x<=binNr2Bound(binNr+1), str(binNr) + "X"],
            range(0, maxBins)
        )

        # binConditions.append([lambda x: x>binNr2Bound(maxBins), ">" + str(maxBins-1) + str("X")])

        diffBins, diffLabels = pieData(binConditions, diffs)
        
        distBinConditions = map(
            lambda binNr: [lambda x: x==binNr, "X=" + str(binNr)],
            range(0, maxBins)
        )

        def getBins(beta, binConditions):
            s = map(lambda x: int(x), numpy.random.exponential(beta, 10000))
            bins, labels = pieData(binConditions, s)
            return bins

        def binDiffs(bins1, bins2):
            return sum(map((lambda (a, b): abs(a-b)), zip(bins1, bins2)))

        def searchInRangeRec(minBeta, maxBeta, steps, depth, maxDepth):
            minError = min(
                map(lambda beta: [beta, binDiffs(getBins(beta, distBinConditions), diffBins)], numpy.arange(minBeta, maxBeta, steps)),
                key = lambda x: x[1]
            )

            errorBelow = binDiffs(getBins(minError[0]-(float(steps)/2), distBinConditions), diffBins)
            errorAbove = binDiffs(getBins(minError[0]+(float(steps)/2), distBinConditions), diffBins)

            if depth==maxDepth:
                return minError
            elif errorBelow <= errorAbove:
                x = searchInRangeRec(minError[0]-steps, minError[0], float(steps)/10, depth+1, maxDepth)
                return x[0], x[1]
            else:
                x = searchInRangeRec(minError[0], minError[0]+steps, float(steps)/10, depth+1, maxDepth)
                return x[0], x[1]

        beta, error = searchInRangeRec(1, 10, 1, 0, 3)

        print param, (error/maxBins)
    # s = numpy.random.poisson(1.2, 10000)
    # s = numpy.random.zipf(1.5, 10000)
    # f = 3.0
    # s = map(lambda x: (float(x)-(1+(random.random()/f)))*f, s)
    # s.extend([0] * (100*60))

    
    #binConditions2.append([lambda x: x>maxBins, ">" + str(maxBins-1) + str("X")])


    """expDistData = map(lambda x: int(x), numpy.random.exponential(beta, 10000))
    expDistBins, expDistLabels = pieData(distBinConditions, expDistData)

    plt.figure()
    plt.pie(diffBins, autopct='%1.1f%%', 
        startangle=90, labels=diffLabels)
    plt.figure()

    plt.pie(expDistBins, autopct='%1.1f%%', 
        startangle=90, labels=expDistLabels)
    plt.show()"""


def numTweets():
    plt.figure()
    
    numTweets = list(len(simpleDoc.tweets) for simpleDoc in SimpleDoc.getall())
    labels, values = hist(numTweets, [1, 2, 5, 10, 20, 50, 100, 500, 1000])
    barPlot(plt, labels, values)
    plt.show()

def userHist():
    plt.figure()

    users = []
    for doc in SimpleDoc.getall():
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
    for doc in SimpleDoc.getall():
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

    for doc in SimpleDoc.getall():
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

    for doc in SimpleDoc.getall():
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

    for doc in SimpleDoc.getall():
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

    for doc in SimpleDoc.getall():
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

    for doc in SimpleDoc.getall():
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
    def generalCondition(doc):
        time = doc.publicationDatetime()
        return ( 
                (time.year == 2012 and time.month >= 6 and time.month <= 8) or 
                (time.year > 2012) 
            ) and doc.mendeleyDisciplines != None

    def domainDocs(domain):
        return [doc for doc in consideredDocs if generalCondition(doc) and domain in doc.mendeleyDisciplines]

    consideredDocs = list(filter(lambda doc: generalCondition(doc), SimpleDoc.getall()))
    totalDocs = len(consideredDocs)

    distinctDomains = set()
    for doc in consideredDocs:
        distinctDomains |= set(doc.mendeleyDisciplines)

    domainData = []
    for domain in distinctDomains:
        d = domainDocs(domain)
        numDocs = len(d)
        meanTweets = numpy.mean([doc.numTweets() for doc in d])

        domainData.append((domain, numDocs, ("%2.2f" % (float(numDocs)*100 / totalDocs)) + "\\%", "%2.2f" % meanTweets ))

    domainDataSorted = sorted(domainData, key=lambda x: x[1], reverse=True)

    compileTex(
        simpleTabular(["Disziplin", "\\#Dokumente", "Anteil", "AvgTweets"], domainDataSorted, orientation="lrrr"),
        figurePath("mendeleyDisciplines2.pdf")
    )

def crossrefVsTwitter(yearBounds = [None, None], minTweetAge = None, maxTweetAge = None):
    tweetVsCitationList = []
    minTweetAge = 60*60*24*0
    maxTweetAge = 60*60*24*100

    totalDocs = 0
    totalTweets = 0
    nullWeights = 0
    nonNullWeights = 0
    for doc in filter(
        lambda doc: 
            (doc.publicationDatetime().year==2012 and 
            doc.publicationDatetime().month>=6 and doc.publicationDatetime().month<=8),
        SimpleDoc.getall()
    ):
        docsTweets = filter(lambda tweet: 
            (not minTweetAge or (tweet.timestamp-doc.publicationTimestamp) >= minTweetAge) and
            (not maxTweetAge or (tweet.timestamp-doc.publicationTimestamp) <= maxTweetAge), 
            doc.tweets)
        
        def userWeight(tweet):
            user = tweet.user()
            return None if user is None else user.weight()

        userWeights = map(lambda tweet: userWeight(tweet), docsTweets)

        nullWeights += sum((1 for weight in userWeights if weight is None))
        nonNullWeights += sum((1 for weight in userWeights if not weight is None))

        tweetVsCitationList.append([doc.numCitations(), 0 if len(userWeights) == 0 else sum(filter(lambda weight: weight != None, userWeights))])
        totalDocs += 1
        totalTweets += len(docsTweets)

    print totalDocs
    print totalTweets
    print float(nullWeights) / (nullWeights+nonNullWeights)

    # tweetVsCitationList = sorted(tweetVsCitationList, key=lambda tc: tc[1], reverse=True)[:100]
    x, y = zip(*tweetVsCitationList)
    paperFigure(plt)
    plt.scatter(x, y)
    # plt.title("Korrelation zwischen Tweets und Zitationen (Papieren zwischen " + str(yearBounds[0]) + " und " + str(yearBounds[1]) + "; #Docs: " + str(totalDocs) + ")")
    plt.ylabel("#Tweets")
    plt.xlabel("#Citations")
    #plt.xlim((0,200))
    #plt.ylim((0,30))

    p = numpy.polyfit(x, y, 1)
    xTrend = range(min(x), max(x)+1)
    yTrend = map(lambda x: numpy.polyval(p, x), xTrend)
    plt.plot(xTrend, yTrend, color='r')

    # plt.figtext(0.80, 0.05,  'korrelationskoeffizient: ' + str(korrelationskoeffizient(x, y)))
    print 'korrelationskoeffizient: ' + str(korrelationskoeffizient(x, y))
    plt.tight_layout()
    plt.show()

def tweetVsMendeleyReaders(yearBounds = [None, None], maxTweets = 300, maxReaders = 300):
    tweetVsMendeleyReaderList = []

    totalDocs = 0
    for doc in filter(lambda doc: 
        (doc.mendeleyReaders != None and doc.mendeleyReaders<=maxReaders) and 
            (doc.tweets != None and len(doc.tweets)<=maxTweets) and
            (not yearBounds[0] or doc.publicationDatetime().year>=yearBounds[0]) and
            (not yearBounds[1] or doc.publicationDatetime().year<=yearBounds[1]), 
        SimpleDoc.getall()
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

def tweetVsViewCounts():
    tweetVsViewCountList = []

    totalDocs = 0
    for doc in twitterHorizonDocs():
        if(len(doc.tweets) != None and doc.citationWeight(method = "max") != None):
            tweetVsViewCountList.append([doc.citationWeight(method = "max"), doc.numTweets()])
            totalDocs += 1

    x, y = zip(*tweetVsViewCountList)

    plt.figure()

    plt.scatter(x, y)
    plt.title("Korrelation zwischen Tweets und citation weight")
    plt.ylabel("#Tweets")
    plt.xlabel("itation weight")

    p = numpy.polyfit(x, y, 1)
    xTrend = range(int(min(x)), int(max(x)+1))
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

        for doc in SimpleDoc.getall():
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

    allDocs = list(SimpleDoc.getall())
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
    x, y = zip(*map(lambda doc: [doc.publicationTimestamp, len(doc.tweets)], SimpleDoc.getall()))
    print korrelationskoeffizient(x, y) # 0.082


def alteringTweetStreamAfterFirstPeak():
    relativeTweetDiffAfter1WeekAndTotal = map(
        lambda doc: 
            float(doc.numTweets()) / doc.numTweetsBetweenRelative(None, 60*60*24*7),
            filter(lambda doc: doc.numTweetsBetweenRelative(None, 60*60*24*7) >= 5, SimpleDoc.getall())
    )

    relBins, labels = pieData([
        [lambda x: x==1.0, "+0%"], 
        [lambda x: x>1.0 and x<=1.1, "+0-10%"],
        [lambda x: x>1.1 and x<=1.2, "+10-20%"],
        [lambda x: x>1.2 and x<=1.3, "+20-30%"],
        [lambda x: x>1.3 and x<=1.4, "+30-40%"],
        [lambda x: x>1.4 and x<=1.5, "+40-50%"],
        [lambda x: x>1.5, ">50%"]
    ], relativeTweetDiffAfter1WeekAndTotal)

    plt.figure()
    plt.pie(relBins, autopct='%1.1f%%', 
        startangle=90, labels=labels)

    plt.title("Relative Anzahl Tweets im Vergleich zu Anzahl Tweets nach einer Woche")
    plt.show()

def cummulativeTwitterPlots():
    # twitterTimelines, publicationTimestamps = zip(*filter(lambda timelinePubTs: len(timelinePubTs[0]) != 0, map(lambda doc: [doc.cummulativeTwitterTimeline(), doc.publicationTimestamp], SimpleDoc.getall())))
    twitterTimelines = filter(lambda tl: len(tl) != 0, map(lambda doc: map(lambda point: [point[0]-doc.publicationTimestamp, point[1]], doc.cummulativeTwitterTimeline()), SimpleDoc.getall()))

    # twitterTimelines = filter(lambda tl: len(tl) < 20, twitterTimelines)
    # twitterTimelines = filter(lambda tl: len(tl) > 50, twitterTimelines)
    plt.figure()
    for timeline in twitterTimelines:
        x, y = zip(*timeline)
        plt.plot(x, y)
    
    plt.show()

def groupByJournalAndVolume():
    issns = { }
    docs = list(SimpleDoc.getall())
    for doc in docs:
        issns[doc.issn] = issns.get(doc.issn, 0) + 1

    validIssns = map(lambda kv: kv[0], filter(lambda item: item[1]>5 and item[0] != None, issns.items()))

    groups = { }
    for doc in docs:
        if doc.issn in validIssns:
            groupList = groups.get((doc.issn, doc.volume), [])
            # groupList = groups.get(doc.issn, [])
            groupList.append(doc)
            groups[(doc.issn, doc.volume)] = groupList
            # groups[doc.issn] = groupList

    validGroups = filter(lambda group: len(group[1]) > 5, groups.items())
    # validGroups = groups.items()
    
    correlationValues = []    
    for ident, docs in validGroups:
        docTweets = map(lambda doc: doc.numTweets(), docs)
        docCitations = map(lambda doc: doc.numCitations(), docs)
        korr = None

        # docTweetCitationRatios = map(lambda doc: [float(doc.numTweets()) / doc.numCitations() if doc.numCitations() != 0 else float('nan')], docs)

        maxYear = max(map(lambda doc: doc.publicationDatetime().year, docs))
        minYear = min(map(lambda doc: doc.publicationDatetime().year, docs))

        yearRange = None
        if maxYear == minYear:
            yearRange = str(minYear)
        else:
            yearRange = str(minYear) + "-" + str(maxYear)

        try:
            korr = "%2.3f" % korrelationskoeffizient(docTweets, docCitations)
        except ZeroDivisionError:
            korr = "NaN"
            
        # correlationValues.append([ident[0], ident[1], len(docs), "%2.2f" % numpy.mean(docTweets), "%2.2f" % numpy.std(docTweets), korr, yearRange])
        correlationValues.append([ident[0], ident[1], len(docs), "%2.2f" % numpy.mean(docTweets), "%2.2f" % numpy.mean(docCitations), "%2.2f" % (float(numpy.sum(docTweets))/numpy.sum(docCitations)),  yearRange])
        # correlationValues.append([ident, len(docs), "%2.2f" % numpy.mean(docTweets), "%2.2f" % numpy.std(docTweets), korr])

    correlationValues = sorted(correlationValues, key=lambda x: x[0])

    compileTex(
        # simpleTabular(["ISSN", "Volume", "\\#Docs", "AVG Tweets", "StdDev", "korr", "Years"], correlationValues, orientation="llrrrrl"),
        simpleTabular(["ISSN", "Volume", "\\#Docs", "AVG T", "AVG C", "T/C", "Years"], correlationValues, orientation="llrrrrl"),
        # simpleTabular(["ISSN", "\\#Docs", "AVG Tweets", "StdDev", "korr", "Years"], correlationValues, orientation="lrrrrl"),
        figurePath("correlationsInJournals2.pdf")
    )

def exponentialTest(doc, referencePoint = 3):
    timeSlot = 60*60*24*2

    numTweetsInFirstTimeslot = doc.numTweetsBetweenRelative(None, 1*timeSlot)
    numTweetsAtReferencePoint = doc.numTweetsBetweenRelative(None, (referencePoint+1)*timeSlot) - numTweetsInFirstTimeslot
    
    x, y = zip(
        *filter(
            lambda timePoint: timePoint[0]>0,
            map(
                lambda timePoint: [
                    (timePoint[0]-doc.publicationTimestamp)/timeSlot, 
                    timePoint[1]-numTweetsInFirstTimeslot
                ],
                doc.cummulativeTwitterTimeline(padding=False)
            )
        )
    )
    plt.figure()
    plt.plot(x, y)

    lam = 0.333333333
    expFunAtReferencePoint = 1-numpy.exp(-lam*referencePoint)
    factor = numTweetsAtReferencePoint / expFunAtReferencePoint

    x2 = range(0, doc.timespan()/timeSlot)
    y2 = map(lambda xx: (1-numpy.exp(-lam*xx))*factor, x2)
    plt.plot(x2, y2)

    plt.show()

from scipy import stats

def findDensity():
    allDocs = list(simpleDoc.getall())
    #maximumDocAge = 60*60*24*300
    timeslot = 60*60*24*1
    maximumTweetAge = 60*60*24*365
    minimumTweetAge = 60*60*24*0
    
    consideredDocs = filter(lambda doc: len(doc.tweets) != 0 and doc.year() == 2012 and doc.month()>=6 and doc.month()<=8, allDocs)
    print "numDocs: " + str(len(consideredDocs))

    diffs = [tweet.timestamp-doc.publicationTimestamp for doc in consideredDocs for tweet in doc.tweets ]
    diffs = filter(lambda diff: minimumTweetAge <= diff <= maximumTweetAge, diffs)
    diffs2 = filter(lambda diff: diff >= timeslot*20, diffs)
    diffs = map(lambda x: float(x)/(timeslot), diffs)
    print "numTweets: " + str(len(diffs))
    print "oldTweets" + str(len(diffs2))

    kernel = stats.gaussian_kde(diffs)
    xmin = min(diffs)
    xmax = max(diffs)
    numTweets = len(diffs)
    xPoints = numpy.arange(xmin, xmax, (xmax-xmin)/1000)
    yPoints = map(lambda x: kernel(x)*numTweets, xPoints)

    # exp-fun
    plt.figure(num=None, figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')
    val, bins, patches = plt.hist([diffs, [1]], 50, stacked=True)
    #plt.plot(xPoints, yPoints)
    plt.ylim((0, 300))
    ylim = plt.ylim()
    plt.xlim((0, 365))
    xlim = plt.xlim()
    plt.xlabel("day")
    plt.ylabel("#tweets")
    plt.tight_layout()

    # randomTweetTimes = []
    rand1 = map(lambda x: float(x)+bins[0], numpy.random.gamma(0.75, 1.75, (numTweets*60)/100))
    rand2 = map(lambda x: float(x)+bins[0], numpy.random.gamma(2, 6, (numTweets*30)/100))
    rand3 = map(lambda x: float(x)+bins[0], numpy.random.gamma(1, 200, (numTweets*10)/100))

    plt.figure(num=None, figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')
    val, bins, patches = plt.hist([rand3, rand2, rand1], bins, stacked=True, color = ['y', 'r', 'b'])
    plt.ylim(ylim)
    plt.xlim(xlim)
    plt.xlabel("day")
    plt.ylabel("#tweets")
    #plt.plot(xPoints, yPoints)
    # yExp = map(lambda xx: (1-numpy.exp(-lam*xx)), xPoints)
    # yExp = map(lambda xx: lam*numpy.exp(-lam*xx), xPoints)
    # plt.plot(xPoints, yExp)
    plt.tight_layout()
    plt.show()

def twitterHist():
    plt.figure(num=None, figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')

    tweetTime = [(tweet.datetime().year, tweet.datetime().month) for doc in SimpleDoc.getall() for tweet in doc.tweets]
    histDisc(plt, tweetTime, width=0.5)
    #plt.title("Verteilung der Tweets nach Jahr und Monat")
    plt.tight_layout()
    plt.show()

def overviewData():
    # earliest tweet timestamp: 1337079632
    docs = list(SimpleDoc.getall())
    tweets = [ tweet for doc in docs for tweet in doc.tweets ]

    print "total Tweets: " + str(len(tweets))
    print "latest tweet: " + str(max(tweets, key=lambda x: x.timestamp).datetime())
    print "earliest tweet: " + str(min(tweets, key=lambda x: x.timestamp).datetime())
    
    print "total Documents: " + str(len(docs))
    print "latest document: " + str(max(docs, key=lambda doc: doc.publicationTimestamp).publicationDatetime())
    print "earliest document: " + str(min(docs, key=lambda doc: doc.publicationTimestamp).publicationDatetime())

def tweetHist():
    docs = list(filter(
        lambda doc: 
            (doc.publicationDatetime().year==2012 and 
            doc.publicationDatetime().month>=6 and doc.publicationDatetime().month<=8),
        SimpleDoc.getall()
    ))

    numTweets = [doc.numTweets() for doc in docs]
    plt.figure()
    plt.hist(numTweets, bins=xrange(0, 150, 5))
    
    plt.figure()
    numCite = [doc.numCitations() for doc in docs]
    plt.hist(numCite, bins=xrange(0, 150, 5))
    plt.show()

def tweetsBySpecificUserCorrelations():
    docs = SimpleDoc.getallBetween((2012, 6), (2012, 8))

    pairs = []
    for doc in docs:
        numTweets = len(filter(lambda tweet: tweet.username=="ATP_CME" ,doc.tweets))
        citations = doc.averageCitations()
        pairs.append([numTweets, citations])

    x, y = zip(*pairs)

    print allCorrelations(x, y)
    plt.scatter(x, y)
    plt.show()

tweetsBySpecificUserCorrelations()
