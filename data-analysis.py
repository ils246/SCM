from analysisFunc import filenames,getData,meanScm, pcurves, getmemdata,heatmap
import glob
import json
import numpy as np
import matplotlib.pyplot as plt
from math import log


# List of experiements to be analyzed organized by row of heatmap
rows = [list(i) for i in [range(26,29), range(29,32), range(32,35)]]

# Names of the files to be analyzed
# files_row = [filenames('C',i,100,100, 'scm', mem=False) for i in range(7,8)]
# Hierarchy of row1:
    #Level0: length=4, items=Experiments
        #Level1: length=100, items=iterations of each Experiment
            #Level2: length=20, items= pvalues
                #level3: length=2000, items=Collective Memory per tick
# data_row = [getData(i) for i in files_row]

# List of the average behavior across the 100 iterations of each Experiment
# length = number of experiments, in this case 4
# means_row = meanScm(data_row)
# pcurves(means_row,0,'test', 'test.png')

#        P curves
#------------------------
# Plot SCM as a function of p
# Points in the plot are the average of the 100 iterations per experiement

pvals=[0.05*i for i in range(21)]
pmax,maxval=[[] for i in range(2)]
for row in range(len(rows)):
    counter=0
    files_row = [filenames('R',i,50,100, 'scm', mem=False) for i in rows[row]]
    data_row=[getData(j) for j in files_row]
    means_row = meanScm(data_row)
    pmaxr = [pvals[i.index(max(i))] for i in means_row]
    pmax.append(pmaxr)
    maxvalr = [max(i) for i in means_row]
    maxval.append(maxvalr)
    titles=['Random Network - Experiment %d' % i for i in rows[row]]
    files = ['RN%d.png' % i for i in rows[row]]
    for i in means_row:
        pcurves(i,counter,titles[counter], files[counter])
        counter+=1

# f=open('R-max-p.csv', 'w+')
# json.dump(pmax,f)
# f.close()
# g=open('R-max-val.csv', 'w+')
# json.dump(maxval,g)
# g.close()

#        Heatmap
#------------------------

# plotfont = {'fontname':'Arial Narrow'}
# hm_pvalues = json.load(open(glob.glob('R-max-p.csv')[0]))
# heatmap(hm_pvalues,x=[0.0001,0.001, 0.01, 0.1],y=[0.1, 0.01, 0.001],title='Model 0 - Complete Network p Values',filename='C-heatmap-pvals.pdf')
#
# hm_values = json.load(open(glob.glob('R-max-val.csv')[0]))
# hm_values = [[log(x) for x in j] for j in hm_values]
# heatmap(hm_values,x=[0.0001,0.001, 0.01, 0.1],y = [0.1, 0.01, 0.001],title='Model 0 - Complete Network log SCM Values',filename='C-heatmap-scmvals.pdf')
