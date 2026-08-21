"""
学习播放器协调器 - 统一视频/文档播放入口（跨平台）
"""
import subprocess
import os
import sys
import shutil
import platform
from pathlib import Path


class LessonPlayer:
    """课程播放器协调器"""

    def __init__(self):
        self.current_video = None
        self._mpv_path = self._find_mpv()

    def _find_mpv(self):
        """查找mpv播放器（跨平台）"""
        system = platform.system()

        if system == "Darwin":  # macOS
            candidates = ["mpv"]
        else:  # Linux和其他
            candidates = ["mpv"]

        for path in candidates:
            if shutil.which(path) or os.path.exists(path):
                return path
        return None

    def play_video(self, video_path):
        """播放视频文件（跨平台）"""
        system = platform.system()
        if not os.path.exists(video_path):
            return False, "文件不存在"
        try:
            if self._mpv_path:
                subprocess.Popen([self._mpv_path, video_path])
            else:
                # fallback: use system default player
                if system == "Darwin":  # macOS
                    subprocess.Popen(["open", video_path])
                else:  # Linux和其他
                    subprocess.Popen(["xdg-open", video_path])
            return True, "播放中"
        except Exception as e:
            return False, str(e)

    def open_pdf(self, pdf_path):
        """打开PDF文件（跨平台）"""
        system = platform.system()
        if not os.path.exists(pdf_path):
            return False, "文件不存在"
        try:
            if system == "Darwin":  # macOS
                subprocess.Popen(["open", pdf_path])
            else:  # Linux和其他
                subprocess.Popen(["xdg-open", pdf_path])
            return True, "已打开"
        except Exception as e:
            return False, str(e)

    def play_resource(self, resource):
        """根据类型播放资源"""
        if resource["type"] == "video":
            return self.play_video(resource["path"])
        elif resource["type"] == "pdf":
            return self.open_pdf(resource["path"])
        return False, "不支持的资源类型"
