from main.util.common import SimpleDoc, User
import json
from main.util.db import openDb
import numpy as np
from main.util.odds_ratio import oddsRatioForEachFactor

"""docs = map(lambda doc: [map(lambda tweet: tweet.username, doc.tweets), doc.maxCitations()], SimpleDoc.getallBetween((2012,6), (2012,8)))

usersTweetFrequence = { }
for doc in docs:
    for user in doc[0]:
        usersTweetFrequence[user] = usersTweetFrequence.get(user, 0) + 1

allUsers = set(map(lambda x: x[0], usersTweetFrequence.items()))

lowTweetUsers = set(map(
    lambda userKV: userKV[0],
    filter(lambda userKV: 0 <= userKV[1] <= 4, usersTweetFrequence.items())
))"""

"""db = openDb("stuff/localconnect.json")

cur = db.cursor()
#sql = """
#SELECT screen_name, cat_title
#FROM twitter_id_2_screenname AS t2s 
#JOIN users_professions_2 AS up2 ON up2.user_id=t2s.twitter_id
"""
cur.execute(sql)

userProfessions = { }
for row in cur.fetchall():
    s = userProfessions.get(row[0], set())
    s.add(row[1])
    userProfessions[row[0]] = s

for key in userProfessions.keys():
    userProfessions[key] = list(userProfessions[key])"""

#f = open("userProfessions.json", "w")
#f.write(json.dumps(userProfessions))
#f.close()

negativeUsernames = map(lambda x: x[0], json.load(open("user_exclude_list_negative")))
positiveUsernames = json.load(open("positive_users.json"))
userProfessions = json.load(open("userProfessions.json"))

"""negativeUserProfessions = { }
positiveUserProfessions = { }

for user in negativeUsernames:
    if user in userProfessions:
        for profession in userProfessions[user]:
            negativeUserProfessions[profession] = negativeUserProfessions.get(profession, 0) + 1

for user in positiveUsernames:
    if user in userProfessions:
        for profession in userProfessions[user]:
            positiveUserProfessions[profession] = positiveUserProfessions.get(profession, 0) + 1

print len(negativeUsernames)
print negativeUserProfessions
print len(positiveUsernames)
print positiveUserProfessions"""

"""stats = [
    ("#Followers", lambda user: user.numFollowers),
    ("#Tweets", lambda user: user.numTweetsPosted),
    ("#Friends", lambda user: user.numFriends),
    ("#Lists", lambda user: user.listedCount)
]

statistics = [
    ("mean", lambda values: np.mean(values)),
    ("std", lambda values: np.std(values))
]

negativeMatrix = []
for username in negativeUsernames:
    user = User.findByTwitterName(username)
    if user != None:
        userStats = map(lambda stat: stat[1](user), stats)
        negativeMatrix.append(userStats)

positiveMatrix = []
for username in positiveUsernames:
    user = User.findByTwitterName(username)
    if user != None:
        userStats = map(lambda stat: stat[1](user), stats)
        positiveMatrix.append(userStats)

for ind, stat in zip(range(0, len(stats)), stats):
    valuesForStat = filter(lambda x: x!=None, map(lambda x: x[ind], negativeMatrix))
    print stat[0]
    for statistic in statistics:
        print statistic[0] + ": " + str(statistic[1](valuesForStat))

print "\n\n\n"

for ind, stat in zip(range(0, len(stats)), stats):
    valuesForStat = filter(lambda x: x!=None, map(lambda x: x[ind], positiveMatrix))
    print stat[0]
    for statistic in statistics:
        print statistic[0] + ": " + str(statistic[1](valuesForStat))
"""

userListTopics = json.load(open("data/userListTopics.json"))
userTopics = { }
topicCounts = { }
for item in userListTopics:
    if "topics" in item:
        topics = map(lambda topic: topic["topicName"], item["topics"])
        userTopics[item["userName"]] = topics

        for topic in topics:
            topicCounts[topic] = topicCounts.get(topic, 0) + 1

fraquentLists = map(lambda x: x[0], filter(lambda x: x[1] > 50, topicCounts.items()))

negativeUserTopics = filter(lambda x: x!= None, map(lambda username: userTopics.get(username, None), negativeUsernames))
positiveUserTopics = filter(lambda x: x!= None, map(lambda username: userTopics.get(username, None), positiveUsernames))

print "\n".join(map(lambda x: ("%s" % (x[0])), filter(lambda x: x[0] in fraquentLists and x[1]>1.0, sorted(oddsRatioForEachFactor(positiveUserTopics, negativeUserTopics), key=lambda x: x[1]))))