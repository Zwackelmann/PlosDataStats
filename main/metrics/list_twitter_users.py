import json

from os import listdir
from os.path import isfile, join
from os.path import basename
from main.util.common import plosDataFiles, plosDataBaseDir, readAsJson, writeJsonToData, doForEachPlosDoc

users = []

def getRelevantData(plosDoc):
    global users
    sources = plosDoc['sources']
    for source in sources:
        if source['name'] == 'twitter':
            events = source['events']
            for event in events:
                user = event['event']['user']
                users.append(user)


doForEachPlosDoc(getRelevantData)

writeJsonToData(users, "users.json")
