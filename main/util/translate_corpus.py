import json

f = open("relevant_data_dtptcmr.json", "w")
for doc in simpleDocs():
    doi = doc.doi
    title = doc.title
    pDate = doc.publicationDatetime()
    tweets = []
    for tweet in doc.tweets:
        tweetText = tweet.text
        tweetUser = tweet.user
        retweetUser = tweet.retweetUser
        tweetTimestamp = tweet.datetime()
        tweets.append([tweetText, tweetUser, retweetUser, tweetTimestamp])

    citationTimeline = []
    for citationTimepoint in doc.citationTimeline:
        timestamp = citationTimepoint.datetime()
        totalCitations = citationTimepoint.totalCitations
        citationTimeline.append([timestamp, totalCitations])

    mendeleyDisciplines = doc.mendeleyDisciplines
    mendeleyReaders = doc.mendeleyReaders

    f.write(json.dumps([doi, title, pDate, tweets, citationTimeline, mendeleyDisciplines, mendeleyReaders]) + "\n")

f.close()