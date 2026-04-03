每次收到 Telegram 消息时（尤其是带 <voice>、<image>、<attachment> 或 <url> 标记的）：
1. 如果是语音：使用转录文本作为主要内容，记录原始语音时长/来源。
2. 如果是图片：分析图像内容（白板、截图、照片），提取关键信息、文字（OCR 如果需要）。
3. 如果是链接：总结页面核心观点，提取标题、作者、关键引用。
4. 整体处理：
   - 提取原子想法、洞见、待办、资源。
   - 自动分类：
     - 快速闪念/日记 → 存入 500 Daily/YYYY-MM-DD.md（追加带时间戳）。
     - 知识/资源/文章总结 → 存入 300 Resources/（文件名如 `2026-04-03-[主题].md`，添加 frontmatter：tags, source, date）。
   - 创建/更新相关 MOC（Maps of Content）或反向链接到 Vision/Goals/Projects。
   - 使用 [[Wikilinks]] 连接到现有笔记。
5. 处理后，回复 Telegram：“已摄入并整理到 [文件路径]，摘要：xxx。需要调整吗？”
6. 所有变更后自动 Git commit（message: "Telegram ingest: [简短描述]"）。
