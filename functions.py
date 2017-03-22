import numpy as np
from random import randint,choice
from collections import Counter
from networkx import barabasi_albert_graph,star_graph,connected_watts_strogatz_graph,erdos_renyi_graph,degree
from operator import itemgetter
import matplotlib.pyplot as plt
import json
import glob


#---------------------------------------
#          Functions for models
#---------------------------------------

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
		neighs = G.neighbors(agent)
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

def set_hubs(G,pStar,pHubs,top):
	'''
	Given a sequence, it applies function f (len) and then counts each occurence.

	Parameters
	----------
	G  : networkx.Graph
	pStar: float
		 p value for all the nodes that are not hubs
	pHubs: float
	     p value for hubs
	top : float
		Fracion of nodes top nodes to assing pHubs
		takes top hubs based on degree

	Returns
	-------
	ps : list
		List with pvalues for all nodes in the network
	'''
	N = len(G)
	ps = [pStar]*N
	t=int(N*top)
	topDegrees=sorted(G.degree().items(), key=itemgetter(1), reverse=True)[:t]
	for i in topDegrees:
		ps[i[0]]= pHubs
	return ps


#---------------------------------------
#       Functions for data analysis
#---------------------------------------

plotfont = {'fontname':'Arial Narrow'}

def filenames(net,exp, runNum, N, suffix, mem):
    '''
    Returns list of filenames to be analyzed given the parameters of the experiment.

    Parameters
    -----------
    exp    : int
             Experiment number
    runNum : int
    		 Number of iterations for each E / files have consecutive numbers to show iteration
    N      : int
             Population Size
    net    : str
             Network used in the simulation
    suffix : str
            'scm' / 'mem' depending on the output file that is being used
    mem    : bool
            'True' /'False' depending on the names of files requiered. Files for agent memory analysis start with 'M'
    Returns
    ------------
    filenames: list
               List of filenames to be analyzed.
    '''
    if mem:
        return ['M%sN%d-E%d-%s%d.csv' % (net,N,exp,suffix, i) for i in range(1,runNum + 1)]
    else:
        return ['%sN%d-E%d-%s%d.csv' % (net,N,exp,suffix, i) for i in range(1,runNum + 1)]

def getData(filenames):
    '''
    Takes list of filenames and returns an array of arrays
	Array is Num-of-sims X P-vals X ticks

    Parameters
    -----------
    filenames: list
               List of lists containing the names of the files to load.
    Returns
    ------------
    filenames: list
               List of data to be analyzed.
    '''
    aux1 = []
    for f in filenames:
        f = '/Volumes/Isabella/SCM/model0/RN100/'+f
        data = json.load(open(glob.glob(f)[0]))
        aux1.append(data)
    return aux1

def meanScm(data):
    '''
    Takes list of filenames and returns an array of arrays

    Parameters
    -----------
    data : list
           List of lists containing the names of the files to anayze.
    Returns
    ------------
    meanVals: list
              List of length 20 that is the average across the files in filenames.
    '''
    meanVals=[]
    for j in data:
        out = [np.mean([np.mean(f[i][500:]) for f in j]) for i in range(len(j[0]))]
        meanVals.append(out)
        out=[]
    return meanVals


def getGaps(mems, scms):
    gaps=[]
    for j in range(len(mems)):
        memdata=json.load(open(glob.glob(mems[j])[0]))
        scmdata=json.load(open(glob.glob(scms[j])[0]))
        average = [[np.mean(timestep) for timestep in pval] for pval in memdata]
        average1  = [np.mean(i) for i in average]
        scmdata1=[np.mean(i) for i in scmdata]
        gap=[scmdata1[i]-average1[i] for i in range(20)]
        gaps.append(gap)
    return gaps


#---------------------------------------
#       Functions for plotting
#---------------------------------------


def pcurves(pvallist, fig, title, filename):
    '''
    Takes list of lists of scm per pval.

    Parameters
    -----------
    pvallist : list
              List of lists with SCM per pval in that experiment.
    fig      : int
               number of figure
    title    : str
               Title of the plot
    filename : str
               Name to save the file

    Returns
    ------------
    plot of pvalist.
    '''
    plotfont = {'fontname':'Arial Narrow'}
    plt.figure(fig)
    plt.plot(pvallist, 'bo')
    plt.xlabel('P values',size=14, **plotfont)
    plt.ylabel('Social Collective Memory',size =14. **plotfont)
    plt.xticks(range(21), [round((0.05*i),2) for i in range(1,21)], size=14,**plotfont)
    plt.yticks(size=14,**plotfont)
    plt.title(title,size=16, **plotfont)
    plt.savefig(filename, bbox_inches='tight')
    plt.close()


def heatmap(M,x=None,y=None,title=None,filename=None,labels=('Beta','Q'),annotate=True):
    '''
    Makes heatmap of pvalsues or scm values across experiments.

    Parameters
    ----------
    M : np.array
        Data organized in a numpy.array.
        (A list of lists also works)
    x : list (optional)
        Tick labels for the x axis
    y : list (optional)
        Tick labels for the y axis
    title : str (optional)
        Title of the plot
    filename : str (Optional)
        If provided, the image will be saved with the given filename
    labels : tuple (default=('Beta','q'))
        Labels for the x and y axis.
    annotate : Boolean (True)
        If True it will annotate the values of the provided matrix.
    '''
    ys,xs = np.shape(M)
    x = range(xs) if x is None else x
    y = range(ys) if y is None else y
    if (len(x)!=xs)&(len(y)!=ys):
        raise NameError('Dimension of x and y do not match dimensions of M.')
    plt.figure()
    plt.imshow(M, cmap='viridis', interpolation='nearest')
    ax = plt.subplot(111)
    plt.xlabel(labels[0],color='k',size=14,**plotfont)
    plt.ylabel(labels[1],color='k',size=14, **plotfont)
    if title is not None:
        plt.title(title, **plotfont)
    plt.xticks(np.arange(len(x)), x, ha='center', **plotfont)
    plt.yticks(np.arange(len(y)), y, ha='right', **plotfont)
    ax.set_frame_on(False)
    if annotate:
        for i,pp in enumerate(M):
            for j,p in enumerate(pp):
                ax.text(j,i, str(round(p,2)),ha='center', style='italic', size=15, **plotfont)
    if filename is not None:
        plt.savefig(filename, bbox_inches='tight', transparent=True)


def model1_getdata(net, exp, hubs):

    '''
    Makes heatmap of the difference between model 0 and model1 across the 9 worlds under study.
    Makes file with the mean SCM across the 9 worlds under study.
	Makes file with the variance of SCM across the  worlds under study.

    Parameters:
    -----------
    net  : str
          Network type for which data is being analyzed ('S' - scale-free, 'R'- random)
    exp  : tuple
          Range of experiment numbers, non inclusive of last number
    hubs: int
         Number of hubs that have higher p

    Returns:
    --------
    File with mean SCM across the 9 worlds for a number of hubs.
    file with variances of SCM across the 9 worlds for a number of hubs.
    File with differences between mean SCM in model 1 and max SCM in model 0
    across the 9 worlds for a number of hubs.
    Heatmap of differences across the 9 worlds.
    '''
    filenames = ['%sN100-E%d-scm%d.csv' % (net,i,hubs) for i in range(exp[0],exp[1])]
    m1,variances=[[] for i in range(2)]
    for i in filenames:
        data=json.load(open(glob.glob(i)[0]))
        m = [np.mean(i[500:]) for i in data]
        means = np.mean(m)
        var = pvariance(m)
        m1.append(means)
        variances.append(var)

    m0_data=json.load(open(glob.glob('S-max-val.csv')[0]))
    m0=[item for sublist in m0_data for item in sublist]
    diff=[m1[i]-m0[i] for i in range(len(m1))]
    diff_array=[[diff[0+i],diff[1+i], diff[2+i]] for i in range(0,9,3)]
    heatmap(diff_array,x=[0.001, 0.01, 0.1],y=[0.1, 0.01, 0.001],title='Differences between M0 and M1 (%s% of hubs)' % hubs, filename='s-diff%d.png' % hubs)

	f=open('s-means-%d.csv' % hubs, 'w+')
    json.dump(m1,f)
    f.close()
    g=open('s-variance-%d.csv' % hubs, 'w+')
    json.dump(var,g)
    g.close()
    k=open('diff%d.csv' % hubs, 'w+')
    json.dump(diff,k)
    k.close()

def plotmemories(fig,list_of_mem, scm, filename, title):
    '''
    Takes list of lists of scm per pval.

    Parameters
    -----------
    list_of_mem : list
                  list of each agent's memories
    title       : str
                  Title of the plot
    filename    : str
                  Name to save the file
    scm         : list of social collective memory

    Returns
    ------------
    plot of memories and scm.
    '''
    for i in list_of_mem:
        plot=plt.figure(fig)
        ax1=plot.add_subplot(111)
        ax1.plot(i)
    ax1.plot(scm)
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Number of Ideas')
    plt.savefig(filename)
    plt.close()
