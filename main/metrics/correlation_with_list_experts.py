import json
from main.util.db import openDb
from scipy import stats
from main.util.common import SimpleDoc, powerset, Log
import math
import itertools

expertTopics = list(map(lambda s: s.strip(), open("data/expert_topics", "r")))

l = Log(filename="foo", verbose=True)

docs = map(lambda doc: [map(lambda tweet: tweet.username, doc.tweets), map(lambda metric: metric[1](doc), metrics)], SimpleDoc.getallBetween((2012,6), (2012,8)))

baseline = { }

for ind, metricName in zip(range(0, len(metricNames)), metricNames):
    pairs = []
    for doc in docs:
        numTweets = len(doc[0])
        metricScore = doc[1][ind]
        pairs.append([numTweets, metricScore])

    x, y = zip(*pairs)
    s, p = stats.spearmanr(x, y)

    baseline[metricName] = s

count = 0
count2 = 0
for ind, metricName in zip(range(0, len(metricNames)), metricNames):
    pairs = []
    for doc in docs:
        tweetScore = 0
        for usr in doc[0]:
            if usr in userListScore:
                tweetScore+=userListScore[usr]
                count2 += 1
            else:
                count += 1

        # numExpertTweets = sum((userListScore.get(usr, 0) for usr in doc[0]))
        
        metricScore = doc[1][ind]
        pairs.append([tweetScore, metricScore])

    x, y = zip(*pairs)
    s, p = stats.spearmanr(x, y)

    l.log("%-20s: %1.3f %1.3f" % (metricName, s, (s-baseline[metricName])))

print count / len(metricNames)
print count2 / len(metricNames)

l.close()