import json
import numpy
from scipy import interpolate
from main.util.common import readFromJson, dataPath


def interpolateDatapoint(timeline, time):
    exactMatches = filter(lambda x: x[0] == time, timeline)
    if(len(exactMatches) > 1):
        raise Exception("more than one exact match for a timepoint: " + str(exactMatches))
    elif(len(exactMatches) == 1):
        return float(exactMatches[0][1])
    else:
        f = interpolate.interp1d(map(lambda x: x[0], timeline), map(lambda x: x[1], timeline))
        return float(f(time))

def addDummyPointIfNoDataAvailable(timeline, publicationDate, delayFromPubDate):
    if(timeline[0][0] > publicationDate+delayFromPubDate):
        timeline.insert(0, [publicationDate+delayFromPubDate, 0])

lines = open(dataPath("points_filtered_2.json"), "r")

for line in lines:
    doc = json.loads(line)

    docId = doc['id']
    publicationDate = doc['publication_date']
    timeline = doc['twitter-data']

    addDummyPointIfNoDataAvailable(timeline, publicationDate, -10*24*60*60)

    normalizedTimeline = []
    for dayDiff in [-10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]:
        timePoint = publicationDate + (dayDiff * 24*60*60)
        value = interpolateDatapoint(timeline, timePoint)
        normalizedTimeline.append([dayDiff, value])

    print json.dumps({"id" : docId, "publication_date" : publicationDate, "twitter-data" : normalizedTimeline})


