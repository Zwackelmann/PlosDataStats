import numpy as np

def histDisc(plt, x, bins = None, width = 0.35):
    dataMap = { }
    for value in x:
        dataMap[value] = dataMap.get(value, 0) + 1

    if bins == None:
        bins = dataMap.keys()
        bins.sort()

    values = list(dataMap[key] for key in bins)
    labels = map(lambda x: str(x), bins)

    totalBars = len(bins)
    ind = np.arange(totalBars)

    ax = plt.axes()
    rects = ax.bar(ind+width/2, values, width, color='r')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(labels, rotation='horizontal')
    plt.yticks(xrange(0, 30001, 2000))
    ax.set_yticklabels(["0", "2k", "4k", "6k", "8k", "10k", "12k", "14k", "16k", "18k", "20k", "22k", "24k", "26k", "28k", "30k"], rotation='horizontal')
    # ax.set_ylabel('Scores')
    # ax.set_title('Scores by group and gender')


def barPlot(plt, labels, values, width = 0.35):
    totalBars = len(values)
    ind = np.arange(totalBars)

    ax = plt.axes()
    for valueRow in values:
        print valueRow
        rects = ax.bar(ind+width/2, valueRow, width, color='r')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(labels)

    # ax.set_ylabel('Scores')
    # ax.set_title('Scores by group and gender')

def hist(x, bounds):
    bins = { }

    for val in x:
        if val >= bounds[0]:
            for i in range(0, len(bounds)-1):
                if val < bounds[i+1]:
                    bins[i] = bins.get(i, 0) + 1
                    break

    labels = []
    for i in range(0, len(bounds)-1):
        lowerBound = bounds[i]
        upperBound = bounds[i+1] - 1

        if(lowerBound == upperBound):
            labels.append(str(lowerBound))
        else:
            labels.append(str(lowerBound) + " - " + str(upperBound))

    values = map(lambda x: x[1], sorted(bins.items(), key=lambda x: x[0]))

    return labels, values

def pieData(binDescriptions, x):
    bins = [0] * len(binDescriptions)
    
    for d in x:
        for i in range(0, len(binDescriptions)):
            if binDescriptions[i][0](d):
                bins[i] += 1

    total = sum(bins)
    relBins = 0.0
    relBins = map(lambda x: float(x)*100 / total, bins)

    labels = map(lambda x: x[0][1] + '(' + str(x[1]) + ')', zip(binDescriptions, bins))

    return relBins, labels

def paperFigure(plt):
    plt.figure(num=None, figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')


    