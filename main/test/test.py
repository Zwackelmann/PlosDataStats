import json
import matplotlib.pyplot as plt
from main.util.common import SimpleDoc
import numpy as np

docs = SimpleDoc.getallBetween((2012, 6), (2012, 8))

avgTweetsOnDay = []
for relDay in range(0, 365):
    tweetsOnDay = []
    for doc in docs:
        tweetsOnDay.append(len(filter(lambda tweet: tweet.timestamp < doc.publicationTimestamp+(relDay*60*60*24), doc.tweets)))
    avgTweetsOnDay.append(np.mean(tweetsOnDay))

print avgTweetsOnDay


