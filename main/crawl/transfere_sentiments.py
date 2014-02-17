from main.util.sentiment_processor import Sentiment
import re

fin = open("tweetTexts_benni_results.txt", "r")
fout = open("sentiments_benni.json", "w")
for line in fin:
    data = map(lambda x: x.strip(), re.split(" +", line))

    fout.write(Sentiment((data[1], data[2], data[3]), data[0]).asJsonString() + "\n")

