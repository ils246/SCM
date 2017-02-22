from analysisFunc import filenames,getData,meanScm, meanSimple, pcurves, getmemdata,heatmap
import glob
import json
import numpy as np
import matplotlib.pyplot as plt
from math import log


# Number of iterations per experiment
iterations=100

# List of experiements to be analyzed organized by row of heatmap
rows = [list(i) for i in [range(1,5), range(5,9), range(9,13)]]

# Names of the files to be analyzed
# files_row1 = [filenames(i,100,100, 'scm') for i in rows[2]]

# Hierarchy of row1:
    #Level0: length=4, items=Experiments
        #Level1: length=100, items=iterations of each Experiment
            #Level2: length=20, items= pvalues
                #level3: length=2000, items=Collective Memory per tick
# data_row1 = [getData(i) for i in files_row1]

# List of the average behavior across the 100 iterations of each Experiment
# length = number of experiments, in this case 4
# means_row1 = meanScm(data_row1)

#        P curves
#------------------------
# Plot SCM as a function of p
# Points in the plot are the average of the 100 iterations per experiement

# titles = ['Complete Network - Experiment %d' % i for i in range(5,9)]
# files = ['E%d.png' % i for i in range(5,9)]
# for i in range(len(means_row1)):
#     pcurves(means_row1[i], i, titles[i], files[i])

pvals=[0.05*i for i in range(21)]
pmax,maxval=[[] for i in range(2)]
for row in range(len(rows)):
    files_row = [filenames(i,100,100, 'scm') for i in rows[row]]
    data_row = [getData(i) for i in files_row]
    means_row = meanScm(data_row)
    pmaxr = [pvals[i.index(max(i))] for i in means_row]
    pmax.append(pmaxr)
    maxvalr = [max(i) for i in means_row]
    maxval.append(maxvalr)
    titles = ['Complete Network - Experiment %d' % i for i in range(1,len(means_row)+1)]
    files = ['E%d-test.png' % i for i in range(1,len(means_row)+1)]
    for i in range(len(means_row)):
        pcurves(means_row[i], i, titles[i], files[i])

f=open('max-p.csv', 'w+')
json.dump(pmax,f)
f.close()
g=open('max-val.csv', 'w+')
json.dump(maxval,g)
g.close()

#        Heatmap
#------------------------

plotfont = {'fontname':'Arial Narrow'}

hm_pvalues = json.load(open(glob.glob('max-p.csv')[0]))
heatmap(hm_pvalues,x=[0.0001, 0.001, 0.01, 0.1],y = [0.1, 0.01, 0.001],title='Model 0 Heatmap p Values',filename='heatmap-pvals.pdf')

hm_values = json.load(open(glob.glob('max-val.csv')[0]))
hm_values = [[log(x) for x in j] for j in hm_values]
heatmap(hm_pvalues,x=[0.0001, 0.001, 0.01, 0.1],y = [0.1, 0.01, 0.001],title='Model 0 Heatmap log SCM Values',filename='heatmap-scmvals.pdf')

#       Memories
#------------------------

#Hierarchy of mem
#Level0: length=20, items= list per pvalue
    #Level 1: length=20,000, items=list per tick of agents' memories
        #Level 2: length=100, items= number of ideas per agent

mem = json.load(open(glob.glob('CN100-E2-mem2.csv')[0]))
scm = json.load(open(glob.glob('CN100-E2-scm2.csv')[0]))

# a=[]
# for i in range(len(mem[0])):
#     a.append(mem[0][i][0])
#
# mems1 ->pval = 0.2
# mems2 ->pval = 0.5
# mems3 ->pval = 0.8
mems1=[getmemdata(mem,3,j) for j in range(100)]
mems2=[getmemdata(mem,9,j) for j in range(100)]
mems3=[getmemdata(mem,15,j) for j in range(100)]


def plotmemories(list_of_mem, scm, filename, title):
    for i in mems1:
        plt.plot(i)
    plt.plot(scm)
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Number of Ideas')
    plt.savefig(filename)

plotmemories(mems1, scm[3], 'testing.pdf')




#Parking lot:


# a =[]
# for pval in mem:
#     for i in range(len(pval[0])):
#         a.append(pval[i][0])




# b= [[[np.mean(pval[500:]) for pval in file_] for file_ in experiment] for experiment in row1]

            # if len(aux) <= 19:
            #     x = np.mean(pval[500:])
            #     aux.append(x)
            #     test.append(x)
            # else:
            #     mean_for_p.append(aux)
            #     aux=[]
            #     x = np.mean(pval[500:])
            #     aux.append(x)
            #     test.append(x)




            # mean_for_p.append(x)
# print(len(mean_for_p))
# print(len(mean_for_p[0]))
# print(test)
# print(len(test))
#
#

# print('')
# for experiment in row1:
#     print(1)
    # print('experiment 2 p0.5', experiment[0], len(experiment[0]) )
# test=[np.mean(a[500:]) for a in i]




# b = [[np.mean(a[500:]) for a in i]) for i in row1]
# for i in range(len(b)):
#     c=[]
#     c.append()
#
# print(len(b))
# print(len(b[0]))
#










    # print(simpleMean(i))

# test = simpleMean(row1)
# print(len(test))

# print(len(row1), len(row1[0]))
# test = meanSimple(row1)
# print(test)
# hmFiles = [[filenames(i,100,100, 'scm') for i in e] for e in exp]
# hm = [getData(i) for i in hmfiles]
# test = meanScm(hm)
# pmaxr1 = [pvals[i.index(max(i))] for i in meanValsrow1]
# maxval1 = [max(i) for i in meanValsrow1]

#ROW 1
# hmfiles1 = [filenames(i, 100, 100, 'scm') for i in exp[0]]
# print(len(hmfiles1), len(hmfiles1[0]))
