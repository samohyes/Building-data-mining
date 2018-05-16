import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.cluster import KMeans
from operator import itemgetter
import seaborn as sns
import fpgrowth
import generaterules

with open('SAX_day_weekday_cp_sys.basket') as f:
    content = f.readlines()
content = [x.strip() for x in content]
content = content[1:]

ruleset = []
temp = []
for i in range(5422):
    if(float(content[i].split(',')[-1]) > float(content[i+1].split(',')[-1])):
        temp.append(content[i])
        ruleset.append(temp)
        temp = []
    else:
        temp.append(content[i])

fitdata = []
for j in range(len(ruleset)):
    datamid = []
    for i in range(len(ruleset[j])):
        datamid.append(ruleset[j][i].split(',')[:-1])
    fitdata.append(datamid)

###fitdata contains the data for every week
itemset = fpgrowth.createInitSet(fitdata[2])
minSup = 0.1
itemnumber = 3
retTree, headerTable = fpgrowth.createTree(itemset, sum(itemset.values()), minSup=minSup)
freqItems = {}
fpgrowth.mineTree(inTree=retTree, headerTable=headerTable, dataSetLen=sum(itemset.values()), 
                  itemnumber = itemnumber, minSup = minSup, freqItemList = freqItems)
minConf = 0.7 
minLift = 0.9
ruleset = generaterules.generateRules(freqItems = freqItems, dataSetLen = sum(itemset.values()), 
                                      minConf = minConf, minLift = minLift)
print(ruleset)
