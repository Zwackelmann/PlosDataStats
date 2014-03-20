from main.util.db import openDb
import json
from scipy import stats
from main.util.common import SimpleDoc, powerset, Log
import math
import itertools
import matplotlib.pyplot as plt

metrics = [
    ("Crossref", lambda doc: doc.numCrossrefs()),
    ("PubMed", lambda doc: doc.pubmedCitations),
    ("Scopus", lambda doc: doc.scopusCitations),
    ("Max Citations", lambda doc: doc.maxCitations()),
    ("PLOS pdf", lambda doc: doc.pdfViews),
    ("PLOS HTML", lambda doc: doc.htmlViews),
    ("PMC pdf", lambda doc: doc.pmcPdf),
    ("PMC HTML", lambda doc: doc.pmcHtml),
    ("Facebook Shares", lambda doc: doc.facebookShares),
    ("Facebook Comments", lambda doc: doc.facebookComments),
    ("Facebook Likes", lambda doc: doc.facebookLikes),
    ("Mendeley Readers", lambda doc: doc.mendeleyReaders),
    ("CiteULike", lambda doc: doc.citeULikeShares)
]

l = Log(filename="foo", verbose=True)

metricNames = map(lambda metric: metric[0], metrics)
docs = map(lambda doc: [map(lambda tweet: tweet.username, doc.tweets), map(lambda metric: metric[1](doc), metrics)], SimpleDoc.getallBetween((2012,6), (2012,8)))

negativeUsernames = map(lambda x: x[0], json.load(open("user_exclude_list_negative")))

usersTweetFrequence = { }
for doc in docs:
    for user in doc[0]:
        usersTweetFrequence[user] = usersTweetFrequence.get(user, 0) + 1

lowTweetUsers = set(map(
    lambda userKV: userKV[0],
    filter(lambda userKV: 0 <= userKV[1] <= 4, usersTweetFrequence.items())
))


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

for ind, metricName in zip(range(0, len(metricNames)), metricNames):
    pairs = []
    for doc in docs:
        numExpertTweets = sum((1 for usr in doc[0] if (not usr in negativeUsernames) and (not usr in lowTweetUsers)))
        metricScore = doc[1][ind]
        pairs.append([numExpertTweets, metricScore])

    x, y = zip(*pairs)
    s, p = stats.spearmanr(x, y)

    print "%-20s: %1.3f     %+1.3f" % (metricName, s, s-baseline[metricName])

l.log("\n\n")