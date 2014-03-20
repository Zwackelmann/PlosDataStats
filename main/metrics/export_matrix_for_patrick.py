import json
from main.util.common import SimpleDoc

metrics = [
    ("Crossref", lambda doc: doc.numCrossrefs()),
    ("PubMed", lambda doc: doc.pubmedCitations),
    ("Scopus", lambda doc: doc.scopusCitations),
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

"""docs = SimpleDoc.getallBetween((2012,6), (2012,8))

docs2 = []
for doc in docs:
    data = []
    data.append(map(lambda tweet: tweet.username, doc.tweets))
    data.extend(map(lambda metric: metric[1](doc), metrics))
    docs2.append(data)

f = open("corpus.json", "w")
f.write(json.dumps(docs2))
f.close()"""

docs = json.load(open("corpus.json"))
print len(docs)