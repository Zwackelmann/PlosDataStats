import json
import time

minTweetsToRegardDocument = 5

maxDaysUntilFirstTweet = 50
minDaysUntilLastTweet = 150
minNumDaysWithTweets = 150

lines = open("points_filtered.json", "r")

# load doi2Publicationdate Map
doi2PublicationdateMapStream = open('doi_publicationdate_map.json')
doi2PublicationdateMap = json.load(doi2PublicationdateMapStream)
doi2PublicationdateMapStream.close()

for line in lines:
    doc = json.loads(line)
    
    docId = doc['id']
    timelineSorted = sorted(doc['twitter-data'], key=lambda limelineItem: limelineItem[0])

    maxTweets = timelineSorted[-1][1]

    if(maxTweets >= minTweetsToRegardDocument):
    	if(doi2PublicationdateMap.get(docId, None) != None):
    		publicationDateTimestamp = int(time.mktime(time.strptime(doi2PublicationdateMap[docId][:10], "%Y-%m-%d")))
    		timelineSortedAsTimestamps = map(lambda timelineItem: [timelineItem[0] / 1000, timelineItem[1]], timelineSorted)

    		# filter by timeline data available
    		pubDateToFirst = timelineSortedAsTimestamps[0][0] - publicationDateTimestamp
    		pubDateToLast = timelineSortedAsTimestamps[-1][0] - publicationDateTimestamp
    		span = timelineSortedAsTimestamps[-1][0] - timelineSortedAsTimestamps[0][0]

    		if(
    			pubDateToFirst <= maxDaysUntilFirstTweet*24*60*60 and 
    			pubDateToLast >= minDaysUntilLastTweet*24*60*60 and 
    			span >= minNumDaysWithTweets*24*60*60
    		):
    			print json.dumps({"id" : docId, "publication_date" : publicationDateTimestamp, "twitter-data" : timelineSortedAsTimestamps})

