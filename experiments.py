
from model0 import model0
import json
from joblib import Parallel, delayed
from multiprocessing import cpu_count
n_cores = cpu_count()

params = [100, i, 0.1, 0.01,'complete']
ticks = 20000

#Simulations that do record the memories
output1 = ['CN100-E1-scm%d.csv' % i for i in range(1,11)]
output2 = ['CN100-E1-mem%d.csv' % i for i in range(1,11)]
pvals = [(i * 0.05) for i in range(1,21)]

print "Splitting into",n_cores
for j in range(len(output1)):
    rs = Parallel(n_jobs=n_cores)(delayed(model0)
    (params,ticks) for i in pvals)
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
output3 = ['CN100-E1-scm%d.csv' % i for i in range(11,101)]
for k in range(len(output3)):
        results = Parallel(n_jobs=n_cores)(delayed(model0)
        (params,ticks) for i in pvals)
        c = [r[0] for r in results]
        p = open(output3[k],'w+')
        json.dump(c,p)
        p.close()
