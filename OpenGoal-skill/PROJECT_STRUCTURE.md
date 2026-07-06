# OpenGoal Skill - 项目结构

```
opengoal-skill/
│
├── 📄 skill.md                          # Skill 主文件（功能描述、工作流程）
├── 📘 README.md                         # 使用文档（快速开始指南）
├── 📊 SUMMARY.md                        # 项目完成总结
├── 📦 DELIVERY.md                       # 最终交付清单
│
├── 📂 static/                           # 静态资源（知识库）
│   └── 📂 core/
│       ├── 📄 contract.md               # 核心工作契约
│       │   ├── 工作原则
│       │   ├── 质量标准
│       │   ├── 反模式检测规则
│       │   ├── 拆解粒度标准
│       │   ├── 术语标准化
│       │   ├── 量化标准
│       │   ├── 默认假设清单
│       │   └── 交付物清单
│       │
│       └── 📄 knowledge-base.md         # DDD/SOA 知识库
│           ├── 领域驱动设计（8个概念）
│           │   ├── 领域识别
│           │   ├── 限界上下文
│           │   ├── 实体与值对象
│           │   ├── 聚合根
│           │   ├── 领域事件
│           │   ├── 领域服务
│           │   ├── 仓储模式
│           │   └── 业务规则提取
│           ├── 面向服务架构（7个概念）
│           │   ├── 服务边界
│           │   ├── 服务拆分
│           │   ├── 编排 vs 协作
│           │   ├── API契约
│           │   ├── 依赖管理
│           │   ├── 可观测性
│           │   └── Saga模式
│           └── 架构模式决策树
│
└── 📂 scripts/                          # 功能脚本
    ├── 🚀 main.py                       # 主执行引擎
    │   ├── OpenGoalEngine 类
    │   ├── analyze_requirement()        # 需求分析
    │   ├── decompose_requirement()      # 需求拆解
    │   ├── detect_anti_patterns()       # 反模式检测
    │   ├── generate_supplementary_questions()  # 生成补充问题
    │   ├── generate_goal_command()      # 生成 /goal
    │   ├── generate_acceptance_criteria()      # 生成验收标准
    │   └── draw_diagrams()              # 绘制图表
    │
    ├── 🎨 draw_diagrams.py              # 绘图脚本
    │   ├── DiagramDrawer 类
    │   ├── draw_dependency_graph()      # 依赖关系图
    │   ├── draw_architecture_diagram()  # 架构图
    │   ├── draw_service_map()           # 服务关系图
    │   └── draw_domain_model()          # 领域模型图
    │
    ├── 💾 context_manager.py            # 上下文管理
    │   ├── ContextManager 类
    │   ├── save_goal()                  # 保存 /goal
    │   ├── get_current_goal()           # 获取当前 /goal
    │   ├── get_goal_history()           # 获取历史
    │   ├── update_goal_incremental()    # 增量更新
    │   └── identify_project()           # 项目识别
    │
    ├── 🧪 test_all.py                   # 完整测试套件
    │   ├── test_diagram_drawer()
    │   ├── test_context_manager()
    │   ├── test_opengoal_engine()
    │   └── test_integration()
    │
    └── 🧪 test_simple.py                # 简化测试套件
        ├── test_context_manager()
        ├── test_requirement_analysis()
        ├── test_decomposition()
        ├── test_anti_pattern_detection()
        └── test_goal_generation()
```

---

## 📊 文件统计

| 类型 | 文件数 | 代码/文档行数 | 说明 |
|------|--------|---------------|------|
| 📄 Markdown 文档 | 7 个 | ~3,700 行 | skill.md, README.md, contract.md 等 |
| 🐍 Python 脚本 | 4 个 | ~1,700 行 | main.py, draw_diagrams.py 等 |
| **总计** | **11 个** | **~5,400 行** | **完整的需求分析专家系统** |

---

## 🎯 核心模块关系

```
┌─────────────────────────────────────────────────────────────┐
│                        OpenGoal Skill                        │
│                    (skill.md - 入口)                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
           ┌───────────┴───────────┐
           │                       │
    ┌──────▼──────┐        ┌──────▼──────┐
    │   知识库     │        │  执行引擎   │
    │ (static/)   │        │ (scripts/)  │
    └──────┬──────┘        └──────┬──────┘
           │                       │
    ┌──────▼──────┐        ┌──────▼──────┐
    │ contract.md │        │   main.py   │
    │ knowledge-  │        │ draw_       │
    │   base.md   │        │ diagrams.py │
    └─────────────┘        │ context_    │
                          │ manager.py  │
                          └─────────────┘
```

---

## 🔄 工作流程

```
用户输入
   ↓
[1] 需求分析 (analyze_requirement)
   ├─ 识别领域
   ├─ 提取实体
   ├─ 提取动作
   └─ 提取约束
   ↓
[2] 需求拆解 (decompose_requirement)
   ├─ 功能需求
   ├─ 技术架构
   ├─ 领域模型
   ├─ 非功能需求
   └─ 依赖关系
   ↓
[3] 反模式检测 (detect_anti_patterns)
   ├─ 架构反模式
   ├─ 安全反模式
   └─ 性能反模式
   ↓
[4] 生成补充问题 (generate_supplementary_questions)
   ├─ 隐式需求
   ├─ 技术选型
   └─ 性能量化
   ↓
[5] 用户回答 / 默认假设
   ↓
[6] 生成 /goal (generate_goal_command)
   ├─ 人类可读版 (Markdown)
   └─ AI可读版 (结构化 Markdown)
   ↓
[7] 生成验收标准 (generate_acceptance_criteria)
   ├─ 功能完整性
   ├─ 性能指标
   ├─ 安全检查
   ├─ 代码质量
   └─ 文档完备
   ↓
[8] 绘制图表 (draw_diagrams)
   ├─ 依赖关系图
   ├─ 架构图
   ├─ 服务关系图
   └─ 领域模型图
   ↓
[9] 保存上下文 (save_goal)
   └─ .opengoal/context.json
   ↓
完整交付物输出
```

---

## 💡 使用示例

### 命令行使用
```bash
cd opengoal-skill/scripts
python main.py "我要做一个电商系统，包括用户、商品、订单、支付"
```

### Claude Code 中使用
```
/opengoal 我要做一个用户管理系统，包括注册、登录、资料管理
```

### 输出位置
```
.opengoal/
├── context.json              # 项目上下文
└── diagrams/                 # 生成的图表
    ├── dependency_graph.png
    ├── architecture_diagram.png
    ├── service_map.png
    └── domain_model.png
```

---

## 🎓 知识库内容

### DDD 知识库 (knowledge-base.md)
- 8 个核心概念，每个都有：
  - 定义
  - 识别方法
  - 示例代码
  - 应用场景

### SOA 知识库 (knowledge-base.md)
- 7 个核心概念，每个都有：
  - 定义
  - 适用场景
  - 优缺点
  - 实战案例

### 架构决策树
- 何时同步 vs 异步
- 何时编排 vs 协作
- 何时单体 vs 微服务

---

## ✅ 质量保证

- ✅ 代码注释完整（每个函数都有 docstring）
- ✅ 文档结构清晰（4 个层次：用户、技术、知识、代码）
- ✅ 测试套件完备（完整测试 + 简化测试）
- ✅ 错误处理健全（try-except + 错误提示）
- ✅ 扩展性良好（模块化设计）

---

## 🚀 开始使用

1. **查看文档** → `README.md`
2. **了解设计** → `SUMMARY.md`
3. **学习知识** → `static/core/knowledge-base.md`
4. **运行测试** → `python scripts/test_simple.py`
5. **开始分析** → `/opengoal <你的需求>`

---

**OpenGoal Skill - 从需求到实现的智能桥梁 🌉**
