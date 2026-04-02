#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Personal Second Brain v3.3 - 项目本地 Hook 脚本（含智能 promote）
仅限本 Second Brain 项目使用
"""

import sys
import json
import os
from datetime import datetime
import re

# 自动获取 Vault 根目录（项目本地）
VAULT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(VAULT_PATH, "raw")
MEMORY_DIR = os.path.join(VAULT_PATH, "memory")
KNOWLEDGE_BASE = os.path.join(VAULT_PATH, "knowledge_base.md")
TASKS_FILE = os.path.join(VAULT_PATH, "tasks.json")
DAILY_PLAN = os.path.join(VAULT_PATH, "daily_plan.md")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(MEMORY_DIR, exist_ok=True)

def get_today():
    return datetime.now().strftime("%Y-%m-%d")

def append_to_raw(user_msg, assistant_msg):
    today = get_today()
    raw_file = os.path.join(RAW_DIR, f"{today}_raw.md")
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(raw_file, "a", encoding="utf-8") as f:
        f.write(f"\n## {timestamp} 用户输入\n{user_msg}\n")
        f.write(f"\n## {timestamp} 助手回复\n{assistant_msg}\n")

def generate_daily_summary(user_msg, assistant_msg):
    today = get_today()
    memory_file = os.path.join(MEMORY_DIR, f"{today}.md")
    summary = f"""
# {today} Daily Log

## 对话总结
- 一句话：{user_msg[:150]}...

## 决策 & 洞见
{assistant_msg[:300]}...

## 任务状态
- 新增/更新：（智能提取中）

## 待 promote 内容
（知识 / 任务 / 计划）
"""
    with open(memory_file, "a", encoding="utf-8") as f:
        f.write(summary)

def intelligent_promote(user_msg, assistant_msg):
    today = get_today()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 1. Promote 到 knowledge_base.md（长期知识）
    knowledge_section = f"\n\n### {timestamp} 新增知识\n"
    # 简单规则提取（可后续用正则或 Claude 增强）
    if len(assistant_msg) > 50:
        knowledge_section += f"- {assistant_msg[:250].replace('\n', ' ')}...\n"
    with open(KNOWLEDGE_BASE, "a", encoding="utf-8") as f:
        f.write(knowledge_section)

    # 2. Promote 到 tasks.json（任务管理）
    tasks = []
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            try:
                tasks = json.load(f)
            except:
                tasks = []
    
    # 简单任务提取示例（实际可根据关键词增强）
    if "任务" in assistant_msg or "todo" in assistant_msg.lower() or "记得" in assistant_msg:
        new_task = {
            "id": len(tasks) + 1,
            "title": assistant_msg[:80] + "...",
            "status": "pending",
            "date": today,
            "source": "auto_promote"
        }
        tasks.append(new_task)
    
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

    # 3. Promote 到 daily_plan.md（计划）
    plan_entry = f"\n\n### {timestamp} 自动计划建议\n"
    plan_entry += f"- 来自本次对话：{assistant_msg[:200].replace('\n', ' ')}...\n"
    with open(DAILY_PLAN, "a", encoding="utf-8") as f:
        f.write(plan_entry)

# 主入口
def main():
    try:
        # 当前为简化版：实际运行中，建议让 CLAUDE.md 提示 Claude 在回复末尾输出结构化 JSON（如 {"knowledge": [...], "tasks": [...], "plans": [...] }）
        # 这里用简单文本规则演示 promote
        user_msg = sys.argv[1] if len(sys.argv) > 1 else "用户最新输入"
        assistant_msg = sys.argv[2] if len(sys.argv) > 2 else "助手最新回复"

        append_to_raw(user_msg, assistant_msg)
        generate_daily_summary(user_msg, assistant_msg)
        intelligent_promote(user_msg, assistant_msg)

        print("✅ Second Brain 项目本地智能 promote 完成（后台）")
    except Exception as e:
        print(f"Hook 执行异常: {e}")

if __name__ == "__main__":
    main()