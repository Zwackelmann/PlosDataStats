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
from dateutil.parser import parse
import calendar

file = open(dataPath("relevant_document_data.json"), "w")

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
    pdfViews = None
    htmlViews = None
    citeULikeShares = None
    citeULikeTotal = None
    connoteaCitations = None
    connoteaTotal = None
    natureCitations = None
    natureTotal = None
    postgenomicCitations = None
    postgenomicTotal = None
    pubmedCitations = None
    pubmedTotal = None
    scopusCitations = None
    scopusTotal = None
    pmcPdf = None
    pmcHtml = None
    facebookShares = None
    facebookComments = None
    facebookLikes = None
    facebookTotal = None
    mendeleyGroups = None
    mendeleyShares = None
    mendeleyTotal = None
    relativemetricTotal = None

    for source in doc['sources']:
        if source['name'] == 'citeulike':
            metrics = source['metrics']
            citeULikeShares = metrics['shares']
            citeULikeTotal = metrics['total']
        if source['name'] == 'connotea':
            metrics = source['metrics']
            connoteaCitatinos = metrics['citations']
            connoteaTotal = metrics['total']
        if source['name'] == 'nature':
            metrics = source['metrics']
            natureCitatinos = metrics['citations']
            natureTotal = metrics['total']
        if source['name'] == 'postgenomic':
            metrics = source['metrics']
            postgenomicCitatinos = metrics['citations']
            postgenomicTotal = metrics['total']
        if source['name'] == 'pubmed':
            metrics = source['metrics']
            pubmedCitatinos = metrics['citations']
            pubmedTotal = metrics['total']
        if source['name'] == 'scopus':
            metrics = source['metrics']
            scopusCitatinos = metrics['citations']
            scopusTotal = metrics['total']
        if source['name'] == 'pmc':
            metrics = source['metrics']
            pmcPdf = metrics['pdf']
            pmcHtml = metrics['html']
        if source['name'] == 'facebook':
            metrics = source['metrics']
            facebookShares = metrics['shares']
            facebookComments = metrics['comments']
            facebookLikes = metrics['likes']
            facebookTotal = metrics['total']
        if source['name'] == 'twitter':
            twitterData = extractRelevantTwitterData(source)
        if source['name'] == 'mendeley':
            metrics = source['metrics']
            mendeleyGroups = metrics['groups']
            mendeleyShares = metrics['shares']
            mendeleyTotal = metrics['total']

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
            citationTimeline = map(lambda x: [timestr2timestamp(x['update_date']), x['total']], source['histories'])
            citations = []
            for event in source['events']:
                event = event['event']
                issn = event.get('issn', None)
                publication_type = event.get('publication_type', None)
                doi = event.get('doi', None)
                citations.append([doi, issn, publication_type])

        if source['name'] == 'counter':
            counterMetrics = source.get('metrics', None)
            if counterMetrics:
                pdfViews = counterMetrics.get('pdf', None)
                htmlViews = counterMetrics.get('html', None)
        if source['name'] == 'relativemetric':
            metrics = source['metrics']
            relativemetricTotal = metrics['total']


    jdoc = json.dumps([doi, title, timestr2timestamp(pubDate), twitterData, citationTimeline, citations, mendeleyDisciplineList, mendeleyReaders, issn, issue, volume, pdfViews, htmlViews, citeULikeShares, citeULikeTotal, connoteaCitations, connoteaTotal, natureCitations, natureTotal, postgenomicCitations, postgenomicTotal, pubmedCitations, pubmedTotal, scopusCitations, scopusTotal, pmcPdf, pmcHmtl, facebookShares, facebookComments, facebookLikes, facebookTotal, mendeleyGroups, mendeleyShares, mendeleyTotal, relativemetricTotal])
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
        
        tweetData = [text, user, retweetUser, timestr2timestamp(date)]
        tweets.append(tweetData)

    return tweets

def timestr2timestamp(timestr):
    return calendar.timegm(parse(timestr).timetuple())

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
