"""
主窗口 - 整体布局
"""
import customtkinter as ctk
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.paths import get_app_dir, ensure_dirs
from config.settings import load_settings
from ui.styles import COLORS, FONTS, SIDEBAR, BUTTON_CONFIG
from ui.components.course_selector_widget import CourseSelectorWidget
from ui.components.video_player import VideoPlayer
from ui.components.pdf_viewer import PDFViewer
from core.engine.progress_tracker import ProgressTracker
from core.storage.database import StudyDatabase


class MainWindow(ctk.CTk):
    """柏慧学堂主窗口"""

    def __init__(self):
        super().__init__()
        ensure_dirs()
        self.settings = load_settings()

        # 窗口设置
        self.title(f"柏慧学堂 v{self.settings.get('version', '2.0.0')}")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        # 设置外观
        ctk.set_appearance_mode(self.settings.get("theme", "light"))
        ctk.set_default_color_theme("blue")

        # 初始化数据
        self.db = StudyDatabase()
        self.tracker = ProgressTracker(self.db)

        # 构建UI
        self._build_layout()
        self._load_recent()

    def _build_layout(self):
        """构建主布局"""
        # 主框架
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True)

        # 左侧导航栏
        self._build_sidebar(main_frame)

        # 右侧内容区
        self.content_frame = ctk.CTkFrame(main_frame, fg_color=COLORS["bg_light"])
        self.content_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # 顶部工具栏
        self._build_toolbar()

        # 内容区域（多页面）
        self._build_content_area()

    def _build_sidebar(self, parent):
        """左侧边栏"""
        sidebar = ctk.CTkFrame(parent, width=SIDEBAR["width"], fg_color=SIDEBAR["bg_color"])
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", pady=15)
        ctk.CTkLabel(
            logo_frame,
            text="📚 柏慧学堂",
            font=FONTS["large"],
            text_color=COLORS["white"],
        ).pack()
        ctk.CTkLabel(
            logo_frame,
            text="初中离线自学",
            font=FONTS["small"],
            text_color="#888888",
        ).pack()

        # 导航按钮
        nav_items = [
            ("📖", "课程学习", "courses"),
            ("📝", "题库练习", "quiz"),
            ("🤖", "AI诊断", "ai"),
            ("📕", "错题本", "error_book"),
            ("⚙️", "设置", "settings"),
        ]

        for icon, text, page in nav_items:
            btn = ctk.CTkButton(
                sidebar,
                text=f"  {icon}  {text}",
                font=FONTS["body"],
                fg_color="transparent",
                hover_color="#3498db",
                text_color="#ffffff",
                anchor="w",
                height=40,
                command=lambda p=page: self._switch_page(p),
            )
            btn.pack(fill="x", padx=10)

        # 课程选择器（下拉筛选）
        self.course_selector = CourseSelectorWidget(sidebar)
        self.course_selector.pack(fill="both", expand=True, padx=0, pady=10)
        self.course_selector.set_callback(self._on_course_selected)

    def _build_toolbar(self):
        """顶部工具栏"""
        toolbar = ctk.CTkFrame(self.content_frame, fg_color=COLORS["primary"], height=45)
        toolbar.pack(fill="x")
        toolbar.pack_propagate(False)

        # 标题
        self.toolbar_title = ctk.CTkLabel(
            toolbar,
            text="课程学习",
            font=FONTS["heading"],
            text_color=COLORS["white"],
        )
        self.toolbar_title.pack(side="left", padx=20)

        # 网络状态
        self.net_status = ctk.CTkLabel(
            toolbar,
            text="🌐 检测中...",
            font=FONTS["small"],
            text_color=COLORS["white"],
        )
        self.net_status.pack(side="right", padx=20)

        # 刷新按钮
        ctk.CTkButton(
            toolbar,
            text="🔄 刷新",
            font=FONTS["small"],
            fg_color="transparent",
            text_color=COLORS["white"],
            hover_color="#1a5276",
            command=self._refresh_data,
            width=60,
            height=25,
        ).pack(side="right", padx=10)

    def _build_content_area(self):
        """内容区域"""
        # 课程学习页
        self.courses_page = ctk.CTkFrame(self.content_frame, fg_color=COLORS["bg_light"])
        self._build_courses_page(self.courses_page)

        # 导入设置页面
        from ui.settings_page import SettingsPage
        from core.engine.quiz_manager import QuizManager
        from ui.components.quiz_panel import QuizPanel
        
        # 导入AI聊天面板
        from ui.components.ai_chat_panel import AIChatPanel
        
        # 初始化题库管理器
        self.quiz_manager = QuizManager()
        
        # 题库练习页
        self.quiz_page = QuizPanel(self.content_frame, quiz_manager=self.quiz_manager)
        self.ai_page = AIChatPanel(self.content_frame)
        self.error_book_page = self._create_placeholder("📕 错题本\n\n功能开发中...")
        self.settings_page = SettingsPage(self.content_frame)

        # 默认显示课程页
        self.current_page = self.courses_page
        self.current_page.pack(fill="both", expand=True)

    def _build_courses_page(self, parent):
        """课程学习页布局 - 左视频+课时，右AI答疑"""
        # 外层容器
        main_container = ctk.CTkFrame(parent, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # 左侧区域（50%宽度）
        left_panel = ctk.CTkFrame(main_container, fg_color="transparent")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 3))

        # 左上：视频播放器
        video_frame = ctk.CTkFrame(left_panel, fg_color="white", corner_radius=8)
        video_frame.pack(fill="both", expand=True, pady=(0, 5))

        ctk.CTkLabel(video_frame, text="📺 视频学习",
                     font=FONTS["heading"]).pack(anchor="w", padx=10, pady=5)

        self.video_player = VideoPlayer(video_frame)
        self.video_player.pack(fill="both", expand=True, padx=10, pady=5)

        # 左下：课时列表
        lesson_frame = ctk.CTkFrame(left_panel, fg_color="white", corner_radius=8)
        lesson_frame.pack(fill="both", expand=True, pady=(5, 0))

        ctk.CTkLabel(lesson_frame, text="📋 课时列表",
                     font=FONTS["body"]).pack(anchor="w", padx=10, pady=5)

        self.lesson_listbox = ctk.CTkScrollableFrame(
            lesson_frame, fg_color="transparent"
        )
        self.lesson_listbox.pack(fill="both", expand=True, padx=10, pady=5)

        # 右侧区域（50%宽度）- AI答疑
        right_panel = ctk.CTkFrame(main_container, fg_color="white", corner_radius=8)
        right_panel.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(right_panel, text="🤖 AI答疑",
                     font=FONTS["heading"]).pack(anchor="w", padx=10, pady=5)

        # 集成AI答疑面板
        from ui.components.ai_chat_panel import AIChatPanel
        self.ai_panel = AIChatPanel(right_panel)
        self.ai_panel.pack(fill="both", expand=True, padx=5, pady=(0, 5))

    def _create_placeholder(self, text):
        """创建占位页面"""
        page = ctk.CTkFrame(self.content_frame, fg_color=COLORS["bg_light"])
        label = ctk.CTkLabel(
            page,
            text=text,
            font=FONTS["title"],
            text_color=COLORS["text_secondary"],
        )
        label.place(relx=0.5, rely=0.5, anchor="center")
        return page


    def _switch_page(self, page_name):
        """切换页面"""
        pages = {
            "courses": (self.courses_page, "课程学习"),
            "quiz": (self.quiz_page, "题库练习"),
            "ai": (self.ai_page, "AI诊断"),
            "error_book": (self.error_book_page, "错题本"),
            "settings": (self.settings_page, "设置"),
        }

        if page_name in pages:
            page, title = pages[page_name]
            if hasattr(self, "current_page"):
                self.current_page.pack_forget()
            page.pack(fill="both", expand=True)
            self.current_page = page
            self.toolbar_title.configure(text=title)

    def _on_course_selected(self, selection):
        """课程选择回调（新：下拉筛选格式）"""
        subject = selection.get("subject")
        grade = selection.get("grade")
        term = selection.get("term")
        chapter = selection.get("chapter")
        if not all([subject, grade, term, chapter]):
            return
        self._load_course_content(subject, grade, term, chapter)

    def _play_video(self, video_path, lesson_title):
        """播放视频"""
        self.video_player._play_video(video_path, lesson_title)

    def _load_course_content(self, subject, grade, term, chapter_label=None):
        """加载课程学习内容 - 显示章节视频列表（靶向特定章节）"""
        from core.engine.course_selector import CourseSelector
        selector = CourseSelector()

        # 获取所有章节数据
        all_chapters = selector.get_chapters(subject, grade, term)
        if not all_chapters:
            self.video_player.info_label.configure(
                text=f"⚠️ {grade}{term} 暂无可用课程"
            )
            return

        # 清空课时列表
        for widget in self.lesson_listbox.winfo_children():
            widget.destroy()

        # 如果指定了章节，只展示该章节
        if chapter_label:
            # 从下拉标签中提取章节名（格式："第X章-xxx (N节)"）
            ch_title = chapter_label.split(" (")[0]
            chapters = [ch for ch in all_chapters if ch["title"] == ch_title]
            if not chapters:
                chapters = [ch for ch in all_chapters if ch["number"] in ch_title]
        else:
            chapters = all_chapters

        # 更新播放器信息
        self.video_player.info_label.configure(
            text=f"📚 {subject} {grade}{term}\n{chapters[0]['title'] if chapters else ''}"
        )

        # 显示章节和课时列表
        for idx, ch in enumerate(chapters):
            ch_title = ch["title"]
            videos = ch.get("videos", [])

            # 章节标题
            ch_label = ctk.CTkLabel(
                self.lesson_listbox,
                text=f"{'第' + ch_title if not ch_title.startswith('第') else ch_title}",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#2c3e50",
            )
            ch_label.pack(fill="x", padx=8, pady=(8, 4))

            # 课时按钮
            for video in videos:
                video_path = video.get("path", "")
                video_title = video.get("title", video_path.split("/")[-1].replace(".mp4", ""))

                btn = ctk.CTkButton(
                    self.lesson_listbox,
                    text=f"▶ {video_title}",
                    font=("Microsoft YaHei", 10),
                    height=28,
                    fg_color="#3498db",
                    hover_color="#2980b9",
                    text_color="white",
                    command=lambda p=video_path, t=video_title: self._play_video(p, t),
                    width=260,
                    border_width=0,
                )
                btn.pack(fill="x", padx=8, pady=2)

        # 更新进度显示
        progress = self.tracker.get_dashboard()
        self.progress_label.configure(
            text=f"共 {progress['total_lessons']} 课时，已完成 {progress['completed']} 课时"
        )

    def _load_recent(self):
        """加载最近学习"""
        pass  # TODO: 从数据库加载最近记录

    def _refresh_data(self):
        """刷新数据"""
        self.net_status.configure(text="🔄 刷新中...")
        self.after(500, lambda: self.net_status.configure(text="🌐 已连接"))

    def run(self):
        """运行应用"""
        self.mainloop()


def main():
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
