# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 16:40:55 2018

@author: ChaoboZhang
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#算法来源：http://blog.csdn.net/sinat_17196995/article/details/71191869
#https://www.cnblogs.com/qwertWZ/p/4510857.html

#FP树中节点的类定义
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None #nodeLink 变量用于链接相似的元素项
        self.parent = parentNode #指向当前节点的父节点
        self.children = {} #空字典，存放节点的子节点

    def inc(self, numOccur):#计数加1
        self.count += numOccur

#将树以文本形式显示
    def disp(self, ind=1):
        print ('  ' * ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind + 1)

#构建FP-tree
def createTree(dataSet, dataSetLen, minSup=0.5): #输入参数：数据集，数据集长度，最小支持度
    headerTable = {}
    for trans in dataSet:  #第一次遍历：统计各个数据的频繁度
        for item in trans:
            #dict.get(key, default=None)，key：表示字典中要查找的键，default：如果指定键的值不存在时，返回该默认值值。
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
            #用头指针表统计各个类别的出现的次数，计算频繁量：头指针表[类别]=出现次数
    for k in list(headerTable):  #删除未达到最小频繁度的数据
        if headerTable[k] / dataSetLen < minSup:
            del (headerTable[k])
########修改后########
    freqItemSet = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1], reverse=True)]#保存达到要求的数据（按从大到小顺序）
########修改后########
########修改前########
    #freqItemSet = set(headerTable.keys())#保存达到要求的数据
########修改前########
    #print ('freqItemSet: ',freqItemSet)
    if len(freqItemSet) == 0:
        return None, None
    for k in headerTable: #遍历头指针表
        headerTable[k] = [headerTable[k], None]  #保存计数值及指向每种类型第一个元素项的指针
    #print ('headerTable: ',headerTable)
    retTree = treeNode('Null Set', 1, None)  #初始化tree
    for tranSet, count in dataSet.items():  # 第二次遍历,count其实就是等于1
        localD = {}
########修改前########
        #for item in tranSet:  # put transaction items in order
            #if item in freqItemSet:#记录该组数据中包含的频繁项
                #localD[item] = headerTable[item][0]

        #创建该组数据对于的数
        #if len(localD) > 0:
           # orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]  #对该组数据中包含的频繁项进行排序
            #print(orderedItems)
            #updateTree(orderedItems, retTree, headerTable, count)  # populate tree with ordered freq itemset
########修改前########
########修改后########
        for item in freqItemSet:  # put transaction items in order
            if item in tranSet:#记录该组数据中包含的频繁项
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = list(localD.keys())
            updateTree(orderedItems, retTree, headerTable, count)   
########修改后########
    return retTree, headerTable  #返回树和头指针表

def updateTree(items, inTree, headerTable, count): #输入：按出现次数排序后的项集，原始节点，头指针表，计数
    if items[0] in inTree.children:  # 首先检查是否存在该节点
        inTree.children[items[0]].inc(count)  # 存在则计数增加
    else:  # 不存在则将新建该节点
        inTree.children[items[0]] = treeNode(items[0], count, inTree)#创建一个新节点
        if headerTable[items[0]][1] == None:  # 若原来不存在该类别，更新头指针列表
            headerTable[items[0]][1] = inTree.children[items[0]]#更新指向
        else:#更新指向
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:  #仍有未分配完的树，即超过一项，迭代
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)

#节点链接指向树中该元素项的每一个实例。
#从头指针表的 nodeLink 开始,一直沿着nodeLink直到到达链表末尾
def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def loadSimpData():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat

#createInitSet() 用于实现上述从列表到字典的类型转换过程
def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        if frozenset(trans) in list(retDict.keys()):
            retDict[frozenset(trans)] = retDict[frozenset(trans)] + 1
        else:
            retDict[frozenset(trans)] = 1  #frozenset(不可变集合)
    return retDict

#从FP树中发现频繁项集
def ascendTree(leafNode, prefixPath):  #递归上溯整棵树
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath) #得到以最底部变量为根节点的一个分支

def findPrefixPath(basePat, treeNode):  #参数：指针项，该项对应的节点；
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)#寻找当前非空节点的前缀
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count #将条件模式基添加到字典中
        treeNode = treeNode.nodeLink
    #print(basePat,":",condPats)
    return condPats

#递归查找频繁项集(修改前)
def mineTree(inTree, headerTable, dataSetLen, itemnumber, minSup=0.5, preFix=set([]), freqItemList={}):
    # 头指针表中的元素项按照频繁度排序,从小到大
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: str(p[1]))]
    for basePat in bigL:  #从底层开始
        #加入频繁项列表
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        #print ('finalFrequent Item: ',newFreqSet)
        ###加一个判别器，防止生成过多的项造成爆内存
        if len(newFreqSet) > itemnumber:
            break
        ######################################
        freqItemList[frozenset(newFreqSet)]=headerTable[basePat][0] #频繁集由2元列表组成，第一项为频繁项集，第二项为支持度
        #递归调用函数来创建基
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        #print ('condPattBases :',basePat, condPattBases)
        #2. 构建条件模式Tree
        myCondTree, myHead = createTree(condPattBases, dataSetLen, minSup)
        #将创建的条件基作为新的数据集添加到fp-tree
        #print ('head from conditional tree: ', myHead)
        if myHead != None: #3. 递归
            #print ('conditional tree for: ',newFreqSet)
            #myCondTree.disp(1)
            mineTree(myCondTree, myHead, dataSetLen, itemnumber, minSup, newFreqSet, freqItemList)