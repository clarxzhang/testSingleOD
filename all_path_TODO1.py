# coding: utf-8
# od 全路径

from copy import deepcopy

import pandas as pd 
import networkx as nx
## 定义函数
def forward_star_net(networkDf):
    '''get forward star network'''
    # 初始化
    sourceSet = set(networkDf.source)
    targetSet = set(networkDf.target)
    nodeSet = sourceSet.union(targetSet)
    forwardStarNet = {s:[] for s in nodeSet }
    # 创建前向星网络
    for s, t in zip(networkDf.source, networkDf.target):
        forwardStarNet[s].append(t)
    #
    return forwardStarNet
#
## 加载双向田字网络
pathFile = r"D:\Jobsplay\MyPython\netset\Grid9e24\Grid9e24_net.csv"
networkDf = pd.read_csv(pathFile)

#Grid4e12
# pathFile = r"D:\Jobsplay\MyPython\netset\Grid4e12\Grid4e12_net.xlsx"
# networkDf = pd.read_excel(pathFile)

# 


## 生成前向星网络
forwardStarNet0 = forward_star_net(networkDf)
forwardStarNet = deepcopy(forwardStarNet0)
# {1: [2, 3], 
# 2: [1, 3, 4], 
# 3: [1, 2, 4], 
# 4: [2, 3]}
o, d = 1, 4

## init path from o has no acyclic path
pathSet = []
path = [o]
flag = {o:[] }
for _ in range(1000):    
    node = path[-1]; print('node=', node)
    idx = path.index(node)
    nodeDownLst = forwardStarNet[node]; print('nodeDownLst=', nodeDownLst)
    for nodeDown in nodeDownLst: 
        if nodeDown in path: 
            flag[node].append(nodeDown);
            continue
        elif nodeDown not in path:
            path.append(nodeDown)
            flag[node].append(nodeDown);
            flag[nodeDown] = [] 
            print('flag=', flag)
            print('path=', path)
            break

    if set(nodeDownLst).issubset(set(path[:idx])):
        pathSet.append(path)
        break
        print('path = ', path)

## init path and flag       
path = [o]
flag = {o:[]}
pathSet = []

## new path and flag

for _ in range(100):    
    node = path[-1]; print('node = ', node)
    if flag[node] == forwardStarNet[node]: print('break'); break;
    
    idx = path.index(node)
    nodeDownLst = forwardStarNet[node]; print('nodeDownLst=', nodeDownLst)    
    for nodeDown in nodeDownLst:
        if nodeDown in flag[node]:
            continue
        elif nodeDown in path[:idx]:
            flag[node].append(nodeDown)
            continue
        else:    
            path.append(nodeDown)
            flag[node].append(nodeDown)
            flag[nodeDown] = []
            break
            
print('path = ', path)
print('flag = ', flag)

## collect path
pathSet.append(deepcopy(path)); 
 
## semi path and flag  
# in : full path and flag
# out: semi path and flag
# path =  [1, 3, 4]
# flag =  {1: [2, 3], 3: [1, 2, 4], 4: [2, 3]}

#for _ in range(1):
for node in reversed(list(flag.keys()) ):
    if flag[node] == forwardStarNet[node]:
        del flag[node]
        path.remove(node)
        # print('semi flag :', flag)
        # print('semi path', path)
    else:        
        break    

#
print('semi flag :', flag)
print('semi path', path)

print('pathset:', pathSet)
    
         



    
    

    
    

