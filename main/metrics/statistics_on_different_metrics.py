from os import listdir
from os.path import isfile, join
from os.path import basename
import re
import json
import numpy
from main.common.util import readFromJson

def formatHist(hist):
    print '     ' + str(map(lambda x: "%5d" % x, hist[0]))
    print map(lambda x: "%5d" % x, hist[1])


"""path = "/home/toennies/plosALM/data/"
files = [ f for f in listdir(path) if isfile(join(path,f)) ]
        
nameRe = re.compile('"name": "([^"]*)"')
totalRe = re.compile('"total": ([0-9]*)')

maxLinesToCheck = 20

matches = []

for file in files:
    lines = open(path+file, "r")
       
    distToMatchLine = None
    matchName = None

    for line in lines:
        if distToMatchLine == None:
            match = nameRe.search(line)
            if match:
                matchName = match.group(1)
                distToMatchLine = 1

        elif distToMatchLine < maxLinesToCheck:
            match = totalRe.search(line)
            if match:
                matchTotal = int(match.group(1))
                matches.append([matchName, matchTotal])

                distToMatchLine = None
                matchName = None
            else:
                distToMatchLine = distToMatchLine + 1
        else:
            distToMatchLine = None
            matchName = None


f = open("result.json", "w")
f.write(json.dumps(matches))
f.close()"""

"""matchesStream = open('result.json')
matches = json.load(matchesStream)
matchesStream.close()

dict = {}
for item in matches:
    list = dict.get(item[0], [])
    list.append(item[1])

    dict[item[0]] = list

f = open("result_grouped.json", "w")
f.write(json.dumps(dict))
f.close()"""

irrelevant = ['scienceseeker', 'postgenomic', 'bloglines', 'biod', 'nature', 'connotea', 'wikipedia', 'f1000', 'researchblogging']
boundsPerSource = {
    'twitter' : (1, 30),
    'counter' : (1, 5000),
    'scopus' : (1, 50),
    'citeulike' : (1, 10),
    'pubmed' :  (1, 25),
    'facebook' : (1, 50),
    'pmc' : (1, 1000),
    'mendeley' : (1, 50),
    'relativemetric' : (1, 350000),
    'figshare' : (1, 15),
    'crossref' : (1, 30)
}

groupedResults = readFromJson('result_grouped.json')

for key in filter(lambda x: x not in irrelevant, groupedResults.keys()):
    values = groupedResults[key]
    bounds = boundsPerSource[key]
        
    hist = numpy.histogram(filter(lambda x: x>=bounds[0] and x<=bounds[1], values), bins=10)
    numOverScale = sum(1 for x in values if x>bounds[1])
        
    print "\n\n"
    print key + ":"
    for i in range(0, len(hist[0])):
        numDocuments = 0
        for j in range(i, len(hist[0])):
            numDocuments += hist[0][j]
        numDocuments += numOverScale

        print ">= " + str(int(round(hist[1][i]))) + ": " + str(numDocuments)



































