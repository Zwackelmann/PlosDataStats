from main.util.common import doForEachPlosDoc, dataPath, readJsonFromData
import re
import json
from dateutil.parser import parse
import calendar

file = open(dataPath("document_timelines.json"), "w")

def findRelevantData(doc):
    doi = doc['doi']
    pubDate = timestr2timestamp(doc['publication_date'])
    citeULikeTimeline = None
    pubmedTimeline = None
    scopusTimeline = None
    counterTimeline = None
    counterEvents = None
    pmcTimeline = None
    pmcEvents = None
    facebookTimeline = None
    mendeleyTimeline = None
    crossrefTimeline = None
    relativemetricTimeline = None
    crossrefTimeline = None
    twitterTimeline = None

    for source in doc['sources']:
        if source['name'] == 'citeulike':
            citeULikeTimeline = map(lambda item: [timestr2timestamp(item['update_date']), item['total']], source['histories'])
        if source['name'] == 'pubmed':
            pubmedTimeline = map(lambda item: [timestr2timestamp(item['update_date']), item['total']], source['histories'])
        if source['name'] == 'scopus':
            scopusTimeline = map(lambda item: [timestr2timestamp(item['update_date']), item['total']], source['histories'])
        if source['name'] == 'pmc':
            pmcTimeline = map(lambda item: [timestr2timestamp(item['update_date']), item['total']], source['histories'])
            pmcEvents = source['events']
        if source['name'] == 'facebook':
            facebookTimeline = map(lambda item: [timestr2timestamp(item['update_date']), item['total']], source['histories'])
        if source['name'] == 'mendeley':
            mendeleyTimeline = map(lambda item: [timestr2timestamp(item['update_date']), item['total']], source['histories'])
        if source['name'] == 'crossref':
            crossrefTimeline = map(lambda item: [timestr2timestamp(item['update_date']), item['total']], source['histories'])
        if source['name'] == 'counter':
            counterTimeline = map(lambda item: [timestr2timestamp(item['update_date']), item['total']], source['histories'])
            counterEvents = source['events']
        if source['name'] == 'relativemetric':
            relativemetricTimeline = map(lambda item: [timestr2timestamp(item['update_date']), item['total']], source['histories'])
        if source['name'] == 'twitter':
            twitterTimeline = map(lambda item: [timestr2timestamp(item['update_date']), item['total']], source['histories'])

    jdoc = json.dumps([ doi, pubDate, citeULikeTimeline, pubmedTimeline, scopusTimeline, pmcTimeline, facebookTimeline, mendeleyTimeline, crossrefTimeline, counterTimeline, relativemetricTimeline ])
    file.write(jdoc + "\n")

def timestr2timestamp(timestr):
    return calendar.timegm(parse(timestr).timetuple())

doForEachPlosDoc(findRelevantData, verbose=True)
file.close()
