import json
import numpy
import matplotlib.pyplot as plt

lines = open("points_filtered_2.json", "r")

def formatHist(hist):
	print '     ' + str(map(lambda x: "%5d" % x, hist[0]))
	print map(lambda x: "%5d" % int(x/60/60/24), hist[1])
	print sum(hist[0])


distancesToFirstPost = []
distancesToLastPost = []
firstToLastPost = []

count = 0
for line in lines:
    doc = json.loads(line)

    docId = doc['id']
    publicationDate = doc['publication_date']
    timeline = doc['twitter-data']

    timelineSotred = sorted(timeline, key = lambda timelineItem: timelineItem[0])

    pubDateToFirst = timelineSotred[0][0] - publicationDate
    pubDateToLast = timelineSotred[-1][0] - publicationDate
    span = timelineSotred[-1][0] - timelineSotred[0][0]

    """if(pubDateToFirst < 50*24*60*60):
    	distancesToFirstPost.append(pubDateToFirst)

    if(span > 200*24*60*60):
    	firstToLastPost.append(span)"""

    if(pubDateToFirst < 50*24*60*60 and pubDateToLast > 150*24*60*60 and span > 150*24*60*60):
    	count += 1

print count

# hist1 = numpy.histogram(distancesToFirstPost, bins=10)
# hist2 = numpy.histogram(distancesToLastPost, bins=10)
# hist3 = numpy.histogram(firstToLastPost, bins=10)    

# formatHist(hist1)
# formatHist(hist3)