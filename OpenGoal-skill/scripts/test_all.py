#!/usr/bin/env python3
"""
OpenGoal Skill - 测试脚本
验证所有核心功能是否正常工作
"""

import sys
import os
from pathlib import Path

# 添加 scripts 目录到路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from draw_diagrams import DiagramDrawer
from context_manager import ContextManager
from main import OpenGoalEngine


def test_diagram_drawer():
    """测试绘图功能"""
    print("=" * 60)
    print("测试 1: 绘图功能")
    print("=" * 60)

    drawer = DiagramDrawer(output_dir="test_output")

    # 测试依赖关系图
    print("\n1.1 测试依赖关系图...")
    dependencies = [
        {"from": "OrderService", "to": "UserService"},
        {"from": "OrderService", "to": "ProductService"},
        {"from": "OrderService", "to": "PaymentService"},
        {"from": "PaymentService", "to": "UserService"},
    ]
    dep_path = drawer.draw_dependency_graph(dependencies, title="订单系统依赖关系图")
    print(f"✓ 依赖关系图已生成: {dep_path}")

    # 测试架构图
    print("\n1.2 测试架构图...")
    layers = [
        {"name": "前端层", "components": ["React", "TypeScript"]},
        {"name": "接口层", "components": ["API Gateway", "REST API"]},
        {"name": "业务逻辑层", "components": ["UserService", "OrderService"]},
        {"name": "数据访问层", "components": ["Repository"]},
        {"name": "基础设施层", "components": ["PostgreSQL", "Redis"]},
    ]
    arch_path = drawer.draw_architecture_diagram(layers, title="系统架构图")
    print(f"✓ 架构图已生成: {arch_path}")

    # 测试服务关系图
    print("\n1.3 测试服务关系图...")
    services = [
        {"name": "UserService", "type": "core"},
        {"name": "OrderService", "type": "core"},
        {"name": "EmailService", "type": "support"},
    ]
    interactions = [
        {"from": "OrderService", "to": "UserService", "type": "sync"},
        {"from": "OrderService", "to": "EmailService", "type": "async"},
    ]
    service_path = drawer.draw_service_map(services, interactions, title="服务关系图")
    print(f"✓ 服务关系图已生成: {service_path}")

    # 测试领域模型图
    print("\n1.4 测试领域模型图...")
    aggregates = [
        {
            "name": "Order",
            "type": "aggregate_root",
            "entities": ["OrderItem"],
            "value_objects": ["Money", "Address"]
        },
        {
            "name": "User",
            "type": "aggregate_root",
            "entities": ["UserProfile"],
            "value_objects": ["Email"]
        },
    ]
    domain_path = drawer.draw_domain_model(aggregates, title="领域模型图")
    print(f"✓ 领域模型图已生成: {domain_path}")

    print("\n✅ 绘图功能测试通过！\n")


def test_context_manager():
    """测试上下文管理"""
    print("=" * 60)
    print("测试 2: 上下文管理")
    print("=" * 60)

    cm = ContextManager(project_root="test_output")

    # 测试保存 goal
    print("\n2.1 测试保存 /goal...")
    goal_data = {
        "project_name": "测试项目",
        "goal_human": "这是人类可读的 /goal",
        "goal_ai": "这是AI可读的 /goal",
        "acceptance_criteria": "测试验收标准",
    }
    cm.save_goal(goal_data)
    print("✓ /goal 已保存")

    # 测试读取 goal
    print("\n2.2 测试读取 /goal...")
    current = cm.get_current_goal()
    assert current is not None, "读取失败"
    assert current["project_name"] == "测试项目", "项目名称不匹配"
    print(f"✓ 读取成功: {current['project_name']}")

    # 测试项目信息
    print("\n2.3 测试获取项目信息...")
    info = cm.get_project_info()
    print(f"✓ 项目名称: {info['project_name']}")
    print(f"✓ 版本: {info['version']}")
    print(f"✓ 有 goal: {info['has_goal']}")

    print("\n✅ 上下文管理测试通过！\n")


def test_opengoal_engine():
    """测试 OpenGoal 主引擎"""
    print("=" * 60)
    print("测试 3: OpenGoal 主引擎")
    print("=" * 60)

    engine = OpenGoalEngine(project_root="test_output")

    # 测试需求分析
    print("\n3.1 测试需求分析...")
    user_input = "我要做一个用户管理系统，包括注册、登录、资料管理"
    analysis = engine.analyze_requirement(user_input)
    print(f"✓ 识别的领域: {analysis['domain']}")
    print(f"✓ 关键实体: {', '.join(analysis['key_entities'])}")
    print(f"✓ 动作: {', '.join(analysis['actions'])}")

    # 测试需求拆解
    print("\n3.2 测试需求拆解...")
    decomposition = engine.decompose_requirement(analysis)
    print(f"✓ 功能需求数量: {len(decomposition['functional_requirements'])}")
    print(f"✓ 技术层次: {len(decomposition['technical_architecture']['layers'])}")

    # 测试生成 /goal
    print("\n3.3 测试生成 /goal 命令...")
    human_goal, ai_goal = engine.generate_goal_command(decomposition)
    print(f"✓ 人类版长度: {len(human_goal)} 字符")
    print(f"✓ AI版长度: {len(ai_goal)} 字符")

    # 测试生成验收标准
    print("\n3.4 测试生成验收标准...")
    criteria = engine.generate_acceptance_criteria(decomposition)
    print(f"✓ 验收标准长度: {len(criteria)} 字符")

    print("\n✅ OpenGoal 主引擎测试通过！\n")


def test_integration():
    """集成测试：完整流程"""
    print("=" * 60)
    print("测试 4: 完整流程集成测试")
    print("=" * 60)

    engine = OpenGoalEngine(project_root="test_output")

    user_input = "我要做一个电商系统，包括用户管理、商品管理、订单、支付"

    print(f"\n用户输入: {user_input}\n")

    # 完整流程
    print("执行步骤 1/5: 分析需求...")
    analysis = engine.analyze_requirement(user_input)
    print(f"✓ 完成")

    print("执行步骤 2/5: 拆解需求...")
    decomposition = engine.decompose_requirement(analysis)
    print(f"✓ 完成")

    print("执行步骤 3/5: 生成 /goal 命令...")
    decomposition["project_name"] = "电商系统"
    decomposition["description"] = "完整的电商系统"
    human_goal, ai_goal = engine.generate_goal_command(decomposition)
    print(f"✓ 完成")

    print("执行步骤 4/5: 生成验收标准...")
    criteria = engine.generate_acceptance_criteria(decomposition)
    print(f"✓ 完成")

    print("执行步骤 5/5: 绘制图表...")
    diagram_paths = engine.draw_diagrams(decomposition)
    print(f"✓ 生成 {len(diagram_paths)} 个图表")

    # 保存结果
    print("\n保存上下文...")
    goal_data = {
        "project_name": "电商系统",
        "goal_human": human_goal,
        "goal_ai": ai_goal,
        "acceptance_criteria": criteria,
    }
    engine.context_manager.save_goal(goal_data)
    print("✓ 上下文已保存")

    print("\n✅ 完整流程集成测试通过！\n")

    # 输出结果预览
    print("=" * 60)
    print("输出预览")
    print("=" * 60)
    print("\n## 人类可读版 /goal 命令（前500字符）\n")
    print(human_goal[:500] + "...")
    print("\n## 生成的图表\n")
    for path in diagram_paths:
        print(f"- {path}")


def cleanup():
    """清理测试文件"""
    import shutil
    if os.path.exists("test_output"):
        shutil.rmtree("test_output")
        print("\n✓ 测试文件已清理")


def main():
    """运行所有测试"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "OpenGoal Skill 测试套件" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")

    try:
        # 测试 1: 绘图功能
        test_diagram_drawer()

        # 测试 2: 上下文管理
        test_context_manager()

        # 测试 3: OpenGoal 主引擎
        test_opengoal_engine()

        # 测试 4: 完整流程集成
        test_integration()

        print("\n")
        print("╔" + "=" * 58 + "╗")
        print("║" + " " * 18 + "所有测试通过！" + " " * 18 + "║")
        print("╚" + "=" * 58 + "╝")
        print("\n")

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        # 询问是否清理测试文件
        response = input("\n是否清理测试文件？(y/n): ")
        if response.lower() == 'y':
            cleanup()

    return 0


if __name__ == "__main__":
    sys.exit(main())
