import json
import re

lines = open("/home/simon/dois", "r")

doi = None
publicationDate = None
documents = {}

doiRe = re.compile('"doi": "([^"]*)"')
publicationDateRe = re.compile('"publication_date": "([^"]*)"')


def endDoc():
    global doi
    global publicationDate

    if doi != None and publicationDate != None:
        documents[doi] = publicationDate

    doi = None
    publicationDate = None

for line in lines:
    m = doiRe.search(line)
    if m:
        doi = m.group(1)
    else:
        m = publicationDateRe.search(line)
        if m:
            publicationDate = m.group(1)
        else:
            if line[:2] == "--":
                endDoc()

print json.dumps(documents)
