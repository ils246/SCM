
from model0 import model0
import json
# from joblib import Parallel, delayed
# from multiprocessing import cpu_count
# n_cores = cpu_count()

output1 = ['CN100-P1-scm%d.csv' % i for i in range(1,10)]
output2 = ['CN100-P1-mem%d.csv' % i for i in range(1,10)]



pvals = [(i * 0.05) for i in range(1,21)]
#
# output1 = ['CN100-P1-scm%d.csv' % i for i in range(1,2)]
# output2 = ['CN100-P1-mem%d.csv' % i for i in range(1,2)]

print "Splitting into",n_cores
for j in range(len(output1)):
    # rs = Parallel(n_jobs=n_cores)(delayed(model0)([10, i, 0.1, 0.01,
    # 'complete'],100) for i in pvals)
    rs = [model0([10, i, 0.1, 0.1, 'complete'],10)  for i in pvals]
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
