"""
# WTF!?
docs = [
    [ ['a', 'b', 'c', 'd'], [1, 2, 3] ], 
    [ ['d', 'e'], [4, 5, 6] ], 
    [ ['g', 'h', 'i'], [7, 8, 9] ]
]

print docs
totalStrings = sum((1 for doc in docs for doc[0] in doc))
print docs"""

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

t = np.arange(0.0, 1.0, 0.1)
s = np.sin(2*np.pi*t)
linewidths = [ 1.0, 2.0, 2.0, 3.0 ]
linestyles = ['-', '-.', '--', ':']
colors = ('b', 'g', 'r', 'k', 'm', 'y', 'k')

axisNum = 0
for row in range(len(linestyles)):
    axisNum += 1
    ax = plt.subplot(1, len(linestyles), axisNum)
    color = colors[(axisNum-1) % len(colors)]
    plt.plot(t, s, linestyles[(axisNum-1)], color=color, linewidth=linewidths[(axisNum-1)])

    ax.set_yticklabels([])
    ax.set_xticklabels([])

plt.show()