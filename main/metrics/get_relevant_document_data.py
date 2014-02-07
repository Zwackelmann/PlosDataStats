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

file = open(dataPath("relevant_document_data_plus_mendeley.json"), "w")

def findRelevantData(doc):
    doi = doc['doi']
    title = doc['title']
    twitterData = None # liste von [ "tweet text", user, retweetUser (None, wenn kein retweet), zeitpunkt ]
    citations = None # [ zeitpunkt, totalCitations ]
    mendeleyDisciplineList = None
    pubDate = doc['publication_date']
    mendeleyReaders = None
    issn = None
    issue = None
    volume = None

    for source in doc['sources']:
        if source['name'] == 'twitter':
            twitterData = extractRelevantTwitterData(source)
        if source['name'] == 'mendeley':
            events = source['events']
            if len(events) != 0:
                stats = events['stats']
                mendeleyDisciplineList = map(lambda x: x['name'], stats['discipline'])
                mendeleyReaders = stats.get('readers', None)
                if "identifiers" in events:
                    issn = events['identifiers'].get('issn', None)
                
                issue = events.get('issue', None)
                volume = events.get('volume', None)

        if source['name'] == 'crossref':
            citations = map(lambda x: [x['update_date'], x['total']], source['histories'])
    jdoc = json.dumps([doi, title, pubDate, twitterData, citations, mendeleyDisciplineList, mendeleyReaders, issn, issue, volume])
    file.write(jdoc + "\n")


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



def findRelevantData2(doc):
    for source in doc['sources']:
        if source['name'] == 'mendeley':
            events = source['events']
            if len(events) != 0:
                print "publication_outlet: " + str(events.get('publication_outlet', None))
                print "issue: " + str(events.get('issue', None))
                print "type: " + str(events.get('type', None))
                print "volume: " + str(events.get('volume', None))
                print "year: " + str(events.get('year', None))
                print ""

doForEachPlosDoc(findRelevantData, verbose=True)
file.close()
