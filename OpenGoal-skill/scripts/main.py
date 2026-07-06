#!/usr/bin/env python3
"""
OpenGoal Skill - 主执行引擎
整合需求分析、DDD/SOA分析、依赖分析、绘图等所有功能
"""

import sys
import os
import json
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path

# 添加 scripts 目录到路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from draw_diagrams import DiagramDrawer
from context_manager import ContextManager, identify_project


class OpenGoalEngine:
    """OpenGoal 主引擎"""

    def __init__(self, project_root: str = "."):
        self.project_root = project_root
        self.context_manager = ContextManager(project_root)
        self.diagram_drawer = DiagramDrawer(output_dir=os.path.join(project_root, ".opengoal", "diagrams"))

    def analyze_requirement(self, user_input: str) -> Dict[str, Any]:
        """
        分析用户需求

        Args:
            user_input: 用户输入的自然语言需求

        Returns:
            分析结果字典
        """
        result = {
            "user_input": user_input,
            "is_simple": self._is_simple_requirement(user_input),
            "domain": self._identify_domain(user_input),
            "key_entities": self._extract_entities(user_input),
            "actions": self._extract_actions(user_input),
            "constraints": self._extract_constraints(user_input),
            "technical_stack": self._infer_tech_stack(user_input),
        }

        return result

    def decompose_requirement(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        拆解需求（混合拆解模式：功能+技术+领域+非功能需求+依赖）

        Args:
            analysis: 需求分析结果

        Returns:
            拆解结果
        """
        decomposition = {
            "functional_requirements": self._decompose_functional(analysis),
            "technical_architecture": self._design_architecture(analysis),
            "domain_model": self._design_domain_model(analysis),
            "non_functional_requirements": self._extract_nfr(analysis),
            "dependencies": self._analyze_dependencies(analysis),
        }

        return decomposition

    def detect_anti_patterns(self, decomposition: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        检测反模式和风险

        Args:
            decomposition: 需求拆解结果

        Returns:
            反模式和风险列表
        """
        issues = []

        # 这里是示例逻辑，实际应该基于规则引擎
        # 检查是否有明显的反模式

        return issues

    def generate_supplementary_questions(self, analysis: Dict[str, Any],
                                        decomposition: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        生成补充问题列表

        Args:
            analysis: 需求分析结果
            decomposition: 需求拆解结果

        Returns:
            补充问题列表
        """
        questions = []

        # 隐式需求问题
        if "用户注册" in str(decomposition):
            questions.append({
                "category": "隐式需求",
                "question": "用户注册是否需要邮箱验证？",
                "options": ["需要", "不需要"],
                "default": "需要",
                "reason": "安全性考虑"
            })
            questions.append({
                "category": "隐式需求",
                "question": "是否需要防刷机制（验证码）？",
                "options": ["需要", "不需要"],
                "default": "需要",
                "reason": "防止恶意注册"
            })

        # 技术选型问题
        if not analysis.get("constraints", {}).get("tech_stack"):
            questions.append({
                "category": "技术选型",
                "question": "是否确认使用推断的技术栈？",
                "options": ["确认", "修改"],
                "default": "确认",
                "inferred_stack": analysis.get("technical_stack", {})
            })

        # 非功能需求量化问题
        if "高并发" in str(analysis) or "性能" in str(analysis):
            questions.append({
                "category": "性能需求",
                "question": "预期的并发量是多少？",
                "options": ["< 1000 QPS", "1000-10000 QPS", "> 10000 QPS"],
                "default": "1000-10000 QPS"
            })

        return questions

    def generate_goal_command(self, decomposition: Dict[str, Any],
                             assumptions: List[str] = None,
                             anti_patterns: List[Dict[str, str]] = None) -> Tuple[str, str]:
        """
        生成 /goal 命令（人类版 + AI版）

        Args:
            decomposition: 需求拆解结果
            assumptions: 假设条件列表
            anti_patterns: 反模式列表

        Returns:
            (human_readable_goal, ai_readable_goal)
        """
        # 人类可读版
        human_goal = self._generate_human_goal(decomposition, assumptions, anti_patterns)

        # AI可读版（结构化Markdown）
        ai_goal = self._generate_ai_goal(decomposition, assumptions)

        return human_goal, ai_goal

    def generate_acceptance_criteria(self, decomposition: Dict[str, Any]) -> str:
        """
        生成完整验收标准（功能+性能+安全+代码质量+文档）

        Args:
            decomposition: 需求拆解结果

        Returns:
            验收标准文本
        """
        criteria = """# 验收标准

## 1. 功能完整性
"""
        # 添加功能点检查
        for req in decomposition.get("functional_requirements", []):
            priority = req.get("priority", "P0")
            module = req.get("module", "")
            criteria += f"- [ ] [{priority}] {module} 功能已实现\n"

        criteria += """
## 2. 性能指标
- [ ] 响应时间 < 200ms（90分位）
- [ ] 并发量 > 1000 QPS
- [ ] 数据库查询优化（已添加必要索引）
- [ ] 缓存命中率 > 80%（如适用）

## 3. 安全检查
- [ ] 密码已加密（BCrypt/Argon2）
- [ ] SQL注入防护（参数化查询）
- [ ] XSS防护（输入验证+输出转义）
- [ ] CSRF防护（Token验证）
- [ ] 敏感数据加密传输（HTTPS）
- [ ] 权限验证完整

## 4. 代码质量
- [ ] 单元测试覆盖率 > 80%
- [ ] 集成测试通过
- [ ] 代码符合团队规范（Linter通过）
- [ ] 无明显技术债务
- [ ] 日志完整（关键操作有日志）

## 5. 文档完备
- [ ] API文档完整（Swagger/OpenAPI）
- [ ] 部署文档（环境要求、部署步骤）
- [ ] 数据库迁移脚本
- [ ] README（项目说明、快速开始）
"""

        return criteria

    def draw_diagrams(self, decomposition: Dict[str, Any]) -> List[str]:
        """
        自动生成图表

        Args:
            decomposition: 需求拆解结果

        Returns:
            生成的图片文件路径列表
        """
        diagram_paths = []

        # 依赖关系图
        dependencies = decomposition.get("dependencies", [])
        if dependencies:
            path = self.diagram_drawer.draw_dependency_graph(
                dependencies,
                title="依赖关系图"
            )
            diagram_paths.append(path)

        # 架构图
        architecture = decomposition.get("technical_architecture", {})
        if architecture.get("layers"):
            path = self.diagram_drawer.draw_architecture_diagram(
                architecture["layers"],
                title="系统架构图"
            )
            diagram_paths.append(path)

        # 服务关系图
        if architecture.get("services"):
            path = self.diagram_drawer.draw_service_map(
                architecture["services"],
                architecture.get("interactions", []),
                title="服务关系图"
            )
            diagram_paths.append(path)

        # 领域模型图
        domain_model = decomposition.get("domain_model", {})
        if domain_model.get("aggregates"):
            path = self.diagram_drawer.draw_domain_model(
                domain_model["aggregates"],
                title="领域模型图"
            )
            diagram_paths.append(path)

        return diagram_paths

    # ========== 私有辅助方法 ==========

    def _is_simple_requirement(self, user_input: str) -> bool:
        """判断是否为简单需求"""
        simple_keywords = ["hello world", "测试", "demo", "示例"]
        return any(kw in user_input.lower() for kw in simple_keywords)

    def _identify_domain(self, user_input: str) -> str:
        """识别业务领域"""
        # 简化的领域识别逻辑
        if any(kw in user_input for kw in ["电商", "商品", "订单", "支付", "购物车"]):
            return "电商领域"
        elif any(kw in user_input for kw in ["用户", "注册", "登录", "认证"]):
            return "用户管理领域"
        elif any(kw in user_input for kw in ["病人", "医生", "诊断", "处方"]):
            return "医疗领域"
        else:
            return "通用业务领域"

    def _extract_entities(self, user_input: str) -> List[str]:
        """提取关键实体"""
        # 简化的实体提取逻辑
        common_entities = ["用户", "订单", "商品", "支付", "物流", "库存", "评论"]
        return [entity for entity in common_entities if entity in user_input]

    def _extract_actions(self, user_input: str) -> List[str]:
        """提取动作"""
        common_actions = ["注册", "登录", "创建", "查询", "修改", "删除", "支付", "发货"]
        return [action for action in common_actions if action in user_input]

    def _extract_constraints(self, user_input: str) -> Dict[str, Any]:
        """提取约束条件"""
        constraints = {}
        # 简化的约束提取逻辑
        if "高并发" in user_input:
            constraints["performance"] = "high_concurrency"
        if "安全" in user_input:
            constraints["security"] = "high"
        return constraints

    def _infer_tech_stack(self, user_input: str) -> Dict[str, str]:
        """推断技术栈"""
        # 简化的技术栈推断逻辑
        tech_stack = {
            "backend": "Spring Boot + Java",
            "frontend": "React + TypeScript",
            "database": "PostgreSQL + Redis",
            "message_queue": "Kafka"
        }

        # 根据需求特征调整
        if "快速原型" in user_input or "demo" in user_input.lower():
            tech_stack["backend"] = "Node.js + Express"

        return tech_stack

    def _decompose_functional(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """拆解功能需求"""
        # 这里应该是复杂的需求拆解逻辑
        # 简化示例
        requirements = []

        entities = analysis.get("key_entities", [])
        actions = analysis.get("actions", [])

        for entity in entities:
            for action in actions:
                requirements.append({
                    "priority": "P0" if action in ["注册", "登录", "创建"] else "P1",
                    "module": f"{entity}{action}",
                    "features": [f"{action}{entity}功能"]
                })

        return requirements

    def _design_architecture(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """设计技术架构"""
        tech_stack = analysis.get("technical_stack", {})

        architecture = {
            "layers": [
                {"name": "前端层", "components": [tech_stack.get("frontend", "React")]},
                {"name": "接口层", "components": ["API Gateway", "RESTful API"]},
                {"name": "业务逻辑层", "components": ["UserService", "OrderService"]},
                {"name": "数据访问层", "components": ["Repository"]},
                {"name": "基础设施层", "components": [
                    tech_stack.get("database", "PostgreSQL"),
                    tech_stack.get("message_queue", "Kafka")
                ]},
            ],
            "services": [
                {"name": "UserService", "type": "core"},
                {"name": "OrderService", "type": "core"},
            ],
            "interactions": [
                {"from": "OrderService", "to": "UserService", "type": "sync"},
            ]
        }

        return architecture

    def _design_domain_model(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """设计领域模型"""
        entities = analysis.get("key_entities", [])

        aggregates = []
        for entity in entities[:2]:  # 简化：只取前2个实体
            aggregates.append({
                "name": entity,
                "type": "aggregate_root",
                "entities": [f"{entity}Item"],
                "value_objects": ["Money", "Address"]
            })

        return {"aggregates": aggregates}

    def _extract_nfr(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """提取非功能需求"""
        return {
            "performance": {
                "response_time": "< 200ms",
                "concurrency": "> 1000 QPS"
            },
            "security": {
                "authentication": "JWT Token",
                "password_encryption": "BCrypt"
            },
            "availability": "99.9%"
        }

    def _analyze_dependencies(self, analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """分析依赖关系"""
        # 简化的依赖分析
        entities = analysis.get("key_entities", [])
        dependencies = []

        for i, entity in enumerate(entities):
            if i > 0:
                dependencies.append({
                    "from": f"{entity}Service",
                    "to": f"{entities[i-1]}Service"
                })

        return dependencies

    def _generate_human_goal(self, decomposition: Dict[str, Any],
                            assumptions: List[str],
                            anti_patterns: List[Dict[str, str]]) -> str:
        """生成人类可读的 /goal 命令"""
        goal = f"""# {decomposition.get('project_name', '项目')} - /goal 命令

## 项目概述
{decomposition.get('description', '（需补充）')}

## 功能需求
"""
        for req in decomposition.get("functional_requirements", []):
            goal += f"- [{req['priority']}] {req['module']}\n"

        goal += "\n## 技术架构\n"
        arch = decomposition.get("technical_architecture", {})
        for layer in arch.get("layers", []):
            goal += f"- {layer['name']}: {', '.join(layer['components'])}\n"

        if assumptions:
            goal += "\n## 假设条件\n"
            for assumption in assumptions:
                goal += f"- {assumption}\n"

        if anti_patterns:
            goal += "\n## ⚠️ 风险提示\n"
            for issue in anti_patterns:
                goal += f"- {issue['type']}: {issue['description']}\n"

        return goal

    def _generate_ai_goal(self, decomposition: Dict[str, Any],
                         assumptions: List[str]) -> str:
        """生成AI可读的 /goal 命令（结构化Markdown）"""
        return json.dumps(decomposition, indent=2, ensure_ascii=False)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python main.py '<用户需求>'")
        sys.exit(1)

    user_input = sys.argv[1]

    print("OpenGoal Skill - 需求分析与 /goal 命令生成")
    print("=" * 60)
    print(f"用户输入: {user_input}\n")

    engine = OpenGoalEngine()

    # 1. 分析需求
    print("步骤 1/9: 分析需求...")
    analysis = engine.analyze_requirement(user_input)
    print(f"✓ 识别的领域: {analysis['domain']}")
    print(f"✓ 关键实体: {', '.join(analysis['key_entities'])}")
    print(f"✓ 动作: {', '.join(analysis['actions'])}\n")

    # 2. 拆解需求
    print("步骤 2/9: 拆解需求...")
    decomposition = engine.decompose_requirement(analysis)
    print(f"✓ 功能需求数量: {len(decomposition['functional_requirements'])}")
    print(f"✓ 技术层次: {len(decomposition['technical_architecture']['layers'])}")
    print(f"✓ 依赖关系: {len(decomposition['dependencies'])}\n")

    # 3. 检测反模式
    print("步骤 3/9: 检测反模式...")
    anti_patterns = engine.detect_anti_patterns(decomposition)
    if anti_patterns:
        print(f"⚠️  发现 {len(anti_patterns)} 个反模式")
    else:
        print("✓ 未发现明显反模式\n")

    # 4. 生成补充问题
    print("步骤 4/9: 生成补充问题...")
    questions = engine.generate_supplementary_questions(analysis, decomposition)
    print(f"✓ 生成 {len(questions)} 个补充问题\n")

    # 5. 生成 /goal 命令
    print("步骤 5/9: 生成 /goal 命令...")
    human_goal, ai_goal = engine.generate_goal_command(decomposition)
    print("✓ /goal 命令已生成（人类版 + AI版）\n")

    # 6. 生成验收标准
    print("步骤 6/9: 生成验收标准...")
    acceptance_criteria = engine.generate_acceptance_criteria(decomposition)
    print("✓ 验收标准已生成\n")

    # 7. 绘制图表
    print("步骤 7/9: 绘制图表...")
    diagram_paths = engine.draw_diagrams(decomposition)
    print(f"✓ 生成 {len(diagram_paths)} 个图表\n")

    # 8. 保存上下文
    print("步骤 8/9: 保存上下文...")
    goal_data = {
        "project_name": decomposition.get("project_name", "未命名项目"),
        "goal_human": human_goal,
        "goal_ai": ai_goal,
        "acceptance_criteria": acceptance_criteria,
        "architecture": decomposition.get("technical_architecture"),
        "dependencies": decomposition.get("dependencies"),
        "assumptions": []
    }
    engine.context_manager.save_goal(goal_data)
    print("✓ 上下文已保存\n")

    # 9. 输出完整交付物
    print("步骤 9/9: 输出完整交付物")
    print("=" * 60)
    print("\n## 人类可读版 /goal 命令\n")
    print(human_goal)
    print("\n## 验收标准\n")
    print(acceptance_criteria)
    print("\n## 生成的图表\n")
    for path in diagram_paths:
        print(f"- {path}")

    print("\n✅ 所有步骤完成！")


if __name__ == "__main__":
    main()
