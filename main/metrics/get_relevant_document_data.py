"""
trage zu jedem dokument zusammen:
    - die Liste von Twitter usern
    - ob es ein Retweet ist
        - wenn ja: wie ist der Benutzername des Ursprünglichen Users?
    - zu welcher Menedely Disziplin das Dokument gehört
    - die Zeitreihe der
        - Citation counts
        - Twitter counts
    - veröffentlichungsdatum

"""

from main.util.common import doForEachPlosDoc, dataPath, readJsonFromData
import re
import json

file = open(dataPath("relevant_document_data.json"), "w")

def findRelevantData(doc):
    doi = doc['doi']
    twitterData = None # liste von [ "tweet text", user, retweetUser (None, wenn kein retweet), zeitpunkt ]
    citations = None # [ zeitpunkt, totalCitations ]
    mendeleyDisciplineList = None
    pubDate = doc['publication_date']
    
    for source in doc['sources']:
        if source['name'] == 'twitter':
            twitterData = extractRelevantTwitterData(source)
        if source['name'] == 'mendeley':
            events = source['events']
            if len(events) != 0:
                stats = events['stats']
                mendeleyDisciplineList = map(lambda x: x['name'], stats['discipline'])
        if source['name'] == 'crossref':
            citations = map(lambda x: [x['update_date'], x['total']], source['histories'])

    file.write(json.dumps([doi, pubDate, twitterData, citations, mendeleyDisciplineList]) + "\n")


retweetPattern = re.compile("^RT @([^:]*): (.*)$")

def extractRelevantTwitterData(twitterSource):
    events = twitterSource['events']
    tweets = []
    for event in events:
        tweet = event['event']
        date = tweet['created_at']
        user = tweet['user']
        
        rawText = tweet['text']
        retweet = retweetPattern.search(rawText)
        if(retweet):
            retweetUser = retweet.group(1)
            text = retweet.group(2)
        else:
            retweetUser = None
            text = rawText
        
        tweetData = [text, user, retweetUser, date]
        tweets.append(tweetData)

    return tweets

doForEachPlosDoc(findRelevantData)

file.close()
