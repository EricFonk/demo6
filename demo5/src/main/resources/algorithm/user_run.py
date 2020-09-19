#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:MIAO
@file: user_run.py
@time: 2020/07/28
前端用户输入的内容调用此方法
"""
import trees
import json
import sys
from collections import Counter
import os
import numpy as np

path = os.getcwd().replace("\\","/")
path = path+"/target/classes/algorithm"
# 将字符串转为列表
def transformList(text):
    result = list(text)
    return result
def get_labels():
    '''
            获取属性
            :return:
            '''
    with open(path+'/data/labels.txt', 'r', encoding="utf-8") as f:
        content = f.read().splitlines()
    labels = []
    for i in range(len(content)):
        labels.append(content[i])
    return labels
if __name__ == '__main__':
    # for i in range(1, len(sys.argv)):
    #     # 获取系统传来的参数
    #     listWm = sys.argv[i]
    #     listWm = transformList(listWm)
    #     print(listWm)
    #     labels = get_labels()
    #     testData = listWm
    #     testClass = trees.classify(trees.grabTree(r'data/tree.txt'), labels, testData)
    #     # testClass = trees.classify(save, labels, testData)
    #     print(type(json.dumps(testClass, ensure_ascii=False)))
    #     print('根据您的条件，适合您的岗位是：', json.dumps(testClass, ensure_ascii=False))
    # listWm = transformList('1 0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0')
    listWm = sys.argv[1]
    # listWm = transformList("1234200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
    listWm = transformList(listWm)
    labels = get_labels()
    testData = listWm
    testClass = trees.classify(trees.grabTree(path+'/data/tree.txt'), labels, testData)
    position_name = json.dumps(testClass, ensure_ascii=False).replace('[', '').replace(']', ' ').replace('"','').replace(' ','').split(',')
    list_unique = list(position_name)
    result = []
    for i in list_unique:
        if len(i) > 0:
            result.append(i)
    sort_result = Counter(result)
    end_result = sort_result.most_common(len(sort_result))
    result = []
    num = np.array(end_result).shape[0]
    if num > 5:
        num = 5
    for i in range(num):
       result.append(end_result[i][0])
    print(json.dumps(result, ensure_ascii=False))