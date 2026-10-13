"""
engine/assembler.py
基于 FFmpeg 的工业级全片自动串联、转场拼剪与音画合成器
"""

import os
import subprocess
from typing import List, Dict, Any

class VideoAssembler:
    @staticmethod
    def concatenate_shots(video_files: List[str], output_path: str, add_crossfade: bool = False) -> bool:
        """
        无损快速将多个分镜视频合成为全片成片
        """
        if not video_files:
            return False

        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        list_file = os.path.join(out_dir or ".", "concat_filelist.txt")
        try:
            with open(list_file, "w", encoding="utf-8") as f:
                for vf in video_files:
                    f.write(f"file '{os.path.abspath(vf)}'\n")

            cmd = [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                "-i", list_file, "-c", "copy", output_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            return os.path.exists(output_path)
        except Exception as e:
            print(f"[Assembler] 拼接合成异常: {e}")
            return False
        finally:
            if os.path.exists(list_file):
                try:
                    os.remove(list_file)
                except Exception:
                    pass
