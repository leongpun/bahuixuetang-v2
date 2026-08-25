"""
PDF ViewingComponent - EmbeddedPDFReading
"""
import customtkinter as ctk
import os
import subprocess
import sys


class PDFViewer(ctk.CTkFrame):
    """PDF ViewingComponent"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.current_pdf = None
        self._build_ui()

    def _build_ui(self):
        # PDFShowArea
        self.pdf_area = ctk.CTkFrame(self, fg_color="#f0f0f0", corner_radius=8)
        self.pdf_area.pack(fill="both", expand=True, padx=10, pady=10)

        self.info_label = ctk.CTkLabel(
            self.pdf_area,
            text="📄 ClickLeftCourseInPDFTextbook",
            font=("Microsoft YaHei", 12),
            text_color="#888888",
        )
        self.info_label.place(relx=0.5, rely=0.5, anchor="center")

        # ControlByButton
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(btn_frame, text="📂 OpenPDF", command=self._open_dialog,
                      width=100, height=30).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🔄 Refresh", command=self._refresh,
                      width=100, height=30).pack(side="left", padx=5)

    def open(self, pdf_path):
        """OpenPDFFile（Cross-platform）"""
        import platform
        if not os.path.exists(pdf_path):
            self._show_error("PDFFileNot found")
            return

        self.current_pdf = pdf_path
        # Use System DefaultPDFReading
        import platform
        system = platform.system()
        if system == "Darwin":  # macOS
            subprocess.Popen(["open", pdf_path])
        else:  # LinuxAndOther
            subprocess.Popen(["xdg-open", pdf_path])
        self.info_label.configure(text=f"📄 AlreadyOpen: {os.path.basename(pdf_path)}")

    def _open_dialog(self):
        """OpenFileSelectDialog"""
        from tkinter import filedialog
        path = filedialog.askopenfilename(
            title="SelectPDFFile",
            filetypes=[("PDFFile", "*.pdf"), ("All Files", "*.*")],
        )
        if path:
            self.open(path)

    def _refresh(self):
        self.info_label.configure(text="📄 ClickLeftCourseInPDFTextbook")
        self.current_pdf = None

    def _show_error(self, msg):
        self.info_label.configure(text=f"❌ {msg}", text_color="#e74c3c")
