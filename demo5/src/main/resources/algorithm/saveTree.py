# -*- coding: utf-8 -*-
import JobTree
import trees
import keras
fileName = r'tree.txt'
trees.storeTree(JobTree.Trees, fileName)
# import json
# print(json.dumps(trees.grabTree('job_tree.txt'), encoding="cp936", ensure_ascii=False))
import json
print(json.dumps(trees.grabTree(fileName), ensure_ascii=False))
print("1代表熟练掌握，2代表精通，3代表熟悉，4代表了解")

