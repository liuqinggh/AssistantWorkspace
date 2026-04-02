#!/usr/bin/env python3
import os
from datetime import datetime, timedelta

VAULT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_DIR = os.path.join(VAULT_PATH, "memory")

def get_recent_memory(days=2):
    today = datetime.now()
    context = ""
    for i in range(days):
        date_str = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        file_path = os.path.join(MEMORY_DIR, f"{date_str}.md")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                context += f.read()[:800] + "\n"
    return context

if __name__ == "__main__":
    recent = get_recent_memory()
    if recent:
        print(f"已注入最近记忆上下文")