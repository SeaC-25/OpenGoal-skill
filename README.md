# OpenGoal Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/SeaC-25/opengoal-skill?style=social)

> **将自然语言需求转化为结构化的、可执行的 /goal 命令**

一个基于 DDD（领域驱动设计）和 SOA（面向服务架构）的需求分析专家系统，通过 **100 个问答驱动设计** 而构建。

---

## 🎯 核心功能

✅ **智能需求分析** - 语义分析、实体识别、模糊需求澄清  
✅ **DDD/SOA 专家** - 8个DDD概念 + 7个SOA概念  
✅ **混合拆解模式** - 功能+技术+领域+非功能需求+依赖  
✅ **质量保证** - 反模式识别、完整验收标准（5个维度）  
✅ **自动绘图** - 依赖图、架构图、服务图、领域模型图  
✅ **双版本输出** - 人类可读版 + AI可读版  
✅ **上下文记忆** - 项目历史、增量更新  

---

## 🚀 快速开始

### 在 Claude Code 中使用

```bash
/opengoal 我要做一个电商系统，包括用户管理、商品管理、订单、支付、物流
```

### 命令行使用

```bash
cd opengoal-skill/scripts
python main.py "我要做一个用户管理系统，包括注册、登录、资料管理"
```

### 安装依赖（绘图功能，可选）

```bash
pip install matplotlib networkx
```

---

## 📦 输出示例

### /goal 命令（人类可读版）

```markdown
# 电商系统 - /goal 命令

## 功能需求
- [P0] 用户管理：注册、登录、资料管理
- [P0] 商品管理：商品信息、分类、搜索
- [P0] 订单管理：创建订单、订单查询、状态管理
- [P0] 支付处理：支付集成、退款
- [P1] 物流跟踪：发货、物流查询

## 技术架构
- 前端：React + TypeScript
- 后端：Spring Boot + Java
- 数据库：PostgreSQL + Redis
- 消息队列：Kafka

## 分步执行计划
Phase 1: 基础设施搭建
Phase 2: 用户模块实现
Phase 3: 商品模块实现
...
```

### 验收标准

包含 5 个维度的完整检查清单：
- ✅ 功能完整性
- ✅ 性能指标
- ✅ 安全检查
- ✅ 代码质量
- ✅ 文档完备

### 自动生成的图表

- `dependency_graph.png` - 依赖关系图（检测循环依赖）
- `architecture_diagram.png` - 系统架构图
- `service_map.png` - 微服务关系图
- `domain_model.png` - 领域模型图

---

## 💡 为什么需要这个 Skill？

### 问题：AI 在复杂项目中"越用越笨"

我们分析了 7 个根本原因：

1. **上下文窗口污染** → OpenGoal 用结构化输出解决
2. **目标漂移** → OpenGoal 用完整拆解和验收标准解决
3. **抽象层级混乱** → OpenGoal 用混合拆解模式解决
4. **依赖关系图缺失** → OpenGoal 自动生成依赖图
5. **上下文一致性丢失** → OpenGoal 提供项目记忆
6. **缺乏状态检查点** → OpenGoal 生成验收标准
7. **提示词熵增** → OpenGoal 规范化需求

详见：[为什么需要 OpenGoal？](./BUILD_YOUR_OWN.md#-为什么需要这个-skill)

---

## 🏗️ 构建你自己的 Goal Skill

**OpenGoal 的独特之处**：它不是凭空想象出来的，而是通过 **100 个问答驱动设计** 构建的。

你也可以使用同样的方法，构建属于你自己领域的 Goal Skill！

### 构建方法

1. **明确目标** - 你的 Skill 要解决什么问题？
2. **深度提问** - 设计 100+ 个问题，分 10 个维度
3. **整理答案** - 将答案转化为设计决策
4. **实现功能** - 基于设计决策实现核心模块
5. **测试优化** - 用真实案例测试并优化

### 详细指南

👉 **[如何构建你自己的 Goal Skill](./BUILD_YOUR_OWN.md)** 👈

**完整的 100 个问答记录**：[answer.md](./answer.md)

---

## 📚 文档

- **[README.md](./README.md)** - 使用指南和功能介绍
- **[BUILD_YOUR_OWN.md](./BUILD_YOUR_OWN.md)** - 构建方法（**推荐阅读**）
- **[answer.md](./answer.md)** - 完整的 100 个问答记录
- **[PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)** - 项目结构可视化
- **[static/core/contract.md](./static/core/contract.md)** - 核心工作契约
- **[static/core/knowledge-base.md](./static/core/knowledge-base.md)** - DDD/SOA 完整知识库

---

## 📁 项目结构

```
opengoal-skill/
├── skill.md                          # Skill 主文件
├── README.md                         # 本文档
├── BUILD_YOUR_OWN.md                 # 构建方法指南
├── answer.md                         # 100 个问答记录
├── static/core/
│   ├── contract.md                   # 核心工作契约
│   └── knowledge-base.md             # DDD/SOA 知识库
└── scripts/
    ├── main.py                       # 主执行引擎
    ├── draw_diagrams.py              # 绘图脚本
    ├── context_manager.py            # 上下文管理
    └── test_simple.py                # 测试套件
```

---

## 🎨 特色功能

### 1. 基于 DDD/SOA 的需求分析

- **领域驱动设计（DDD）**：8个核心概念（领域、限界上下文、聚合根、领域事件等）
- **面向服务架构（SOA）**：7个核心概念（服务边界、编排 vs 协作、Saga模式等）
- **架构决策树**：何时同步 vs 异步、何时编排 vs 协作

### 2. 混合拆解模式

不是简单的功能拆解，而是五维拆解：

- 功能需求（按优先级 P0/P1/P2）
- 技术架构（5层架构）
- 领域模型（聚合、实体、值对象）
- 非功能需求（性能、安全、可用性）
- 依赖关系（自动检测循环依赖）

### 3. 自动绘图

基于 matplotlib + networkx，继承 nature-figure 风格：

- **依赖关系图**：检测循环依赖并标红
- **架构图**：5层架构可视化
- **服务关系图**：区分同步/异步交互
- **领域模型图**：聚合、实体、值对象可视化

### 4. 完整的验收标准

5个维度，每个维度都有具体检查清单：

1. 功能完整性
2. 性能指标（响应时间、并发量等）
3. 安全检查（密码加密、SQL注入防护等）
4. 代码质量（测试覆盖率、代码规范等）
5. 文档完备（API文档、部署文档等）

---

## 🎓 学习价值

这个 Skill 不仅是工具，更是**软件工程最佳实践的教学案例**：

- **需求工程**：如何从自然语言到结构化需求
- **领域驱动设计**：DDD 的 8 个核心概念实战
- **面向服务架构**：SOA 的 7 个核心概念实战
- **质量工程**：如何定义完整的验收标准
- **架构设计**：从需求到架构的系统化思考

---

## 🌟 示例场景

### 场景 1：电商系统

**输入**：
```
/opengoal 我要做一个电商系统，包括用户管理、商品管理、订单、支付、物流
```

**输出**：
- 识别为"电商领域"
- 拆解为 5 个核心服务
- 生成完整的微服务架构
- 生成服务依赖图
- 生成验收标准

### 场景 2：用户管理系统

**输入**：
```
/opengoal 实现用户注册、登录、资料管理功能
```

**输出**：
- 识别为"用户管理领域"
- 设计 User 聚合
- 生成完整事件链（UserRegistrationStarted → UserRegistered）
- 建议技术栈（Spring Boot + JWT）
- 生成分步执行计划

---

## 🤝 贡献

欢迎贡献！

### 如何贡献

1. **Fork 这个项目**
2. **创建你的功能分支** (`git checkout -b feature/AmazingFeature`)
3. **提交你的改动** (`git commit -m 'Add some AmazingFeature'`)
4. **推送到分支** (`git push origin feature/AmazingFeature`)
5. **打开一个 Pull Request**

### 贡献方向

- 增加新的反模式检测规则
- 增加新的 DDD/SOA 知识
- 增加新的图表类型
- 优化需求分析逻辑
- 改进文档

---

## 📊 统计

- **代码行数**：~5,400 行（代码 + 文档）
- **文档数量**：11 个
- **功能模块**：7 个
- **问答数量**：100 个
- **知识概念**：15 个（8个DDD + 7个SOA）
- **图表类型**：4 种

---

## 💬 讨论与交流

- **Issues**：报告 Bug 或提出功能建议
- **Discussions**：讨论构建方法、分享你的 Goal Skill
- **Pull Requests**：贡献代码或文档

---

## 📄 许可证

本项目基于 [MIT License](./LICENSE) 开源。

---

## 🙏 致谢

- **绘图风格**：继承自 [nature-skills](https://github.com/nature-of-code/nature-skills)
- **DDD 理论**：Eric Evans 的《领域驱动设计》
- **SOA 理论**：Martin Fowler 的微服务架构理论
- **构建方法**：问答驱动设计

---

## 🔗 相关资源

- [DDD 参考资料](./static/core/knowledge-base.md#一领域驱动设计ddd)
- [SOA 参考资料](./static/core/knowledge-base.md#二面向服务架构soa)
- [架构决策树](./static/core/knowledge-base.md#三架构模式决策树)

---

<div align="center">

**用问答驱动设计，构建属于你的 Goal Skill！🚀**

[开始使用](./README.md) • [构建方法](./BUILD_YOUR_OWN.md) • [100 个问答](./answer.md)

</div>
