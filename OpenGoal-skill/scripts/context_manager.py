#!/usr/bin/env python3
"""
OpenGoal Skill - 上下文管理脚本
用于存储和读取项目的历史 /goal 命令和验收标准
"""

import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path


class ContextManager:
    """项目上下文管理器"""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.context_dir = self.project_root / ".opengoal"
        self.context_file = self.context_dir / "context.json"
        self._ensure_context_dir()

    def _ensure_context_dir(self):
        """确保上下文目录存在"""
        self.context_dir.mkdir(parents=True, exist_ok=True)

    def save_goal(self, goal_data: Dict[str, Any]) -> None:
        """
        保存 /goal 命令到上下文

        Args:
            goal_data: /goal 数据，格式:
            {
                "project_name": "用户管理系统",
                "goal_human": "人类可读的 /goal 命令",
                "goal_ai": "AI可读的 /goal 命令",
                "acceptance_criteria": "验收标准",
                "architecture": {...},
                "dependencies": [...],
                "assumptions": [...],
                "created_at": "2024-07-06T12:00:00Z",
                "version": 1
            }
        """
        context = self._load_context()

        # 添加时间戳和版本号
        goal_data["created_at"] = datetime.now().isoformat()
        goal_data["version"] = len(context.get("history", [])) + 1

        # 保存到历史记录
        if "history" not in context:
            context["history"] = []
        context["history"].append(goal_data)

        # 更新当前 goal
        context["current_goal"] = goal_data

        # 更新项目信息
        context["project_name"] = goal_data.get("project_name", "Unknown Project")
        context["last_updated"] = datetime.now().isoformat()

        self._save_context(context)

    def get_current_goal(self) -> Optional[Dict[str, Any]]:
        """
        获取当前的 /goal 命令

        Returns:
            当前的 goal 数据，如果不存在返回 None
        """
        context = self._load_context()
        return context.get("current_goal")

    def get_goal_history(self) -> List[Dict[str, Any]]:
        """
        获取所有历史 /goal 命令

        Returns:
            历史 goal 列表，按时间倒序排列
        """
        context = self._load_context()
        history = context.get("history", [])
        return sorted(history, key=lambda x: x.get("created_at", ""), reverse=True)

    def get_project_info(self) -> Dict[str, Any]:
        """
        获取项目信息

        Returns:
            项目信息字典
        """
        context = self._load_context()
        return {
            "project_name": context.get("project_name", "Unknown Project"),
            "last_updated": context.get("last_updated"),
            "version": len(context.get("history", [])),
            "has_goal": "current_goal" in context
        }

    def update_goal_incremental(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        增量更新当前 /goal

        Args:
            updates: 更新内容，格式:
            {
                "added_features": ["OAuth登录"],
                "modified_modules": ["用户认证模块"],
                "reason": "增加OAuth登录支持"
            }

        Returns:
            更新后的 goal 数据
        """
        current_goal = self.get_current_goal()
        if not current_goal:
            raise ValueError("没有找到当前的 /goal，请先创建初始 /goal")

        # 创建增量更新记录
        update_record = {
            "type": "incremental_update",
            "updates": updates,
            "timestamp": datetime.now().isoformat(),
            "previous_version": current_goal.get("version", 1)
        }

        # 合并更新（这里只是示例，实际逻辑需要根据具体需求实现）
        updated_goal = current_goal.copy()
        updated_goal["incremental_updates"] = current_goal.get("incremental_updates", [])
        updated_goal["incremental_updates"].append(update_record)

        # 保存更新后的 goal
        self.save_goal(updated_goal)

        return updated_goal

    def clear_context(self) -> None:
        """清空上下文（慎用）"""
        if self.context_file.exists():
            self.context_file.unlink()

    def _load_context(self) -> Dict[str, Any]:
        """从文件加载上下文"""
        if not self.context_file.exists():
            return {}

        try:
            with open(self.context_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"警告: 无法加载上下文文件: {e}")
            return {}

    def _save_context(self, context: Dict[str, Any]) -> None:
        """保存上下文到文件"""
        try:
            with open(self.context_file, 'w', encoding='utf-8') as f:
                json.dump(context, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"错误: 无法保存上下文文件: {e}")
            raise


def identify_project(project_name: Optional[str] = None,
                    working_dir: Optional[str] = None) -> tuple[str, bool]:
    """
    识别项目（根据项目名称+工作目录）

    Args:
        project_name: 用户提到的项目名称
        working_dir: 当前工作目录

    Returns:
        (project_root, is_existing_project)
    """
    if working_dir is None:
        working_dir = os.getcwd()

    project_root = working_dir

    # 检查是否存在 .opengoal 目录
    context_dir = Path(project_root) / ".opengoal"
    if context_dir.exists():
        # 验证项目名称是否匹配
        context_file = context_dir / "context.json"
        if context_file.exists():
            try:
                with open(context_file, 'r', encoding='utf-8') as f:
                    context = json.load(f)
                    existing_name = context.get("project_name", "")

                    # 如果用户提到的项目名称与现有项目匹配，认为是同一项目
                    if project_name and existing_name:
                        if project_name.lower() in existing_name.lower() or \
                           existing_name.lower() in project_name.lower():
                            return project_root, True
            except:
                pass

    # 如果没有找到匹配的项目，认为是新项目
    return project_root, False


def main():
    """测试用例"""
    # 创建上下文管理器
    cm = ContextManager(project_root=".")

    # 测试保存 goal
    print("测试保存 /goal...")
    goal_data = {
        "project_name": "用户管理系统",
        "goal_human": "实现一个用户管理系统，包括注册、登录、资料管理功能",
        "goal_ai": """
# 项目：用户管理系统

## 功能需求
- [P0] 用户注册
- [P0] 用户登录
- [P1] 资料管理

## 技术架构
- 后端：Spring Boot + Java
- 前端：React + TypeScript
- 数据库：PostgreSQL + Redis
        """,
        "acceptance_criteria": "功能完整、性能达标、安全合规",
        "architecture": {
            "frontend": "React + TypeScript",
            "backend": "Spring Boot + Java",
            "database": "PostgreSQL + Redis"
        },
        "dependencies": [
            {"from": "LoginService", "to": "UserRepository"}
        ],
        "assumptions": [
            "使用 JWT Token 认证",
            "密码使用 BCrypt 加密"
        ]
    }
    cm.save_goal(goal_data)
    print("✓ /goal 已保存")

    # 测试获取当前 goal
    print("\n测试获取当前 /goal...")
    current = cm.get_current_goal()
    if current:
        print(f"✓ 项目名称: {current.get('project_name')}")
        print(f"✓ 版本: {current.get('version')}")
        print(f"✓ 创建时间: {current.get('created_at')}")

    # 测试获取项目信息
    print("\n测试获取项目信息...")
    info = cm.get_project_info()
    print(f"✓ 项目名称: {info['project_name']}")
    print(f"✓ 最后更新: {info['last_updated']}")
    print(f"✓ 版本: {info['version']}")
    print(f"✓ 有 goal: {info['has_goal']}")

    # 测试增量更新
    print("\n测试增量更新...")
    updates = {
        "added_features": ["OAuth登录"],
        "modified_modules": ["用户认证模块"],
        "reason": "增加OAuth登录支持"
    }
    updated = cm.update_goal_incremental(updates)
    print(f"✓ 更新后版本: {updated.get('version')}")
    print(f"✓ 增量更新次数: {len(updated.get('incremental_updates', []))}")

    # 测试项目识别
    print("\n测试项目识别...")
    project_root, is_existing = identify_project(project_name="用户管理系统", working_dir=".")
    print(f"✓ 项目根目录: {project_root}")
    print(f"✓ 是否为现有项目: {is_existing}")

    print("\n所有测试通过！")


if __name__ == "__main__":
    main()
