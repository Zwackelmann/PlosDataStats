import json
from matplotlib.pyplot import show

from hcluster import pdist, linkage, dendrogram, fcluster
import numpy
from numpy.random import rand
from main.util.common import dataPath

# load distance matrix

# Z = linkage(distanceMatrix)
# numpy.save("dendrogram.npy", Z)
# dendrogram(Z)
# show()

Z = numpy.load(dataPath("dendrogram.npy"))

dendrogram(Z)
show()

clu = fcluster(Z, 2, depth=5000, criterion='distance')

cluInstances = {}
for i in clu:
    cluInstances[i] = cluInstances.get(i, 0) + 1

# numpy.save(dataPath("clusters.npy"), clu)
# clu = numpy.load(dataPath("clusters.npy"))

"""hist1 = numpy.histogram(list(cluInstances.itervalues()))

print len(cluInstances.keys())
print hist1[0]
print map(lambda x: int(x), hist1[1])"""
