from main.util.db import openDb
import json
from scipy import stats
from main.util.common import SimpleDoc, powerset, Log

db = openDb("stuff/localconnect.json")

metrics = [
    ("Crossref", lambda doc: doc.numCrossrefs()),
    ("PubMed", lambda doc: doc.pubmedCitations),
    ("Scopus", lambda doc: doc.scopusCitations),
    ("Max Citations", lambda doc: doc.maxCitations()),
    ("PLOS pdf", lambda doc: doc.pdfViews),
    ("PLOS HTML", lambda doc: doc.htmlViews),
    ("PMC pdf", lambda doc: doc.pmcPdf),
    ("PMC HTML", lambda doc: doc.pmcHtml),
    ("Facebook Shares", lambda doc: doc.facebookShares),
    ("Facebook Comments", lambda doc: doc.facebookComments),
    ("Facebook Likes", lambda doc: doc.facebookLikes),
    ("Mendeley Readers", lambda doc: doc.mendeleyReaders),
    ("CiteULike", lambda doc: doc.citeULikeShares)
]

l = Log(filename="foo", verbose=True)

metricNames = map(lambda metric: metric[0], metrics)
docs = map(lambda doc: [map(lambda tweet: tweet.username, doc.tweets), map(lambda metric: metric[1](doc), metrics)], SimpleDoc.getallBetween((2012,6), (2012,8)))

topCategories = ['Medicine', 'Sports', 'Culture', 'Technology', 'Education', 'Health', 
    'Business', 'Belief', 'Humanities', 'Society', 'Life', 'Arts', 'Language', 'Law', 
    'History', 'Geography', 'Agriculture', 'Politics', 'Mathematics', 'Science', 
    'Nature', 'Environment', 'People', 'Chronology' ]

excludeCategories = [ "Education", "Business", "Belief", "Society", "Language", "Mathematics", "Science" ]


baseline = { }

for ind, metricName in zip(range(0, len(metricNames)), metricNames):
    pairs = []
    for doc in docs:
        numTweets = len(doc[0])
        metricScore = doc[1][ind]
        pairs.append([numTweets, metricScore])

    x, y = zip(*pairs)
    s, p = stats.spearmanr(x, y)

    baseline[metricName] = s

for cats in powerset(excludeCategories):
    l.log("analyze categories: " + repr(cats))

    cur = db.cursor()
    sql = """
    SELECT DISTINCT screen_name AS expert 
    FROM twitter_id_2_screenname AS t2s 
    JOIN users_professions_2 AS up2 ON up2.user_id=t2s.twitter_id
    WHERE up2.cat_title IN (%s)
    """ % ((", ".join(map(lambda cat: "'" + cat + "'", cats))) if len(cats) != 0 else "''")
    print sql
    cur.execute(sql)

    patrickExperts = set()
    for row in cur.fetchall():
        patrickExperts.add(row[0])

    scores = { }
    for ind, metricName in zip(range(0, len(metricNames)), metricNames):
        pairs = []
        for doc in docs:
            numExpertTweets = sum((1 for usr in doc[0] if not usr in patrickExperts))
            metricScore = doc[1][ind]
            pairs.append([numExpertTweets, metricScore])

        x, y = zip(*pairs)
        s, p = stats.spearmanr(x, y)

        scores[metricName] = s

    for metricName in metricNames:
        l.log("%-20s: %1.3f %1.3f" % (metricName, scores[metricName], (scores[metricName]-baseline[metricName])))

    l.log("\n\n")

l.close()