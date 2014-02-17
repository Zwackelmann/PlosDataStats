from main.util.common import SimpleDoc
import random
import string

def canBeEncoded(text):
    try:
        str(text)
        return True
    except UnicodeEncodeError:
        return False

def tweetsBetweenDay(documents, lowerBound, upperBound):
    return [[tweet.text, tweet.timestamp, tweet.username, doc.doi, doc.title, doc.publicationTimestamp] for doc in documents for tweet in doc.tweets 
        if 
            ((lowerBound*60*60*24) <= (tweet.timestamp - doc.publicationTimestamp) <= (upperBound*60*60*24)) and
            canBeEncoded(tweet.text) and
            canBeEncoded(doc.title)
    ]

relevantDocuments = SimpleDoc.getallBetween((2012, 6), (2012, 8))

tweets = []
tweets.extend(random.sample(tweetsBetweenDay(relevantDocuments, 0, 1), 111))
tweets.extend(random.sample(tweetsBetweenDay(relevantDocuments, 1, 3), 111))
tweets.extend(random.sample(tweetsBetweenDay(relevantDocuments, 3, 5), 111))
tweets.extend(random.sample(tweetsBetweenDay(relevantDocuments, 7, 30), 333))
tweets.extend(random.sample(tweetsBetweenDay(relevantDocuments, 100, 300), 333))

tweetTexts = map(lambda tweetdata: "\t".join([str(tweetdata[0]), str(tweetdata[1]), tweetdata[2], tweetdata[3], tweetdata[4], str(tweetdata[5])]), tweets)
random.shuffle(tweetTexts)

f = open("tweetTexts_1.txt", "w")
for text in tweetTexts[0:333]:
    f.write(text.replace("\n", " ").replace("\"", "").replace("'", "") + "\n")
f.close()

f = open("tweetTexts_2.txt", "w")
for text in tweetTexts[333:666]:
    f.write(text.replace("\n", " ") + "\n")
f.close()

f = open("tweetTexts_3.txt", "w")
for text in tweetTexts[666:999]:
    f.write(text.replace("\n", " ") + "\n")
f.close()