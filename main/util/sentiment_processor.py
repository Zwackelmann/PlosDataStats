import json
from main.util.common import Sentiment

class TweetForSentiment:
    def __init__(self, string):
        splitted = string.split("\t")

        self.tweetText = splitted[0]
        self.tweetTimestamp = splitted[1]
        self.tweetUser = splitted[2]
        self.docDoi = splitted[3]
        self.docTitle = splitted[4]
        self.docPublicationTimestamp = splitted[5]

    def ident(self):
        return (self.tweetTimestamp, self.tweetUser, self.docDoi)

    @staticmethod
    def getTweetsForSentiment():
        l = []
        lines = open("tweetTexts_simon.txt", "r")

        for line in lines:
            l.append(TweetForSentiment(line))

        return l

"""
for tweet in Sentiment.tweetsForSentiment:
    if not sentimentAvailable(tweet.ident()):
        print "Tweet text:\n" + tweet.tweetText + "\n\nDoc Title:\n" + tweet.docTitle + "\n\n"
        classification = raw_input("=> ")
        print "\n\n"

        appendSentiment(tweet.ident(), classification)
"""