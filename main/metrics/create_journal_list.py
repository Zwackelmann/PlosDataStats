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

mendeleyPublicationOutlets = []
def findRelevantData(doc):
    for source in doc['sources']:
        if source['name'] == 'mendeley':
            events = source['events']
            if len(events) != 0:
                if 'publication_outlet' in events:
                    mendeleyPublicationOutlets.append(events['publication_outlet'])

file = open(dataPath("publication_outlets.json"), "w")
doForEachPlosDoc(findRelevantData, verbose=True)
file.write(json.dumps(mendeleyPublicationOutlets))
file.close()
