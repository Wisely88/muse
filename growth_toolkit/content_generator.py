#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Muse Growth Engine · 社媒引流内容生成与协同小工具
供多 Agent 协同：为负责运维小红书的 muse 提供标准化发帖物料，并生成对应的 X (Twitter) 英文/双语 Thread。
"""

import json
import os
import sys
from datetime import datetime

CAMPAIGNS = [
    {
        "id": "campaign_01_painpoint_avoidance",
        "topic": "避坑痛点 · 提升出片率",
        "target_audience": "经常生成僵硬、塑料感、被风控视频的小白创作者",
        "xhs": {
            "title": "别再乱写Prompt了！90%人AI视频翻车的4个致命误区🔥",
            "subtitle": "好莱坞导演级视频提示词黄金架构拆解",
            "video_script": """【0-5s 黄金前黄金秒 · 痛点抓取】
（画面：左边放一个动作抽搐变形的AI失败视频，打上巨大红叉❌；右边放电影级丝滑雨后晚霞推轨镜头，打上绿色勾勾✅）
口播：“你生成的AI视频是不是总像PPT幻灯片，人物僵硬、运镜抽搐？别怪Sora和可灵模型不行，是你提示词从第一句就写错了！”

【5-18s 核心误区拆解 · 权威感】
（画面：分屏展示四大雷区文字动画）
口播：“记住这三大必踩雷区：第一，中文直翻，关键细节被大模型严重吃词；第二，堆砌‘唯美、真实、大片’这种主观形容词，AI完全听不懂；第三，带有阿迪达斯等真实品牌，直接被安全审查拦截！”

【18-35s 神器亮相 · 7大黄金公式】
（画面：展示 Muse 提示词工坊 Studio Max 的界面操作，一键点选风格与运镜）
口播：“真正专业的电影导演都在用这个公式：[镜头景别] + [主体面料] + [环境纵深] + [物理动态] + [视觉风格] + [光影冷暖] + [原生音效]。不仅自动清洗品牌违规词，还能一键生成纯正地道的好莱坞英文Prompt和长镜头分镜！”

【35-45s 行动号召 CTA · 评论区引流】
（画面：展示评论区引导弹窗与高清成片）
口播：“工具和全套分镜预设我已经全部打包好了，评论区扣【提示词】或【666】，我把在线体验地址和一键部署包发你，赶紧收藏开练！”""",
            "post_body": """玩了这么久 AI 视频生成，你是不是也经常遇到：
❌ 动作一动就崩，人物四肢扭曲
❌ 画面塑料感极强，像 20 年前的劣质特效
❌ 中文喂给海外模型，出来的效果风马牛不相及

别慌！真正的高阶玩家早就不用大白话写词了。今天拆解好莱坞工业级的【7大视频黄金提示词公式】：

📐 1. 镜头景别 (Framing)：Cinematic medium tracking shot（拒绝静止机位）
👤 2. 主体物理 (Subject)：服装面料、随身配饰、神态微表情（规避主观词）
🌆 3. 环境纵深 (Setting)：雨后积水反光、视线景深、空气透视
🏃 4. 动作演变 (Motion)：步伐溅起细密水花、转角回眸（指定物理动词）
🎬 5. 视觉美学 (Aesthetics)：阿莱电影机35mm / 柯达500T / 王家卫抽帧
💡 6. 光影氛围 (Lighting)：金色晚霞逆光、丁达尔光束、冷暖对冲
🔊 7. 原生音效 (Audio)：脚步踏水声、远方闷雷、城市白噪音

✨ 我们还把这套逻辑做成了纯前端离线小工具【Muse 视频提示词工坊】！
- 支持 22 款顶级影视/二次元风格
- 自动版权清洗（把阿迪等词转为物理描述）
- 支持 0-3s / 3-6s 长镜头时序分镜

🎁 评论区留言【提示词】或【666】，无偿分享在线体验入口和一键离线部署包！👇""",
            "tags": [
                "#AI视频", "#提示词工程", "#Sora提示词", "#RunwayGen3",
                "#可灵AI", "#即梦AI", "#AI生产力工具", "#自媒体干货",
                "#神仙工具", "#视频剪辑"
            ],
            "comment_hook": "想要在线体验网址和单页部署包的小伙伴，评论区扣【666】，我逐个私发给大家！",
            "images": ["xhs_cover.jpg", "xhs_slide2.jpg"]
        },
        "x_thread": [
            {
                "tweet_num": 1,
                "text": """🚨 Stop writing AI video prompts in broken sentences!

If your Sora, Runway Gen-3, or Kling videos look like stiff PPTs, you're missing the Hollywood 7-part director formula.

Here is how pros architect cinematic prompts (and a free open-source studio to build them) 🧵👇"""
            },
            {
                "tweet_num": 2,
                "text": """1/ The Golden Video Formula:
• Framing: [Shot type & optics]
• Subject: [Garments & physical textures]
• Space: [Atmospheric depth & reflections]
• Motion: [Action evolution + tracking]
• Aesthetic: [35mm / Kodak 500T / Ghibli]
• Lighting & Audio: [Volumetric + Sound]"""
            },
            {
                "tweet_num": 3,
                "text": """2/ Claim 1 BILLION Free Tokens on Muse:
🎁 Join: https://muse.ai/join
🔑 Code: YB9JT8 (Redeem in "Settings" within 48h!)

🎬 Free 1-click Prompt Studio (22 styles, brand sanitization, 0-6s timeline):
👉 https://wisely88.github.io/muse/

RT to share! 🚀"""
            }
        ]
    },
    {
        "id": "campaign_02_anime_ghibli_shinkai",
        "topic": "二次元动漫 · 吉卜力与新海诚神仙美学",
        "target_audience": "喜欢动漫、壁纸、治愈系与二次元风格的创作者与粉丝",
        "xhs": {
            "title": "一秒做出宫崎骏吉卜力手绘！神仙运镜提示词大公开🌿",
            "subtitle": "你的名字与天气之子光影美学，一键套用",
            "video_script": """【0-5s 视觉轰炸 · 抓眼球】
（画面：播放一段极度治愈的吉卜力风草坡女孩追蒲公英视频，色彩极其饱满清澈，背景伴随久石让轻音乐）
口播：“你敢相信？这段吉卜力动画电影质感的视频，只用了一句提示词就直接生成了！”

【5-20s 美学拆解 · 核心关键词】
（画面：高亮展示核心英语术语卡片）
口播：“很多人写‘宫崎骏风格’，大模型根本不懂精髓。你必须给它这套专有词组：‘lush vibrant watercolor painted background’（浓郁手绘水彩画风）、‘whimsical fluffy clouds’（梦幻积雨云），以及‘emotional summer nostalgia’（夏日治愈怀旧感）。”

【20-35s 工具实操演示】
（画面：展示在提示词工坊中选择‘🌿 宫崎骏·吉卜力手绘’或‘🌧️ 新海诚·唯美光影’，自动生成纯正英文）
口播：“工坊里直接内置了吉卜力、新海诚、皮克斯3D、美漫蜘蛛侠等8大动漫分类！只要选好风格，输入中文描述，它就自动翻译成大模型最认的地道语法，彻底杜绝中文乱码！”

【35-45s 转化引流】
（画面：展示模版一键加载功能）
口播：“想做出这种封神动画分镜的，评论区扣【动漫】，把提示词模版和工具直接打包送你！”""",
            "post_body": """看腻了千篇一律的真人视频？今天教你用 AI 做出宫崎骏电影级别的神仙手绘动画！🍃

普通人写 Prompt：
❌ “一个女孩在草地上跑，宫崎骏风格，高清唯美” （AI 听了一头雾水，生成出来塑料感拉满）

电影级 Prompt 架构：
✅ [Framing]: A cinematic medium tracking shot follows a sweet anime girl wearing a woven straw hat with ribbon and white dress...
✅ [Setting]: sunlit idyllic countryside hills with swaying green wheat waves under azure sky, vintage coastal train beside glittering blue sea...
✅ [Motion]: running joyfully across the grassy hill chasing floating dandelion seeds...
✅ [Aesthetic]: Studio Ghibli anime aesthetic, Hayao Miyazaki directorial style, hand-drawn 2D animation, lush vibrant watercolor painted background...
✅ [Audio]: gentle summer breeze rustling tall grass, distant train horn echoing...

✨ 工具推荐：
在我们的【Muse 提示词工坊 Studio Max】里，点击【🎨 动画卡通】，一键预设好吉卜力、新海诚、皮克斯 3D、蜘蛛侠平行宇宙美漫波普！

💬 想要这套动漫神仙模版的小伙伴，在评论区打【动漫】，我私信发你！记得点赞收藏防走丢～""",
            "tags": [
                "#宫崎骏动画", "#吉卜力风格", "#新海诚美学", "#动漫提示词",
                "#AI视频教程", "#可灵AI生成", "#即梦AI", "#Midjourney视频",
                "#治愈系风景", "#二次元创作者"
            ],
            "comment_hook": "需要吉卜力 & 新海诚提示词模版的小伙伴，在评论区留言【动漫】，我私信发你体验链接！",
            "images": ["xhs_cover.jpg", "xhs_slide2.jpg"]
        },
        "x_thread": [
            {
                "tweet_num": 1,
                "text": """Studio Ghibli & Makoto Shinkai aesthetics in AI video are mindblowing when prompt architecture is dialed in. 🌿⛅

Here is how to get authentic hand-drawn watercolor anime motion in Sora, Kling & Runway Gen-3: 🧵👇"""
            },
            {
                "tweet_num": 2,
                "text": """2/ Don't just type "Miyazaki style". Use optical descriptors:
• "lush vibrant watercolor painted background"
• "whimsical towering cumulonimbus clouds"
• "emotional summer nostalgia mood"
• "panning camera tracking running subject"
• "breeze rustling tall grass" """
            },
            {
                "tweet_num": 3,
                "text": """3/ Try our 8 anime modules in Muse Prompt Studio:
👉 https://wisely88.github.io/muse/

🎁 Plus, get 1 BILLION Free Tokens on Muse:
Sign up: https://muse.ai/join
Code: YB9JT8 (Redeem in Settings in 48h!)

RT & create magic! 🌸✨"""
            }
        ]
    },
    {
        "id": "campaign_03_wong_kar_wai_retro",
        "topic": "电影质感 · 80-90年代王家卫抽帧港风",
        "target_audience": "追求高级影视质感、复古情怀、摄影与文艺片爱好者",
        "xhs": {
            "title": "王家卫电影那种抽帧霓虹感，用这句Prompt直接拿捏🎞️",
            "subtitle": "复古港风、慢门抽帧、繁体字霓虹招牌教程",
            "video_script": """【0-5s 经典台词氛围切入】
（画面：慢门抽帧绿粉霓虹雨夜，深咖色风衣男子在电话亭点烟，电影烟雾缭绕，配怀旧萨克斯BGM）
口播：“不知道从什么时候开始，连AI视频都开始有了保质期。但王家卫这种高级的抽帧胶片质感，任何时候看都是封神！”

【5-20s 专业术语解码】
（画面：红线标出画面的拖影、色彩和颗粒）
口播：“很多人以为王家卫就是下雨和调色，大错特错！精髓在两个摄影技术词：‘step-printing slow shutter’——慢门抽帧拖影；以及杜可风摄影标志性的‘Christopher Doyle cinematography with handheld breathing’！”

【20-35s 工坊快速实操】
（画面：点击‘🇭🇰 80-90s 港片黄金期’，瞬间组合出完整的双向解析分镜表）
口播：“用我们开发的提示词工坊，直接选中港片黄金期。繁体字粉绿霓虹、湿漉漉深水埗街巷、慢门拖影点烟，全套参数秒出！”

【35-45s 互动转化】
（画面：展示 Markdown 分镜台账一键导出）
口播：“整套分镜台账一键复制就能喂给大模型。评论区扣【港风】，免费领走完整模版！”""",
            "post_body": """“如果记忆也是一个罐头的话，我希望它永远不会过期。” 🚬

想要用 AI 做出《重庆森林》《堕落天使》那种高级到骨子里的王家卫港片质感，请把这套好莱坞导演参数刻进 DNA：

🎬 核心参数结构：
【风格基调】：1990s Hong Kong cinema aesthetic, Wong Kar-wai style, Christopher Doyle cinematography, step-printing slow shutter motion blur, neon green and warm amber hue, rich 35mm celluloid film grain
【主体人物】：身着复古深咖色风衣的男子，微卷碎发被雨水打湿，神情落寞
【场景环境】：狭窄逼仄的深水埗街巷，头顶繁体字粉绿霓虹招牌在雨雾中晕染，潮湿沥青路面流淌着彩色倒影
【动作动态】：男子在慢门抽帧拖影中穿过拥挤街头，在闪烁的公用电话亭旁驻足点烟，烟雾缓缓升腾

💡 这个提示词工坊把 80-90s 港片、90s VHS录像带、70s暖调柯达、Y2K千禧DV全部打包做成了一键生成！

💬 喜欢这种复古电影质感的朋友，评论区扣【港风】，把工具链接发给你！""",
            "tags": [
                "#王家卫美学", "#电影质感", "#港风复古", "#AI视频教程",
                "#电影分镜", "#胶片摄影", "#Sora提示词", "#Runway视频",
                "#视觉中国", "#影视后期"
            ],
            "comment_hook": "想要王家卫港片复古提示词预设的朋友，评论区留言【港风】，自动私发工具体验地址！",
            "images": ["xhs_cover.jpg", "xhs_slide2.jpg"]
        },
        "x_thread": [
            {
                "tweet_num": 1,
                "text": """Wong Kar-wai's cinematic visual style in 90s Hong Kong cinema is legendary. 🇭🇰🎞️

To recreate his hypnotic aesthetic in AI video models (Runway / Sora / Kling), standard keywords won't cut it. 

Here is the director-level breakdown: 🧵👇"""
            },
            {
                "tweet_num": 2,
                "text": """2/ The optical formula for the 90s Hong Kong look:
• Shutter: "step-printing slow shutter motion blur, hypnotic frame-lag"
• Optics: "handheld lens with natural breathing"
• Palette: "magenta & jade green neon reflections"
• Medium: "organic 35mm celluloid film grain" """
            },
            {
                "tweet_num": 3,
                "text": """3/ 22 film aesthetics built-in to Muse Studio:
👉 https://wisely88.github.io/muse/

🎁 Plus, grab 1 BILLION Free Tokens on Muse:
Join: https://muse.ai/join
Code: YB9JT8 (Go to Settings within 48h!)

RT & bookmark for film buffs! 🎥🇭🇰"""
            }
        ]
    },
    {
        "id": "campaign_04_long_take_timeline",
        "topic": "技术进阶 · 长镜头时序分镜 (0-3s / 3-6s)",
        "target_audience": "中高阶创作者、商业广告片导演、希望视频运镜有故事感的专业用户",
        "xhs": {
            "title": "终于有人把AI长镜头讲明白了！0-6秒时序分镜保姆级教学🎥",
            "subtitle": "告别画面抽搐，教会你电影级推拉摇移视线交汇",
            "video_script": """【0-5s 痛点直击】
（画面：展示一个镜头突然卡顿、跳帧变形的对比案例）
口播：“为什么你生成的AI视频只有前两秒好看，后面运镜就突然发疯变形？因为你没有给AI输入时序分镜逻辑！”

【5-20s 原理解释 · 视线引导】
（画面：展示时间轴图解 0-3s 与 3-6s）
口播：“在大模型底层，单镜头超过4秒就会出现物理发散。真正聪明的做法是用时序锚点：0到3秒固定起幅动作；3到6秒镜头越肩推进，把视线延伸交汇到第二主体！”

【20-35s 工具生成长镜头】
（画面：展示在提示词工坊中勾选‘开启长镜头时序分镜’，分别输入0-3s和3-6s动作，一键生成结构化Prompt）
口播：“看看工坊生成的输出：自动划分[0-3s]与[3-6s]动作延伸，还附带好莱坞标准的导演分镜Markdown台账，直接复制就能用在各种商业短片里！”

【35-45s 引流转化】
（画面：展示分镜台账导出与多平台支持）
口播：“想要这套长镜头时序生成器的，评论区扣【长镜头】，我把工具和实操指南发你！”""",
            "post_body": """很多人生成视频发现：画面只帅了 2 秒，第 3 秒运镜就开始抽搐变形… 🤯

这是因为视频大模型（无论是 Sora 还是 Runway Gen-3）在没有时间轴指令时，会自动发散！

解决这个问题的绝招就是——【分段时序长镜头架构】：

🎬 结构标准范例：
⏱️ [0-3s 起幅动作]：中景跟随少年步履，在雨后反光积水路面溅起细密水花
⏱️ [3-6s 运镜延伸]：镜头顺滑越过少年肩膀向前推入对焦，交汇至公园门口焦急等待的紫裙女孩
🎬 运镜指令：Camera smoothly tracks alongside then pushes in toward subject
💡 光影配合：低角度夕阳逆光穿透云层，地面反射金色晚霞

在我们的【Muse 视频提示词工坊】里，直接勾选【开启长镜头时序分镜】，填入起幅与推进，自动生成工业级长镜头指令包与 Markdown 导演台账！

💬 想做出丝滑电影级长镜头的朋友，评论区留言【长镜头】，私信发送工具体验地址！""",
            "tags": [
                "#AI长镜头", "#运镜技巧", "#影视分镜", "#AI视频教程",
                "#导演思维", "#Sora", "#RunwayGen3", "#视频剪辑技巧",
                "#电影摄影", "#AI创作"
            ],
            "comment_hook": "评论区留言【长镜头】，自动私发全套长镜头分镜提示词生成器与在线地址！",
            "images": ["xhs_cover.jpg", "xhs_slide2.jpg"]
        },
        "x_thread": [
            {
                "tweet_num": 1,
                "text": """Why do AI videos fall apart after 3 seconds? 🎬

Video models hallucinate physics unless you provide temporal anchors.

Here is how to structure 0-6s cinematic long takes using sequential camera directives: 🧵👇"""
            },
            {
                "tweet_num": 2,
                "text": """2/ The 2-Phase Sequence Structure:
• [0-3s Establish]: Tracking shot locking primary subject physics (footsteps in puddles).
• [3-6s Reveal]: Camera pushes past shoulder, shifting focus to reveal secondary subject ahead.
• Constant lighting and optics throughout."""
            },
            {
                "tweet_num": 3,
                "text": """3/ Try 0-6s long takes in Muse Studio:
👉 https://wisely88.github.io/muse/

🎁 Grab 1 BILLION Free Tokens on Muse:
Join: https://muse.ai/join
Code: YB9JT8 (Redeem in Settings within 48h!)

RT & share with AI filmmakers! 🚀🎥"""
            }
        ]
    }
]

def export_all_campaigns():
    output_dir = os.path.join(os.path.dirname(__file__), "queue")
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. 导出主任务队列表（供 muse 自动化 Agent 直接读取）
    queue_file = os.path.join(output_dir, "ready_to_post.json")
    with open(queue_file, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "campaign_count": len(CAMPAIGNS),
            "campaigns": CAMPAIGNS
        }, f, ensure_ascii=False, indent=2)
    print(f"✅ 已生成标准发帖队列文件: {queue_file}")

    # 2. 为每个专题生成独立的发布包（小红书帖子、视频脚本、推特串）
    for idx, c in enumerate(CAMPAIGNS, 1):
        c_dir = os.path.join(os.path.dirname(__file__), "posts", f"{idx:02d}_{c['id']}")
        os.makedirs(c_dir, exist_ok=True)
        
        # 小红书全套物料
        xhs_file = os.path.join(c_dir, "xhs_post.md")
        with open(xhs_file, "w", encoding="utf-8") as f:
            f.write(f"# 📌 小红书发布包：{c['xhs']['title']}\n\n")
            f.write(f"**副标题**：{c['xhs']['subtitle']}\n\n")
            f.write(f"**目标人群**：{c['target_audience']}\n\n")
            f.write(f"## 🎬 30-45s 口播与分镜短视频脚本\n\n```text\n{c['xhs']['video_script']}\n```\n\n")
            f.write(f"## 📝 小红书图文/视频笔记正文\n\n```text\n{c['xhs']['post_body']}\n```\n\n")
            f.write(f"## 🏷️ 话题标签\n\n{' '.join(c['xhs']['tags'])}\n\n")
            f.write(f"## 💬 评论区置顶引流引导语\n\n> {c['xhs']['comment_hook']}\n")

        # X (Twitter) 推文串
        x_file = os.path.join(c_dir, "x_thread.md")
        with open(x_file, "w", encoding="utf-8") as f:
            f.write(f"# 🐦 X (Twitter) Thread: {c['topic']}\n\n")
            for t in c['x_thread']:
                f.write(f"### Tweet {t['tweet_num']}/{len(c['x_thread'])}\n\n```text\n{t['text']}\n```\n\n")

    print(f"✅ 已为 muse 生成 {len(CAMPAIGNS)} 个独立主题发布包（含口播脚本、正文与 X Thread）")

if __name__ == "__main__":
    export_all_campaigns()
