# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 20:29:01 2018

@author: Admin
"""

import fpgrowth
import generaterules

#导入数据，转化为相应的形式
testdata = fpgrowth.loadSimpData()
print(testdata)
itemset = fpgrowth.createInitSet(testdata)

#设置参数，minSup为最小支持度，itemnumber为频繁集中的项数
minSup = 0.1
itemnumber = 3

#生成树和项头表
retTree, headerTable = fpgrowth.createTree(itemset, sum(itemset.values()), minSup=minSup)
print(itemset)
#生成频繁项
freqItems = {}
fpgrowth.mineTree(inTree=retTree, headerTable=headerTable, dataSetLen=sum(itemset.values()), itemnumber = itemnumber, minSup = minSup, freqItemList = freqItems)

#从频繁集中挖掘相关规则
minConf = 0.8 #最小置信度
minLift = 1.3 #最小提升度
ruleset = generaterules.generateRules(freqItems = freqItems, dataSetLen = sum(itemset.values()),  minConf = minConf, minLift = minLift)

#规则形式：
# ({frozenset({'t'}): frozenset({'x'})},
#  frozenset({'t'}), 先验
#  frozenset({'x'}), 结论
#  0.5, 支持度
#  1.0,置信度
#  1.5 提升度)