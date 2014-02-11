from main.util.common import User

bigusers = []
for username, user in User.twitterName2UserMap.items():
    if not user is None and user.numTweetsInCorpus() >= 10:
        bigusers.append(user)

sortedBigusers = sorted(bigusers, key=lambda user: user.listedCount, reverse=True)

f = open("big_users.json", "w")
f.write(json.dumps(map(lambda user: user.twitterName, sortedBigusers)))
f.close()