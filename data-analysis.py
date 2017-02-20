from analysisFunc import filenames,getData,meanScm


#        Heatmap
#------------------------

exp = [list(i) for i in [range(1,17), range(1,17), range(1,17), range(1,17)]]
hmFiles = [[filenames(i,100,100, 'scm') for i in e] for e in exp]
hm = [getData(i) for i in hmfiles]
test = meanScm(hm)
# pmaxr1 = [pvals[i.index(max(i))] for i in meanValsrow1]
# maxval1 = [max(i) for i in meanValsrow1]
