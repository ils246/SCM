
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
output1 = ['CN800-E70-scm%d.csv' % i for i in range(1,101)]
pvals = [(i * 0.05) for i in range(1,21)]

print "Splitting into",n_cores
for j in range(len(output1)):
    rs = Parallel(n_jobs=n_cores)(delayed(model0)
    ([N, i, q, beta, net],ticks) for i in pvals)
    a = [r[0] for r in rs]
    f = open(output1[j],'w+')
    json.dump(a,f)
    f.close()


#      Model 0 experiments with memory
#-----------------------------------------



#           Model 1 experiments
#-----------------------------------------

filenames = ['RN100-E%d-scm8.csv' % i for i in range(44,53)]
list_of_params = [[100, 0.2, 0.9, 0.1, 0.001,'random',0.08],   [100, 0.2, 0.9, 0.1, 0.01,'random',0.08],   [100, 0.2, 0.9, 0.1, 0.1,'random',0.08],
                  [100, 0.3, 0.9, 0.01, 0.001,'random',0.08],  [100, 0.2, 0.9, 0.01, 0.01,'random',0.08],  [100, 0.45, 0.9, 0.01, 0.1,'random',0.08],
                  [100, 0.2, 0.9, 0.001, 0.001,'random',0.08], [100, 0.65, 0.9, 0.001, 0.01,'random',0.08], [100, 0.85, 0.9, 0.001, 0.1,'random',0.08]]

for i in range(len(list_of_params)):
    print ("Splitting into",n_cores)
    print "Working on", filenames[i]
    N, pStar, pHubs, q, beta, net, top = list_of_params[i]
    pvals=[pStar]*250
    rs = Parallel(n_jobs=n_cores)(delayed(model1)
    ([N, i, pHubs, q, beta, net, top],ticks) for i in pvals)
    a = [r[0] for r in rs]
    f = open(filenames[i],'w+')
    json.dump(a,f)
    f.close()
