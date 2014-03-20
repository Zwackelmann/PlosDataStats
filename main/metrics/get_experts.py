from main.util.db import openDb
import json
from scipy import stats
from main.util.common import SimpleDoc, powerset, Log
import math
import itertools
import random
import numpy as np
import copy

db = openDb("stuff/localconnect.json")
def getPatrickExperts(cats):
    cur = db.cursor()

    if type(cats) is str:
        cats = [cats]

    sql = """
    SELECT DISTINCT name AS expert 
    FROM cat_experts
    WHERE cat_name IN (%s)
    """ % ((", ".join(map(lambda cat: "'" + cat + "'", cats))) if len(cats) != 0 else "''")
    cur.execute(sql)

    patrickExperts = set()
    for row in cur.fetchall():
        patrickExperts.add(row[0])

    return patrickExperts

def getListScore(cats):
    cur = db.cursor()

    if type(cats) is str:
        cats = [cats]

    sql = """
    SELECT twitter_name, sum(num_lists) 
    FROM user_lists_in_category
    WHERE cat_name IN (%s)
    GROUP BY twitter_name
    """ % ((", ".join(map(lambda cat: "'" + cat + "'", cats))) if len(cats) != 0 else "''")
    cur.execute(sql)

    listExperts = set()
    for row in cur.fetchall():
        listExperts.add((row[0], row[1]))

    return dict(listExperts)

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
metricNames = map(lambda x: x[0], metrics)

def getBaseline(docs, metricNames, maxNumTweets=None):
    runs = []
    numRuns = 1 if maxNumTweets is None else 100
    for i in range(0, numRuns):
        docsForRun = docs if maxNumTweets is None else remainNTweets(docs, maxNumTweets)

        baseline = { }

        for ind, metricName in zip(range(0, len(metricNames)), metricNames):
            pairs = []
            for doc in docsForRun:
                numTweets = len(doc[0])
                metricScore = doc[1][ind]
                pairs.append([numTweets, metricScore])

            x, y = zip(*pairs)
            s, p = stats.spearmanr(x, y)

            baseline[metricName] = s

        runs.append(baseline)

    return avgCorrs(runs)

def minimizedDocs(docs, metrics):
    return map(lambda doc: [map(lambda tweet: tweet.username, doc.tweets), map(lambda metric: metric[1](doc), metrics)], docs)

userDescriptions = json.load(open("data/twitter_users_with_description.json"))
def getWordExperts(expertWords):
    descs = map(lambda x: x[1],
        filter(lambda desc: desc[1] != None and any(map(lambda word: word in desc[1].lower(), expertWords)), userDescriptions.items())
    )

    # print "\n\n\n\n".join(descs[0:100])

    return set(map(lambda x: x[0],
        filter(lambda desc: desc[1] != None and any(map(lambda word: word in desc[1].lower(), expertWords)), userDescriptions.items())
    ))

def correlationWrtUsers(docs, users, metricNames):
    corrs = { }

    for ind, metricName in zip(range(0, len(metricNames)), metricNames):
        pairs = []

        for doc in docs:
            if type(users) is set:
                numExpertTweets = sum((1 for usr in doc[0] if usr in users))
            elif type(users) is dict:
                numExpertTweets = sum((users[usr] for usr in doc[0] if usr in users))
            else:
                raise ValueError("Argument users must be a set or a dict")

            metricScore = doc[1][ind]
            pairs.append([numExpertTweets, metricScore])

        x, y = zip(*pairs)
        s, p = stats.spearmanr(x, y)

        corrs[metricName] = s

    return corrs

def corrDiffs(baseline, corrs):
    keys = set(baseline.keys()).intersection(set(corrs.keys()))

    diffs = { }
    for key in keys:
        diffs[key] = corrs[key] - baseline[key]

    return diffs

def corrComparision(baseline, corrs):
    keys = set(baseline.keys()).intersection(set(corrs.keys()))

    buff = ""
    for key in keys:
        diff = corrs[key] - baseline[key]
        buff += ("%-20s: %1.3f  %1.3f\n" % (key, corrs[key], diff))

    return buff

def remainNTweets(minDocs, n):
    docsCopy = copy.deepcopy(minDocs)
    totalNumTweets = sum((1 for doc in docsCopy for u in doc[0]))
    
    if totalNumTweets < n:
        raise ValueError(str(n) + " is greater than the total number of tweets in document set")

    removeIndexes = sorted(random.sample(xrange(0, totalNumTweets), totalNumTweets-n))

    count = 0
    removedItems = 0
    removeInd = removeIndexes.pop(0)

    for doc in docsCopy:
        while removeInd != None and (removeInd < count+len(doc[0]) and removeInd >= count):
            relRemInd = removeInd-count
            usrs = doc[0]
            del usrs[relRemInd]
            removedItems += 1

            if len(removeIndexes) == 0:
                removeInd = None
                break
            else:
                removeInd = removeIndexes.pop(0)-removedItems

        count += len(doc[0])

    return docsCopy

def avgCorrs(corrList):
    if len(corrList) == 0:
        raise ValueError("cannot calculate average correlations from empty list of correlations")

    corrsByKey = { }
    for corrs in corrList:
        for key, value in corrs.items():
            l = corrsByKey.get(key, [])
            l.append(value)
            corrsByKey[key] = l


    return dict(map(lambda kv: (kv[0], np.mean(kv[1])), corrsByKey.items()))
