
from models import model0, model1
import json
import numpy as np
from random import shuffle
from joblib import Parallel, delayed
from multiprocessing import cpu_count
n_cores = cpu_count()


#           Model 0 experiments
#-----------------------------------------
#
#                 N,  q,  beta,   gtype
N, q,beta,net =[100, 0.001, 0.1,'random']
ticks = 20000

#Simulations that do record the memories
output1 = ['RN100-E34-scm%d.csv' % i for i in range(1,11)]
output2 = ['RN100-E34-mem%d.csv' % i for i in range(1,11)]
pvals = [(i * 0.05) for i in range(1,21)]

print "Splitting into",n_cores
for j in range(len(output1)):
    rs = Parallel(n_jobs=n_cores)(delayed(model0)
    ([N, i, q, beta, net],ticks) for i in pvals)
    # rs = [model0([10, i, 0.1, 0.1, 'complete'],10)  for i in pvals]
    a = [r[0] for r in rs]
    b = [r[1] for r in rs]
    f = open(output1[j],'w+')
    # So this will give me the list per p of
    # length ticks
    json.dump(a,f)
    f.close()

    f = open(output2[j],'w+')
    # array that is divided by p, then by tick and the items
    # inside are the memories of each agent.
    json.dump(b,f)
    f.close()


# Simulations that don't record the memories
output3 = ['RN100-E34-scm%d.csv' % i for i in range(11,101)]
for k in range(len(output3)):
        results = Parallel(n_jobs=n_cores)(delayed(model0)
        ([N, i, q, beta, net],ticks) for i in pvals)
        c = [r[0] for r in results]
        p = open(output3[k],'w+')
        json.dump(c,p)
        p.close()


#           Model 1 experiments
#-----------------------------------------

# N,p, q, beta,net =[100, 0.2, 0.001, 0.01, 'complete']
# ticks = 20000
# pvals = [p]*N
# for i in range(10):
#     item = np.random.randint(N)
#     pvals[item]=0.1
#
#
# #Simulations that do record the memories
# output1 = ['CN100-E24-scm%d.csv' % i for i in range(1,10)]
# output2 = ['CN100-E24-mem%d.csv' % i for i in range(1,10)]
#
# print "Splitting into",n_cores
# for j in range(len(output1)):
#     rs = Parallel(n_jobs=n_cores)(delayed(model1)
#     ([N, i, q, beta, net],ticks) for i in [pvals]) # supongo que para que cambie entonces le pones shuffle antes del pval
#     # rs = [model0([10, i, 0.1, 0.1, 'complete'],10)  for i in pvals]
#     a = [r[0] for r in rs]
#     b = [r[1] for r in rs]
#     f = open(output1[j],'w+')
#     # So this will give me the list per p of
#     # length ticks
#     json.dump(a,f)
#     f.close()
#
#     f = open(output2[j],'w+')
#     # array that is divided by p, then by tick and the items
#     # inside are the memories of each agent.
#     json.dump(b,f)
#     f.close()
#
# # # Simulations that don't record the memories
# output3 = ['CN100-E25-scm%d.csv' % i for i in range(11,101)]
# for k in range(len(output3)):
#         results = Parallel(n_jobs=n_cores)(delayed(model1)
#         ([N, i, q, beta, net],ticks) for i in [pvals])
#         c = [r[0] for r in results]
#         p = open(output3[k],'w+')
#         json.dump(c,p)
#         p.close()
