#!/bin/bash
# AssistantWorkspace 启动脚本
# 一键启动个人助手系统

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PROJECT_DIR="/Users/cd-la-067/project/Igloo-ai/personal-assistant"
WORKSPACE_DIR="/Users/cd-la-067/project/Igloo-ai/AssistantWorkspace"

echo -e "${GREEN}╔══════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  启动个人助手系统                    ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════╝${NC}"

# 1. 启动 STT 服务
echo -e "\n${YELLOW}[1/2] 启动 STT 服务...${NC}"
if [ -f "$PROJECT_DIR/start-stt-services.sh" ]; then
    "$PROJECT_DIR/start-stt-services.sh"
else
    echo -e "${YELLOW}⚠ STT 启动脚本不存在，跳过${NC}"
fi

# 2. 启动 cc-connect（会自动启动 Claude Code）
echo -e "\n${YELLOW}[2/2] 启动 cc-connect...${NC}"
if [ -f "$PROJECT_DIR/config/user/config.toml" ]; then
    echo -e "${GREEN}配置文件: $PROJECT_DIR/config/user/config.toml${NC}"
    echo -e "${GREEN}工作区: $WORKSPACE_DIR${NC}"
    echo -e "\n${YELLOW}执行命令:${NC}"
    echo -e "cc-connect --config $PROJECT_DIR/config/user/config.toml"
    echo -e "\n${YELLOW}提示: 按 Ctrl+C 停止服务${NC}\n"

    cd "$WORKSPACE_DIR"
    cc-connect --config "$PROJECT_DIR/config/user/config.toml"
else
    echo -e "${YELLOW}⚠ cc-connect 配置文件不存在${NC}"
    echo -e "${YELLOW}请先创建配置文件: $PROJECT_DIR/config/user/config.toml${NC}"
    exit 1
fi
