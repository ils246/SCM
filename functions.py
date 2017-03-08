from random import randint,choice
from collections import Counter
from networkx import barabasi_albert_graph,star_graph,connected_watts_strogatz_graph,erdos_renyi_graph
import numpy as np

def talk(agent,memories,G=None):
	'''
	Selects a random partner for agent to get a new idea from.
	(agent gets idea from partner, not the other way around)
	If G is provided, then it chooses a partner from the network.

	Parameters
	----------
	agent : int
		Agent id
	memories : list
		List of sets for all the agents
	G : networkx.Graph (optional)
		Network of connections between agents

	Returns
	-------
	memories : list
		Updated list of sets for all the agents
	'''
	N=len(memories)
	if G is None:
		partner = np.random.randint(0,N)
		while partner == agent:
			partner = np.random.randint(0,N)
	else:
		neighs = G.neighbors(agent) #Change this line to upgrade to igraph
		if len(neighs)!=0:
			partner = choice(neighs)
		else:
			return memories
	partner = memories[partner]
	if len(partner) >  0:
		borrowedIdea = choice(list(partner))
		memories[agent].add(borrowedIdea)
	return memories

def think(agent,memories,idea_tick):
	'''
	Adds a new idea to the memory of agent.
	(Successfully think)

	Parameters
	----------
	agent : int
		Agent id
	memories : list
		List of sets for all the agents
	idea_tick : int
		Keeps track of the id of the last created idea

	Returns
	-------
	memories : list
		Updated list of sets for all the agents
	idea_tick : int
		Updated counter that keeps track of the id of the last created idea
	'''
	newIdea = idea_tick
	idea_tick+=1
	memories[agent].add(newIdea)
	return memories,idea_tick

def die(agent,memories):
	'''
	Sets the memory of agent to an empty set.

	Parameters
	----------
	agent : int
		Agent id
	memories : list
		List of sets for all the agents

	Returns
	-------
	memories : list
		Updated list of sets for all the agents
	'''
	memories[agent] = set()
	return memories

def countby(seq,f=len):
	'''
	Given a sequence, it applies function f (len) and then counts each occurence.

	Parameters
	----------
	seq : list
		List of elements to which apply f to
	f : function (default=len)
		Function to apply to each one of elements in seq

	Returns
	-------
	result : dict
		Number of occurences of the key value.
	'''
	result = Counter([f(value) for value in seq])

	return result


def initialize_net(gtype,N):
	'''
	Initializes the network to be used in the simulation.

	Parameters
	----------
	gtype : str
		Graph type, can be random, scale-free, or star.
	N : int
		Number of nodes in the network.

	Returns
	-------
	G : networkx.Graph
		Graph object of the desired network.
	'''
	if gtype=='random':
		G = erdos_renyi_graph(N,0.04)
	elif gtype=='scale-free':
		m = 30
		G = barabasi_albert_graph(N,m)
	elif gtype=='star':
		G = star_graph(N)
	elif gtype=='sw':
		G = connected_watts_strogatz_graph(N,4,0.005)
	else:
		G=None
	return G
