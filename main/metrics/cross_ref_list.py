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

from main.util.common import doForEachPlosDoc, dataPath
import re
import json

crossrefs = {}
def findRelevantData(doc):
    doi = doc['doi']
    refs = []

    for source in doc['sources']:
        if source['name'] == 'crossref':
            events = source['events']
            if len(events) != 0:
                for event in [event['event'] for event in events]:
                    issn = event.get('issn', None)
                    referencingDoi = event.get('doi', None)
                    publicationType = event.get('publication_type', None)
                    
                    refs.append({'doi' : referencingDoi, 'issn' : issn, 'type' : publicationType})

    crossrefs[doi] = refs


file = open(dataPath("crossrefs.json"), "w")
doForEachPlosDoc(findRelevantData, verbose=True)
file.write(json.dumps(crossrefs))
file.close()
