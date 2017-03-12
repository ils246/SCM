import itertools
from functions import talk,think,die,countby,initialize_net
from random import random,choice
import numpy as np

def model0(par, ticks,save_every=10):
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
	save_every : int (default=10)
		Save every how many ticks. save_every=0 saves at every tick.
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
		if save_every == 0 or tick % save_every == 0:
			scm = set(itertools.chain.from_iterable(memories))
			longScm.append(len(scm))
	return longScm, individualMem


def model1(par, ticks, top, save_every=10):
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
	N,pStar,pHubs,q,beta,gtype = par
	G = initialize_net(gtype,N)
	ps = set_hubs(G,N,pStar,pHubs,top)
	memories = [set() for i in range(N)]
	longScm, recordMem, individualMem = [[] for a in range(3)]
	scm =set()
	idea_tick=0

	for tick in range(ticks):
		for agent in np.random.randint(0,N,N):
			myp = random()
			if myp < ps[agent]:
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
		if save_every == 0 or tick % save_every == 0:
			scm = set(itertools.chain.from_iterable(memories))
			longScm.append(len(scm))
	return longScm, individualMem


if __name__ == "__main__":
	import time
	print ('Testing model0')
	start_time = time.time()
	rs= model0([2000,0.5,0.1,0.1,'complete'],20000)
	print ("--- %s seconds ---" % (time.time() - start_time))

	print ('Testing model1')
	start_time = time.time()
	rs= model1([2000,2000*[0.5],2000*[0.1],2000*[0.1],'complete'],20000)
	print ("--- %s seconds ---" % (time.time() - start_time))
