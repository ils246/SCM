import itertools
from functions import talk,think,die,countby,initialize_net
from random import random,choice
from models import model0_memories
import numpy as np
import json


'''This scirpt runs simulations that record the memories and then plots them
        to show the gap between individual memory and collective memory'''

output1 = ['CN100-E2-scm-all%d.csv' % i for i in range(1,6)]
output2 = ['CN100-E2-mem-all%d.csv' % i for i in range(1,6)]

pvals = [(i * 0.05) for i in range(1,21)]

for j in range(len(output1)):
	#  N,   ,p, q,  beta,     gtype
    rs = [model0_memories([100, i, 0.1, 0.001, 'complete'],20000)  for i in pvals]
    a = [r[0] for r in rs]
    b = [r[1] for r in rs]
    f = open(output1[j],'w+')
    json.dump(a,f)
    f.close()

    f = open(output2[j],'w+')
    json.dump(b,f)
    f.close()

# 0.1 = 1, 0.5 = 9, 0.8=15
# memories('CN100-E2-mem-all%d.csv', 'CN100-E2-scm-all%d.csv',1,9,15, 'test0.1', 'test0.5', 'test0.5' )
