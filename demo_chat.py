"""
自然语言交互演示脚本
展示如何用自然语言与 Agent 交互
"""

from agent_chat import DialogManager
from project_agent import ProjectAgent


def demo_natural_language_interaction():
    """演示自然语言交互"""
    print("\n" + "="*60)
    print("🎯 自然语言对话 Agent 演示")
    print("="*60 + "\n")
    
    # 创建项目 Agent
    agent = ProjectAgent(".")
    
    # 创建对话管理器
    dialog = DialogManager(agent)
    
    # 演示对话
    demo_queries = [
        "分析项目",
        "有哪些任务",
        "读取 test_bpr.py 文件",
        "运行测试",
        "分析 test_bpr.py"
    ]
    
    for query in demo_queries:
        print(f"\n{'='*60}")
        print(f"你: {query}")
        print(f"{'='*60}")
        
        # 解析命令
        parsed = dialog.parse_command(query)
        print(f"🤖 Agent: 正在{parsed['description']}...")
        
        # 执行命令
        try:
            if parsed['params']:
                parsed['handler'](*parsed['params'])
            else:
                parsed['handler']()
        except Exception as e:
            print(f"❌ 错误: {e}")
        
        print("\n" + "-"*60 + "\n")


if __name__ == "__main__":
    demo_natural_language_interaction()
