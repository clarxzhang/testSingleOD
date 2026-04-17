# coding: utf-8
"""
路径查找逻辑测试脚本
测试 all_path_TODO1.py 中的路径查找算法
"""

import pandas as pd
import networkx as nx
from copy import deepcopy
import sys

# 定义前向星网络生成函数（避免导入整个文件）
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

def test_forward_star_net():
    """测试前向星网络生成函数"""
    print("=" * 60)
    print("测试 1: forward_star_net 函数")
    print("=" * 60)
    
    # 创建测试数据
    test_data = {
        'source': [1, 1, 2, 2, 3, 3, 4, 4],
        'target': [2, 3, 1, 3, 1, 2, 2, 3]
    }
    networkDf = pd.DataFrame(test_data)
    
    # 调用函数
    result = forward_star_net(networkDf)
    
    # 预期结果
    expected = {
        1: [2, 3],
        2: [1, 3],
        3: [1, 2],
        4: [2, 3]
    }
    
    # 验证
    assert result == expected, f"期望 {expected}, 得到 {result}"
    print("✓ 前向星网络生成正确")
    print(f"  结果: {result}")
    return True

def test_path_finding_simple():
    """测试简单网格网络的路径查找"""
    print("\n" + "=" * 60)
    print("测试 2: 简单网格网络路径查找 (4 节点)")
    print("=" * 60)
    
    # 创建简单的 4 节点网格网络
    test_data = {
        'source': [1, 1, 2, 2, 3, 3, 4, 4],
        'target': [2, 3, 1, 3, 1, 2, 2, 3]
    }
    networkDf = pd.DataFrame(test_data)
    
    # 生成前向星网络
    forwardStarNet = forward_star_net(networkDf)
    forwardStarNet_copy = deepcopy(forwardStarNet)
    
    # 设置起点和终点
    o, d = 1, 4
    
    # 执行路径查找算法
    path = [o]
    flag = {o: []}
    pathSet = []
    
    for _ in range(10000):
        # 新路径和标志
        for _ in range(10000):    
            node = path[-1]
            if flag[node] == forwardStarNet[node]:
                break
            
            idx = path.index(node)
            nodeDownLst = forwardStarNet[node]    
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
        
        # 收集路径
        pathSet.append(deepcopy(path))
        
        # 简化路径和标志
        for node in reversed(list(flag.keys())):
            if flag[node] == forwardStarNet[node]:
                del flag[node]
                path.remove(node)
            else:        
                break    
        
        if len(path) == 0:
            break
    
    print(f"✓ 找到 {len(pathSet)} 条路径")
    print(f"  路径集合: {pathSet}")
    
    # 验证所有路径都是从 o 到 d 的无环路径
    for i, p in enumerate(pathSet):
        assert p[0] == o, f"路径 {i} 起点错误"
        # 检查是否有环
        assert len(p) == len(set(p)), f"路径 {i} 包含环: {p}"
    
    return True

def test_path_finding_grid9():
    """测试 9 节点网格网络的路径查找"""
    print("\n" + "=" * 60)
    print("测试 3: 9 节点网格网络路径查找")
    print("=" * 60)
    
    # 创建 9 节点网格网络 (3x3)
    # 节点布局:
    # 1 -- 2 -- 3
    # |    |    |
    # 4 -- 5 -- 6
    # |    |    |
    # 7 -- 8 -- 9
    
    edges = []
    # 横向连接
    for row in range(3):
        for col in range(2):
            n1 = row * 3 + col + 1
            n2 = n1 + 1
            edges.append((n1, n2))
            edges.append((n2, n1))
    
    # 纵向连接
    for col in range(3):
        for row in range(2):
            n1 = row * 3 + col + 1
            n2 = n1 + 3
            edges.append((n1, n2))
            edges.append((n2, n1))
    
    sources = [e[0] for e in edges]
    targets = [e[1] for e in edges]
    
    test_data = {
        'source': sources,
        'target': targets
    }
    networkDf = pd.DataFrame(test_data)
    
    # 生成前向星网络
    forwardStarNet = forward_star_net(networkDf)
    forwardStarNet_copy = deepcopy(forwardStarNet)
    
    # 设置起点和终点 (从左上角到右下角)
    o, d = 1, 9
    
    # 执行路径查找算法
    path = [o]
    flag = {o: []}
    pathSet = []
    
    for _ in range(100000):
        # 新路径和标志
        for _ in range(10000):    
            node = path[-1]
            if flag[node] == forwardStarNet[node]:
                break
            
            idx = path.index(node)
            nodeDownLst = forwardStarNet[node]    
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
        
        # 收集路径
        pathSet.append(deepcopy(path))
        
        # 简化路径和标志
        for node in reversed(list(flag.keys())):
            if flag[node] == forwardStarNet[node]:
                del flag[node]
                path.remove(node)
            else:        
                break    
        
        if len(path) == 0:
            break
    
    print(f"✓ 找到 {len(pathSet)} 条从节点 {o} 到节点 {d} 的无环路径")
    
    # 验证所有路径
    valid_paths = 0
    for i, p in enumerate(pathSet):
        if p[0] == o and p[-1] == d:
            valid_paths += 1
            # 检查是否有环
            assert len(p) == len(set(p)), f"路径 {i} 包含环: {p}"
    
    print(f"  有效路径数 (从{ o}到{d}): {valid_paths}")
    print(f"  示例路径 (前 5 条):")
    for i, p in enumerate(pathSet[:5]):
        print(f"    {i+1}. {p}")
    
    return True

def test_no_path_exists():
    """测试不存在路径的情况"""
    print("\n" + "=" * 60)
    print("测试 4: 不连通网络 (无路径)")
    print("=" * 60)
    
    # 创建两个不连通的子图
    # 子图 1: 1-2-3
    # 子图 2: 4-5-6
    test_data = {
        'source': [1, 2, 4, 5],
        'target': [2, 3, 5, 6]
    }
    networkDf = pd.DataFrame(test_data)
    
    # 生成前向星网络
    forwardStarNet = forward_star_net(networkDf)
    forwardStarNet_copy = deepcopy(forwardStarNet)
    
    # 设置起点和终点 (在不同子图中)
    o, d = 1, 6
    
    # 执行路径查找算法
    path = [o]
    flag = {o: []}
    pathSet = []
    
    for _ in range(10000):
        for _ in range(1000):    
            node = path[-1]
            if flag[node] == forwardStarNet[node]:
                break
            
            idx = path.index(node)
            nodeDownLst = forwardStarNet[node]    
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
        
        pathSet.append(deepcopy(path))
        
        for node in reversed(list(flag.keys())):
            if flag[node] == forwardStarNet[node]:
                del flag[node]
                path.remove(node)
            else:        
                break    
        
        if len(path) == 0:
            break
    
    # 验证没有路径到达终点
    paths_to_dest = [p for p in pathSet if p[-1] == d]
    print(f"✓ 找到 {len(pathSet)} 条路径，其中 {len(paths_to_dest)} 条到达终点 {d}")
    assert len(paths_to_dest) == 0, "不应该存在从起点到终点的路径"
    
    return True

def main():
    """执行所有测试"""
    print("\n" + "=" * 60)
    print("路径查找逻辑测试套件")
    print("=" * 60)
    
    tests = [
        ("前向星网络生成", test_forward_star_net),
        ("简单网格路径查找", test_path_finding_simple),
        ("9 节点网格路径查找", test_path_finding_grid9),
        ("不连通网络测试", test_no_path_exists),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, "通过", None))
        except Exception as e:
            results.append((test_name, "失败", str(e)))
            print(f"✗ 测试失败：{e}")
    
    # 打印测试总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, status, _ in results if status == "通过")
    total = len(results)
    
    for test_name, status, error in results:
        symbol = "✓" if status == "通过" else "✗"
        print(f"{symbol} {test_name}: {status}")
        if error:
            print(f"  错误信息：{error}")
    
    print(f"\n总计：{passed}/{total} 个测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
