from sklearn.feature_extraction.text import CountVectorizer
from main.util.db import openDb
import json
import string
from main.util.odds_ratio import oddsRatioForEachFactor

db = openDb("stuff/localconnect.json")
cur = db.cursor()

usersSorted = []
f = open("user-ordering-sum", "r")
for line in f:
    usersSorted.append(json.loads(line)[0])
usersSorted = list(reversed(usersSorted))
consideredUsers = set(usersSorted)

positiveUsers = set(usersSorted[0:150])
negativeUsers = set(usersSorted[150:])

username2id = { }
id2username = { }
for user in usersSorted:
    cur.execute("SELECT twitter_id, twitter_name FROM twitter_id2twitter_name WHERE twitter_name = %s", (user))

    for row in cur.fetchall():
        if row[1] != "-1" and row[1] != -1 and int(row[0]) != -1:
            username2id[row[1]] = row[0]
            id2username[row[0]] = row[1]

consideredUserIds = map(lambda u: username2id[u], filter(lambda u: u in username2id ,consideredUsers))

"""tokenizer = CountVectorizer().build_tokenizer()
userWords = { }
for user in usersSorted:
    cur.execute("SELECT description FROM users_twitter WHERE Twitter_ScreenName = %s", (user))

    desc = None
    for row in cur.fetchall():
        if row[0] != None:
            desc = row[0]

    if desc != None:
        tokens = map(lambda s: filter(lambda c: c in string.printable, s).lower(), tokenizer(desc))
        userWords[user] = list(set(tokens))
    else:
        userWords[user] = None

print userWords

f = open("user_words.json", "w")
f.write(json.dumps(userWords))
f.close()"""

"""f = open("/home/simon/user_articles.txt")

def foo(s):
    if len(s) < 2:
        raise ValueError("There was a line without any semicolon - cannot be!!")
    if len(s) == 2: # expected normal case
        usr = int(s[0])
        concept = s[1].strip()
    else: # semicolon occurres in concept name
        usr = int(s[0])
        concept = ";".join(s[1:])

    return filter(lambda c: c in string.printable, concept).strip().lower()

userTweetCats = { }
counter = 0
for line in f:
    if counter % 10000 == 0:
        print counter

    s = line.split(";")
    usrId = int(s[0])

    if usrId in consideredUserIds:
        concept = foo(s)
        usrName = id2username[usrId]

        usrSet = userTweetCats.get(usrName, set())
        usrSet.add(concept)
        userTweetCats[usrName] = usrSet

    counter += 1

print len(userTweetCats)
userTweetCats = dict(map(lambda kv: (kv[0], list(kv[1])), userTweetCats.items()))
f.close()
print len(userTweetCats)

f2 = open("user_tweet_concepts.json", "w")
f2.write(json.dumps(userTweetCats))
f2.close()


# usersWordLists = """

"""userLists = { }
cur.execute(
    """#SELECT mem.screenName, l.name FROM users_memberships mem
    #join lists l on mem.listId=l.listId"""
""")

for row in cur.fetchall():
    if row[0] != "-1" and row[1] != "-1" and row[0] in consideredUsers:
        s = userLists.get(row[0], set())
        listname = filter(lambda c: c in string.printable, row[1]).strip().lower()
        s.add(listname)
        userLists[row[0]] = s

print len(userLists)
userLists = dict(map(lambda kv: (kv[0], list(kv[1])), userLists.items()))
print len(userLists)

f2 = open("user_lists.json", "w")
f2.write(json.dumps(userLists))
f2.close()"""

f = open("user_tweet_concepts.json", "r")
j = json.load(f)

counts = { }
for username, words in j.items():
    if words != None:
        for word in words:
            counts[word] = counts.get(word, 0) + 1

positiveWords = filter(lambda x: x != None, map(lambda x: x[1], filter(lambda x: x[0] in positiveUsers, j.items())))
negativeWords = filter(lambda x: x != None, map(lambda x: x[1], filter(lambda x: x[0] in negativeUsers, j.items())))

ors = oddsRatioForEachFactor(positiveWords, negativeWords)
ors = sorted(ors, key=lambda x: counts[x[0]], reverse=True)[0:3000]
print len(ors)
sortedOrs = map(lambda x: x[0], sorted(ors, key=lambda x: x[1]))
print ", ".join(sortedOrs[0:20])
print ", ".join(reversed(sortedOrs[-20:]))