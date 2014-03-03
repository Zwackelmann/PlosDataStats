from main.util.common import SimpleDoc, rankCorrelation, pearsonCorrelation, allCorrelations
import json
import numpy as np
from scipy import stats

userDescriptions = json.load(open("twitter_users_with_description.json"))
"""
base:
0.139337080006

allWords:
0.126176375845
"""

allWords = ["science", "disease", "medical", "logy", "clinical", "medicine", "school", "health", "university", "ph.d", "ph. d", "ph d", "research", "professor", "doctor", "dr", "institute", "expert", "student", "postdoc", "post doc", "prof"]

docs = map(lambda doc: [map(lambda tweet: tweet.username, doc.tweets), doc.maxCitations()], SimpleDoc.getallBetween((2012,6), (2012,8)))

baseline = 0.126176375845
for i in range(0, 10):
    corrs = []
    for ind in range(0, len(allWords)):
        print "\nwithout " + allWords[ind]
        words = allWords[:]
        del words[ind]

        experts = set(map(lambda x: x[0],
            filter(lambda desc: desc[1] != None and any(map(lambda word: word in desc[1].lower(), words)), userDescriptions.items())
        ))
        
        print len(experts)

        pairs = []
        for doc in docs:
            numExpertTweets = sum((1 for usr in doc[0] if usr in experts))
            numCitations = doc[1]

            pairs.append([numExpertTweets, numCitations])
        
        x, y = zip(*pairs)

        s, p = stats.spearmanr(x, y)

        print s, s-baseline
        corrs.append(s)

    maxIndex = max(zip(range(0, len(allWords)), corrs), key=lambda x: x[1])[0]
    print "\n\nremove " + allWords[maxIndex] + " permanently:"
    del allWords[maxIndex]
    print "new word list: " + repr(allWords)
    baseline = corrs[maxIndex]
    print "new baseline: " + str(corrs[maxIndex])

