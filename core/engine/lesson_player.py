"""
StudyPlayCoordinate - UnifiedVideo/DocumentPlayEntry（Cross-platform）
"""
import subprocess
import os
import sys
import shutil
import platform
from pathlib import Path


class LessonPlayer:
    """CoursePlayCoordinate"""

    def __init__(self):
        self.current_video = None
        self._mpv_path = self._find_mpv()

    def _find_mpv(self):
        """FindmpvPlay（Cross-platform）"""
        system = platform.system()

        if system == "Darwin":  # macOS
            candidates = ["mpv"]
        else:  # LinuxAndOther
            candidates = ["mpv"]

        for path in candidates:
            if shutil.which(path) or os.path.exists(path):
                return path
        return None

    def play_video(self, video_path):
        """PlayVideoFile（Cross-platform）"""
        system = platform.system()
        if not os.path.exists(video_path):
            return False, "FileNot found"
        try:
            if self._mpv_path:
                subprocess.Popen([self._mpv_path, video_path])
            else:
                # fallback: use system default player
                if system == "Darwin":  # macOS
                    subprocess.Popen(["open", video_path])
                else:  # LinuxAndOther
                    subprocess.Popen(["xdg-open", video_path])
            return True, "PlayIn"
        except Exception as e:
            return False, str(e)

    def open_pdf(self, pdf_path):
        """OpenPDFFile（Cross-platform）"""
        system = platform.system()
        if not os.path.exists(pdf_path):
            return False, "FileNot found"
        try:
            if system == "Darwin":  # macOS
                subprocess.Popen(["open", pdf_path])
            else:  # LinuxAndOther
                subprocess.Popen(["xdg-open", pdf_path])
            return True, "AlreadyOpen"
        except Exception as e:
            return False, str(e)

    def play_resource(self, resource):
        """RootDataClassTypePlayResource"""
        if resource["type"] == "video":
            return self.play_video(resource["path"])
        elif resource["type"] == "pdf":
            return self.open_pdf(resource["path"])
        return False, "NotSupportResourceClassType"
