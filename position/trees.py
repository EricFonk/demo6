# -*- coding: UTF-8 -*-
from math import log
import operator
import os
import random

# 计算信息熵
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:  # 遍历每个样本
        currentLabel = featVec[-1]  # 当前样本的类别,即职位
        if currentLabel not in labelCounts.keys():  # 生成类别字典

            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:  # 计算信息熵
        prob = float(labelCounts[key]) / numEntries
        shannonEnt = shannonEnt - prob * log(prob, 2)
    return shannonEnt


# 划分数据集，axis:按第几个属性划分，value:要返回的子集对应的属性值
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    featVec = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis + 1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

# 选择最好的数据集划分方式
def chooseBestFeatureToSplit(dataSet):

    numFeatures = len(dataSet[0]) - 1  # 属性的个数
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):  # 对每个属性技术信息增益
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)  # 该属性的取值集合
        newEntropy = 0.0
        for value in uniqueVals:  # 对每一种取值计算信息增益
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if (infoGain > bestInfoGain):  # 选择信息增益最大的属性
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

# 通过排序返回出现次数最多的类别
def majorityCnt(classList):
    classCount = {}
    # 数据传递进来classList
    #print(classList)
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    # print(classCount.items())
    sortedClassCount = sorted(classCount.items(),
                              key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


# 递归构建决策树
def createTree(dataSet, labels):

    classList = [example[-1] for example in dataSet]  # 类别向量opposition职位

    if classList.count(classList[0]) == len(classList):     # 当类别只有一个时，返回
        return classList[0]
    if len(dataSet[0]) == 1:  # 如果所有特征都被遍历完了，返回出现次数最多的类别
        return majorityCnt(classList)
    # rowData = rowDataDie(dataSet)
    # bestFeat = cowFeatureDie(rowData)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel: {}}
    del (labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueValue = set(featValues)
    for value in uniqueValue:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(
            splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree


# 算法预测
classLabel = []
def classify(inputTree, featLabels, testVec):
    firstStr = list(inputTree.keys())[0]

    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    classLabel = []
    for key in secondDict.keys():

        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
            else:  # 如果是叶子， 返回结果, featLabels, testVec
                classLabel.append(secondDict[key])
    return classLabel

def classifyAll(inputTree, featLabels, testDataSet):
    classLabelAll = []
    for testVec in testDataSet:
        classLabelAll.append(classify(inputTree, featLabels, testVec))
    return classLabelAll


# 存储决策树
def storeTree(inputTree, filename):
    import pickle
    fw = open(filename, 'wb')
    pickle.dump(inputTree, fw)
    fw.close()


# 读取决策树, 文件不存在返回None
def grabTree(filename):
    import pickle
    if os.path.isfile(filename):
        fr = open(filename, 'rb')
        return pickle.load(fr)
    else:
        return None
