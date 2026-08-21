"""
PDF查看组件 - 内嵌PDF阅读
"""
import customtkinter as ctk
import os
import subprocess
import sys


class PDFViewer(ctk.CTkFrame):
    """PDF查看器组件"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.current_pdf = None
        self._build_ui()

    def _build_ui(self):
        # PDF显示区域
        self.pdf_area = ctk.CTkFrame(self, fg_color="#f0f0f0", corner_radius=8)
        self.pdf_area.pack(fill="both", expand=True, padx=10, pady=10)

        self.info_label = ctk.CTkLabel(
            self.pdf_area,
            text="📄 点击左侧课程中的PDF课本",
            font=("Microsoft YaHei", 12),
            text_color="#888888",
        )
        self.info_label.place(relx=0.5, rely=0.5, anchor="center")

        # 控制按钮
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(btn_frame, text="📂 打开PDF", command=self._open_dialog,
                      width=100, height=30).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🔄 刷新", command=self._refresh,
                      width=100, height=30).pack(side="left", padx=5)

    def open(self, pdf_path):
        """打开PDF文件（跨平台）"""
        import platform
        if not os.path.exists(pdf_path):
            self._show_error("PDF文件不存在")
            return

        self.current_pdf = pdf_path
        # 使用系统默认PDF阅读器
        import platform
        system = platform.system()
        if system == "Darwin":  # macOS
            subprocess.Popen(["open", pdf_path])
        else:  # Linux和其他
            subprocess.Popen(["xdg-open", pdf_path])
        self.info_label.configure(text=f"📄 已打开: {os.path.basename(pdf_path)}")

    def _open_dialog(self):
        """打开文件选择对话框"""
        from tkinter import filedialog
        path = filedialog.askopenfilename(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")],
        )
        if path:
            self.open(path)

    def _refresh(self):
        self.info_label.configure(text="📄 点击左侧课程中的PDF课本")
        self.current_pdf = None

    def _show_error(self, msg):
        self.info_label.configure(text=f"❌ {msg}", text_color="#e74c3c")
