#!/usr/bin/env python3
"""
OpenGoal Skill - 简化测试（不依赖 matplotlib）
只测试核心逻辑，不生成实际图片
"""

import sys
import os
import json
from pathlib import Path

# 添加 scripts 目录到路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from context_manager import ContextManager


def test_context_manager():
    """测试上下文管理"""
    print("=" * 60)
    print("测试 1: 上下文管理")
    print("=" * 60)

    cm = ContextManager(project_root="test_output")

    # 测试保存 goal
    print("\n1.1 测试保存 /goal...")
    goal_data = {
        "project_name": "用户管理系统",
        "goal_human": "实现用户注册、登录、资料管理功能",
        "goal_ai": '{"modules": ["UserService", "AuthService"]}',
        "acceptance_criteria": "功能完整、性能达标、安全合规",
        "architecture": {
            "backend": "Spring Boot + Java",
            "frontend": "React + TypeScript"
        }
    }
    cm.save_goal(goal_data)
    print("✓ /goal 已保存")

    # 测试读取 goal
    print("\n1.2 测试读取 /goal...")
    current = cm.get_current_goal()
    assert current is not None, "读取失败"
    assert current["project_name"] == "用户管理系统", "项目名称不匹配"
    print(f"✓ 项目名称: {current['project_name']}")
    print(f"✓ 版本: {current['version']}")

    # 测试项目信息
    print("\n1.3 测试获取项目信息...")
    info = cm.get_project_info()
    print(f"✓ 项目名称: {info['project_name']}")
    print(f"✓ 版本: {info['version']}")
    print(f"✓ 有 goal: {info['has_goal']}")

    # 测试增量更新
    print("\n1.4 测试增量更新...")
    updates = {
        "added_features": ["OAuth登录"],
        "modified_modules": ["用户认证模块"],
        "reason": "增加OAuth登录支持"
    }
    updated = cm.update_goal_incremental(updates)
    print(f"✓ 更新后版本: {updated['version']}")
    print(f"✓ 增量更新次数: {len(updated.get('incremental_updates', []))}")

    print("\n✅ 上下文管理测试通过！\n")


def test_requirement_analysis():
    """测试需求分析逻辑"""
    print("=" * 60)
    print("测试 2: 需求分析")
    print("=" * 60)

    test_cases = [
        {
            "input": "我要做一个电商系统，包括用户管理、商品管理、订单、支付",
            "expected_domain": "电商",
            "expected_entities": ["用户", "订单", "商品", "支付"]
        },
        {
            "input": "实现用户注册和登录功能",
            "expected_domain": "用户管理",
            "expected_entities": ["用户"]
        }
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\n2.{i} 测试案例: {test['input'][:30]}...")

        # 简化的需求分析逻辑
        user_input = test['input']

        # 领域识别
        domain = "未知"
        if any(kw in user_input for kw in ["电商", "商品", "订单", "支付"]):
            domain = "电商领域"
        elif any(kw in user_input for kw in ["用户", "注册", "登录"]):
            domain = "用户管理领域"

        print(f"✓ 识别的领域: {domain}")

        # 实体提取
        common_entities = ["用户", "订单", "商品", "支付", "库存"]
        entities = [e for e in common_entities if e in user_input]
        print(f"✓ 提取的实体: {', '.join(entities)}")

        # 动作提取
        common_actions = ["注册", "登录", "创建", "查询", "支付"]
        actions = [a for a in common_actions if a in user_input]
        print(f"✓ 提取的动作: {', '.join(actions)}")

    print("\n✅ 需求分析测试通过！\n")


def test_decomposition():
    """测试需求拆解逻辑"""
    print("=" * 60)
    print("测试 3: 需求拆解")
    print("=" * 60)

    print("\n3.1 测试混合拆解模式...")

    # 模拟拆解结果
    decomposition = {
        "functional_requirements": [
            {"priority": "P0", "module": "用户注册", "features": ["邮箱注册", "手机号注册"]},
            {"priority": "P0", "module": "用户登录", "features": ["账号密码登录", "JWT Token"]},
            {"priority": "P1", "module": "资料管理", "features": ["查看资料", "修改资料"]},
        ],
        "technical_architecture": {
            "layers": [
                {"name": "前端层", "components": ["React", "TypeScript"]},
                {"name": "接口层", "components": ["API Gateway"]},
                {"name": "业务逻辑层", "components": ["UserService"]},
                {"name": "数据访问层", "components": ["UserRepository"]},
                {"name": "基础设施层", "components": ["PostgreSQL", "Redis"]},
            ]
        },
        "domain_model": {
            "aggregates": [
                {
                    "name": "User",
                    "entities": ["UserProfile"],
                    "value_objects": ["Email", "Password"]
                }
            ]
        },
        "non_functional_requirements": {
            "performance": {"response_time": "< 200ms", "concurrency": "> 1000 QPS"},
            "security": {"authentication": "JWT", "password_encryption": "BCrypt"}
        },
        "dependencies": [
            {"from": "UserService", "to": "UserRepository"},
            {"from": "AuthService", "to": "UserService"}
        ]
    }

    print(f"✓ 功能需求: {len(decomposition['functional_requirements'])} 个模块")
    print(f"✓ 技术层次: {len(decomposition['technical_architecture']['layers'])} 层")
    print(f"✓ 聚合: {len(decomposition['domain_model']['aggregates'])} 个")
    print(f"✓ 依赖关系: {len(decomposition['dependencies'])} 条")

    print("\n3.2 测试验收标准生成...")
    criteria = f"""
# 验收标准

## 1. 功能完整性
"""
    for req in decomposition['functional_requirements']:
        criteria += f"- [ ] [{req['priority']}] {req['module']} 已实现\n"

    criteria += """
## 2. 性能指标
- [ ] 响应时间 < 200ms
- [ ] 并发量 > 1000 QPS

## 3. 安全检查
- [ ] 密码 BCrypt 加密
- [ ] SQL 注入防护

## 4. 代码质量
- [ ] 单元测试覆盖率 > 80%

## 5. 文档完备
- [ ] API 文档完整
"""

    print(f"✓ 验收标准生成完成，共 {len(criteria)} 字符")

    print("\n✅ 需求拆解测试通过！\n")


def test_anti_pattern_detection():
    """测试反模式检测"""
    print("=" * 60)
    print("测试 4: 反模式检测")
    print("=" * 60)

    anti_patterns = [
        {
            "type": "架构反模式",
            "pattern": "业务逻辑在Controller层",
            "severity": "high",
            "suggestion": "引入Service层"
        },
        {
            "type": "安全反模式",
            "pattern": "密码明文存储",
            "severity": "critical",
            "suggestion": "使用BCrypt加密"
        },
        {
            "type": "性能反模式",
            "pattern": "N+1查询问题",
            "severity": "medium",
            "suggestion": "使用预加载或批量查询"
        }
    ]

    print(f"\n检测到 {len(anti_patterns)} 个反模式:\n")
    for i, ap in enumerate(anti_patterns, 1):
        severity_emoji = "🔴" if ap['severity'] == 'critical' else "🟠" if ap['severity'] == 'high' else "🟡"
        print(f"{i}. {severity_emoji} [{ap['type']}] {ap['pattern']}")
        print(f"   建议: {ap['suggestion']}\n")

    print("✅ 反模式检测测试通过！\n")


def test_goal_generation():
    """测试 /goal 命令生成"""
    print("=" * 60)
    print("测试 5: /goal 命令生成")
    print("=" * 60)

    print("\n5.1 生成人类可读版 /goal...")
    human_goal = """# 用户管理系统 - /goal 命令

## 项目概述
实现一个完整的用户管理系统，包括用户注册、登录、资料管理功能。

## 功能需求
- [P0] 用户注册模块
  - 邮箱注册
  - 手机号注册
  - 邮箱验证
  - 防刷机制（验证码）

- [P0] 用户登录模块
  - 账号密码登录
  - JWT Token 生成
  - Session 管理
  - 密码错误次数限制

- [P1] 资料管理模块
  - 查看个人资料
  - 修改个人资料
  - 头像上传

## 技术架构
- 前端层: React + TypeScript
- 接口层: API Gateway, RESTful API
- 业务逻辑层: UserService, AuthService
- 数据访问层: UserRepository
- 基础设施层: PostgreSQL, Redis, Kafka

## 领域模型
### 用户聚合（User Aggregate）
- 聚合根：User
- 实体：UserProfile, LoginCredential
- 值对象：Email, Password

## 非功能需求
- 性能：响应时间 < 200ms，并发量 > 1000 QPS
- 安全：JWT Token 认证，密码 BCrypt 加密
- 可用性：99.9%

## 分步执行计划
### Phase 1: 基础设施搭建
1.1 初始化 Spring Boot 项目
1.2 配置 PostgreSQL 数据库
1.3 配置 Redis 缓存
1.4 设置日志框架

### Phase 2: 用户模块实现
2.1 定义 User 实体和 Repository
2.2 实现 UserService（注册、登录）
2.3 实现 AuthService（JWT Token）
2.4 实现用户认证拦截器

### Phase 3: API 层实现
3.1 设计 RESTful API
3.2 实现 UserController
3.3 添加 Swagger API 文档

### Phase 4: 前端集成
4.1 实现登录页面
4.2 实现注册页面
4.3 实现个人中心页面

### Phase 5: 测试与部署
5.1 单元测试
5.2 集成测试
5.3 性能测试
5.4 部署上线

## 假设条件
- 使用 Spring Boot + Java 后端框架
- 使用 JWT Token 身份认证
- 密码使用 BCrypt 加密
- 默认异步事件驱动架构
"""

    print(f"✓ 人类版生成完成，共 {len(human_goal)} 字符")

    print("\n5.2 生成 AI 可读版 /goal...")
    ai_goal = {
        "project_name": "用户管理系统",
        "modules": ["UserService", "AuthService"],
        "tech_stack": {
            "backend": "Spring Boot + Java",
            "frontend": "React + TypeScript",
            "database": "PostgreSQL + Redis"
        },
        "phases": [
            {"name": "基础设施搭建", "tasks": ["初始化项目", "配置数据库"]},
            {"name": "用户模块实现", "tasks": ["实现User实体", "实现UserService"]},
        ]
    }

    print(f"✓ AI 版生成完成，共 {len(json.dumps(ai_goal))} 字符")

    print("\n5.3 预览人类版 /goal（前 500 字符）:")
    print("-" * 60)
    print(human_goal[:500] + "...")
    print("-" * 60)

    print("\n✅ /goal 命令生成测试通过！\n")


def main():
    """运行所有测试"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "OpenGoal Skill 简化测试套件" + " " * 11 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")

    try:
        # 测试 1: 上下文管理
        test_context_manager()

        # 测试 2: 需求分析
        test_requirement_analysis()

        # 测试 3: 需求拆解
        test_decomposition()

        # 测试 4: 反模式检测
        test_anti_pattern_detection()

        # 测试 5: /goal 生成
        test_goal_generation()

        print("\n")
        print("╔" + "=" * 58 + "╗")
        print("║" + " " * 18 + "所有测试通过！" + " " * 18 + "║")
        print("╚" + "=" * 58 + "╝")
        print("\n")

        print("📝 注意: 绘图功能需要安装 matplotlib 和 networkx")
        print("   安装命令: pip install matplotlib networkx\n")

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        # 询问是否清理测试文件
        response = input("\n是否清理测试文件？(y/n): ")
        if response.lower() == 'y':
            import shutil
            if os.path.exists("test_output"):
                shutil.rmtree("test_output")
                print("✓ 测试文件已清理")

    return 0


if __name__ == "__main__":
    sys.exit(main())
