"""
课程选择器组件 - 过滤式下拉列表
修复：使用多级下拉框替代Treeview，避免窗口遮挡问题
"""
import customtkinter as ctk
from config.courses import SUBJECTS, TERMS
from core.engine.course_selector import CourseSelector


class CourseSelectorWidget(ctk.CTkFrame):
    """过滤式课程选择器 - 多级下拉框"""

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
        """构建UI - 四级下拉筛选"""
        # 标题
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", padx=10, pady=(10, 5))
        ctk.CTkLabel(
            title_frame,
            text="📚 课程选择",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")

        # 第一级：学科下拉
        subject_frame = ctk.CTkFrame(self, fg_color="transparent")
        subject_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(subject_frame, text="学科：", width=50).pack(side="left")
        self.subject_var = ctk.StringVar(value="")
        self.subject_combo = ctk.CTkOptionMenu(
            subject_frame,
            variable=self.subject_var,
            values=["-- 请选择 --"] + [SUBJECTS[k]["name"] for k in SUBJECTS],
            width=120,
            height=28,
            command=self._on_subject_change
        )
        self.subject_combo.pack(side="left", padx=5)

        # 第二级：年级下拉
        grade_frame = ctk.CTkFrame(self, fg_color="transparent")
        grade_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(grade_frame, text="年级：", width=50).pack(side="left")
        self.grade_var = ctk.StringVar(value="")
        self.grade_combo = ctk.CTkOptionMenu(
            grade_frame,
            variable=self.grade_var,
            values=["-- 请选择 --"],
            width=100,
            height=28,
            state="disabled",
            command=self._on_grade_change
        )
        self.grade_combo.pack(side="left", padx=5)

        # 第三级：学期下拉
        term_frame = ctk.CTkFrame(self, fg_color="transparent")
        term_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(term_frame, text="学期：", width=50).pack(side="left")
        self.term_var = ctk.StringVar(value="")
        self.term_combo = ctk.CTkOptionMenu(
            term_frame,
            variable=self.term_var,
            values=["-- 请选择 --"],
            width=100,
            height=28,
            state="disabled",
            command=self._on_term_change
        )
        self.term_combo.pack(side="left", padx=5)

        # 第四级：章节下拉
        chapter_frame = ctk.CTkFrame(self, fg_color="transparent")
        chapter_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(chapter_frame, text="章节：", width=50).pack(side="left")
        self.chapter_var = ctk.StringVar(value="")
        self.chapter_combo = ctk.CTkOptionMenu(
            chapter_frame,
            variable=self.chapter_var,
            values=["-- 请选择 --"],
            width=200,
            height=28,
            state="disabled",
            command=self._on_chapter_change
        )
        self.chapter_combo.pack(side="left", padx=5)

        # 统计信息
        self.info_label = ctk.CTkLabel(
            self,
            text="请选择学科、年级、学期和章节开始学习",
            font=ctk.CTkFont(size=11),
            text_color="#7f8c8d"
        )
        self.info_label.pack(padx=10, pady=(5, 10))

    def _on_subject_change(self, subject_name):
        """学科变化时更新年级选项"""
        if subject_name == "-- 请选择 --":
            self._reset_grades()
            return
        
        # 找到对应的code
        self.selected_subject = None
        for code, info in SUBJECTS.items():
            if info["name"] == subject_name:
                self.selected_subject = code
                break
        
        if not self.selected_subject:
            return
        
        # 更新年级下拉
        grades = SUBJECTS[self.selected_subject]["grades"]
        self.grade_combo.configure(values=["-- 请选择 --"] + grades, state="normal")
        self.grade_var.set("-- 请选择 --")
        # 注意：不清除年级，保留选项供用户选择

    def _on_grade_change(self, grade):
        """年级变化时更新学期选项"""
        if grade == "-- 请选择 --":
            self._reset_terms()
            return
        
        self.selected_grade = grade
        
        # 更新学期下拉
        self.term_combo.configure(values=["-- 请选择 --"] + TERMS, state="normal")
        self.term_var.set("-- 请选择 --")
        # 注意：不清除学期，保留选项供用户选择

    def _on_term_change(self, term):
        """学期变化时加载章节选项"""
        if term == "-- 请选择 --":
            self._reset_chapters()
            return
        
        self.selected_term = term
        
        if not self.selected_subject or not self.selected_grade:
            return
        
        # 从视频提取真实章节
        chapters = self.selector.get_chapters(
            self.selected_subject, self.selected_grade, term
        )
        
        if not chapters:
            self.chapter_combo.configure(
                values=["(暂无可用课程)"], state="disabled"
            )
            self.info_label.configure(text=f"⚠️ {self.selected_grade}{term} 暂无可用视频资源")
            return
        
        # 构建章节选项
        chapter_labels = []
        for ch in chapters:
            video_count = len(ch["videos"])
            label = f"{ch['title']} ({video_count}节)"
            chapter_labels.append(label)
        
        self.chapter_combo.configure(
            values=["-- 请选择 --"] + chapter_labels,
            state="normal"
        )
        self.chapter_var.set("-- 请选择 --")
        # 注意：不清除章节，保留选项供用户选择
        
        # 更新统计
        total_videos = sum(len(ch["videos"]) for ch in chapters)
        total_chapters = len(chapters)
        self.info_label.configure(
            text=f"📊 {self.selected_grade}{term}：{total_chapters}个章节，共{total_videos}节视频"
        )

    def _on_chapter_change(self, chapter_label):
        """章节变化时触发回调"""
        if chapter_label == "-- 请选择 --" or chapter_label == "(暂无可用课程)":
            return
        
        self.selected_chapter = chapter_label
        if self.on_select_callback:
            # 传递原始标签（用于筛选），回调中解析
            self.on_select_callback({
                "subject": self.selected_subject,
                "grade": self.selected_grade,
                "term": self.selected_term,
                "chapter": chapter_label  # 传递完整标签 "第X章-xxx (N节)"
            })

    def _reset_grades(self):
        """重置年级及以下"""
        self.grade_combo.configure(values=["-- 请选择 --"], state="disabled")
        self.grade_var.set("-- 请选择 --")
        self.term_combo.configure(values=["-- 请选择 --"], state="disabled")
        self.term_var.set("-- 请选择 --")
        self.chapter_combo.configure(values=["-- 请选择 --"], state="disabled")
        self.chapter_var.set("-- 请选择 --")
        self.selected_grade = None
        self.selected_term = None
        self.selected_chapter = None

    def _reset_terms(self):
        """重置学期及以下"""
        self.term_combo.configure(values=["-- 请选择 --"], state="disabled")
        self.term_var.set("-- 请选择 --")
        self.chapter_combo.configure(values=["-- 请选择 --"], state="disabled")
        self.chapter_var.set("-- 请选择 --")
        self.selected_term = None
        self.selected_chapter = None

    def _reset_chapters(self):
        """重置章节"""
        self.chapter_combo.configure(values=["-- 请选择 --"], state="disabled")
        self.chapter_var.set("-- 请选择 --")
        self.selected_chapter = None

    def set_callback(self, callback):
        """设置选择回调"""
        self.on_select_callback = callback
