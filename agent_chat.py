"""
自然语言对话接口 - 让 Agent 支持自然语言交互
"""

import re
import json
import readline
from typing import List, Dict, Callable
from dataclasses import dataclass


@dataclass
class Command:
    """命令定义"""
    name: str
    description: str
    patterns: List[str]
    handler: Callable
    params: List[str] = None


class DialogManager:
    """对话管理器"""
    
    def __init__(self, agent):
        self.agent = agent
        self.commands = self._register_commands()
        self.history = []
    
    def _register_commands(self) -> List[Command]:
        """注册命令"""
        return [
            Command(
                name="read",
                description="读取文件内容",
                patterns=[
                    r"读取(.+?)文件",
                    r"查看(.+?)文件",
                    r"打开(.+?)",
                    r"读(.+?).py"
                ],
                handler=self._handle_read_file,
                params=["filepath"]
            ),
            Command(
                name="edit",
                description="编辑代码",
                patterns=[
                    r"修改(.+?)文件",
                    r"编辑(.+?)",
                    r"更改(.+?).py"
                ],
                handler=self._handle_edit_file,
                params=["filepath"]
            ),
            Command(
                name="test",
                description="运行测试",
                patterns=[
                    r"运行测试",
                    r"执行测试",
                    r"测试代码",
                    r"运行(.+?)测试"
                ],
                handler=self._handle_run_tests,
                params=["test_file"]
            ),
            Command(
                name="analyze",
                description="分析代码",
                patterns=[
                    r"分析(.+?)",
                    r"代码分析",
                    r"检查代码",
                    r"评估(.+?).py"
                ],
                handler=self._handle_analyze_code,
                params=["filepath"]
            ),
            Command(
                name="search",
                description="搜索代码",
                patterns=[
                    r"搜索(.+?)",
                    r"查找(.+?)",
                    r"搜索代码中的(.+?)"
                ],
                handler=self._handle_search_code,
                params=["pattern"]
            ),
            Command(
                name="task",
                description="执行任务",
                patterns=[
                    r"执行任务(.+?)",
                    r"运行任务(.+?)",
                    r"开始(.+?)任务"
                ],
                handler=self._handle_execute_task,
                params=["task_name"]
            ),
            Command(
                name="list_tasks",
                description="列出任务",
                patterns=[
                    r"有哪些任务",
                    r"任务列表",
                    r"查看任务",
                    r"可用任务"
                ],
                handler=self._handle_list_tasks
            ),
            Command(
                name="project",
                description="分析项目",
                patterns=[
                    r"分析项目",
                    r"项目概览",
                    r"项目结构",
                    r"查看项目"
                ],
                handler=self._handle_analyze_project
            ),
            Command(
                name="help",
                description="显示帮助",
                patterns=[
                    r"帮助",
                    r"帮助我",
                    r"显示帮助",
                    r"命令列表"
                ],
                handler=self._handle_help
            ),
            Command(
                name="exit",
                description="退出",
                patterns=[
                    r"退出",
                    r"离开",
                    r"结束",
                    r"拜拜"
                ],
                handler=self._handle_exit
            )
        ]
    
    def parse_command(self, user_input: str) -> Dict:
        """解析用户输入"""
        user_input = user_input.strip()
        
        for cmd in self.commands:
            for pattern in cmd.patterns:
                match = re.search(pattern, user_input)
                if match:
                    params = match.groups() if match.groups() else []
                    return {
                        'command': cmd.name,
                        'description': cmd.description,
                        'handler': cmd.handler,
                        'params': params
                    }
        
        return {
            'command': None,
            'description': '未知命令',
            'handler': self._handle_unknown,
            'params': [user_input]
        }
    
    def _handle_read_file(self, filepath: str):
        """处理读取文件命令"""
        result = self.agent.agent.environment.executor.execute({
            'type': 'read_file',
            'params': {'filepath': filepath.strip()}
        })
        
        if result['success']:
            print(f"\n📄 文件内容 ({filepath}):")
            print("-" * 60)
            content = result['content']
            lines = content.split('\n')
            for i, line in enumerate(lines[:50], 1):
                print(f"{i:4d}: {line}")
            if len(lines) > 50:
                print(f"... (还有 {len(lines) - 50} 行)")
            print("-" * 60)
        else:
            print(f"❌ 读取失败: {result['error']}")
    
    def _handle_edit_file(self, filepath: str):
        """处理编辑文件命令"""
        print(f"\n📝 准备编辑文件: {filepath}")
        print("请输入要修改的旧代码（空行结束）:")
        
        old_code = []
        while True:
            line = input("> ")
            if not line:
                break
            old_code.append(line)
        old_code = '\n'.join(old_code)
        
        print("\n请输入新代码（空行结束）:")
        new_code = []
        while True:
            line = input("> ")
            if not line:
                break
            new_code.append(line)
        new_code = '\n'.join(new_code)
        
        result = self.agent.agent.environment.executor.execute({
            'type': 'edit_code',
            'params': {
                'filepath': filepath.strip(),
                'old_code': old_code,
                'new_code': new_code
            }
        })
        
        if result['success']:
            print("✅ 编辑成功!")
        else:
            print(f"❌ 编辑失败: {result['error']}")
    
    def _handle_run_tests(self, test_file: str = None):
        """处理运行测试命令"""
        print(f"\n🧪 运行测试{' (文件: ' + test_file + ')' if test_file else ''}...")
        
        result = self.agent.agent.environment.executor.execute({
            'type': 'run_tests',
            'params': {'test_file': test_file.strip() if test_file else None}
        })
        
        if result['success']:
            print("\n测试结果:")
            print("-" * 60)
            print(result['stdout'][-2000:] if len(result['stdout']) > 2000 else result['stdout'])
            if result.get('passed'):
                print("✅ 所有测试通过!")
            else:
                print("❌ 测试失败")
                if result['stderr']:
                    print("\n错误信息:")
                    print(result['stderr'])
        else:
            print(f"❌ 运行失败: {result['error']}")
    
    def _handle_analyze_code(self, filepath: str):
        """处理分析代码命令"""
        result = self.agent.agent.environment.executor.execute({
            'type': 'analyze_code',
            'params': {'filepath': filepath.strip()}
        })
        
        if result['success']:
            analysis = result['analysis']
            print(f"\n📊 代码分析结果 ({filepath}):")
            print("-" * 60)
            print(f"总行数: {analysis['total_lines']}")
            print(f"代码行: {analysis['code_lines']}")
            print(f"注释行: {analysis['comment_lines']}")
            print(f"空行: {analysis['blank_lines']}")
            print(f"注释比例: {(analysis['comment_lines'] / analysis['total_lines'] * 100):.1f}%")
            print("-" * 60)
        else:
            print(f"❌ 分析失败: {result['error']}")
    
    def _handle_search_code(self, pattern: str):
        """处理搜索代码命令"""
        result = self.agent.agent.environment.executor.execute({
            'type': 'search_code',
            'params': {'pattern': pattern.strip()}
        })
        
        if result['success']:
            matches = result['matches']
            print(f"\n🔍 搜索结果 (模式: '{pattern}'):")
            print("-" * 60)
            if matches:
                for i, match in enumerate(matches, 1):
                    print(f"{i}. {match}")
            else:
                print("没有找到匹配的文件")
            print("-" * 60)
        else:
            print(f"❌ 搜索失败: {result['error']}")
    
    def _handle_execute_task(self, task_name: str):
        """处理执行任务命令"""
        print(f"\n🚀 执行任务: {task_name}")
        result = self.agent.execute_task(task_name.strip())
        
        print(f"\n任务结果:")
        print(f"  成功: {'✅' if result['success'] else '❌'}")
        print(f"  总奖励: {result['total_reward']:.2f}")
        print(f"  步数: {result['steps']}")
    
    def _handle_list_tasks(self):
        """处理列出任务命令"""
        self.agent.list_tasks()
    
    def _handle_analyze_project(self):
        """处理分析项目命令"""
        self.agent.analyze_project()
    
    def _handle_help(self):
        """处理帮助命令"""
        print("\n📖 可用命令:")
        print("-" * 60)
        for cmd in self.commands:
            print(f"{cmd.name}: {cmd.description}")
            print(f"   示例: {', '.join(cmd.patterns[:2])}")
        print("-" * 60)
    
    def _handle_exit(self):
        """处理退出命令"""
        print("\n👋 再见!")
        exit(0)
    
    def _handle_unknown(self, user_input: str):
        """处理未知命令"""
        print(f"\n❓ 抱歉，我不太理解: '{user_input}'")
        print("请尝试以下命令:")
        print("  - 读取 test_bpr.py 文件")
        print("  - 运行测试")
        print("  - 分析项目")
        print("  - 帮助")
    
    def chat(self):
        """启动对话模式"""
        print("\n" + "="*60)
        print("🎯 代码 Agent 对话系统")
        print("="*60)
        print("欢迎使用代码 Agent! 请用自然语言输入命令。")
        print("输入 '帮助' 查看可用命令，输入 '退出' 结束对话。")
        print("-" * 60)
        
        while True:
            try:
                user_input = input("\n你: ")
                if not user_input.strip():
                    continue
                
                # 解析命令
                parsed = self.parse_command(user_input)
                
                # 执行命令
                print(f"\n🤖 Agent: 正在{parsed['description']}...")
                
                # 调用处理函数
                if parsed['params']:
                    parsed['handler'](*parsed['params'])
                else:
                    parsed['handler']()
                
                # 记录历史
                self.history.append({
                    'user': user_input,
                    'response': parsed['description']
                })
                
            except KeyboardInterrupt:
                print("\n👋 再见!")
                break
            except Exception as e:
                print(f"❌ 发生错误: {e}")


class AgentChat:
    """Agent 聊天接口"""
    
    @staticmethod
    def start():
        """启动聊天界面"""
        from project_agent import ProjectAgent
        
        # 创建项目 Agent
        agent = ProjectAgent(".")
        
        # 创建对话管理器
        dialog = DialogManager(agent)
        
        # 启动对话
        dialog.chat()


if __name__ == "__main__":
    AgentChat.start()
