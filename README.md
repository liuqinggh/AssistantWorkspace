# AssistantWorkspace

这是你的个人 AI 助手工作区，包含所有个人数据、知识库和配置。

## 📂 目录结构

```
AssistantWorkspace/
├── .claude/
│   └── CLAUDE.md          # Claude 全局提示词（第二大脑）
├── knowledge_base.md      # 知识库（结构化存储）
├── tasks.json             # 任务和提醒
├── daily_plan.md          # 每日/每周计划
├── raw/                   # 原始记录（永久保留）
│   └── YYYY-MM-DD_raw.md
├── archive/               # 历史归档
├── logs/                  # 所有日志
│   ├── stt_api.log       # STT API 日志
│   ├── stt_proxy.log     # STT 代理日志
│   └── assistant.log     # 助手处理日志
├── start.sh              # 一键启动脚本
└── README.md             # 本文件
```

## 🚀 快速开始

### 启动助手系统

```bash
# 方式 1：使用工作区启动脚本
./start.sh

# 方式 2：手动启动
# 1. 启动 STT 服务
~/project/Igloo-ai/personal-assistant/start-stt-services.sh

# 2. 启动 cc-connect（会自动启动 Claude Code）
cc-connect --config ~/project/Igloo-ai/personal-assistant/config/user/config.toml
```

### 停止助手系统

```bash
~/project/Igloo-ai/personal-assistant/stop-stt-services.sh
pkill -f cc-connect
```

## 📝 使用说明

### 通过 IM 交互

1. 打开 Telegram（或你配置的 IM）
2. 找到你的 Bot
3. 发送消息（文字/语音/图片）
4. Claude 会自动：
   - 保存原始记录到 raw/
   - 更新知识库
   - 管理任务和计划
   - 检测冲突
   - 智能回复

### 直接使用 Claude Code

```bash
cd ~/AssistantWorkspace
claude-code
```

## 🔧 配置

### cc-connect 配置

配置文件位于：`~/project/Igloo-ai/personal-assistant/config/user/config.toml`

关键配置：
```toml
[[projects]]
path = "/Users/cd-la-067/project/Igloo-ai/AssistantWorkspace"  # 指向本工作区
```

### Claude 提示词

编辑 `.claude/CLAUDE.md` 可以自定义 Claude 的行为。

## 📊 数据管理

### 备份

建议定期备份整个工作区：

```bash
# 备份到 iCloud
cp -R ~/AssistantWorkspace ~/Library/Mobile\ Documents/com~apple~CloudDocs/

# 或备份到外部存储
cp -R ~/AssistantWorkspace /Volumes/Backup/

# 或使用 Git（推荐）
cd ~/AssistantWorkspace
git init
git add .
git commit -m "Backup $(date +%Y-%m-%d)"
```

### 清理

每月自动归档 raw 文件：
```bash
# raw/ 中超过 30 天的文件自动移到 archive/
```

## 📚 相关文档

- 项目文档：`~/project/Igloo-ai/personal-assistant/docs/`
- 快速开始：`~/project/Igloo-ai/personal-assistant/docs/快速开始.md`
- 配置指南：`~/project/Igloo-ai/personal-assistant/docs/配置指南/`

## ⚠️ 注意事项

- ✅ 本工作区包含个人隐私数据，请妥善保管
- ✅ 定期备份，防止数据丢失
- ✅ 不要将本工作区上传到公开仓库
- ✅ raw/ 文件夹只追加，不删除

## 🆘 故障排查

### Claude 无法读取文件

检查工作目录：
```bash
# 确保 cc-connect 配置正确
grep "path" ~/project/Igloo-ai/personal-assistant/config/user/config.toml
```

### STT 服务无法启动

查看日志：
```bash
tail -f logs/stt_api.log
tail -f logs/stt_proxy.log
```

### 更多帮助

查看项目文档或提交 Issue：
https://github.com/your-repo/personal-assistant
