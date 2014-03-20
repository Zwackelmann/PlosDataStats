from main.util.common import SimpleDoc, rankCorrelation, pearsonCorrelation, allCorrelations
import json
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from main.util.plotting import histDisc, hist, barPlot, pieData, paperFigure

docs = map(lambda doc: [map(lambda tweet: tweet.username, doc.tweets), doc.maxCitations()], SimpleDoc.getallBetween((2012,6), (2012,8)))
users = { }
for doc in docs:
    for user in doc[0]:
        users[user] = users.get(user, 0) + 1

powerUsers = map(
    lambda userKV: userKV[0],
    filter(lambda userKV: userKV[1] >= 5, users.items())
)

def loadBaselines():
    baselines = { }
    f = open("baselines", "r")
    for line in f:
        j = json.loads(line)
        baselines[j["num-tweets"]] = j["baseline"]

    f.close()
    return baselines

baselines = loadBaselines()

def getCachedBaseline(numTweets):
    if numTweets > 21300:
        query = 21300
    elif numTweets < 100:
        query = 100
    elif numTweets % 100 > 50:
        query = numTweets + (100 - (numTweets%100))
    else:
        query = numTweets - (numTweets%100)
    return baselines[query]["Max Citations"]


"""f = open("user-ordering-sum", "w")

for i in range(0, len(powerUsers)):
    print "iteration " + str(i)
    diffs = []
    for ind in range(0, len(powerUsers)):
        users = set()
        users.update(powerUsers[0:ind])
        users.update(powerUsers[ind+1:])

        pairs = []
        totalExpertTweets = 0
        for doc in docs:
            numExpertTweets = sum((1 for usr in doc[0] if usr in users))
            totalExpertTweets += numExpertTweets
            numCitations = doc[1]

            pairs.append([numExpertTweets, numCitations])
        
        x, y = zip(*pairs)
        s, p = stats.spearmanr(x, y)

        baseline = getCachedBaseline(totalExpertTweets)
        diffs.append(s-baseline)

    maxIndex = max(zip(range(0, len(powerUsers)), diffs), key=lambda x: x[1])[0]
    print "\n\nremove " + powerUsers[maxIndex] + " permanently:"
    f.write(json.dumps([powerUsers[maxIndex], diffs[maxIndex]]) + "\n")
    f.flush()
    del powerUsers[maxIndex]
    print "improvement: " + str(diffs[maxIndex])

f.close()"""


usersSorted = []
f = open("user-ordering-sum", "r")
for line in f:
    usersSorted.append(json.loads(line)[0])
usersSorted = list(reversed(usersSorted))

usersTweetFrequence = { }
for doc in docs:
    for user in doc[0]:
        usersTweetFrequence[user] = usersTweetFrequence.get(user, 0) + 1

allUsers = set(usersTweetFrequence.keys())

lowTweetUsers = set(map(
    lambda userKV: userKV[0],
    filter(lambda userKV: 0 <= userKV[1] <= 4, usersTweetFrequence.items())
))

consideredUsers = set(usersSorted[0:120])
pairs = []
totalExpertTweets=0
for doc in docs:
    numExpertTweets = sum((1 for usr in doc[0] if (usr in consideredUsers) and (not usr in lowTweetUsers)))
    totalExpertTweets += numExpertTweets
    numCitations = doc[1]
    pairs.append([numExpertTweets, numCitations])

baseline = getCachedBaseline(totalExpertTweets)
x, y = zip(*pairs)
s, p = stats.spearmanr(x, y)

print baseline, s, s-baseline

"""xValues = []
yValues = []
for i in range(0, len(usersSorted)):
    consideredUsers = usersSorted[0:i+1]

    pairs = []
    totalExpertTweets = 0
    for doc in docs:
        numExpertTweets = sum((1 for usr in doc[0] if (usr in consideredUsers) and (not usr in lowTweetUsers)))
        totalExpertTweets += numExpertTweets
        numCitations = doc[1]
        pairs.append([numExpertTweets, numCitations])

    x, y = zip(*pairs)
    s, p = stats.spearmanr(x, y)

    baseline = getCachedBaseline(totalExpertTweets)

    xValues.append(i)
    yValues.append(s-baseline)

paperFigure(plt)
plt.plot(xValues, yValues)
plt.xlabel("Rank of user")
plt.ylabel(u'$\Delta$ to baseline')
plt.xlim((0, len(usersSorted)))
plt.ylim((0.0, 0.2))
plt.tight_layout()
plt.show()"""

