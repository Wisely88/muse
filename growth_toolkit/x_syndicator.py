#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X (Twitter) Syndication Tool · 跨平台引流转发工具
自动从小红书发帖队列中提取内容，校验 Twitter 字符长度（<280 字符），生成高质量 X 线程。
"""

import json
import os
import sys

def load_queue():
    queue_path = os.path.join(os.path.dirname(__file__), "queue", "ready_to_post.json")
    if not os.path.exists(queue_path):
        print(f"❌ 未找到发帖队列文件，请先运行 content_generator.py")
        sys.exit(1)
    with open(queue_path, "r", encoding="utf-8") as f:
        return json.load(f)

def preview_x_threads():
    data = load_queue()
    print("=" * 65)
    print(f"🐦 X (Twitter) 引流线程预览库 (共 {data['campaign_count']} 组专题)")
    print("=" * 65)
    
    for idx, c in enumerate(data['campaigns'], 1):
        print(f"\n📌 专题 {idx}: {c['topic']} ({c['id']})")
        print("-" * 50)
        for tweet in c['x_thread']:
            text = tweet['text']
            char_count = len(text)
            status = "✅ 合规 (<280)" if char_count <= 280 else f"⚠️ 超长 ({char_count}/280)"
            print(f"[Tweet {tweet['tweet_num']}] {status}")
            print(text)
            print("." * 40)

def export_x_batch():
    data = load_queue()
    export_file = os.path.join(os.path.dirname(__file__), "queue", "x_threads_export.json")
    threads_only = [
        {
            "campaign_id": c["id"],
            "topic": c["topic"],
            "tweets": [t["text"] for t in c["x_thread"]]
        }
        for c in data["campaigns"]
    ]
    with open(export_file, "w", encoding="utf-8") as f:
        json.dump(threads_only, f, ensure_ascii=False, indent=2)
    print(f"✅ 已导出 X 独立发布包: {export_file}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--export":
        export_x_batch()
    else:
        preview_x_threads()
        export_x_batch()
