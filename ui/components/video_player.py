"""
视频播放组件 - 支持章节课程列表选择
优化：Windows原生播放器+改进布局
"""
import customtkinter as ctk
import subprocess
import os
import sys
import re
from datetime import datetime


class VideoPlayer(ctk.CTkFrame):
    """视频播放器组件"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.current_file = None
        self.current_lesson_info = None
        self.player_process = None
        self._build_ui()

    def _smart_truncate(self, text, max_len=30):
        """智能截断：保留有意义的中文字符"""
        if len(text) <= max_len:
            return text
        
        # 尝试在标点处截断
        punctuations = ['，', '。', '、', '：', '；', '!', '?', ')', '】', '》', '】']
        for punct in punctuations:
            idx = text.rfind(punct, 0, max_len + 5)
            if idx > max_len * 0.6:
                return text[:idx + 1]
        
        # 否则直接截断
        return text[:max_len - 3] + "..."

    def _build_ui(self):
        # 纯视频播放区域
        self.video_area = ctk.CTkFrame(self, fg_color="#1a1a2e", corner_radius=8)
        self.video_area.pack(fill="both", expand=True, padx=10, pady=5)

        self.info_label = ctk.CTkLabel(
            self.video_area,
            text="📺 请选择章节和课时开始学习",
            font=("Microsoft YaHei", 13),
            text_color="#a0a0b0",
        )
        self.info_label.place(relx=0.5, rely=0.5, anchor="center")

        # 控制按钮
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=8)

        self.play_btn = ctk.CTkButton(
            btn_frame,
            text="▶ 播放",
            command=self._play_selected,
            width=80,
            height=28,
            fg_color="#27ae60",
            hover_color="#219653",
        )
        self.play_btn.pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="⏹ 停止",
            command=self._stop,
            width=70,
            height=28,
            fg_color="#e74c3c",
            hover_color="#c0392b",
        ).pack(side="left", padx=5)

        self.progress_var = ctk.StringVar(value="准备就绪")
        ctk.CTkLabel(
            btn_frame, textvariable=self.progress_var,
            font=("Microsoft YaHei", 10),
            text_color="#34495e",
        ).pack(side="left", padx=15)

    def set_lessons(self, lessons):
        """设置章节视频列表（保留接口，实际由main_window管理）"""
        # 此方法保留用于兼容，课时列表已在main_window中独立管理
        pass

    def _expand_lesson(self, lesson):
        """展开/收起章节课时列表"""
        pass

    def _play_video(self, video_path, lesson_title):
        """使用系统默认播放器播放视频"""
        self._stop()
        if not os.path.exists(video_path):
            self._show_error("视频文件不存在")
            return

        self.current_file = video_path
        self.current_lesson_info = {"title": lesson_title, "path": video_path}

        try:
            # Windows使用start命令打开默认播放器
            result = subprocess.Popen([
                "cmd", "/c", "start", "", video_path
            ], creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0)
            
            self.info_label.configure(text=f"🎬 正在播放\n{lesson_title}")
            self.progress_var.set(f"▶ {lesson_title[:20]}")
        except Exception as e:
            self._show_error(f"无法播放: {str(e)[:30]}")

    def _play_selected(self):
        """播放当前选中的视频"""
        if self.current_file:
            self._play_video(self.current_file, self.current_lesson_info.get("title", ""))

    def _stop(self):
        """停止播放"""
        if self.player_process:
            try:
                self.player_process.terminate()
            except:
                pass
            self.player_process = None
        self.current_file = None
        self.info_label.configure(text="📺 请选择章节和课时开始学习")
        self.progress_var.set("准备就绪")

    def _show_error(self, msg):
        self.info_label.configure(text=f"❌ {msg}", text_color="#e74c3c")
        self.progress_var.set(f"错误: {msg}")


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("800x600")
    player = VideoPlayer(app)
    player.pack(fill="both", expand=True)
    app.mainloop()
