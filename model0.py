import itertools
from functions import talk,think,die,countby
from random import random,choice
import networkx as nx
import json
#import igraph as ig


def sim(par, ticks):
    N,p,q,beta,gtype = par

    if gtype=='random':
        r = 4/N
        G = nx.gnp_random_graph(N,r)
    elif gtype=='scale-free':
        m = 30
        G = nx.barabasi_albert_graph(N,m)
    else:
        G=None

    pop = [dict.fromkeys(['q', 'p', 'beta']) for n in range(N)]
    pList=[ p ] * N
    memories = [set() for i in range(N)]

    for i,agent in enumerate(pop):
        agent['q'] = q
        agent['beta'] = beta
        agent['p'] = pList[i]

    longScm = []
    recordMem = []
    scm =set()
    idea_tick=0
    for tick in range(ticks):
        for i in range(N):
            agent = choice(range(N))
            params=pop[agent]
            myp = random()
            if myp < params['p']:
                memories = talk(agent,memories,G=G)
            else:
                myq = random()
                if myq < params['q']:
                    memories,idea_tick = think(agent,memories,idea_tick)
            b = random()
            if b < params['beta']:
                memories = die(agent,memories)
        if tick % 10 == 0:
            scm = set(itertools.chain.from_iterable(memories))
            longScm.append(len(scm))
        if tick == ticks - 1:
            memAux = countby(len, memories)
    return longScm, memAux


pvals = [(i * 0.05) for i in range(1,21)]

# mylist = []
# for i in pvals:
#     r = sim([1000, i, 0.01, 0.01],10000)
#     mylist.append(r[0])

output1 = ['CN100-P1-scm%d.csv' % i for i in range(1,10)]
output2 = ['CN100-P1-mem%d.csv' % i for i in range(1,10)]

# output1 = ['world2-scm.csv']
# output2 = ['world2-mem.csv']



from joblib import Parallel, delayed
from multiprocessing import cpu_count
n_cores = cpu_count()

# print "Splitting into",n_cores
for j in range(len(output1)):
    rs = Parallel(n_jobs=n_cores)(delayed(sim)([100, i, 0.1, 0.01, 'complete'],20000) for i in pvals)
    # rs = [sim([100, i, 0.005, 0.005, 'complete'],20000)  for i in pvals]
    a = [r[0] for r in rs]
    b = [r[1] for r in rs]
    f = open(output1[j],'w+')
    json.dump(a,f)  ## So this will give me the list per p of length ticks
    f.close()

    f = open(output2[j],'w+')
    json.dump(b,f) ## 3D array that is divided by p, then by tick and the items inside are the memories of each agent.
    f.close()


# sabemos poco
#
# los sistemas nerviosos y como la communicacion afecta la capcaidad de estos sitemas para andcuando os sitemas estan hipercomunicados e
# inovaion -> l gente va a decir que la innovacion biende hablar on la gente



#for j in range(len(output1)):
#    a,b = [[] for i in range(2)]
#    for i in pvals:
#        r = sim([100, i, 0.001, 0.01, 'complete'],10000)
#        a.append(r[0])
#        b.append(r[1])
#    f = open(output1[j],'w+')
#    json.dump(a,f)  ## So this will give me the list per p of length ticks
#    f.close()
#    f = open(output2[j],'w+')
#    json.dump(b,f) ## 3D array that is divided by p, then by tick and the items inside are the memories of each agent.
#    f.close()
