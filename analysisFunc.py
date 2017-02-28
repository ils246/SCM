import matplotlib.pyplot as plt
from scipy import stats
import json
import numpy as np
import glob


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
        # f = 'model0-data/model0-data/'+f
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

def getmemdata(datafile, pval,agent):
    '''
    Takes memory file and a list of all the agent's memories in time.

    Parameters
    -----------
    datafile : list
               List of lists containing all of the agent's memories per tick.
    pval     : int
               position in the list of pvals to be used.
    agent    : int
               Agent (index number) whose memory is to be recovered
    Returns
    ------------
    meanVals: list
              List of length N, each N is of length ticks.
    '''
    a=[]
    for i in range(len(datafile[0])):
        a.append(datafile[pval][i][agent])
    return a

#         p curves
#----------------------------
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
    plt.xlabel('P values', **plotfont)
    plt.ylabel('Social Collective Memory', **plotfont)
    plt.xticks(range(21), [round((0.05*i),2) for i in range(1,21)], size=10,**plotfont)
    plt.yticks(size=11,**plotfont)
    plt.title(title, **plotfont)
    plt.savefig(filename, bbox_inches='tight')

#         Heatmap
#----------------------------


def heatmap(M,x=None,y=None,title=None,filename=None,labels=('Beta','q'),annotate=True):
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
    plt.xlabel(labels[0],color='k',size=15)
    plt.ylabel(labels[1],color='k',size=16)
    if title is not None:
        plt.title(title, **plotfont)
    plt.xticks(np.arange(len(x))+0.5, x, ha='right')
    plt.yticks(np.arange(len(y))+0.5, y, ha='right')
    ax.set_frame_on(False)
    if annotate:
        for i,pp in enumerate(M):
            for j,p in enumerate(pp):
                ax.text(j,i, str(p),ha='center', style='italic', size=15)
    if filename is not None:
        plt.savefig(filename, bbox_inches='tight', transparent=True)

#        Memory-SCM gap
#----------------------------

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
