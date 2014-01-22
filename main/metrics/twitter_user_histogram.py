from main.util.common import doForEachSimpleDoc, writeJsonToData, dataPath, readJsonFromData, formatHist
from os import path
import numpy


numTweetsPerUserFilename = "num_tweets_per_user.json"
if not path.isfile(dataPath(numTweetsPerUserFilename)):
    numTweetsPerUser = {}

    def getRelevantData(doc):
        global userCount

        twitterData = doc[2]
        for tweet in twitterData:
            user = tweet[1]
            usersTotalTweets = numTweetsPerUser.get(user, 0) + 1
            numTweetsPerUser[user] = usersTotalTweets

    doForEachSimpleDoc(getRelevantData)

    writeJsonToData(numTweetsPerUser, numTweetsPerUserFilename)
else:
    numTweetsPerUser = readJsonFromData(numTweetsPerUserFilename)

hist = numpy.histogram(list(numTweetsPerUser.itervalues()), [1, 2, 3, 4, 5, 10, 20, 100, 500, 1000])

print "\n" * 3

# Tweet Histogaram
print "Tweet Histogram:"
formatHist(hist[0], hist[1], 6)


print "\n" * 3

# Top X Tweeters
sortedItems = sorted(list(numTweetsPerUser.items()), key=lambda x: x[1], reverse=True)

numTopUsersList = [10, 20, 50]#, 100, 200, 500]
for numTopUsers in numTopUsersList:
    print str(numTopUsers) + " Top Tweeters:"
    for i in range(0, numTopUsers):
        user = sortedItems[i]
        print '%(user)-20s: %(number)5d' % {"user": user[0], "number": user[1]}

    print "\n" * 3

    # Portion of Tweets tweetet by top X Users
    sumTop = 0
    for i in range(0, numTopUsers):
        sumTop += sortedItems[i][1]
    sumOther = 0
    for i in range(numTopUsers, len(sortedItems)):
        sumOther += sortedItems[i][1]

    print "Portion of Tweets tweetet by top " + str(numTopUsers) + " Users:"
    print str(sumTop) + "/" + str(sumOther + sumTop) + " = " + str(float(sumTop)/(sumOther+sumTop))

    print "\n\n"

print len(sortedItems)