from main.util.common import DocumentTimelines, SimpleDoc, timestr2timestamp
import matplotlib.pyplot as plt
import numpy as np
from main.util.plotting import barPlot, paperFigure
import json
import string
import calendar
import datetime

def differencesInTimeline(publicationTimestamp, timeline, borders):
    if len(timeline) == 0:
        return None
    else:
        values = []
        for i in range(0, len(borders)-1):
            timePointsInRange = filter(lambda x: borders[i]*60*60*24 <= x[0]-publicationTimestamp <= borders[i+1]*60*60*24, timeline)
            if len(timePointsInRange) != 0:
                values.append(max(timePointsInRange, key=lambda x: x[0])[1])
            else:
                values.append(None)

        return values

def earliestTimestampForMetric(metric):
    return min(filter(lambda point: point != None, 
        map(lambda timeline: next( ( point for point in timeline if point[1] != 0 ), None ), 
            map(lambda doc: getattr(doc, metric), DocumentTimelines.fromFile("data/document_timelines.json"))
        )
    ), key=lambda x: x[0])[0]


# print earliestTimestampForMetric("mendeleyTimeline")

# Timelines:
# citeULikeTimeline, pubmedTimeline. scopusTimeline, pmcTimeline, 
# facebookTimeline, mendeleyTimeline, crossrefTimeline, 
# counterTimeline, relativemetricTimeline

"""docsTimelines = DocumentTimelines.fromFile("data/document_timelines.json")

f = open("foo", "w")
for doc in docsTimelines:
    d2 = doc.trimmed()
    d2.publicationTimestamp = timestr2timestamp(d2.publicationTimestamp)

    f.write(d2.toJson(trimmed=True) + "\n")

f.close()"""

maxTimestamp = SimpleDoc.maximumTimestampInDataset
print maxTimestamp

numObservedDays = 500

docsTimelines = DocumentTimelines.fromFile("data/document_timelines_trimmed.json", trimmed=True, sort=True)
attributes = [ ("scopusTimeline", (3,9)), ("crossrefTimeline", (3,9)), ("pubmedTimeline", (3,9)) ]

"""[("citeULikeTimeline", (3,9)), ("pubmedTimeline", (3,9)),
    ("scopusTimeline", (3, 9)), ("pmcTimeline", (6, 11)), ("facebookTimeline", (12, 11)), 
    ("mendeleyTimeline", (1, 12)), ("crossrefTimeline", (3, 9)), ("counterTimeline", (9, 9)),
    ("facebookTimeline", (12, 11)), ("mendeleyTimeline", (1, 12)), ("citeULikeTimeline", (3,9))]"""

for toleranceDays in [2]:
    toleranceSeconds = toleranceDays*60*60*24
    ways = {}
    ys = []
    for attribute, startDate in attributes:
        lowerBound = calendar.timegm(datetime.date(2000+startDate[1], startDate[0], 1).timetuple())
        upperBound = maxTimestamp - (300*60*60*24)

        docsTimelines2 = filter(lambda doc: 
            doc.publicationTimestamp > lowerBound,
            docsTimelines
        )

        print "start: " + attribute + ", " + str(toleranceDays)
        windows = []

        for i in range(0, numObservedDays):
            windows.append([])

        for doc in docsTimelines2:
            pub = doc.publicationTimestamp
            timeline = getattr(doc, attribute) # filter(lambda point: point[0] < pub+(numObservedDays*60*60*24), getattr(doc, attribute))

            if len(timeline) >= 1 and timeline[-1][0] >= pub+(60*60*24*(numObservedDays)):
                for relativeDay in range(0, numObservedDays):
                    time = (relativeDay*60*60*24)+pub
                    point, way = DocumentTimelines.valueAtTime(timeline, time, toleranceSeconds)
                    ways[way] = ways.get(way, 0) + 1

                    if point != None:
                        windows[relativeDay].append(point)

        validValues = map(lambda x: len(x), windows)
        print validValues

        ys.append(map(lambda values: np.mean(values), windows))
        
    paperFigure(plt)


print ways

"""docs = SimpleDoc.getallBetween((2012, 5), (2012, 8))

avgTweetsOnDay = []
for relDay in range(0, numObservedDays):
    tweetsOnDay = []
    for doc in docs:
        tweetsOnDay.append(len(filter(lambda tweet: tweet.timestamp < doc.publicationTimestamp+(relDay*60*60*24), doc.tweets)))
    avgTweetsOnDay.append(np.mean(tweetsOnDay))

ys.append(avgTweetsOnDay)"""

x = range(0, numObservedDays)

plots = []
for y in ys:
    plot, = plt.plot(x, y)
    plots.append(plot)

plt.xlabel("day")
plt.ylabel("avg value of metric")
plt.xlim((0, numObservedDays))
plt.legend(plots, [ "Scopus", "CrossRef", "PubMed" ], loc=2)
plt.tight_layout()
plt.show()