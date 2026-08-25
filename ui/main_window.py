"""
Main Window - Overall Layout
"""
import customtkinter as ctk
import sys
from pathlib import Path

# AddProjectRootDirectoryToPath
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
    """Baihuixuetang MainWindow"""

    def __init__(self):
        super().__init__()
        ensure_dirs()
        self.settings = load_settings()

        # WindowSettings
        self.title(f"柏慧学堂 v{self.settings.get('version', '2.0.0')}")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        # SettingsAppearance
        ctk.set_appearance_mode(self.settings.get("theme", "light"))
        ctk.set_default_color_theme("blue")

        # Initialize Data
        self.db = StudyDatabase()
        self.tracker = ProgressTracker(self.db)

        # Build UI
        self._build_layout()
        self._load_recent()

    def _build_layout(self):
        """Build Main Layout"""
        # Main Frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True)

        # Left Sidebar
        self._build_sidebar(main_frame)

        # Right Content Area
        self.content_frame = ctk.CTkFrame(main_frame, fg_color=COLORS["bg_light"])
        self.content_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # Top Toolbar
        self._build_toolbar()

        # Content Area（MorePagePage）
        self._build_content_area()

    def _build_sidebar(self, parent):
        """LeftEdgeBar"""
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
            text="Junior Offline Study",
            font=FONTS["small"],
            text_color="#888888",
        ).pack()

        # Navigation Buttons
        nav_items = [
            ("📖", "Courses", "courses"),
            ("📝", "Quiz", "quiz"),
            ("🤖", "AI Diagnosis", "ai"),
            ("📕", "Error Book", "error_book"),
            ("⚙️", "Settings", "settings"),
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

        # CourseSelect（DropdownFilter）
        self.course_selector = CourseSelectorWidget(sidebar)
        self.course_selector.pack(fill="both", expand=True, padx=0, pady=10)
        self.course_selector.set_callback(self._on_course_selected)

    def _build_toolbar(self):
        """Top Toolbar"""
        toolbar = ctk.CTkFrame(self.content_frame, fg_color=COLORS["primary"], height=45)
        toolbar.pack(fill="x")
        toolbar.pack_propagate(False)

        # Title
        self.toolbar_title = ctk.CTkLabel(
            toolbar,
            text="Courses",
            font=FONTS["heading"],
            text_color=COLORS["white"],
        )
        self.toolbar_title.pack(side="left", padx=20)

        # Network Status
        self.net_status = ctk.CTkLabel(
            toolbar,
            text="🌐 Checking......",
            font=FONTS["small"],
            text_color=COLORS["white"],
        )
        self.net_status.pack(side="right", padx=20)

        # RefreshByButton
        ctk.CTkButton(
            toolbar,
            text="🔄 Refresh",
            font=FONTS["small"],
            fg_color="transparent",
            text_color=COLORS["white"],
            hover_color="#1a5276",
            command=self._refresh_data,
            width=60,
            height=25,
        ).pack(side="right", padx=10)

    def _build_content_area(self):
        """Content Area"""
        # CoursesPage
        self.courses_page = ctk.CTkFrame(self.content_frame, fg_color=COLORS["bg_light"])
        self._build_courses_page(self.courses_page)

        # Settings Page
        from ui.settings_page import SettingsPage
        from core.engine.quiz_manager import QuizManager
        from ui.components.quiz_panel import QuizPanel
        
        # AI Chat Panel
        from ui.components.ai_chat_panel import AIChatPanel
        
        # Initialize Quiz Manager
        self.quiz_manager = QuizManager()
        
        # QuizPage
        self.quiz_page = QuizPanel(self.content_frame, quiz_manager=self.quiz_manager)
        self.ai_page = AIChatPanel(self.content_frame)
        self.error_book_page = self._create_placeholder("📕 Error Book\n\nFeature in development...")
        self.settings_page = SettingsPage(self.content_frame)

        # Default to Course Page
        self.current_page = self.courses_page
        self.current_page.pack(fill="both", expand=True)

    def _build_courses_page(self, parent):
        """CoursesPageLayout - LeftVideo+Lesson，RightAIQ&A"""
        # Outer LayerContent
        main_container = ctk.CTkFrame(parent, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # LeftArea（50%Width）
        left_panel = ctk.CTkFrame(main_container, fg_color="transparent")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 3))

        # LeftOn：VideoPlay
        video_frame = ctk.CTkFrame(left_panel, fg_color="white", corner_radius=8)
        video_frame.pack(fill="both", expand=True, pady=(0, 5))

        ctk.CTkLabel(video_frame, text="📺 VideoStudy",
                     font=FONTS["heading"]).pack(anchor="w", padx=10, pady=5)

        self.video_player = VideoPlayer(video_frame)
        self.video_player.pack(fill="both", expand=True, padx=10, pady=5)

        # LeftBelow：LessonList
        lesson_frame = ctk.CTkFrame(left_panel, fg_color="white", corner_radius=8)
        lesson_frame.pack(fill="both", expand=True, pady=(5, 0))

        ctk.CTkLabel(lesson_frame, text="📋 LessonList",
                     font=FONTS["body"]).pack(anchor="w", padx=10, pady=5)

        self.lesson_listbox = ctk.CTkScrollableFrame(
            lesson_frame, fg_color="transparent"
        )
        self.lesson_listbox.pack(fill="both", expand=True, padx=10, pady=5)

        # RightSideArea（50%Width）- AIQ&A
        right_panel = ctk.CTkFrame(main_container, fg_color="white", corner_radius=8)
        right_panel.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(right_panel, text="🤖 AIQ&A",
                     font=FONTS["heading"]).pack(anchor="w", padx=10, pady=5)

        # IntegrateAIQ&APanel
        from ui.components.ai_chat_panel import AIChatPanel
        self.ai_panel = AIChatPanel(right_panel)
        self.ai_panel.pack(fill="both", expand=True, padx=5, pady=(0, 5))

    def _create_placeholder(self, text):
        """Create PlaceholderPagePage"""
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
        """SwitchPagePage"""
        pages = {
            "courses": (self.courses_page, "Courses"),
            "quiz": (self.quiz_page, "Quiz"),
            "ai": (self.ai_page, "AI Diagnosis"),
            "error_book": (self.error_book_page, "Error Book"),
            "settings": (self.settings_page, "Settings"),
        }

        if page_name in pages:
            page, title = pages[page_name]
            if hasattr(self, "current_page"):
                self.current_page.pack_forget()
            page.pack(fill="both", expand=True)
            self.current_page = page
            self.toolbar_title.configure(text=title)

    def _on_course_selected(self, selection):
        """CourseSelectCallback（New：DropdownFilterFormat）"""
        subject = selection.get("subject")
        grade = selection.get("grade")
        term = selection.get("term")
        chapter = selection.get("chapter")
        if not all([subject, grade, term, chapter]):
            return
        self._load_course_content(subject, grade, term, chapter)

    def _play_video(self, video_path, lesson_title):
        """PlayVideo"""
        self.video_player._play_video(video_path, lesson_title)

    def _load_course_content(self, subject, grade, term, chapter_label=None):
        """LoadCoursesInsideContent - ShowChapterVideoList（Target SpecificChapter）"""
        from core.engine.course_selector import CourseSelector
        selector = CourseSelector()

        # Get AllChapterData
        all_chapters = selector.get_chapters(subject, grade, term)
        if not all_chapters:
            self.video_player.info_label.configure(
                text=f"⚠️ {grade}{term} NoAvailableCourse"
            )
            return

        # ClearLessonList
        for widget in self.lesson_listbox.winfo_children():
            widget.destroy()

        # Such AsResultPointDefineChapter，OnlyShowTheChapter
        if chapter_label:
            # FromDropdownLabelInExtractChapterName（Format："ThXChapter-xxx (NSection)"）
            ch_title = chapter_label.split(" (")[0]
            chapters = [ch for ch in all_chapters if ch["title"] == ch_title]
            if not chapters:
                chapters = [ch for ch in all_chapters if ch["number"] in ch_title]
        else:
            chapters = all_chapters

        # MoreNewPlayInfo
        self.video_player.info_label.configure(
            text=f"📚 {subject} {grade}{term}\n{chapters[0]['title'] if chapters else ''}"
        )

        # ShowChapterAndLessonList
        for idx, ch in enumerate(chapters):
            ch_title = ch["title"]
            videos = ch.get("videos", [])

            # ChapterTitle
            ch_label = ctk.CTkLabel(
                self.lesson_listbox,
                text=f"{'Th' + ch_title if not ch_title.startswith('Th') else ch_title}",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#2c3e50",
            )
            ch_label.pack(fill="x", padx=8, pady=(8, 4))

            # LessonByButton
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

        # MoreNewProgressShow
        progress = self.tracker.get_dashboard()
        self.progress_label.configure(
            text=f"Total {progress['total_lessons']} Lesson，AlreadyDone {progress['completed']} Lesson"
        )

    def _load_recent(self):
        """LoadRecentStudy"""
        pass  # TODO: FromDataLibraryLoadRecentRecord

    def _refresh_data(self):
        """RefreshData"""
        self.net_status.configure(text="🔄 RefreshIn...")
        self.after(500, lambda: self.net_status.configure(text="🌐 AlreadyConnect"))

    def run(self):
        """RunShouldUse"""
        self.mainloop()


def main():
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
