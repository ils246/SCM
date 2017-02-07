import matplotlib.pyplot as plt
from scipy import stats
import json
import numpy as np
import glob


#         Load data
#----------------------------

# Returns list of filenames to be analyzed
def filenames(E, runNum, N, suffix):
    filenames = ['CN%d-E%d-%s%d.csv' % (N,E,suffix, i) for i in range(1,runNum + 1)]
    return filenames

# Takes list of filenamaes and returns an array of arrays
# Array is Num-of-sims X P-vals X ticks
def getData(filenames):
    aux1 = []
    for f in filenames:
        # f = 'model0-data/model0-data/'+f
        data = json.load(open(glob.glob(f)[0]))
        aux1.append(data)
    return aux1

def meanScm(data):
    meanVals=[]
    for j in data:
        out = [np.mean([np.mean(f[i][500:]) for f in j]) for i in range(len(j[0]))]
        meanVals.append(out)
        out=[]
    return meanVals




#         Heatmap
#----------------------------

pvals = [i*0.05 for i in range(2,21)]
experiments = list(range(3,4))
files=[filenames(i,99,100, 'scm') for i in experiments]

# for i in files:
#     for j in i:
#         print(glob.glob(j))
data = [getData(i) for i in files]
test = meanScm(data)

print (test)
