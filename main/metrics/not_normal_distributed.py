import numpy as np
from main.util.common import SimpleDoc, applyCall
import matplotlib.pyplot as plt
from main.util.plotting import barPlot, paperFigure

attributeList = [
    (("numTweets", ()), (2012, 5), "Tweets"), 
    (("facebookTotal", ()), (2011, 12), "Facebook"), 
    (("mendeleyReaders", None), (2012, 1), "Mendeley readers"), 
    (("citeULikeShares", None), (2009, 3), "CiteULike shares"), 
    (("plosViews", ()), (2009, 9), "PLOS views"), 
    (("pmcViews", ()), (2011, 6), "PMC views"), 
    (("maxCitations", ()), (2009, 3), "Citations")
]

attributeNames = map(lambda x: x[0][0], attributeList)
attributePrintNames = map(lambda x: x[2], attributeList)
calls = map(lambda x: x[0], attributeList)
stats = []

for ind, attr in zip(range(0, len(attributeList)), attributeList):
    call = attr[0]
    lowerBound = attr[1]
    attName = attr[0][0]

    valuesForMetric = filter(lambda x: x != None, map(lambda doc: applyCall(doc, call),
        SimpleDoc.getallBetween(lowerBound, None)
    ))

    minV, maxV, meanV, std = min(valuesForMetric), max(valuesForMetric), np.mean(valuesForMetric), np.std(valuesForMetric)
    stats.append((attName, call, meanV, std, len(valuesForMetric)))
    print attName + "\t" + "\t".join(map(lambda x: str(x), [minV, maxV, meanV, std]))


statValues = []
for stat in stats:
    name = stat[0]
    call = stat[1]
    mean = stat[2]
    std = stat[3]
    numValues = stat[4]

    valuesForMetric = filter(lambda x: x != None, map(lambda doc: applyCall(doc, call),
        SimpleDoc.getallBetween(lowerBound, None)
    ))

    values, bins = np.histogram(valuesForMetric, bins = [mean-std, mean, mean+std, mean+2*std, 1000000000])
    sumValues = sum(values)
    values = map(lambda x: float(x)/sumValues, values)
    statValues.append(values)

# barPlot(plt, ["<my", "<my+si", "<my+2si", "<my+3si"], statValues)
# plt.show()

def barChart(plt, matrix, xLabels, legendLabels, yLabel, colors):
    N = len(xLabels)
    M = len(legendLabels)
    print N
    print M


    ind = np.arange(N)
    width = 0.90*(1.0/M)   # the width of the bars
    ax = plt.axes()

    rects = []
    for i, row in zip(range(0, M), matrix):
        rects.append(ax.bar(0.05+ind+(i*width), row, width, color=colors[i]))

    ax.set_ylabel(yLabel)
    ax.set_xticks(0.05+ind+(0.5*M)*width)
    ax.set_xticklabels( xLabels , fontsize=15 )
    plt.ylim((0, 1.0))


    ax.legend( map(lambda r: r[0], rects), legendLabels )

paperFigure(plt)

barChart(
    plt, 
    statValues, 
    [r'[$\mu-\sigma,  \mu$[', r'[$\mu,  \mu+\sigma$[', r'[$\mu+\sigma,  \mu+2\sigma$[', r'[$\mu+2\sigma,  \infty$]'],
    attributePrintNames,
    "%documents in interval",
    ['r', 'y', 'g', 'b', 'm', 'k', '0.75']
)

plt.tight_layout()
plt.show()