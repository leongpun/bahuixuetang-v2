"""SettingsPagePage - ResourcePathConfigure + AIConfigure"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from config.settings import load_settings, save_settings
from core.api.local_scanner import LocalResourceScanner


class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.settings = load_settings()
        self.scanner = LocalResourceScanner()
        
        # ResourcePathPartPart
        path_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="white")
        path_frame.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(path_frame, text="📁 Local ResourcesPath", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        self.path_list = ctk.CTkOptionMenu(path_frame, values=[], width=300, height=25)
        self.path_list.pack(padx=10, pady=5)
        
        btn_frame = ctk.CTkFrame(path_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(btn_frame, text="➕ Add", height=25, command=self._add_path, fg_color="#3498db").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Delete", height=25, command=self._remove_path, fg_color="#e74c3c").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🔄 Refresh", height=25, command=self._refresh, fg_color="#9b59b6").pack(side="right", padx=5)
        
        self.refresh_status = ctk.CTkLabel(path_frame, text="")
        self.refresh_status.pack(padx=10, pady=5)
        
        # AIConfigurePartPart
        ai_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="white")
        ai_frame.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(ai_frame, text="🤖 AIConfigure（PleaseSelfFill）", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        # APISecret Key
        key_frame = ctk.CTkFrame(ai_frame, fg_color="transparent")
        key_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(key_frame, text="API Key:", width=80, anchor="w").pack(side="left")
        self.ai_key_var = ctk.StringVar(value=self.settings.get("ai_api_key", ""))
        ctk.CTkEntry(key_frame, textvariable=self.ai_key_var, width=300, height=25, placeholder_text="InputAPISecret Key...").pack(side="left", padx=10)
        
        # APIEndpointPoint
        endpoint_frame = ctk.CTkFrame(ai_frame, fg_color="transparent")
        endpoint_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(endpoint_frame, text="APIEndpointPoint:", width=80, anchor="w").pack(side="left")
        self.ai_endpoint_var = ctk.StringVar(value=self.settings.get("ai_endpoint", ""))
        ctk.CTkEntry(endpoint_frame, textvariable=self.ai_endpoint_var, width=300, height=25, placeholder_text="https://api.deepseek.com/v1").pack(side="left", padx=10)
        
        # ModelName
        model_frame = ctk.CTkFrame(ai_frame, fg_color="transparent")
        model_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(model_frame, text="ModelName:", width=80, anchor="w").pack(side="left")
        self.ai_model_var = ctk.StringVar(value=self.settings.get("ai_model", "deepseek-chat"))
        ctk.CTkEntry(model_frame, textvariable=self.ai_model_var, width=300, height=25, placeholder_text="deepseek-chat / qwen-turbo").pack(side="left", padx=10)
        
        ctk.CTkLabel(ai_frame, text="💡 SupportAnyAISubmitProvideProvider，FillServiceProviderSubmitProvideConfigureCan", font=ctk.CTkFont(size=9), text_color="#95a5a6").pack(anchor="w", padx=10, pady=5)
        
        # SaveByButton
        save_btn = ctk.CTkButton(self, text="💾 SaveSettings", height=35, command=self._save, 
                                  fg_color="#27ae60", hover_color="#219653")
        save_btn.pack(pady=15)
        
        # Question BankImportPartPart
        quiz_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="white")
        quiz_frame.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(quiz_frame, text="📚 Question BankImport", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        ctk.CTkLabel(quiz_frame, text="SupportFormat：JSON、Excel、Word(.docx)、PDF", 
                     font=ctk.CTkFont(size=9), text_color="#7f8c8d").pack(anchor="w", padx=10)
        
        btn_row = ctk.CTkFrame(quiz_frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(btn_row, text="📂 SelectFileImport", height=30, command=self._import_quiz,
                      fg_color="#3498db").pack(side="left", padx=5)
        
        self.quiz_status = ctk.CTkLabel(quiz_frame, text="", font=ctk.CTkFont(size=10))
        self.quiz_status.pack(pady=5)
        
        self._load_paths()
    
    def _load_paths(self):
        paths = self.settings.get("external_resource_paths", [])
        self.path_list.configure(values=paths if paths else ["Not yetConfigure"])
    
    def _add_path(self):
        path = filedialog.askdirectory()
        if path:
            paths = self.settings.get("external_resource_paths", [])
            if path not in paths:
                paths.append(path)
                self.settings["external_resource_paths"] = paths
                self._load_paths()
                messagebox.showinfo("Tip", f"AlreadyAdd: {path}")
    
    def _remove_path(self):
        selected = self.path_list.get()
        if selected and selected != "Not yetConfigure":
            paths = self.settings.get("external_resource_paths", [])
            if selected in paths:
                paths.remove(selected)
                self.settings["external_resource_paths"] = paths
                self._load_paths()
                messagebox.showinfo("Tip", f"AlreadyDelete: {selected}")
    
    def _refresh(self):
        self.refresh_status.configure(text="🔄 ScanIn...", text_color="#3498db")
        paths = self.settings.get("external_resource_paths", [])
        self.scanner.set_search_paths(paths)
        
        def scan():
            result = self.scanner.scan()
            status = f"✅ {result['total_videos']}Video, {result['total_pdfs']}PDF"
            self.refresh_status.configure(text=status, text_color="#27ae60")
        
        self.after(500, scan)
    
    def _save(self):
        self.settings["ai_api_key"] = self.ai_key_var.get()
        self.settings["ai_endpoint"] = self.ai_endpoint_var.get()
        self.settings["ai_model"] = self.ai_model_var.get()
        save_settings(self.settings)
        messagebox.showinfo("Success", "SettingsAlreadySave！")
    
    def _import_quiz(self):
        """ImportQuestion BankFile"""
        filepath = filedialog.askopenfilename(
            title="SelectQuestion BankFile",
            filetypes=[
                ("JSONFile", "*.json"),
                ("ExcelFile", "*.xlsx *.xls"),
                ("WordFile", "*.docx"),
                ("PDFFile", "*.pdf"),
                ("All Files", "*.*")
            ]
        )
        if not filepath:
            return
        
        from core.storage.quiz_importer import QuizImporter
        importer = QuizImporter()
        result = importer.import_file(filepath)
        
        if result["success"]:
            count = result["count"]
            self.quiz_status.configure(text=f"✅ SuccessImport {count} Questions", text_color="#27ae60")
            messagebox.showinfo("Success", f"AlreadyImport {count} Questions！")
        else:
            error = result.get("error", "Not yetKnowledgeError")
            self.quiz_status.configure(text=f"❌ {error}", text_color="#e74c3c")
            messagebox.showerror("ImportFailed", error)
