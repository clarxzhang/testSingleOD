# 如何在当前分支使用 Agent 系统

## 🚀 快速开始

### 1. 基本使用

```python
from code_agent import create_agent_for_project

# 创建 Agent
agent = create_agent_for_project(".")

# 运行任务
result = agent.run_task("分析项目代码质量")

# 查看结果
print(f"任务完成: {result['success']}")
print(f"总奖励: {result['total_reward']}")
print(f"执行步数: {result['steps']}")
```

### 2. 使用项目专用 Agent

```python
from project_agent import ProjectAgent

# 创建项目 Agent
agent = ProjectAgent(".")

# 列出所有可用任务
agent.list_tasks()

# 执行特定任务
result = agent.execute_task("refactor_path_finding")

# 分析项目
agent.analyze_project()
```

## 📋 可用任务

### 任务 1: 重构路径查找
- **名称**: `refactor_path_finding`
- **描述**: 重构 all_path_TODO1.py，移除硬编码路径和调试打印
- **目标文件**: all_path_TODO1.py
- **最大步数**: 30

### 任务 2: 添加类型提示
- **名称**: `add_type_hints`
- **描述**: 为 test_bpr.py 添加类型提示
- **目标文件**: test_bpr.py
- **最大步数**: 20

### 任务 3: 改进文档
- **名称**: `improve_documentation`
- **描述**: 为核心函数添加详细的文档字符串
- **目标文件**: all_path_TODO1.py, test_bpr.py
- **最大步数**: 25

### 任务 4: 修复代码问题
- **名称**: `fix_code_issues`
- **描述**: 修复代码审查中发现的问题
- **目标文件**: all_path_TODO1.py
- **最大步数**: 40

## 🎯 Agent 动作类型

| 动作 | 描述 | 参数 |
|------|------|------|
| `read_file` | 读取文件内容 | `filepath` |
| `edit_code` | 编辑代码 | `filepath`, `old_code`, `new_code` |
| `run_tests` | 运行测试 | `test_file` (可选) |
| `search_code` | 搜索代码 | `pattern` |
| `analyze_code` | 分析代码 | `filepath` |

## 💡 使用示例

### 示例 1: 自动化代码审查

```python
from project_agent import ProjectAgent

agent = ProjectAgent(".")

# 执行代码审查任务
result = agent.execute_task("fix_code_issues")

# 查看执行历史
for i, action in enumerate(result['action_history'], 1):
    print(f"{i}. {action['type']}: {action.get('params', {})}")
```

### 示例 2: 训练 Agent

```python
from code_agent import create_agent_for_project

agent = create_agent_for_project(".")

# 训练 10 个回合
rewards = agent.train(num_episodes=10)

# 保存训练结果
agent.save("agent_memory.pkl")
```

### 示例 3: 自定义任务

```python
from code_agent import create_agent_for_project

agent = create_agent_for_project(".")

# 自定义任务
result = agent.run_task("""
优化 all_path_TODO1.py 的性能:
1. 移除不必要的打印语句
2. 优化循环结构
3. 添加性能优化注释
""")

print(f"优化完成，奖励: {result['total_reward']}")
```

## 🔧 配置参数

在 `code_agent.py` 中可以修改以下参数：

```python
config = AgentConfig(
    workspace=".",           # 工作空间路径
    max_steps=50,            # 最大步数
    learning_rate=3e-4,      # 学习率
    gamma=0.99,              # 折扣因子
    epsilon=0.2,             # 探索率
    memory_size=5000,        # 记忆容量
    batch_size=16            # 批次大小
)
```

## 📊 奖励系统

Agent 会根据以下维度获得奖励：

| 维度 | 权重 | 描述 |
|------|------|------|
| 功能性 | 40% | 测试通过、功能实现 |
| 代码质量 | 30% | 代码风格、可读性 |
| 效率 | 20% | 步骤效率、性能 |
| 探索 | 10% | 新文件探索、多样性 |

## 🎓 进阶用法

### 1. 添加自定义动作

```python
from code_agent import CodeAgent, ActionExecutor

class CustomActionExecutor(ActionExecutor):
    def execute(self, action):
        if action['type'] == 'custom_action':
            return self._custom_action(action['params'])
        return super().execute(action)
    
    def _custom_action(self, params):
        # 实现自定义动作
        return {'success': True, 'result': 'custom'}
```

### 2. 自定义奖励函数

```python
from code_agent import RewardCalculator

class CustomRewardCalculator(RewardCalculator):
    def calculate(self, action, result, info):
        reward = super().calculate(action, result, info)
        
        # 添加自定义奖励逻辑
        if action['type'] == 'edit_code':
            reward += 0.5  # 鼓励代码编辑
        
        return reward
```

### 3. 集成到 CI/CD

```bash
# 在 CI 中运行 Agent
python -c "
from project_agent import ProjectAgent
agent = ProjectAgent('.')
result = agent.execute_task('fix_code_issues')
exit(0 if result['success'] else 1)
"
```

## 📁 文件结构

```
/workspace/
├── agent.md              # 主系统文档
├── learning.md           # 学习子系统
├── memory.md             # 记忆子系统
├── action.md             # 行动子系统
├── reward.md             # 奖励子系统
├── environment.md        # 环境子系统
├── code_agent.py         # Agent 核心实现
├── project_agent.py      # 项目专用 Agent
├── all_path_TODO1.py     # 项目文件
├── test_bpr.py           # 测试文件
└── test_path_finding.py  # 测试文件
```

## 🐛 常见问题

### Q: Agent 无法找到文件？
A: 确保 `workspace` 参数指向正确的项目根目录。

### Q: 测试运行失败？
A: 检查是否安装了所有依赖：`pip install numpy pandas networkx pytest`

### Q: 如何查看 Agent 的决策过程？
A: 查看 `action_history` 字段，记录了所有执行的动作。

## 📞 获取帮助

- 查看 [agent.md](file:///workspace/agent.md) 了解系统架构
- 查看 [learning.md](file:///workspace/learning.md) 了解学习算法
- 查看 [action.md](file:///workspace/action.md) 了解动作类型
- 查看 [reward.md](file:///workspace/reward.md) 了解奖励机制
