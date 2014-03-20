from main.util.db import openDb
import json
from scipy import stats
from main.util.common import SimpleDoc, powerset, Log
import math
import itertools
from main.metrics.get_experts import metricNames

db = openDb("stuff/localconnect.json")

l = Log(filename="foo", verbose=True)

topCategories = ['Biology', 'Medicine', 'Sports', 'Culture', 'Technology', 'Education', 'Health', 
    'Business', 'Belief', 'Humanities', 'Society', 'Life', 'Arts', 'Language', 'Law', 
    'History', 'Geography', 'Agriculture', 'Politics', 'Mathematics', 'Science', 
    'Nature', 'Environment', 'People', 'Chronology' ]


outcomes = { }

"""for cats in topCategories:
    l.log("analyze categories: " + repr(cats))

    cur = db.cursor()

    scores = { }
    for ind, metricName in zip(range(0, len(metricNames)), metricNames):
        pairs = []
        for doc in docs:
            numExpertTweets = sum((1 for usr in doc[0] if not usr in patrickExperts))
            metricScore = doc[1][ind]
            pairs.append([numExpertTweets, metricScore])

        x, y = zip(*pairs)
        s, p = stats.spearmanr(x, y)

        scores[metricName] = s


    for metricName in metricNames:
        l.log("%-20s: %1.3f %1.3f" % (metricName, scores[metricName], (scores[metricName]-baseline[metricName])))

        o = outcomes.get(metricName, [])
        o.append((cats, scores[metricName], scores[metricName]-baseline[metricName]))
        outcomes[metricName] = o

    l.log("\n\n")"""

outcomes = {}
f = open("list-corrs", "r")
for line in f:
    logEntry = json.loads(line)
    if logEntry['type'] == "exclude":
        for metricName in metricNames:
            o = outcomes.get(metricName, [])
            o.append((logEntry['cat-name'], logEntry['expert-corrs'][metricName], logEntry['diffs'][metricName]))
            outcomes[metricName] = o

for metricName in metricNames:
    outcomesForMetric = outcomes[metricName]
    s = sorted(filter(lambda x: not math.isnan(x[1]), outcomesForMetric), key=lambda x: x[2])

    x = metricName + "\t"
    x += (",\t".join(map(lambda x: "%s:\t%1.3f" % x, map(lambda x: (x[0], x[2]), reversed(s[-4:-1])))))
    x += ",\t...,\t"
    x += (",\t".join(map(lambda x: "%s:\t%1.3f" % x, map(lambda x: (x[0], x[2]), reversed(s[0:3])))))
    l.log(x)

    """l.log("best settings for " + metricName + ":")
    l.log("\n".join(map(lambda x: "%-50s, %1.3f, %1.3f" % x, reversed(s[-6:-1]))))
    l.log("")
    l.log("worst settings for " + metricName + ":")
    l.log("\n".join(map(lambda x: "%-50s, %1.3f, %1.3f" % x, s[0:5])))
    l.log("\n")"""

l.close()

