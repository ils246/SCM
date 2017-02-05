import itertools
from functions import talk,think,die,countby
from random import random,choice
import networkx as nx
import json
import time
start_time = time.time()

def sim(par, ticks):
    N,p,q,beta,gtype = par

    if gtype=='random':
        r = 4/N
        G = nx.gnp_random_graph(N,r)
    elif gtype=='scale-free':
        m = 30
        G = nx.barabasi_albert_graph(N,m)
    elif gtype=='star':
        G = nx.star_graph(N)
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
    individualMem = []
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
        tempMem = [len(mem) for mem in memories]
        individualMem.append(tempMem)
        if tick % 10 == 0:
            scm = set(itertools.chain.from_iterable(memories))
            longScm.append(len(scm))
        # if tick == ticks - 1:
        #     memAux = countby(len, memories)
    return longScm, individualMem

rs= sim([2000,0.5,0.1,0.1,'complete'],20000)
t = open('testfile.csv', 'w+')
t.write("--- %s seconds ---" % (time.time() - start_time))
