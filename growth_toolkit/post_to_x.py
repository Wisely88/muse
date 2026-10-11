#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X (Twitter) 一键极速发帖助手 (One-Click X Poster)
将校验合规的英文推文串自动编码为 Twitter Web Intent 并在默认浏览器中拉起，实现一键无缝发布！
"""

import json
import os
import sys
import urllib.parse
import webbrowser

def load_x_threads():
    queue_path = os.path.join(os.path.dirname(__file__), "queue", "x_threads_export.json")
    if not os.path.exists(queue_path):
        print("❌ 未找到推特发布队列，正在重新生成...")
        os.system(f"python3 {os.path.join(os.path.dirname(__file__), 'content_generator.py')}")
    with open(queue_path, "r", encoding="utf-8") as f:
        return json.load(f)

def open_tweet_in_browser(text):
    encoded_text = urllib.parse.quote(text)
    intent_url = f"https://twitter.com/intent/tweet?text={encoded_text}"
    print(f"🚀 正在默认浏览器中打开 X (Twitter) 发帖窗口...")
    try:
        import platform, subprocess
        if platform.system() == "Darwin":
            subprocess.run(["open", intent_url], check=False)
        else:
            webbrowser.open(intent_url)
    except Exception as e:
        webbrowser.open(intent_url)
    return intent_url

def dispatch_campaign(campaign_idx=0):
    threads = load_x_threads()
    if campaign_idx >= len(threads):
        print(f"❌ 索引超出范围，共有 {len(threads)} 组专题 (0-{len(threads)-1})")
        return
    
    target = threads[campaign_idx]
    print("=" * 60)
    print(f"🎬 准备向 X (Twitter) 推送专题: {target['topic']}")
    print(f"📌 Campaign ID: {target['campaign_id']}")
    print("=" * 60)

    for i, tweet in enumerate(target["tweets"], 1):
        print(f"\n--- [Tweet {i}/{len(target['tweets'])}] ---")
        print(tweet)
        intent_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(tweet)}"
        print(f"👉 发帖直达链接: {intent_url}")

    # 默认自动在浏览器拉起第 1 条主推文 (Hook Tweet)
    first_tweet = target["tweets"][0]
    open_tweet_in_browser(first_tweet)
    print("\n✨ 主推文 (Tweet 1) 已在浏览器打开！发布后直接在推特回复自己发布 Tweet 2 与 3 即可完成 Thread！")

if __name__ == "__main__":
    idx = 0
    if len(sys.argv) > 1:
        try:
            idx = int(sys.argv[1]) - 1
        except ValueError:
            idx = 0
    dispatch_campaign(idx)
