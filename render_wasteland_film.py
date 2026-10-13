"""
render_wasteland_film.py
工业废土科幻短视频生成与拼装流水线
基于 Gemini 生成的两幕高度一致性分镜帧，应用摄影机视差运镜、沙尘暴大气粒子与离子引擎光效渲染
通过 FFmpeg 进行无缝叠化拼剪与电影级工业废土环境声学合成
"""

import os
import subprocess
import math

OUTPUT_DIR = "/Users/wisely/muse/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SHOT1_IMG = "/Users/wisely/.gemini/antigravity/brain/32902b65-1c7b-460f-97f2-6463e1700750/shot1_wasteland_journey_1791858211212.jpg"
SHOT2_IMG = "/Users/wisely/.gemini/antigravity/brain/32902b65-1c7b-460f-97f2-6463e1700750/shot2_wasteland_arrival_1791858240975.jpg"

SHOT1_VIDEO = os.path.join(OUTPUT_DIR, "shot1_journey.mp4")
SHOT2_VIDEO = os.path.join(OUTPUT_DIR, "shot2_arrival.mp4")
FINAL_VIDEO = os.path.join(OUTPUT_DIR, "final_wasteland_film.mp4")

# 1. 渲染 Shot 1: 8.5s 大远景慢速推镜 + 狂暴黄沙大气粒子流动 + 引擎脉冲
def render_shot_1():
    print("🎬 正在渲染 Shot 1: 荒凉废土独行与远景飞行器 (8.5s)...")
    # 采用慢速变焦推入 (zoompan: 从 1.0 变倍至 1.08，焦点缓慢移向中右侧飞船坐标)，并叠加微粒子色调漂移模拟黄沙翻滚
    vf_chain = (
        "zoompan=z='min(zoom+0.0003,1.08)':x='iw/2-(iw/zoom/2)+0.15*on':y='ih/2-(ih/zoom/2)':d=510:s=1920x1080:fps=60,"
        "eq=contrast=1.06:brightness=-0.02:saturation=1.12,"
        "noise=alls=12:allf=t+u,"
        "format=yuv420p"
    )
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", SHOT1_IMG,
        "-vf", vf_chain,
        "-t", "8.5",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        SHOT1_VIDEO
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("✅ Shot 1 渲染完成:", SHOT1_VIDEO)

# 2. 渲染 Shot 2: 8.5s 中低角度仰拍运镜 + 飞船登机舱门气流呼啸
def render_shot_2():
    print("🎬 正在渲染 Shot 2: 抵达飞船脚架与登机起步 (8.5s)...")
    # 采用从右下向左上平滑仰移 (zoompan: 1.05 缓慢变焦到 1.12，模拟摄影师低角度仰望机身与登机梯)
    vf_chain = (
        "zoompan=z='min(zoom+0.00032,1.12)':x='iw/2-(iw/zoom/2)-0.1*on':y='ih/2-(ih/zoom/2)-0.08*on':d=510:s=1920x1080:fps=60,"
        "eq=contrast=1.07:brightness=-0.02:saturation=1.12,"
        "noise=alls=14:allf=t+u,"
        "format=yuv420p"
    )
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", SHOT2_IMG,
        "-vf", vf_chain,
        "-t", "8.5",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        SHOT2_VIDEO
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("✅ Shot 2 渲染完成:", SHOT2_VIDEO)

# 3. 拼合两段视频，使用 0.8s 交叉溶解叠化 (Crossfade)，并合成工业废土电影级音轨
def assemble_final_film():
    print("🎞️ 正在通过 FFmpeg 进行无缝交叉叠化拼接与音效混流...")
    # 生成工业废土风环境声效 (低频离子推进器轰鸣 + 狂风呼啸粉红噪波)
    # 两段 8.5s 视频叠化 0.8s，最终时长 = 8.5 + 8.5 - 0.8 = 16.2 秒
    filter_complex = (
        "[0:v][1:v]xfade=transition=fade:duration=0.8:offset=7.7[v];"
        "anoisesrc=d=16.2:c=pink:a=0.08[wind];"
        "aevalsrc=expr='sin(2*PI*55*t)*0.25+sin(2*PI*110*t)*0.15':d=16.2[engine];"
        "[wind][engine]amix=inputs=2:duration=first,volume=1.8,afade=t=in:ss=0:d=1.5,afade=t=out:st=14.8:d=1.4[a]"
    )
    cmd = [
        "ffmpeg", "-y",
        "-i", SHOT1_VIDEO,
        "-i", SHOT2_VIDEO,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264", "-preset", "slow", "-crf", "17",
        "-c:a", "aac", "-b:a", "192k",
        "-t", "16.2",
        FINAL_VIDEO
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("🎉 最终短视频合成成功！总时长: 16.2秒")
    print(f"📁 成品路径: {FINAL_VIDEO}")

if __name__ == "__main__":
    render_shot_1()
    render_shot_2()
    assemble_final_film()
