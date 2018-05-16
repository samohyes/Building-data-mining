# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 00:41:57 2018

@author: ChaoboZhang
"""

from itertools import combinations

#提取频繁集中所有可能的项组合情况
def extractItems(freqItem):
    extrItems=[]
    for i in sorted(range(1,len(freqItem)),reverse=True):
        extrItems.append(list(combinations(freqItem, i))) #函数功能：自动提取组合
    return extrItems

def generateRules(freqItems, dataSetLen, minConf = 0.7, minLift = 1):
    bigRuleList = []
    freqItemsKey = list(freqItems.keys())
    for freqItem in freqItemsKey:
        if len(freqItem) > 1:
            calcConf(freqItem, freqItems, dataSetLen, bigRuleList, minConf, minLift)
    return bigRuleList

def calcConf(freqItem, freqItems, dataSetLen, brl, minConf = 0.7, minLift = 1):
    extrItems = extractItems(freqItem)
    for antecedentSet in extrItems:
        for antecedent in antecedentSet:
            antecedent = frozenset(antecedent)
            sup = freqItems[freqItem] / dataSetLen
            conf = freqItems[freqItem] / freqItems[antecedent] #antecedent表示先验，置信度等于先验和结论同时发生的支持度除以先验的支持度
            sup_con = freqItems[freqItem - antecedent] / dataSetLen
            lift = conf/sup_con
            if conf >= minConf and lift > minLift:
                #print (antecedent, '-->', freqItem - antecedent, 'sup:', sup, 'conf:', conf, 'lift:', lift)
                rule = {}
                rule[antecedent] = freqItem - antecedent
                brl.append((rule, antecedent, freqItem - antecedent, sup, conf, lift))
                