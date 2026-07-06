#!/bin/bash
# GitHub 上传脚本

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  OpenGoal Skill - GitHub 上传脚本${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# 检查是否已经是 git 仓库
if [ -d ".git" ]; then
    echo -e "${GREEN}✓ 已存在 Git 仓库${NC}"
else
    echo -e "${BLUE}初始化 Git 仓库...${NC}"
    git init
    echo -e "${GREEN}✓ Git 仓库初始化完成${NC}"
fi

# 添加所有文件
echo ""
echo -e "${BLUE}添加文件到 Git...${NC}"
git add .
echo -e "${GREEN}✓ 文件添加完成${NC}"

# 提交
echo ""
echo -e "${BLUE}创建提交...${NC}"
git commit -m "Initial commit: OpenGoal Skill - 基于 100 个问答驱动设计的需求分析专家系统

- 完整的 DDD/SOA 知识库
- 混合拆解模式（功能+技术+领域+非功能需求+依赖）
- 自动绘图功能（依赖图、架构图、服务图、领域模型图）
- 双版本输出（人类版+AI版）
- 完整的验收标准（5个维度）
- 项目上下文记忆和增量更新
- 100 个问答记录
- 构建方法文档

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"

echo -e "${GREEN}✓ 提交创建完成${NC}"

# 提示用户添加远程仓库
echo ""
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  下一步操作${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""
echo -e "${GREEN}1. 在 GitHub 上创建一个新仓库（名称建议：opengoal-skill）${NC}"
echo ""
echo -e "${GREEN}2. 添加远程仓库：${NC}"
echo "   git remote add origin https://github.com/你的用户名/opengoal-skill.git"
echo ""
echo -e "${GREEN}3. 推送到 GitHub：${NC}"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo -e "${BLUE}================================================${NC}"
echo ""
echo -e "${GREEN}提示：记得将 README_GITHUB.md 重命名为 README.md${NC}"
echo "   mv README.md README_LOCAL.md"
echo "   mv README_GITHUB.md README.md"
echo "   git add README.md README_LOCAL.md"
echo "   git commit -m 'Update README for GitHub'"
echo "   git push"
echo ""
