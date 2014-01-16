import json

from os import listdir
from os.path import isfile, join
from os.path import basename

path = "/home/toennies/plosALM/data/"
files = [ f for f in listdir(path) if isfile(join(path,f)) ]

users = []
for file in files:
    s = open(path+file)
    docMetadataList = json.load(s)
    s.close()

    for docMetadata in docMetadataList:
        sources = docMetadata['sources']
        for source in sources:
            if source['name'] == 'twitter':
                events = source['events']
                for event in events:
                    user = event['event']['user']
                    users.append(user)

f = open("users.json", "w")
f.write(json.dumps(users))
f.close()
