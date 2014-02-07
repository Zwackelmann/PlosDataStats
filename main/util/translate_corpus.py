import json
from main.util.common import simpleDocs

f = open("relevant_data_dtptcmriiv.json", "w")
for doc in simpleDocs():
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

    f.write(json.dumps([
        doc.doi, 
        doc.title, 
        doc.publicationDatetime(), 
        tweets, 
        citationTimeline, 
        doc.mendeleyDisciplines,
        doc.mendeleyReaders,
        doc.issn, 
        doc.issue, 
        doc.volume
    ]) + "\n")

f.close()