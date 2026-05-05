"""
高级代码 Agent 系统 - 核心实现
基于强化学习的智能代码助手
"""

import os
import sys
import json
import pickle
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import deque
import random
import numpy as np
import pandas as pd


@dataclass
class AgentConfig:
    """Agent 配置"""
    workspace: str = "./workspace"
    max_steps: int = 100
    learning_rate: float = 3e-4
    gamma: float = 0.99
    epsilon: float = 0.1
    memory_size: int = 10000
    batch_size: int = 32
    

class Memory:
    """记忆系统"""
    
    def __init__(self, capacity: int = 10000):
        self.capacity = capacity
        self.working_memory = deque(maxlen=100)
        self.experience_buffer = deque(maxlen=capacity)
        self.long_term_knowledge = {
            'code_patterns': {},
            'best_practices': {},
            'bug_patterns': {}
        }
    
    def add_experience(self, state, action, reward, next_state, done):
        """添加经验"""
        self.experience_buffer.append({
            'state': state,
            'action': action,
            'reward': reward,
            'next_state': next_state,
            'done': done
        })
    
    def sample(self, batch_size: int):
        """采样经验"""
        if len(self.experience_buffer) < batch_size:
            return list(self.experience_buffer)
        return random.sample(list(self.experience_buffer), batch_size)
    
    def save(self, filepath: str):
        """保存记忆"""
        data = {
            'experience_buffer': list(self.experience_buffer),
            'long_term_knowledge': self.long_term_knowledge
        }
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
    
    def load(self, filepath: str):
        """加载记忆"""
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
                self.experience_buffer = deque(data['experience_buffer'], maxlen=self.capacity)
                self.long_term_knowledge = data.get('long_term_knowledge', {})


class ActionExecutor:
    """动作执行器"""
    
    def __init__(self, workspace: str):
        self.workspace = Path(workspace)
    
    def execute(self, action: Dict) -> Dict:
        """执行动作"""
        action_type = action.get('type')
        params = action.get('params', {})
        
        try:
            if action_type == 'read_file':
                return self._read_file(params['filepath'])
            elif action_type == 'edit_code':
                return self._edit_code(
                    params['filepath'],
                    params.get('old_code', ''),
                    params.get('new_code', '')
                )
            elif action_type == 'run_tests':
                return self._run_tests(params.get('test_file'))
            elif action_type == 'search_code':
                return self._search_code(params['pattern'])
            elif action_type == 'analyze_code':
                return self._analyze_code(params['filepath'])
            else:
                return {'success': False, 'error': f'Unknown action: {action_type}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _read_file(self, filepath: str) -> Dict:
        """读取文件"""
        full_path = self.workspace / filepath
        if not full_path.exists():
            return {'success': False, 'error': 'File not found'}
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            'success': True,
            'content': content,
            'lines': len(content.split('\n'))
        }
    
    def _edit_code(self, filepath: str, old_code: str, new_code: str) -> Dict:
        """编辑代码"""
        full_path = self.workspace / filepath
        if not full_path.exists():
            return {'success': False, 'error': 'File not found'}
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_code and old_code in content:
            content = content.replace(old_code, new_code)
        elif not old_code:
            content = new_code
        else:
            return {'success': False, 'error': 'Old code not found'}
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {'success': True, 'action': 'edit_code'}
    
    def _run_tests(self, test_file: Optional[str] = None) -> Dict:
        """运行测试"""
        cmd = ['python', '-m', 'pytest', '-v']
        if test_file:
            cmd.append(test_file)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(self.workspace)
        )
        
        return {
            'success': True,
            'passed': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
    
    def _search_code(self, pattern: str) -> Dict:
        """搜索代码"""
        matches = []
        for filepath in self.workspace.rglob('*.py'):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if pattern in content:
                        matches.append(str(filepath.relative_to(self.workspace)))
            except:
                pass
        
        return {'success': True, 'matches': matches}
    
    def _analyze_code(self, filepath: str) -> Dict:
        """分析代码"""
        full_path = self.workspace / filepath
        if not full_path.exists():
            return {'success': False, 'error': 'File not found'}
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        return {
            'success': True,
            'analysis': {
                'total_lines': len(lines),
                'code_lines': sum(1 for line in lines if line.strip() and not line.strip().startswith('#')),
                'comment_lines': sum(1 for line in lines if line.strip().startswith('#')),
                'blank_lines': sum(1 for line in lines if not line.strip())
            }
        }


class RewardCalculator:
    """奖励计算器"""
    
    def __init__(self):
        self.weights = {
            'functionality': 0.4,
            'quality': 0.3,
            'efficiency': 0.2,
            'exploration': 0.1
        }
    
    def calculate(self, action: Dict, result: Dict, info: Dict) -> float:
        """计算奖励"""
        reward = 0.0
        
        if result.get('success'):
            reward += 1.0
            
            if result.get('passed'):
                reward += 5.0
            
            if 'analysis' in result:
                analysis = result['analysis']
                if analysis['comment_lines'] > 0:
                    reward += 0.5
        else:
            reward -= 1.0
        
        return reward


class CodeEnvironment:
    """代码环境"""
    
    def __init__(self, workspace: str, config: AgentConfig):
        self.workspace = Path(workspace)
        self.config = config
        self.executor = ActionExecutor(workspace)
        self.reward_calculator = RewardCalculator()
        self.steps_taken = 0
        self.current_state = {}
        self.action_history = []
    
    def reset(self) -> Dict:
        """重置环境"""
        self.steps_taken = 0
        self.action_history = []
        self.current_state = self._get_state()
        return self.current_state
    
    def step(self, action: Dict) -> Tuple[Dict, float, bool, Dict]:
        """执行一步"""
        result = self.executor.execute(action)
        
        reward = self.reward_calculator.calculate(action, result, {})
        
        self.steps_taken += 1
        self.action_history.append(action)
        
        done = (
            self.steps_taken >= self.config.max_steps or
            result.get('passed', False)
        )
        
        self.current_state = self._get_state()
        
        info = {
            'result': result,
            'steps_taken': self.steps_taken
        }
        
        return self.current_state, reward, done, info
    
    def _get_state(self) -> Dict:
        """获取当前状态"""
        files = list(self.workspace.rglob('*.py'))
        return {
            'files': [str(f.relative_to(self.workspace)) for f in files],
            'steps_taken': self.steps_taken
        }


class CodeAgent:
    """代码 Agent"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.memory = Memory(config.memory_size)
        self.environment = None
        
        self.action_space = [
            'read_file',
            'edit_code',
            'run_tests',
            'search_code',
            'analyze_code'
        ]
    
    def set_environment(self, workspace: str):
        """设置环境"""
        self.environment = CodeEnvironment(workspace, self.config)
    
    def select_action(self, state: Dict) -> Dict:
        """选择动作"""
        if random.random() < self.config.epsilon:
            return self._random_action()
        else:
            return self._policy_action(state)
    
    def _random_action(self) -> Dict:
        """随机动作"""
        action_type = random.choice(self.action_space)
        
        if action_type == 'read_file':
            files = self.environment.current_state.get('files', [])
            filepath = random.choice(files) if files else 'main.py'
            return {
                'type': 'read_file',
                'params': {'filepath': filepath}
            }
        elif action_type == 'run_tests':
            return {'type': 'run_tests', 'params': {}}
        elif action_type == 'analyze_code':
            files = self.environment.current_state.get('files', [])
            filepath = random.choice(files) if files else 'main.py'
            return {
                'type': 'analyze_code',
                'params': {'filepath': filepath}
            }
        else:
            return {'type': 'search_code', 'params': {'pattern': 'def '}}
    
    def _policy_action(self, state: Dict) -> Dict:
        """策略动作"""
        return self._random_action()
    
    def train(self, num_episodes: int = 10):
        """训练 Agent"""
        if not self.environment:
            raise ValueError("Environment not set. Call set_environment() first.")
        
        episode_rewards = []
        
        for episode in range(num_episodes):
            state = self.environment.reset()
            episode_reward = 0
            done = False
            
            while not done:
                action = self.select_action(state)
                next_state, reward, done, info = self.environment.step(action)
                
                self.memory.add_experience(state, action, reward, next_state, done)
                
                episode_reward += reward
                state = next_state
            
            episode_rewards.append(episode_reward)
            
            if (episode + 1) % 5 == 0:
                avg_reward = np.mean(episode_rewards[-5:])
                print(f"Episode {episode + 1}/{num_episodes}, "
                      f"Avg Reward (last 5): {avg_reward:.2f}")
        
        return episode_rewards
    
    def run_task(self, task_description: str) -> Dict:
        """执行任务"""
        if not self.environment:
            raise ValueError("Environment not set. Call set_environment() first.")
        
        print(f"\n{'='*60}")
        print(f"任务: {task_description}")
        print(f"{'='*60}\n")
        
        state = self.environment.reset()
        done = False
        total_reward = 0
        
        while not done:
            action = self.select_action(state)
            next_state, reward, done, info = self.environment.step(action)
            
            total_reward += reward
            
            print(f"步骤 {self.environment.steps_taken}: {action['type']}")
            if info['result'].get('success'):
                print(f"  ✓ 成功")
            else:
                print(f"  ✗ 失败: {info['result'].get('error', 'Unknown')}")
            
            state = next_state
        
        print(f"\n任务完成! 总奖励: {total_reward:.2f}")
        
        return {
            'success': done,
            'total_reward': total_reward,
            'steps': self.environment.steps_taken,
            'action_history': self.environment.action_history
        }
    
    def save(self, filepath: str):
        """保存 Agent"""
        self.memory.save(filepath)
        config_data = {
            'workspace': self.config.workspace,
            'max_steps': self.config.max_steps,
            'learning_rate': self.config.learning_rate,
            'gamma': self.config.gamma,
            'epsilon': self.config.epsilon
        }
        with open(filepath + '.config', 'w') as f:
            json.dump(config_data, f, indent=2)
    
    def load(self, filepath: str):
        """加载 Agent"""
        self.memory.load(filepath)
        if os.path.exists(filepath + '.config'):
            with open(filepath + '.config', 'r') as f:
                config_data = json.load(f)
                self.config = AgentConfig(**config_data)


def create_agent_for_project(workspace: str = ".") -> CodeAgent:
    """为当前项目创建 Agent"""
    config = AgentConfig(
        workspace=workspace,
        max_steps=50,
        learning_rate=3e-4,
        gamma=0.99,
        epsilon=0.2,
        memory_size=5000,
        batch_size=16
    )
    
    agent = CodeAgent(config)
    agent.set_environment(workspace)
    
    return agent


if __name__ == "__main__":
    agent = create_agent_for_project(".")
    
    print("代码 Agent 系统已初始化")
    print(f"工作空间: {agent.config.workspace}")
    print(f"最大步数: {agent.config.max_steps}")
    print(f"探索率: {agent.config.epsilon}")
