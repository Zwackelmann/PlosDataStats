import json
from matplotlib.pyplot import show

from hcluster import pdist, linkage, dendrogram, fcluster
import numpy
from numpy.random import rand

# load distance matrix
# distanceMatrixStream = open('distances.json')
# distanceMatrix = json.load(distanceMatrixStream)
# distanceMatrixStream.close()

# Z = linkage(distanceMatrix)
# numpy.save("dendrogram.npy", Z)
# dendrogram(Z)
# show()

Z = numpy.load("dendrogram.npy")

dendrogram(Z)
show()

clu = fcluster(Z, 2, depth=5000, criterion='distance')

cluInstances = {}
for i in clu:
	cluInstances[i] = cluInstances.get(i, 0) + 1

# numpy.save("clusters.npy", clu)
# clu = numpy.load("clusters.npy")

"""hist1 = numpy.histogram(list(cluInstances.itervalues()))

print len(cluInstances.keys())
print hist1[0]
print map(lambda x: int(x), hist1[1])"""