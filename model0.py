import itertools
from functions import talk,think,die,countby,initialize_net
from random import random,choice
import numpy as np

def model0(par, ticks):
	'''
	Runs Model 0 for the given set of parameters and the given number of timesteps.

	Parameters
	----------
	par : tuple
		Parameters of the simulation.
		N,p,q,beta,gtype
	ticks : int
		Number of ticks to run the simulation for.

	Returns
	-------
	longScm : list
		Size of Social Collective Memory as a function of time, recorded every 10 ticks.
	individualMem : list
		List of lists.
		It contains the lengths of the individual memories as a function of time.
	'''
	N,p,q,beta,gtype = par
	G = initialize_net(gtype,N)
	memories = [set() for i in range(N)]
	longScm, recordMem, individualMem = [[] for a in range(3)]
	scm =set()
	idea_tick=0

	for tick in range(ticks):
		for agent in np.random.randint(0,N,N):
			myp = random()
			if myp < p:
				memories = talk(agent,memories,G=G)
			else:
				myq = random()
				if myq < q:
					memories,idea_tick = think(agent,memories,idea_tick)
			b = random()
			if b < beta:
				memories = die(agent,memories)
		tempMem = [len(mem) for mem in memories]
		individualMem.append(tempMem)
		if tick % 10 == 0:
			scm = set(itertools.chain.from_iterable(memories))
			longScm.append(len(scm))
	return longScm, individualMem


def model1(par, ticks):
	'''
	Runs Model 1 for the given set of parameters and the given number of timesteps.

	Parameters
	----------
	par : tuple
		Parameters of the simulation.
		Parameters p,q, and beta can be iterables of size N or floats.
		N,p,q,beta,gtype
	ticks : int
		Number of ticks to run the simulation for.

	Returns
	-------
	longScm : list
		Size of Social Collective Memory as a function of time, recorded every 10 ticks.
	individualMem : list
		List of lists.
		It contains the lengths of the individual memories as a function of time.
	'''
	N,p,q,beta,gtype = par
	pList = p if hasattr(p,'__getitem__') else None
	qList = q if hasattr(q,'__getitem__') else None
	bList = beta if hasattr(beta,'__getitem__') else None
	G = initialize_net(gtype,N)
	memories = [set() for i in range(N)]
	longScm, recordMem, individualMem = [[] for a in range(3)]
	scm =set()
	idea_tick=0

	for tick in range(ticks):
		for agent in np.random.randint(0,N,N):
			myp = random()
			p = p if pList is None else pList[agent]
			if myp < p:
				memories = talk(agent,memories,G=G)
			else:
				myq = random()
				q = q if qList is None else qList[agent]
				if myq < q:
					memories,idea_tick = think(agent,memories,idea_tick)
			beta = beta if bList is None else bList[agent]
			b = random()
			if b < beta:
				memories = die(agent,memories)
		tempMem = [len(mem) for mem in memories]
		individualMem.append(tempMem)
		if tick % 10 == 0:
			scm = set(itertools.chain.from_iterable(memories))
			longScm.append(len(scm))
	return longScm, individualMem


if __name__ == "__main__":
	import time
	print 'Testing model0'
	start_time = time.time()
	rs= model0([100,0.5,0.1,0.1,'complete'],1000)
	print "--- %s seconds ---" % (time.time() - start_time)

	print 'Testing model1'
	start_time = time.time()
	rs= model1([100,100*[0.5],100*[0.1],100*[0.1],'complete'],1000)
	print "--- %s seconds ---" % (time.time() - start_time)
