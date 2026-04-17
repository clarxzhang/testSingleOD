# SingleUE - 单用户均衡交通分配

## 项目简介

本项目实现了基于 BPR (Bureau of Public Roads) 函数的单用户均衡 (Single User Equilibrium) 交通分配算法。主要用于交通网络分析中的路径搜索和流量分配。

## 文件说明

### 核心文件

- **SingleUE.ipynb**: Jupyter Notebook，包含主要的算法实现
  - BPR 阻抗函数：计算路段行驶时间
  - All-or-Nothing 分配：将 OD 需求分配到最短路径
  - 使用 NetworkX 进行图论分析

- **all_path_TODO1.py**: Python 脚本，实现全路径搜索算法
  - 前向星网络构建
  - 无环路径枚举
  - OD 对之间的所有可行路径搜索

### 依赖库

```
- numpy
- networkx
- matplotlib
- scipy
- pandas
```

## 主要功能

1. **BPR 阻抗函数**
   - 计算路段行驶时间与流量的关系
   - 支持自定义参数 (alpha, beta)

2. **最短路径分配**
   - 基于 NetworkX 的最短路径算法
   - All-or-Nothing 交通分配

3. **全路径搜索**
   - 枚举 OD 对之间的所有无环路径
   - 使用前向星网络结构提高效率

## 使用方法

### 运行 Jupyter Notebook

```bash
jupyter notebook SingleUE.ipynb
```

### 运行路径搜索脚本

```bash
python all_path_TODO1.py
```

## 网络数据格式

项目使用 Grid9e24 或 Grid4e12 网格网络数据，包含以下字段：
- `source`: 起点节点编号
- `target`: 终点节点编号
- `freeTime`: 自由流行驶时间
- `capacity`: 路段通行能力
- `volumn`: 路段流量
- `travelTime`: 路段行驶时间

## 注意事项

- `all_path_TODO1.py` 中的路径需要根据实际数据文件位置进行修改
- 项目处于测试阶段，部分功能可能仍在开发中

## 许可证

本项目仅用于测试和学习目的。
