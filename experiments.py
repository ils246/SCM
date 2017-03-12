
from models import model0, model1
import json
import numpy as np
from random import shuffle
from joblib import Parallel, delayed
from multiprocessing import cpu_count
n_cores = cpu_count()

ticks = 20000

#           Model 0 experiments
#-----------------------------------------

#                 N,  q,  beta,   gtype
N, q,beta,net =[800, 0.005, 0.005,'complete']
output1 = ['CN800-E70-scm%d.csv' % i for i in range(10,101)]
pvals = [(i * 0.05) for i in range(1,21)]

print "Splitting into",n_cores
for j in range(len(output1)):
    rs = Parallel(n_jobs=n_cores)(delayed(model0)
    ([N, i, q, beta, net],ticks) for i in pvals)
    a = [r[0] for r in rs]
    f = open(output1[j],'w+')
    # So this will give me the list per p of length ticks
    json.dump(a,f)
    f.close()

N, q,beta,net =[900, 0.005, 0.005,'complete']
output1 = ['CN900-E71-scm%d.csv' % i for i in range(15,101)]
pvals = [(i * 0.05) for i in range(1,21)]

print "Splitting into",n_cores
for j in range(len(output1)):
    rs = Parallel(n_jobs=n_cores)(delayed(model0)
    ([N, i, q, beta, net],ticks) for i in pvals)
    a = [r[0] for r in rs]
    f = open(output1[j],'w+')
    # So this will give me the list per p of
    # length ticks
    json.dump(a,f)
    f.close()


N, q,beta,net =[1000, 0.005, 0.005,'complete']
output1 = ['CN1000-E72-scm%d.csv' % i for i in range(10,101)]
pvals = [(i * 0.05) for i in range(1,21)]

print "Splitting into",n_cores
for j in range(len(output1)):
    rs = Parallel(n_jobs=n_cores)(delayed(model0)
    ([N, i, q, beta, net],ticks) for i in pvals)
    # rs = [model0([10, i, 0.1, 0.1, 'complete'],10)  for i in pvals]
    a = [r[0] for r in rs]
    # b = [r[1] for r in rs]
    f = open(output1[j],'w+')
    # So this will give me the list per p of
    # length ticks
    json.dump(a,f)
    f.close()

    # f = open(output2[j],'w+')
    # # array that is divided by p, then by tick and the items
    # # inside are the memories of each agent.
    # json.dump(b,f)
    # f.close()


# Simulations that don't record the memories
# output3 = ['RN100-E34-scm%d.csv' % i for i in range(11,101)]
# for k in range(len(output3)):
#         results = Parallel(n_jobs=n_cores)(delayed(model0)
#         ([N, i, q, beta, net],ticks) for i in pvals)
#         c = [r[0] for r in results]
#         p = open(output3[k],'w+')
#         json.dump(c,p)
#         p.close()



#           Model 1 experiments
#-----------------------------------------

# N, pStar, pHubs, q, beta, net =[100, 0.25, 0.9, 0.01, 0.001,'scale-free']
# top=10
# pvals=[pStar]*100
#
# print ("Splitting into",n_cores)
# rs = Parallel(n_jobs=n_cores)(delayed(model1)
# ([N, i, pHubs, q, beta, net],ticks,top) for i in pvals)
# a = [r[0] for r in rs]
# f = open('SN100-E57-scm.csv','w+')
# json.dump(a,f)
# f.close()
