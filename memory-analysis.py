# from analysisFunc import memories, getmemdata
import json
import matplotlib.pyplot as plt
import glob
# from analysisFunc import getmemdata
# output1 = ['CN100-E2-scm-all%d.csv' % i for i in range(1,6)]
# output2 = ['CN100-E2-mem-all%d.csv' % i for i in range(1,6)]
#
# 0.1 = 1, 0.5 = 9, 0.8=15
# memories('CN100-E2-mem-all1.csv', 'CN100-E2-scm-all1.csv',1,9,15, 'test0.1', 'test0.5', 'test0.5' )

def plotmemories(fig,list_of_mem, scm, filename, title):
    plt.figure(fig)
    for i in mems1:
        plt.plot(i)
    plt.plot(scm)
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Number of Ideas')
    plt.savefig(filename)

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


mem = json.load(open(glob.glob('CN100-E2-mem-all1.csv')[0]))
scm = json.load(open(glob.glob('CN100-E2-scm-all1.csv')[0]))

mems1=[getmemdata(mem,3,j) for j in range(100)]
mems2=[getmemdata(mem,9,j) for j in range(100)]
mems3=[getmemdata(mem,15,j) for j in range(100)]

plotmemories(1,mems1, scm[3], 'mem-E2-1.1.pdf', 'Collective Memory Gap: E2 p=0.2')
plotmemories(2,mems2, scm[9], 'mem-E2-1.2.pdf', 'Collective Memory Gap: E2 p=0.5')
plotmemories(3,mems2, scm[15], 'mem-E2-1.3.pdf', 'Collective Memory Gap: E2 p=0.8')

mem = json.load(open(glob.glob('CN100-E2-mem-all2.csv')[0]))
scm = json.load(open(glob.glob('CN100-E2-scm-all2.csv')[0]))

mems1=[getmemdata(mem,3,j) for j in range(100)]
mems2=[getmemdata(mem,9,j) for j in range(100)]
mems3=[getmemdata(mem,15,j) for j in range(100)]

plotmemories(4,mems1, scm[3], 'mem-E2-2.1.pdf', 'Collective Memory Gap: E2 p=0.2')
plotmemories(5,mems2, scm[9], 'mem-E2-2.2.pdf', 'Collective Memory Gap: E2 p=0.5')
plotmemories(6,mems2, scm[15], 'mem-E2-2.3.pdf', 'Collective Memory Gap: E2 p=0.8')
