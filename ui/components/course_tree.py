"""
CourseTreeComponent - ShowSubject/Grade/Term/ChapterTreeStructure
"""
import customtkinter as ctk
from tkinter import ttk
from config.courses import SUBJECTS, TERMS
from core.engine.course_selector import CourseSelector


class CourseTree(ctk.CTkFrame):
    """CourseSelectTreeComponent"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.selector = CourseSelector()
        self.selected_item = None
        self._build_ui()

    def _build_ui(self):
        # SearchBox
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=10, pady=(10, 5))
        ctk.CTkLabel(search_frame, text="🔍", width=30).pack(side="left")
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="SearchCourse...",
            height=30,
            corner_radius=15,
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.search_entry.bind("<Return>", self._on_search)

        # TreeList
        tree_frame = ctk.CTkScrollableFrame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(tree_frame, columns=("code", "name", "status"), show="tree headings")
        self.tree.column("#0", width=200)
        self.tree.column("code", width=60)
        self.tree.column("name", width=120)
        self.tree.column("status", width=60)
        self.tree.heading("#0", text="Course")
        self.tree.heading("code", text="Code")
        self.tree.heading("name", text="Name")
        self.tree.heading("status", text="Status")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        self._populate_tree()

    def _populate_tree(self):
        """FillCourseTree"""
        for code, info in SUBJECTS.items():
            # SubjectRootSectionPoint
            self.tree.insert("", "end", iid=code, text=f"{info['name']} [{info['edition']}]",
                           values=(code, info["name"], self._get_status(code)))
            # GradeChildSectionPoint
            for grade in info["grades"]:
                self.tree.insert(code, "end", iid=f"{code}_{grade}",
                               text=f"  📚 {grade}", values=(code, grade, "-"))
                # TermChildSectionPoint
                for term in TERMS:
                    count = self._count_lessons(code, grade, term)
                    self.tree.insert(f"{code}_{grade}", "end",
                                   iid=f"{code}_{grade}_{term}",
                                   text=f"    📅 {term} ({count}Lesson)",
                                   values=(code, term, "✓" if count > 0 else "✗"))

    def _count_lessons(self, code, grade, term):
        """StatisticsTheTermAvailableLessonCount"""
        try:
            lessons = self.selector.get_available_lessons(code, grade, term)
            return sum(len(l["videos"]) for l in lessons)
        except:
            return 0

    def _get_status(self, code):
        """GetSubjectStatus"""
        count = sum(self._count_lessons(code, g, t) for g in SUBJECTS[code]["grades"] for t in TERMS)
        return "✓" if count > 0 else "✗"

    def _on_select(self, event):
        """ProcessSelectEvent"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.selected_item = item["values"]
            # Trigger Callback
            if hasattr(self, "on_select_callback"):
                self.on_select_callback(item)

    def _on_search(self, event=None):
        """SearchCourse"""
        keyword = self.search_entry.get().lower()
        # Clear andAgainNewFill
        for item in self.tree.get_children():
            self.tree.delete(item)
        # OnlyShowMatching
        for code, info in SUBJECTS.items():
            if keyword in info["name"].lower() or keyword in code.lower():
                self.tree.insert("", "end", iid=code, text=f"{info['name']} [{info['edition']}]",
                               values=(code, info["name"], self._get_status(code)))
                for grade in info["grades"]:
                    self.tree.insert(code, "end", iid=f"{code}_{grade}",
                                   text=f"  📚 {grade}", values=(code, grade, "-"))
                    for term in TERMS:
                        count = self._count_lessons(code, grade, term)
                        self.tree.insert(f"{code}_{grade}", "end",
                                       iid=f"{code}_{grade}_{term}",
                                       text=f"    📅 {term} ({count}Lesson)",
                                       values=(code, term, "✓" if count > 0 else "✗"))

    def set_callback(self, callback):
        """SettingsSelectCallback"""
        self.on_select_callback = callback
