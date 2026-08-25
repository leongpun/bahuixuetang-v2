"""
CourseSelectComponent - FilterTypeDropdownList
Fix：UseMoreLevelDropdownBoxAlternativeTreeview，AvoidWindowBlock QuestionQuestion
"""
import customtkinter as ctk
from config.courses import SUBJECTS, TERMS
from core.engine.course_selector import CourseSelector


class CourseSelectorWidget(ctk.CTkFrame):
    """FilterTypeCourseSelect - MoreLevelDropdownBox"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.selector = CourseSelector()
        self.selected_subject = None
        self.selected_grade = None
        self.selected_term = None
        self.selected_chapter = None
        self.on_select_callback = None
        self._build_ui()

    def _build_ui(self):
        """Build UI - Four-level DropdownFilter"""
        # Title
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", padx=10, pady=(10, 5))
        ctk.CTkLabel(
            title_frame,
            text="📚 CourseSelect",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")

        # ThOneLevel：SubjectDropdown
        subject_frame = ctk.CTkFrame(self, fg_color="transparent")
        subject_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(subject_frame, text="Subject：", width=50).pack(side="left")
        self.subject_var = ctk.StringVar(value="")
        self.subject_combo = ctk.CTkOptionMenu(
            subject_frame,
            variable=self.subject_var,
            values=["-- Please select --"] + [SUBJECTS[k]["name"] for k in SUBJECTS],
            width=120,
            height=28,
            command=self._on_subject_change
        )
        self.subject_combo.pack(side="left", padx=5)

        # Second Level：GradeDropdown
        grade_frame = ctk.CTkFrame(self, fg_color="transparent")
        grade_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(grade_frame, text="Grade：", width=50).pack(side="left")
        self.grade_var = ctk.StringVar(value="")
        self.grade_combo = ctk.CTkOptionMenu(
            grade_frame,
            variable=self.grade_var,
            values=["-- Please select --"],
            width=100,
            height=28,
            state="disabled",
            command=self._on_grade_change
        )
        self.grade_combo.pack(side="left", padx=5)

        # ThThreeLevel：TermDropdown
        term_frame = ctk.CTkFrame(self, fg_color="transparent")
        term_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(term_frame, text="Term：", width=50).pack(side="left")
        self.term_var = ctk.StringVar(value="")
        self.term_combo = ctk.CTkOptionMenu(
            term_frame,
            variable=self.term_var,
            values=["-- Please select --"],
            width=100,
            height=28,
            state="disabled",
            command=self._on_term_change
        )
        self.term_combo.pack(side="left", padx=5)

        # Fourth Level：ChapterDropdown
        chapter_frame = ctk.CTkFrame(self, fg_color="transparent")
        chapter_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(chapter_frame, text="Chapter：", width=50).pack(side="left")
        self.chapter_var = ctk.StringVar(value="")
        self.chapter_combo = ctk.CTkOptionMenu(
            chapter_frame,
            variable=self.chapter_var,
            values=["-- Please select --"],
            width=200,
            height=28,
            state="disabled",
            command=self._on_chapter_change
        )
        self.chapter_combo.pack(side="left", padx=5)

        # StatisticsInfo
        self.info_label = ctk.CTkLabel(
            self,
            text="Please selectSubject、Grade、TermAndChapterStartStudy",
            font=ctk.CTkFont(size=11),
            text_color="#7f8c8d"
        )
        self.info_label.pack(padx=10, pady=(5, 10))

    def _on_subject_change(self, subject_name):
        """SubjectOn ChangeMoreNewGradeOption"""
        if subject_name == "-- Please select --":
            self._reset_grades()
            return
        
        # FoundCorrespondingcode
        self.selected_subject = None
        for code, info in SUBJECTS.items():
            if info["name"] == subject_name:
                self.selected_subject = code
                break
        
        if not self.selected_subject:
            return
        
        # MoreNewGradeDropdown
        grades = SUBJECTS[self.selected_subject]["grades"]
        self.grade_combo.configure(values=["-- Please select --"] + grades, state="normal")
        self.grade_var.set("-- Please select --")
        # Note：NotClearGrade，RetainOptionProvideUserSelect

    def _on_grade_change(self, grade):
        """GradeOn ChangeMoreNewTermOption"""
        if grade == "-- Please select --":
            self._reset_terms()
            return
        
        self.selected_grade = grade
        
        # MoreNewTermDropdown
        self.term_combo.configure(values=["-- Please select --"] + TERMS, state="normal")
        self.term_var.set("-- Please select --")
        # Note：NotClearTerm，RetainOptionProvideUserSelect

    def _on_term_change(self, term):
        """TermOn ChangeLoadChapterOption"""
        if term == "-- Please select --":
            self._reset_chapters()
            return
        
        self.selected_term = term
        
        if not self.selected_subject or not self.selected_grade:
            return
        
        # FromVideoExtract RealChapter
        chapters = self.selector.get_chapters(
            self.selected_subject, self.selected_grade, term
        )
        
        if not chapters:
            self.chapter_combo.configure(
                values=["(NoAvailableCourse)"], state="disabled"
            )
            self.info_label.configure(text=f"⚠️ {self.selected_grade}{term} NoAvailableVideoResource")
            return
        
        # BuildChapterOption
        chapter_labels = []
        for ch in chapters:
            video_count = len(ch["videos"])
            label = f"{ch['title']} ({video_count}Section)"
            chapter_labels.append(label)
        
        self.chapter_combo.configure(
            values=["-- Please select --"] + chapter_labels,
            state="normal"
        )
        self.chapter_var.set("-- Please select --")
        # Note：NotClearChapter，RetainOptionProvideUserSelect
        
        # MoreNewStatistics
        total_videos = sum(len(ch["videos"]) for ch in chapters)
        total_chapters = len(chapters)
        self.info_label.configure(
            text=f"📊 {self.selected_grade}{term}：{total_chapters}ItemChapter，Total{total_videos}SectionVideo"
        )

    def _on_chapter_change(self, chapter_label):
        """ChapterTrigger Callback on Change"""
        if chapter_label == "-- Please select --" or chapter_label == "(NoAvailableCourse)":
            return
        
        self.selected_chapter = chapter_label
        if self.on_select_callback:
            # Pass Original Label（Used ForFilter），CallbackInExplanation
            self.on_select_callback({
                "subject": self.selected_subject,
                "grade": self.selected_grade,
                "term": self.selected_term,
                "chapter": chapter_label  # Pass Complete Label "ThXChapter-xxx (NSection)"
            })

    def _reset_grades(self):
        """ResetGradeAnd Below"""
        self.grade_combo.configure(values=["-- Please select --"], state="disabled")
        self.grade_var.set("-- Please select --")
        self.term_combo.configure(values=["-- Please select --"], state="disabled")
        self.term_var.set("-- Please select --")
        self.chapter_combo.configure(values=["-- Please select --"], state="disabled")
        self.chapter_var.set("-- Please select --")
        self.selected_grade = None
        self.selected_term = None
        self.selected_chapter = None

    def _reset_terms(self):
        """ResetTermAnd Below"""
        self.term_combo.configure(values=["-- Please select --"], state="disabled")
        self.term_var.set("-- Please select --")
        self.chapter_combo.configure(values=["-- Please select --"], state="disabled")
        self.chapter_var.set("-- Please select --")
        self.selected_term = None
        self.selected_chapter = None

    def _reset_chapters(self):
        """ResetChapter"""
        self.chapter_combo.configure(values=["-- Please select --"], state="disabled")
        self.chapter_var.set("-- Please select --")
        self.selected_chapter = None

    def set_callback(self, callback):
        """SettingsSelectCallback"""
        self.on_select_callback = callback
