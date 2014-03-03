from main.util.common import SimpleDoc, rankCorrelation, pearsonCorrelation, allCorrelations
import json
import numpy as np
from scipy import stats

docs = map(lambda doc: [map(lambda tweet: tweet.username, doc.tweets), doc.maxCitations()], SimpleDoc.getallBetween((2012,6), (2012,8)))
users = { }
for doc in docs:
    for user in doc[0]:
        users[user] = users.get(user, 0) + 1

powerUsers = map(
    lambda userKV: userKV[0],
    filter(lambda userKV: userKV[1] >= 10, users.items())
)

baseline = 0.0
f = open("foo", "w")
for i in range(0, 200):
    corrs = []
    for ind in range(0, len(powerUsers)):
        # print "\exclude " + powerUsers[ind]

        users = set()
        users.update(powerUsers[0:ind])
        users.update(powerUsers[ind+1:])

        pairs = []
        for doc in docs:
            numExpertTweets = sum((1 for usr in doc[0] if usr in users))
            numCitations = doc[1]

            pairs.append([numExpertTweets, numCitations])
        
        x, y = zip(*pairs)
        s, p = stats.spearmanr(x, y)

        print s, s-baseline
        corrs.append(s)

    maxIndex = max(zip(range(0, len(powerUsers)), corrs), key=lambda x: x[1])[0]
    print "\n\nremove " + powerUsers[maxIndex] + " permanently:"
    f.write(json.dumps([powerUsers[maxIndex], corrs[maxIndex]]))
    del powerUsers[maxIndex]
    print "new user list: " + repr(powerUsers)
    baseline = corrs[maxIndex]
    print "new baseline: " + str(corrs[maxIndex])

f.close()



