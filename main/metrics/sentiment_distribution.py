from main.util.common import Sentiment
from main.util.plotting import paperFigure
import matplotlib.pyplot as plt

sentiments = Sentiment.fromFile("sentiments_all.json")

x = []
classes = ["1", "2", "3", "4"]
for index, classif in zip(range(0, len(classes)), classes):
    xn = []
    for sentiment in filter(lambda s: s.classification==classif, sentiments):
        doc = sentiment.doc()
        publicationTimestamp = doc.publicationTimestamp
        tweetTimestamp = sentiment.id_tweetTimestamp
        classification = sentiment.classification

        print int(tweetTimestamp)
        xn.append((int(tweetTimestamp)-publicationTimestamp)/(60*60*24))

    x.append(xn)

paperFigure(plt)
plt.hist(x, label=["negative", "neutral", "positive", "t+l"], bins = [ -10, 0, 5, 10, 30, 100, 300 ], normed=True)
plt.legend()
plt.show()

