"""
VideoPlayComponent - SupportChapterCourseListSelect
Optimize：WindowsNativePlay+Improve Layout
"""
import customtkinter as ctk
import subprocess
import os
import sys
import re
from datetime import datetime


class VideoPlayer(ctk.CTkFrame):
    """VideoPlayComponent"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.current_file = None
        self.current_lesson_info = None
        self.player_process = None
        self._build_ui()

    def _smart_truncate(self, text, max_len=30):
        """Smart Truncation：Retain Meaningful Characters"""
        if len(text) <= max_len:
            return text
        
        # TryInTruncate at Punctuation
        punctuations = ['，', '。', '、', '：', '；', '!', '?', ')', '】', '》', '】']
        for punct in punctuations:
            idx = text.rfind(punct, 0, max_len + 5)
            if idx > max_len * 0.6:
                return text[:idx + 1]
        
        # NoThen Directly Truncate
        return text[:max_len - 3] + "..."

    def _build_ui(self):
        # PureVideoPlayArea
        self.video_area = ctk.CTkFrame(self, fg_color="#1a1a2e", corner_radius=8)
        self.video_area.pack(fill="both", expand=True, padx=10, pady=5)

        self.info_label = ctk.CTkLabel(
            self.video_area,
            text="📺 Please selectChapterAndLessonStartStudy",
            font=("Microsoft YaHei", 13),
            text_color="#a0a0b0",
        )
        self.info_label.place(relx=0.5, rely=0.5, anchor="center")

        # ControlByButton
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=8)

        self.play_btn = ctk.CTkButton(
            btn_frame,
            text="▶ Play",
            command=self._play_selected,
            width=80,
            height=28,
            fg_color="#27ae60",
            hover_color="#219653",
        )
        self.play_btn.pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="⏹ Stop",
            command=self._stop,
            width=70,
            height=28,
            fg_color="#e74c3c",
            hover_color="#c0392b",
        ).pack(side="left", padx=5)

        self.progress_var = ctk.StringVar(value="Ready")
        ctk.CTkLabel(
            btn_frame, textvariable=self.progress_var,
            font=("Microsoft YaHei", 10),
            text_color="#34495e",
        ).pack(side="left", padx=15)

    def set_lessons(self, lessons):
        """SettingsChapterVideoList（Retain Interface，Actually Bymain_windowManage）"""
        # This Method Retained for Compatibility，LessonListAlreadyInmain_windowIndependently Managed In
        pass

    def _expand_lesson(self, lesson):
        """Expand/CollapseChapterLessonList"""
        pass

    def _play_video(self, video_path, lesson_title):
        """Use System DefaultPlayPlayVideo"""
        self._stop()
        if not os.path.exists(video_path):
            self._show_error("VideoFileNot found")
            return

        self.current_file = video_path
        self.current_lesson_info = {"title": lesson_title, "path": video_path}

        try:
            # WindowsUsestartCommandOpenDefaultPlay
            result = subprocess.Popen([
                "cmd", "/c", "start", "", video_path
            ], creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0)
            
            self.info_label.configure(text=f"🎬 ProcessingPlay\n{lesson_title}")
            self.progress_var.set(f"▶ {lesson_title[:20]}")
        except Exception as e:
            self._show_error(f"CannotPlay: {str(e)[:30]}")

    def _play_selected(self):
        """PlayCurrently SelectedVideo"""
        if self.current_file:
            self._play_video(self.current_file, self.current_lesson_info.get("title", ""))

    def _stop(self):
        """StopPlay"""
        if self.player_process:
            try:
                self.player_process.terminate()
            except:
                pass
            self.player_process = None
        self.current_file = None
        self.info_label.configure(text="📺 Please selectChapterAndLessonStartStudy")
        self.progress_var.set("Ready")

    def _show_error(self, msg):
        self.info_label.configure(text=f"❌ {msg}", text_color="#e74c3c")
        self.progress_var.set(f"Error: {msg}")


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("800x600")
    player = VideoPlayer(app)
    player.pack(fill="both", expand=True)
    app.mainloop()
