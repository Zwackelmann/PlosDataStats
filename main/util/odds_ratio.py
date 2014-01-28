from main.util.common import simpleDocs, mendeleyDisciplines, writeJsonToData

def oddsRatioForEachUser(mendeleyDiscipline):
    numTargetDocs = 0
    numOtherDocs = 0

    userMapTarget = { }
    userMapOther = { } 

    userSet = set()

    for doc in [ doc for doc in simpleDocs() if doc.mendeleyDisciplines != None]:
        tweeters = set([tweet.user for tweet in doc.tweets])
        userSet |= tweeters
        
        if mendeleyDiscipline in doc.mendeleyDisciplines:
            numTargetDocs += 1
            for user in tweeters:
                userMapTarget[user] = userMapTarget.get(user, 0) + 1

        else:
            numOtherDocs += 1

            for user in tweeters:
                userMapOther[user] = userMapOther.get(user, 0) + 1
    
    def numDocsCatAndUser(user):
        return userMapTarget.get(user, 0)
    def numDocsCatAndNotUser(user):
        return numTargetDocs - userMapTarget.get(user, 0)
    def numDocsNotCatAndUser(user):
        return userMapOther.get(user, 0)
    def numDocsNotCatAndNotUser(user):
        return numOtherDocs - userMapOther.get(user, 0)

    def score(user):
        if numDocsCatAndUser(user) == 0 or numDocsNotCatAndNotUser(user) == 0:
            return 0.0
        elif numDocsCatAndNotUser(user) == 0 or numDocsNotCatAndUser(user) == 0:
            return float("inf")
        else:
            return (float(numDocsCatAndUser(user)) * numDocsNotCatAndNotUser(user)) / (long(numDocsCatAndNotUser(user)) * numDocsNotCatAndUser(user))

    return map(lambda x: [x, score(x)], userSet)

orForDesc = {}
for disc in mendeleyDisciplines:
    descsOrs = oddsRatioForEachUser(disc)
    print disc
    for userOr in descsOrs:
        descList = orForDesc.get(userOr[0], [])
        descList.append([disc, userOr[1]])
        orForDesc[userOr[0]] = descList

writeJsonToData(orForDesc, "user_to_or.json")
