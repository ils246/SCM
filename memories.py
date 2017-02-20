

'''This scirpt runs simulations that record the memories and then plots them
        to show the gap between individual memory and collective memory'''


def model0_memories(par, ticks):
	'''
	Runs Model 0 for the given set of parameters and the given number of timesteps.
    The difference with the 'Model 0' is that this model records the SCM at ech tick,
    not every 10 ticks. This is desirable here because the data from this model is to be
    analyzed case by case, hence we only need to run it a few times. 

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
		scm = set(itertools.chain.from_iterable(memories))
		longScm.append(len(scm))
	return longScm, individualMem

pvals = [(i * 0.05) for i in range(1,21)]
rs = [model0([10, i, 0.1, 0.1, 'complete'],10)  for i in pvals]
a = [r[0] for r in rs]
b = [r[1] for r in rs]
f = open(output1[j],'w+')
json.dump(a,f)
f.close()

f = open(output2[j],'w+')
json.dump(b,f)
f.close()
