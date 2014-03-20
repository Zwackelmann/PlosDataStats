from main.util.common import SimpleDoc, rankCorrelation, pearsonCorrelation, allCorrelations, Log
import json
import numpy as np
from scipy import stats
import random
from get_experts import getPatrickExperts, metrics, metricNames, getBaseline, minimizedDocs, getWordExperts, correlationWrtUsers, corrComparision, remainNTweets, corrDiffs, getListScore
import math

l = Log(filename="foo", verbose=True)

topCategories = ['Biology', 'Medicine', 'Sports', 'Culture', 'Technology', 'Education', 'Health', 
    'Business', 'Belief', 'Humanities', 'Society', 'Life', 'Arts', 'Language', 'Law', 
    'History', 'Geography', 'Agriculture', 'Politics', 'Mathematics', 'Science', 
    'Nature', 'Environment', 'People', 'Chronology' ]

mendeleyDisciplines = [
    'Linguistics', 'Economics', 'Psychology', 'Humanities', 'Materials Science', 
    'Earth Sciences', 'Environmental Sciences', 'Biological Sciences', 'Medicine', 
    'Mathematics', 'Chemistry', 'Physics', 'Social Sciences', 'Electrical and Electronic Engineering', 
    'Astronomy / Astrophysics / Space Science', 'Sports and Recreation', 
    'Management Science / Operations Research', 'Philosophy', 'Law', 
    'Business Administration', 'Engineering', 'Design', 'Arts and Literature', 
    'Education', 'Computer and Information Science'
]

expertWords = ["university", "ph.d", "ph. d", "ph d", "phd", "professor", "doctor", "dr.", "institute", "postdoc" ]# , "post doc", "student", "research", "prof", "post prad", "science", "scientist", "department", "study", "studies", "develop"]
# expertLists = list(map(lambda s: s.strip(), open("data/expert_topics", "r")))
# expertCategories = ['Medicine', 'Health' ]

wordExperts = getWordExperts(expertWords)
# patrickExperts = getPatrickExperts(expertCategories)

"""bioDocs = minimizedDocs(
    filter(
        lambda doc: 
            doc.mendeleyDisciplines != None and 'Biological Sciences' in doc.mendeleyDisciplines, 
            SimpleDoc.getallBetween((2012,6), (2012,8))
    ),
    metrics
)"""

docs = minimizedDocs(
    SimpleDoc.getallBetween((2012,6), (2012,8)),
    metrics
)

usersInTimewindow = set((usr for doc in docs for usr in doc[0]))
totalNumTweets = sum((1 for doc in docs for u in doc[0]))

"""f = open("baselines", "w")

for numTweets in range(100, totalNumTweets, 100):
    print str(numTweets) + " / " + str(totalNumTweets)
    baseline = getBaseline(docs, metricNames, numTweets)
    f.write(json.dumps( { "num-tweets" : numTweets, "baseline" : baseline } ) + "\n")
    f.flush()

f.close()"""

"""f = open("list-corrs", "w")

for cat in topCategories:
    l.log(cat)
    expertsWithWeight = getListScore(cat)
    if len(expertsWithWeight) != 0:
        expertsWithWeight = dict(map(lambda kv: (kv[0], math.log(kv[1])) ,expertsWithWeight.items()))

        experts, expertWeights = zip(*expertsWithWeight.items())
        experts = set(experts)

        l.log("#experts: " + str(len(experts.intersection(usersInTimewindow))))
        numExpertTweets = sum((1 for doc in docs for u in doc[0] if u in experts))
        l.log("#tweets: " + str(numExpertTweets))

        baseline = getBaseline(docs, metricNames, numExpertTweets)
        corrs = correlationWrtUsers(docs, expertsWithWeight, metricNames)
        diffs = corrDiffs(baseline, corrs)

        f.write(json.dumps({
            "cat-name" : cat,
            "type" : "include-log-weighted",
            "num-experts" : len(experts),
            "num-tweets" : numExpertTweets,
            "baseline" : baseline,
            "expert-corrs" : corrs,
            "diffs" : diffs
        }) + "\n")
        f.flush()

for cat in topCategories:
    l.log(cat)
    expertsWithWeight = getListScore(cat)
    if len(expertsWithWeight) != 0:
        experts, expertWeights = zip(*expertsWithWeight.items())
        experts = set(experts)

        l.log("#experts: " + str(len(experts.intersection(usersInTimewindow))))
        numExpertTweets = sum((1 for doc in docs for u in doc[0] if u in experts))
        l.log("#tweets: " + str(numExpertTweets))

        baseline = getBaseline(docs, metricNames, numExpertTweets)
        corrs = correlationWrtUsers(docs, expertsWithWeight, metricNames)
        diffs = corrDiffs(baseline, corrs)

        f.write(json.dumps({
            "cat-name" : cat,
            "type" : "include-lin-weighted",
            "num-experts" : len(experts),
            "num-tweets" : numExpertTweets,
            "baseline" : baseline,
            "expert-corrs" : corrs,
            "diffs" : diffs
        }) + "\n")
        f.flush()

for cat in topCategories:
    l.log(cat)
    expertsWithWeight = getListScore(cat)
    if len(expertsWithWeight) != 0:
        experts, expertWeights = zip(*expertsWithWeight.items())
        experts = set(experts)

        l.log("#experts: " + str(len(experts.intersection(usersInTimewindow))))
        numExpertTweets = sum((1 for doc in docs for u in doc[0] if u in experts))
        l.log("#tweets: " + str(numExpertTweets))

        baseline = getBaseline(docs, metricNames, numExpertTweets)
        corrs = correlationWrtUsers(docs, experts, metricNames)
        diffs = corrDiffs(baseline, corrs)

        f.write(json.dumps({
            "cat-name" : cat,
            "type" : "include-unweighted",
            "num-experts" : len(experts),
            "num-tweets" : numExpertTweets,
            "baseline" : baseline,
            "expert-corrs" : corrs,
            "diffs" : diffs
        }) + "\n")
        f.flush()

for cat in topCategories:
    l.log(cat)
    expertsWithWeight = getListScore(cat)
    if len(expertsWithWeight) != 0:
        experts, expertWeights = zip(*expertsWithWeight.items())
        experts = usersInTimewindow.difference(set(experts))

        l.log("#experts: " + str(len(experts.intersection(usersInTimewindow))))
        numExpertTweets = sum((1 for doc in docs for u in doc[0] if u in experts))
        l.log("#tweets: " + str(numExpertTweets))

        baseline = getBaseline(docs, metricNames, numExpertTweets)
        corrs = correlationWrtUsers(docs, experts, metricNames)
        diffs = corrDiffs(baseline, corrs)

        f.write(json.dumps({
            "cat-name" : cat,
            "type" : "exclude",
            "num-experts" : len(experts),
            "num-tweets" : numExpertTweets,
            "baseline" : baseline,
            "expert-corrs" : corrs,
            "diffs" : diffs
        }) + "\n")
        f.flush()

f.close()"""

"""print len(docs)


print len(bioExperts.intersection(usersInTimewindow))"""
"""for topCategory in topCategories:
    patrickExperts = getPatrickExperts(topCategory)
    print topCategory
    print len(patrickExperts.intersection(usersInTimewindow))
    print """""

#print len(wordExperts)
#print len(patrickExperts)
#print len(listWeights)
#print len(usersInTimewindow)

print ""
#experts = wordExperts.intersection(usersInTimewindow).intersection(bioExperts)
#experts = wordExperts.intersection(usersInTimewindow).intersection(patrickExperts).intersection(set(listWeights.keys()))
#experts = dict(map(lambda x: (x, listWeights[x]), experts))


experts = wordExperts


totalNumExpertTweets = sum((1 for doc in docs for u in doc[0] if u in experts))
baseline = getBaseline(docs, metricNames, len(experts))

corrs = correlationWrtUsers(docs, experts, metricNames)

l.log("number of experts: " + str(len(experts)))
l.log("number of tweets: " + str(totalNumExpertTweets))
l.log("baseline: " + str(baseline))
l.log("diff: " + str(corrComparision(baseline, corrs)))

l.close()
