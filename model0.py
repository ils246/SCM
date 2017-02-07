import itertools
from functions import talk,think,die,countby,initialize_net
from random import random,choice
import numpy as np

def model0(par, ticks):
	'''
	Runs the Model 0 for the given set of parameters and the given number of timesteps.

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

	pList=[ p ] * N
	pop = [{'q':q,'p':pList[n],'beta':beta} for n in range(N)] # make three arrays instead of a list because it will save memory
	memories = [set() for i in range(N)]

	longScm, recordMem, individualMem = [[] for a in range(3)]
	scm =set()
	idea_tick=0

	for tick in range(ticks):
		for agent in np.random.randint(0,N,N):
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
	return longScm, individualMem



 if __name__ == "__main__":
	import time
	print 'Testing model0'
	start_time = time.time()
	rs= model0([5000,0.5,0.1,0.1,'complete'],4000)
	t = open('finaltest.csv', 'w+')
	t.write("--- %s seconds ---" % (time.time() - start_time))
	t.close()
