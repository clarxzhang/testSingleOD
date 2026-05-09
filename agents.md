# 高级 Agent 文档

## SingleUE 交通网络分析 Agent

### 项目背景

本项目实现了基于 BPR (Bureau of Public Roads) 函数的单用户均衡 (Single User Equilibrium) 交通分配算法。主要功能包括：

- **BPR 阻抗函数**：计算路段行驶时间与流量的关系
- **最短路径分配**：基于 NetworkX 的最短路径算法
- **全路径搜索**：枚举 OD 对之间的所有无环路径
- **交通分配算法**：实现单用户均衡的迭代求解

---

## Agent 架构设计

### 五大核心属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `sensing` | `Dict[str, Any]` | 感知模块，接收和解析外部输入/环境信息 |
| `done` | `List[Task]` | 已完成任务列表 |
| `doing` | `Optional[Task]` | 正在执行的任务 |
| `todo` | `List[Task]` | 待办任务队列 |
| `reflecting` | `List[Dict]` | 反思模块，记录执行过程和学习成果 |

### Agent 类实现

```python
"""
高级 Agent 类
基于 ReAct (Reasoning + Acting) 模式
包含 sensing, done, doing, todo, reflecting 五个核心属性
"""

from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class Task:
    """任务单元"""
    id: str
    description: str
    status: str = "pending"  # pending, doing, done, failed
    result: Any = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "result": str(self.result) if self.result else None,
            "error": self.error,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


class AdvancedAgent:
    """
    高级 Agent 类
    
    属性说明:
    - sensing: 感知模块，接收和解析外部输入/环境信息
    - done: 已完成任务列表
    - doing: 正在执行的任务
    - todo: 待办任务队列
    - reflecting: 反思模块，记录执行过程和学习成果
    """
    
    def __init__(self, name: str = "Agent"):
        self.name = name
        
        # 核心状态属性
        self.sensing: Dict[str, Any] = {}  # 感知数据
        self.done: List[Task] = []          # 已完成任务
        self.doing: Optional[Task] = None   # 正在执行的任务
        self.todo: List[Task] = []           # 待办任务队列
        
        # 反思模块
        self.reflecting: List[Dict[str, Any]] = []
        
        # 动作注册表
        self._action_registry: Dict[str, Callable] = {}
        
        # 状态记录
        self._history: List[Dict[str, Any]] = []
```

---

## Agent 初始化示例

### 交通网络分析 Agent 初始化

```python
def initialize_traffic_agent():
    """初始化交通网络分析 Agent"""
    
    # 创建 Agent 实例
    agent = AdvancedAgent(name="交通网络分析Agent")
    
    # ============================================
    # 1. 感知模块初始化 (sensing)
    # ============================================
    agent.sense({
        "network_type": "Grid9e24",
        "node_count": 9,
        "edge_count": 24,
        "data_source": "D:\\Jobsplay\\MyPython\\netset\\Grid9e24\\Grid9e24_net.csv"
    }, source="network_config")
    
    agent.sense({
        "algorithm": "All-or-Nothing",
        "bpr_alpha": 0.15,
        "bpr_beta": 4,
        "convergence_threshold": 0.0001
    }, source="algorithm_config")
    
    agent.sense({
        "od_pair": (1, 9),
        "demand": 2000.0
    }, source="demand_data")
    
    # ============================================
    # 2. 待办任务队列初始化 (todo)
    # ============================================
    agent.add_task("加载 Grid9e24 网络数据文件")
    agent.add_task("构建前向星网络结构")
    agent.add_task("初始化边流量 (All-or-Nothing 分配)")
    agent.add_task("计算 BPR 阻抗函数")
    agent.add_task("执行路径搜索算法")
    agent.add_task("迭代求解均衡流量")
    agent.add_task("验证收敛条件")
    agent.add_task("输出最终结果")
    
    # ============================================
    # 3. 动作注册 (action_registry)
    # ============================================
    
    def load_network_data(file_path: str):
        """加载网络数据"""
        import pandas as pd
        network_df = pd.read_csv(file_path)
        return network_df
    
    def build_forward_star_network(network_df):
        """构建前向星网络"""
        from copy import deepcopy
        source_set = set(network_df.source)
        target_set = set(network_df.target)
        node_set = source_set.union(target_set)
        forward_star_net = {s: [] for s in node_set}
        for s, t in zip(network_df.source, network_df.target):
            forward_star_net[s].append(t)
        return forward_star_net
    
    def calculate_bpr_travel_time(volume, free_time, capacity, alpha=0.15, beta=4):
        """BPR 阻抗函数"""
        travel_time = free_time + free_time * alpha * (volume / capacity) ** beta
        return travel_time
    
    def find_shortest_path(network, source, target, weight='travelTime'):
        """最短路径搜索"""
        import networkx as nx
        G = nx.from_pandas_edgelist(network, create_using=nx.MultiDiGraph)
        return nx.shortest_path(G, source=source, target=target, weight=weight)
    
    def all_nothing_assignment(df, source, target, demand):
        """All-or-Nothing 交通分配"""
        shortest_path = find_shortest_path(df, source, target)
        path_edges = {(s, t) for s, t in zip(shortest_path[:-1], shortest_path[1:])}
        for i, s, t in zip(range(df.shape[0]), df["source"], df["target"]):
            if (s, t) in path_edges:
                df.loc[i, "volume"] = demand
        return df
    
    # 注册所有动作
    agent.register_action("load_network_data", load_network_data)
    agent.register_action("build_forward_star_network", build_forward_star_network)
    agent.register_action("calculate_bpr_travel_time", calculate_bpr_travel_time)
    agent.register_action("find_shortest_path", find_shortest_path)
    agent.register_action("all_nothing_assignment", all_nothing_assignment)
    
    # ============================================
    # 4. 初始反思记录 (reflecting)
    # ============================================
    agent.reflect("Agent 初始化完成，已加载网络配置和算法参数")
    agent.reflect(f"待执行 {len(agent.todo)} 个任务")
    agent.reflect("已注册 5 个核心动作函数")
    
    return agent
```

---

## 核心方法说明

### 感知模块 (sensing)

```python
# 接收外部输入/环境信息
agent.sense(data, source="来源名称")
```

**示例：**
```python
agent.sense({"nodes": 9, "edges": 24}, source="network_data")
agent.sense({"algorithm": "BPR"}, source="config")
```

### 任务管理 (todo / doing / done)

```python
# 添加新任务
task = agent.add_task("任务描述")

# 开始下一个任务
agent.start_next_task()

# 完成当前任务
agent.complete_task(result="任务结果")

# 标记任务失败
agent.fail_task(error="错误信息")
```

### 动作执行

```python
# 注册动作函数
agent.register_action("动作名称", action_function)

# 执行动作
result = agent.execute_action("动作名称", 参数1=value1, 参数2=value2)
```

### 反思模块 (reflecting)

```python
# 记录思考过程
agent.reflect("思考内容")

# 获取反思历史
for ref in agent.reflecting:
    print(ref['thought'])
```

---

## 状态查询

```python
# 获取完整状态
status = agent.get_status()

# 导出为 JSON
json_output = agent.to_json()

# 重置 Agent
agent.reset()
```

**状态输出示例：**
```json
{
  "name": "交通网络分析Agent",
  "sensing": {
    "network_config": {"network_type": "Grid9e24", "node_count": 9},
    "algorithm_config": {"bpr_alpha": 0.15, "bpr_beta": 4}
  },
  "todo": [],
  "doing": null,
  "done": [...],
  "done_count": 8,
  "reflecting_count": 15
}
```

---

## 执行流程

```
┌─────────────────────────────────────┐
│          Agent 初始化               │
│  - 创建实例                         │
│  - 初始化五大属性                    │
│  - 注册动作函数                      │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│          任务循环                   │
│                                     │
│  ┌───────────┐    ┌──────────────┐ │
│  │  todo     │───▶│  start_next  │ │
│  │  任务队列  │    │  取出任务     │ │
│  └───────────┘    └──────┬───────┘ │
│                         │          │
│                         ▼          │
│                  ┌──────────────┐ │
│                  │   执行任务    │ │
│                  │ sensing      │ │
│                  │ 感知环境      │ │
│                  │ doing        │ │
│                  │ 执行中       │ │
│                  └──────┬───────┘ │
│                         │          │
│                         ▼          │
│                  ┌──────────────┐ │
│                  │   反思       │ │
│                  │ reflecting  │ │
│                  │ 记录思考     │ │
│                  └──────┬───────┘ │
│                         │          │
│                         ▼          │
│                  ┌──────────────┐ │
│                  │  完成/失败    │ │
│                  │   done       │ │
│                  └──────┬───────┘ │
│                         │          │
│                         ▼          │
│                  ┌──────────────┐ │
│                  │ todo 为空？  │─┼──▶ 结束
│                  └──────────────┘ │
└─────────────────────────────────────┘
```

---

## 使用示例

```python
# 初始化 Agent
agent = initialize_traffic_agent()

# 执行任务循环
while agent.todo:
    agent.start_next_task()
    
    # 根据任务类型执行相应动作
    if "加载" in agent.doing.description:
        result = agent.execute_action(
            "load_network_data",
            file_path=agent.sensing["network_config"]["data_source"]
        )
    elif "BPR" in agent.doing.description:
        result = agent.execute_action(
            "calculate_bpr_travel_time",
            volume=100, free_time=10, capacity=100
        )
    else:
        result = "执行完成"
    
    agent.complete_task(result)

# 输出最终状态
print(agent.to_json())
```

---

## 交通网络分析专用功能

### 1. BPR 阻抗函数

```python
def bpr_fun(volumn, freeTime, capacity, alpha=0.15, beta=4):
    """
    BPR 阻抗函数
    travelTime = freeTime + freeTime * alpha * (volumn / capacity) ** beta
    """
    travelTime = freeTime + freeTime * alpha * (volumn / capacity) ** beta
    return travelTime
```

### 2. 前向星网络构建

```python
def forward_star_net(networkDf):
    """构建前向星网络结构"""
    sourceSet = set(networkDf.source)
    targetSet = set(networkDf.target)
    nodeSet = sourceSet.union(targetSet)
    forwardStarNet = {s: [] for s in nodeSet}
    for s, t in zip(networkDf.source, networkDf.target):
        forwardStarNet[s].append(t)
    return forwardStarNet
```

### 3. All-or-Nothing 分配

```python
def all_nothing(df, source, target, demand):
    """将 OD 需求分配到最短路径"""
    shortestPath = nx.shortest_path(MDG, source=source, target=target, weight='travelTime')
    pathEdges = {(s, t) for s, t in zip(shortestPath[:-1], shortestPath[1:])}
    for i, s, t in zip(range(df.shape[0]), df["source"], df["target"]):
        if (s, t) in pathEdges:
            df.loc[i, "volumn"] = demand
    return df
```

---

## 文件清单

| 文件 | 说明 |
|------|------|
| `advanced_agent.py` | Agent 类实现 |
| `SingleUE.ipynb` | 主要算法实现 (BPR、路径搜索、交通分配) |
| `all_path_TODO1.py` | 全路径搜索算法 |
| `test_path_finding.py` | 路径查找测试 |
| `test_bpr.py` | BPR 函数测试 |

---

*文档生成时间: 2026-05-09*
