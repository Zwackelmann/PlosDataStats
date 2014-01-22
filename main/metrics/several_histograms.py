import matplotlib.pyplot as plt
from main.util.common import simpleDocs, dataPath, figurePath, groupCount
from matplotlib import ticker
from main.util.plotting import histDisc, hist, barPlot, pieData
import numpy
import itertools
from main.util.tex import simpleTabular, compileTex

def publication_years():
    plt.figure()

    publicationYears = list(simpleDoc.publicationDatetime().timetuple()[0] for simpleDoc in simpleDocs())
    histDisc(plt, publicationYears)
    plt.savefig(figurePath("publication_years.png"))
    plt.show()

def num_tweets():
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

mendeleyDisciplines()