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
        
    def sense(self, data: Any, source: str = "unknown") -> None:
        """
        感知模块：接收外部输入/环境信息
        """
        observation = {
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "data": data
        }
        self.sensing[source] = data
        self._log_history("sensing", observation)
        self.reflect(f"感知到来自 {source} 的数据: {type(data).__name__}")
        
    def add_task(self, description: str, task_id: Optional[str] = None) -> Task:
        """
        添加新任务到待办队列
        """
        if task_id is None:
            task_id = f"task_{len(self.todo) + len(self.done) + 1}"
        
        task = Task(id=task_id, description=description)
        self.todo.append(task)
        self._log_history("task_added", task.to_dict())
        self.reflect(f"添加新任务: {description}")
        return task
    
    def register_action(self, name: str, action_func: Callable) -> None:
        """
        注册动作函数到动作库
        """
        self._action_registry[name] = action_func
        self.reflect(f"注册动作: {name}")
    
    def execute_action(self, action_name: str, **kwargs) -> Any:
        """
        执行注册的动作函数
        """
        if action_name not in self._action_registry:
            raise ValueError(f"动作 '{action_name}' 未注册")
        
        self.reflect(f"执行动作: {action_name}")
        result = self._action_registry[action_name](**kwargs)
        return result
    
    def start_next_task(self) -> bool:
        """
        开始执行下一个待办任务
        """
        if not self.todo:
            self.reflect("任务队列为空，无需执行")
            return False
        
        # 从队列中取出任务
        self.doing = self.todo.pop(0)
        self.doing.status = "doing"
        
        self._log_history("task_started", self.doing.to_dict())
        self.reflect(f"开始执行任务: {self.doing.description}")
        return True
    
    def complete_task(self, result: Any = None) -> None:
        """
        完成当前正在执行的任务
        """
        if self.doing is None:
            self.reflect("没有正在执行的任务")
            return
        
        self.doing.status = "done"
        self.doing.result = result
        self.doing.completed_at = datetime.now()
        
        self.done.append(self.doing)
        self._log_history("task_completed", self.doing.to_dict())
        self.reflect(f"完成任务: {self.doing.description}, 结果: {str(result)[:100]}")
        
        self.doing = None
    
    def fail_task(self, error: str) -> None:
        """
        标记任务失败
        """
        if self.doing is None:
            self.reflect("没有正在执行的任务")
            return
        
        self.doing.status = "failed"
        self.doing.error = error
        
        self._log_history("task_failed", self.doing.to_dict())
        self.reflect(f"任务失败: {self.doing.description}, 错误: {error}")
        
        self.doing = None
    
    def reflect(self, thought: str) -> None:
        """
        反思模块：记录思考过程和学习成果
        """
        reflection = {
            "timestamp": datetime.now().isoformat(),
            "thought": thought,
            "state": self._get_state_summary()
        }
        self.reflecting.append(reflection)
        self._log_history("reflection", reflection)
    
    def _get_state_summary(self) -> Dict[str, Any]:
        """
        获取当前状态摘要
        """
        return {
            "todo_count": len(self.todo),
            "doing": self.doing.description if self.doing else None,
            "done_count": len(self.done),
            "sensing_sources": list(self.sensing.keys())
        }
    
    def _log_history(self, event_type: str, data: Any) -> None:
        """
        记录历史事件
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data
        }
        self._history.append(entry)
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取 Agent 当前状态
        """
        return {
            "name": self.name,
            "sensing": self.sensing,
            "todo": [task.to_dict() for task in self.todo],
            "doing": self.doing.to_dict() if self.doing else None,
            "done": [task.to_dict() for task in self.done[-5:]],  # 最近5个
            "done_count": len(self.done),
            "reflecting_count": len(self.reflecting)
        }
    
    def clear_done(self, keep_last: int = 10) -> int:
        """
        清理已完成任务，保留最近的 N 个
        """
        if len(self.done) > keep_last:
            removed = len(self.done) - keep_last
            self.done = self.done[-keep_last:]
            self.reflect(f"清理已完成任务，移除了 {removed} 个旧任务")
            return removed
        return 0
    
    def to_json(self) -> str:
        """
        导出 Agent 状态为 JSON
        """
        return json.dumps(self.get_status(), indent=2, ensure_ascii=False)
    
    def reset(self) -> None:
        """
        重置 Agent 状态
        """
        self.sensing = {}
        self.done = []
        self.doing = None
        self.todo = []
        self.reflecting = []
        self._history = []
        self.reflect("Agent 状态已重置")


def demo():
    """演示 AdvancedAgent 的使用"""
    
    print("=" * 60)
    print("AdvancedAgent 演示")
    print("=" * 60)
    
    # 创建 Agent 实例
    agent = AdvancedAgent(name="交通网络分析Agent")
    
    # 注册动作
    def calculate_path(start: int, end: int) -> str:
        return f"从节点 {start} 到节点 {end} 的最短路径"
    
    def analyze_network(data: dict) -> str:
        return f"分析了包含 {data.get('nodes', 0)} 个节点的网络"
    
    agent.register_action("calculate_path", calculate_path)
    agent.register_action("analyze_network", analyze_network)
    
    # 添加任务
    agent.add_task("加载 Grid9e24 网络数据")
    agent.add_task("构建前向星网络结构")
    agent.add_task("查找节点 1 到节点 24 的所有路径")
    agent.add_task("计算 BPR 阻抗函数")
    agent.add_task("执行交通分配算法")
    
    # 模拟感知
    agent.sense({"nodes": 9, "edges": 24}, source="network_data")
    agent.sense({"algorithm": "AON"}, source="config")
    
    print(f"\n当前状态:")
    print(f"- 待办任务数: {len(agent.todo)}")
    print(f"- 已完成任务数: {len(agent.done)}")
    
    # 执行任务循环
    print("\n执行任务:")
    while agent.todo:
        agent.start_next_task()
        
        # 模拟任务执行
        if "加载" in agent.doing.description:
            result = agent.execute_action("analyze_network", data={"nodes": 9, "edges": 24})
        elif "路径" in agent.doing.description:
            result = agent.execute_action("calculate_path", start=1, end=24)
        else:
            result = f"执行了: {agent.doing.description}"
        
        agent.complete_task(result)
        print(f"  ✓ {agent.doing.description if agent.doing else ''}")
    
    # 打印反思记录
    print(f"\n反思记录 (最近 3 条):")
    for ref in agent.reflecting[-3:]:
        print(f"  - {ref['thought']}")
    
    # 打印最终状态
    print(f"\n最终状态:")
    print(agent.to_json())


if __name__ == "__main__":
    demo()
