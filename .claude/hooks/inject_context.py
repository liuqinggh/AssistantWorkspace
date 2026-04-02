#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Personal Second Brain v3.3 - 注入最近记忆上下文（loguru 版）
仅限本项目使用
"""

import os
from datetime import datetime, timedelta
from loguru import logger

# 配置 loguru 日志（与主脚本保持一致）
VAULT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(VAULT_PATH, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logger.add(
    os.path.join(LOG_DIR, "second_brain_{time:YYYY-MM-DD}.log"),
    rotation="00:00",
    retention="30 days",
    level="INFO",
    encoding="utf-8",
    backtrace=True,
    diagnose=True
)

MEMORY_DIR = os.path.join(VAULT_PATH, "memory")

def get_recent_memory(days: int = 2) -> str:
    """获取最近 N 天的 memory 日志，用于注入上下文"""
    today = datetime.now()
    context = ""
    injected_count = 0
    
    for i in range(days):
        date_str = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        file_path = os.path.join(MEMORY_DIR, f"{date_str}.md")
        
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    context += f"\n---\n# 来自 {date_str} 的记忆\n{content[:800]}\n"
                injected_count += 1
                logger.info(f"成功读取 {date_str}.md 并注入上下文（长度 {len(content)}）")
            except Exception as e:
                logger.error(f"读取 {date_str}.md 失败: {e}")
    
    if injected_count == 0:
        logger.warning("未找到最近记忆文件，无法注入上下文")
    
    logger.info(f"共注入 {injected_count} 天记忆上下文，总长度 {len(context)} 字符")
    return context

def main():
    try:
        logger.info("开始执行 inject_context Hook")
        
        recent_context = get_recent_memory(days=2)
        
        if recent_context:
            # 输出到 stdout，供 Claude Code 使用（不影响对话界面）
            print(recent_context)
            logger.success("记忆上下文已成功注入到当前会话")
        else:
            logger.info("无可用记忆上下文，跳过注入")
            
    except Exception as e:
        logger.exception(f"inject_context Hook 执行异常: {e}")

if __name__ == "__main__":
    main()