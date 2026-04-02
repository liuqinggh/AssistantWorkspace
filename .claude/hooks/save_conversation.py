#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Personal Second Brain v3.3 - 保存用户与 Agent 对话到本地（loguru 版）
功能：完整记录对话 → 生成每日总结 → 智能 promote → 使用 loguru 记录所有操作
仅限本项目使用
"""

import sys
import json
import os
from datetime import datetime
from loguru import logger

# 配置 loguru 日志（项目本地日志）
VAULT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(VAULT_PATH, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logger.add(
    os.path.join(LOG_DIR, "second_brain_{time:YYYY-MM-DD}.log"),
    rotation="00:00",          # 每天零点新文件
    retention="30 days",       # 保留30天
    level="INFO",
    encoding="utf-8",
    backtrace=True,
    diagnose=True
)

# 项目路径
RAW_DIR = os.path.join(VAULT_PATH, "raw")
MEMORY_DIR = os.path.join(VAULT_PATH, "memory")
KNOWLEDGE_BASE = os.path.join(VAULT_PATH, "knowledge_base.md")
TASKS_FILE = os.path.join(VAULT_PATH, "tasks.json")
DAILY_PLAN = os.path.join(VAULT_PATH, "daily_plan.md")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(MEMORY_DIR, exist_ok=True)

def get_today():
    return datetime.now().strftime("%Y-%m-%d")

def save_conversation_to_raw(user_msg: str, assistant_msg: str):
    today = get_today()
    raw_file = os.path.join(RAW_DIR, f"{today}_raw.md")
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    try:
        with open(raw_file, "a", encoding="utf-8") as f:
            f.write(f"\n## {timestamp} 用户输入\n{user_msg.strip()}\n")
            f.write(f"\n## {timestamp} 助手回复\n{assistant_msg.strip()}\n")
            f.write("\n---\n")
        logger.info(f"对话记录已追加到 raw/{today}_raw.md")
    except Exception as e:
        logger.error(f"保存 raw 文件失败: {e}")

def generate_daily_summary(user_msg: str, assistant_msg: str):
    today = get_today()
    memory_file = os.path.join(MEMORY_DIR, f"{today}.md")
    summary = f"""
# {today} Daily Log

## 对话总结
- 一句话：{user_msg[:150].strip()}...

## 决策 & 洞见
{assistant_msg[:350].strip()}...

## 任务状态
- 新增/更新：（智能提取中）

## 待 promote 内容
（知识 / 任务 / 计划）
"""
    try:
        with open(memory_file, "a", encoding="utf-8") as f:
            f.write(summary + "\n")
        logger.info(f"每日总结已追加到 memory/{today}.md")
    except Exception as e:
        logger.error(f"生成 daily summary 失败: {e}")

def intelligent_promote(user_msg: str, assistant_msg: str):
    today = get_today()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    try:
        # 1. 知识库
        with open(KNOWLEDGE_BASE, "a", encoding="utf-8") as f:
            f.write(f"\n\n### {timestamp} 新增知识\n")
            f.write(f"- {assistant_msg[:280].replace('\n', ' ').strip()}...\n")
        logger.info("知识已 promote 到 knowledge_base.md")

        # 2. 任务
        tasks = []
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                try:
                    tasks = json.load(f)
                except:
                    tasks = []
        
        if any(kw in (user_msg + assistant_msg).lower() for kw in ["任务", "todo", "记得", "要做", "计划", "提醒"]):
            new_task = {
                "id": len(tasks) + 1,
                "title": (user_msg + assistant_msg)[:100].strip() + "...",
                "status": "pending",
                "date": today,
                "source": "auto_promote"
            }
            tasks.append(new_task)
        
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        logger.info(f"任务已更新到 tasks.json（当前共 {len(tasks)} 条）")

        # 3. 计划
        with open(DAILY_PLAN, "a", encoding="utf-8") as f:
            f.write(f"\n\n### {timestamp} 自动计划建议\n")
            f.write(f"- 来自本次对话：{(assistant_msg[:220].replace('\n', ' ').strip())}...\n")
        logger.info("计划已 promote 到 daily_plan.md")

    except Exception as e:
        logger.error(f"智能 promote 失败: {e}")

def main():
    try:
        user_msg = sys.argv[1] if len(sys.argv) > 1 else "用户输入内容"
        assistant_msg = sys.argv[2] if len(sys.argv) > 2 else "助手回复内容"

        logger.info(f"开始处理新对话 | 用户消息长度: {len(user_msg)} | 助手消息长度: {len(assistant_msg)}")

        save_conversation_to_raw(user_msg, assistant_msg)
        generate_daily_summary(user_msg, assistant_msg)
        intelligent_promote(user_msg, assistant_msg)

        logger.success("✅ Second Brain 项目本地对话记录与智能 promote 已完成")
    except Exception as e:
        logger.exception(f"Hook 主流程执行异常: {e}")

if __name__ == "__main__":
    main()