"""
课程树组件 - 显示学科/年级/学期/章节的树形结构
"""
import customtkinter as ctk
from tkinter import ttk
from config.courses import SUBJECTS, TERMS
from core.engine.course_selector import CourseSelector


class CourseTree(ctk.CTkFrame):
    """课程选择树组件"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.selector = CourseSelector()
        self.selected_item = None
        self._build_ui()

    def _build_ui(self):
        # 搜索框
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=10, pady=(10, 5))
        ctk.CTkLabel(search_frame, text="🔍", width=30).pack(side="left")
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="搜索课程...",
            height=30,
            corner_radius=15,
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.search_entry.bind("<Return>", self._on_search)

        # 树形列表
        tree_frame = ctk.CTkScrollableFrame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(tree_frame, columns=("code", "name", "status"), show="tree headings")
        self.tree.column("#0", width=200)
        self.tree.column("code", width=60)
        self.tree.column("name", width=120)
        self.tree.column("status", width=60)
        self.tree.heading("#0", text="课程")
        self.tree.heading("code", text="代码")
        self.tree.heading("name", text="名称")
        self.tree.heading("status", text="状态")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        self._populate_tree()

    def _populate_tree(self):
        """填充课程树"""
        for code, info in SUBJECTS.items():
            # 学科根节点
            self.tree.insert("", "end", iid=code, text=f"{info['name']} [{info['edition']}]",
                           values=(code, info["name"], self._get_status(code)))
            # 年级子节点
            for grade in info["grades"]:
                self.tree.insert(code, "end", iid=f"{code}_{grade}",
                               text=f"  📚 {grade}", values=(code, grade, "-"))
                # 学期子节点
                for term in TERMS:
                    count = self._count_lessons(code, grade, term)
                    self.tree.insert(f"{code}_{grade}", "end",
                                   iid=f"{code}_{grade}_{term}",
                                   text=f"    📅 {term} ({count}课时)",
                                   values=(code, term, "✓" if count > 0 else "✗"))

    def _count_lessons(self, code, grade, term):
        """统计该学期可用课时数"""
        try:
            lessons = self.selector.get_available_lessons(code, grade, term)
            return sum(len(l["videos"]) for l in lessons)
        except:
            return 0

    def _get_status(self, code):
        """获取学科状态"""
        count = sum(self._count_lessons(code, g, t) for g in SUBJECTS[code]["grades"] for t in TERMS)
        return "✓" if count > 0 else "✗"

    def _on_select(self, event):
        """处理选择事件"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.selected_item = item["values"]
            # 触发回调
            if hasattr(self, "on_select_callback"):
                self.on_select_callback(item)

    def _on_search(self, event=None):
        """搜索课程"""
        keyword = self.search_entry.get().lower()
        # 清空并重新填充
        for item in self.tree.get_children():
            self.tree.delete(item)
        # 只显示匹配的
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
                                       text=f"    📅 {term} ({count}课时)",
                                       values=(code, term, "✓" if count > 0 else "✗"))

    def set_callback(self, callback):
        """设置选择回调"""
        self.on_select_callback = callback
