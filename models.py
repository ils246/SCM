import itertools
from functions import talk,think,die,countby,initialize_net
from random import random,choice
import numpy as np

def _master(par, ticks,G=None, save_every=10,save_individual=False):
	'''
	Master function to run all models.

	Parameters
	----------
	par : tuple
		Parameters of the simulation.
		Parameters p,q, and beta can be iterables of size N or floats.
		N,p,q,beta
	ticks : int
		Number of ticks to run the simulation for.
	G : networkx.Graph (optional)
		Graph of the social network.
		If not provided, it will use fully connected.
	save_every : int (default=10)
		Save every save_every ticks.
	save_individual : boolean (True)
		If True, it will return the individual memories as well.

	Returns
	-------
	longScm : list
		Size of Social Collective Memory as a function of time, recorded every 10 ticks.
	individualMem : list
		List of lists if save_individual is True, else is None.
		It contains the lengths of the individual memories as a function of time.
	'''
	N,p,q,beta = par
	pList = p if hasattr(p,'__getitem__') else None
	qList = q if hasattr(q,'__getitem__') else None
	bList = beta if hasattr(beta,'__getitem__') else None
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
		if save_individual:
			individualMem.append(tempMem)
		if save_every == 0 or tick % save_every == 0:
			scm = set(itertools.chain.from_iterable(memories))
			longScm.append(len(scm))
	if save_individual:
		return longScm, individualMem
	else:
		return longScm,None

def model0(par, ticks,save_every=10,save_individual=True):
	'''
	Runs Model 0 for the given set of parameters and the given number of timesteps.

	Parameters
	----------
	par : tuple
		Parameters of the simulation.
		N,p,q,beta,gtype
	ticks : int
		Number of ticks to run the simulation for.
	save_every : int (default=10)
		Save every save_every ticks.
	save_individual : boolean (True)
		If True, it will return the individual memories as well.

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
	if len(par)!=5:
		raise NameError('Parameters must be N,p,q,beta,gtype')
	N,p,q,beta,gtype = par
	G = initialize_net(gtype,N)
	longScm, individualMem = _master((N,p,q,beta), ticks,G=G, save_every=save_every,save_individual=save_individual)
	return longScm, individualMem


def model1(par, ticks, save_every=10,save_individual=True):
	'''
	Runs Model 1 for the given set of parameters and the given number of timesteps.

	Parameters
	----------
	par : tuple
		Parameters of the simulation.
		N,pStar,pHubs,q,beta,gtype,top
	ticks : int
		Number of ticks to run the simulation for.
	save_every : int (default=10)
		Save every save_every ticks.
	save_individual : boolean (True)
		If True, it will return the individual memories as well.

	Returns
	-------
	longScm : list
		Size of Social Collective Memory as a function of time, recorded every 10 ticks.
	individualMem : list
		List of lists.
		It contains the lengths of the individual memories as a function of time.
	'''
	if len(par)!=7:
		raise NameError('Parameters must be N,pStar,pHubs,q,beta,gtype,top')
	N,pStar,pHubs,q,beta,gtype,top = par
	G = initialize_net(gtype,N)
	ps = set_hubs(G,pStar,pHubs,top)
	longScm, individualMem = _master((N,p,q,beta), ticks,G=G, save_every=save_every,save_individual=save_individual)
	return longScm, individualMem

def model0_old(par, ticks,save_every=10):
	'''
	THIS FUNCTION WILL BE DELETED SOON
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


def model1_old(par, ticks, top, save_every=10):
	'''
	THIS FUNCTION WILL BE DELETED SOON
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
