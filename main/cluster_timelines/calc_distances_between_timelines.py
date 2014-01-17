import json
import numpy
from scipy import interpolate
import mlpy
from main.util.common import readFromJson

lines = readFromJson("normalized_points.json")

timelines = map(lambda line: map(lambda x: x[1], json.loads(line)['twitter-data']), lines)
numTimelines = len(timelines)

distances = []

for i in range(0, numTimelines):
    for j in range(i+1, numTimelines):
        distances.append(mlpy.dtw_std(timelines[i], timelines[j]))

print json.dumps(distances)
