"""
项目特定的 Agent 任务定义
针对 SingleUE 交通分配项目的任务
"""

from dataclasses import dataclass
from typing import List, Callable, Optional
from code_agent import CodeAgent, CodeEnvironment


@dataclass
class ProjectTask:
    """项目任务"""
    name: str
    description: str
    target_files: List[str]
    success_criteria: Optional[Callable] = None
    max_steps: int = 50


class ProjectTaskLibrary:
    """项目任务库"""
    
    @staticmethod
    def get_refactor_path_finding_task() -> ProjectTask:
        """重构路径查找任务"""
        return ProjectTask(
            name="refactor_path_finding",
            description="重构 all_path_TODO1.py，移除硬编码路径和调试打印",
            target_files=["all_path_TODO1.py"],
            max_steps=30
        )
    
    @staticmethod
    def get_add_type_hints_task() -> ProjectTask:
        """添加类型提示任务"""
        return ProjectTask(
            name="add_type_hints",
            description="为 test_bpr.py 添加类型提示",
            target_files=["test_bpr.py"],
            max_steps=20
        )
    
    @staticmethod
    def get_improve_documentation_task() -> ProjectTask:
        """改进文档任务"""
        return ProjectTask(
            name="improve_documentation",
            description="为核心函数添加详细的文档字符串",
            target_files=["all_path_TODO1.py", "test_bpr.py"],
            max_steps=25
        )
    
    @staticmethod
    def get_fix_code_issues_task() -> ProjectTask:
        """修复代码问题任务"""
        return ProjectTask(
            name="fix_code_issues",
            description="修复代码审查中发现的问题",
            target_files=["all_path_TODO1.py"],
            max_steps=40
        )
    
    @staticmethod
    def get_all_tasks() -> List[ProjectTask]:
        """获取所有任务"""
        return [
            ProjectTaskLibrary.get_refactor_path_finding_task(),
            ProjectTaskLibrary.get_add_type_hints_task(),
            ProjectTaskLibrary.get_improve_documentation_task(),
            ProjectTaskLibrary.get_fix_code_issues_task(),
        ]


class ProjectAgent:
    """项目专用 Agent"""
    
    def __init__(self, workspace: str = "."):
        from code_agent import create_agent_for_project
        self.agent = create_agent_for_project(workspace)
        self.task_library = ProjectTaskLibrary()
    
    def execute_task(self, task_name: str) -> dict:
        """执行指定任务"""
        tasks = {t.name: t for t in self.task_library.get_all_tasks()}
        
        if task_name not in tasks:
            print(f"错误: 任务 '{task_name}' 不存在")
            print(f"可用任务: {list(tasks.keys())}")
            return {'success': False, 'error': 'Task not found'}
        
        task = tasks[task_name]
        
        print(f"\n执行任务: {task.name}")
        print(f"描述: {task.description}")
        print(f"目标文件: {task.target_files}")
        
        result = self.agent.run_task(task.description)
        
        return result
    
    def list_tasks(self):
        """列出所有可用任务"""
        tasks = self.task_library.get_all_tasks()
        
        print("\n可用任务列表:")
        print("-" * 60)
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task.name}")
            print(f"   描述: {task.description}")
            print(f"   文件: {', '.join(task.target_files)}")
            print(f"   最大步数: {task.max_steps}")
            print()
    
    def analyze_project(self):
        """分析项目"""
        print("\n项目分析")
        print("=" * 60)
        
        state = self.agent.environment.reset()
        
        print(f"\n项目文件:")
        for filepath in state['files']:
            print(f"  - {filepath}")
        
        print(f"\n总文件数: {len(state['files'])}")
        
        return state


def quick_start():
    """快速开始"""
    print("\n" + "="*60)
    print("SingleUE 项目 Agent 快速开始")
    print("="*60)
    
    agent = ProjectAgent(".")
    
    agent.list_tasks()
    
    print("\n开始执行第一个任务...")
    result = agent.execute_task("refactor_path_finding")
    
    print("\n任务结果:")
    print(f"  成功: {result['success']}")
    print(f"  总奖励: {result['total_reward']:.2f}")
    print(f"  步数: {result['steps']}")
    
    return agent


if __name__ == "__main__":
    agent = quick_start()
