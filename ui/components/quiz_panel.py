"""
答题练习面板 - 选择题展示与交互
"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from typing import List, Dict, Optional
import random
import ast
import re


class QuizPanel(ctk.CTkFrame):
    """答题练习面板"""

    def __init__(self, parent, quiz_manager=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.quiz_manager = quiz_manager
        self.current_questions: List[Dict] = []
        self.current_index = 0
        self.user_answers: Dict[str, str] = {}
        self.is_review_mode = False  # 复习模式（显示错题）
        
        self._build_ui()

    def _build_ui(self):
        """构建界面"""
        # 顶部控制栏
        self._build_toolbar()
        
        # 题目区域
        self._build_question_area()
        
        # 导航按钮
        self._build_navigation()
        
        # 结果统计区域（答题后显示）
        self._build_result_area()

    def _build_toolbar(self):
        """顶部工具栏"""
        toolbar = ctk.CTkFrame(self, fg_color="#2c3e50", height=50)
        toolbar.pack(fill="x", padx=0, pady=(0, 10))
        toolbar.pack_propagate(False)
        
        # 标题
        ctk.CTkLabel(
            toolbar,
            text="📝 答题练习",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        ).pack(side="left", padx=15, pady=10)
        
        # 模式切换
        self.mode_var = ctk.StringVar(value="random")
        mode_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        mode_frame.pack(side="right", padx=10)
        
        ctk.CTkOptionMenu(
            mode_frame,
            values=["随机抽题", "按章节练习", "错题复习"],
            variable=self.mode_var,
            width=120,
            height=30,
            fg_color="#34495e",
            button_hover_color="#3d566e",
            text_color="white"
        ).pack(side="left", padx=5)
        
        # 开始按钮
        ctk.CTkButton(
            toolbar,
            text="▶️ 开始练习",
            width=100,
            height=30,
            command=self._start_quiz,
            fg_color="#27ae60",
            hover_color="#219a52"
        ).pack(side="right", padx=10)
        
        # 导入按钮
        ctk.CTkButton(
            toolbar,
            text="📂 导入题库",
            width=100,
            height=30,
            command=self._import_quiz,
            fg_color="#8e44ad",
            hover_color="#7d3c98"
        ).pack(side="right", padx=5)

    def _build_question_area(self):
        """题目显示区域"""
        question_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        question_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # 题号和进度
        progress_frame = ctk.CTkFrame(question_frame, fg_color="transparent")
        progress_frame.pack(fill="x", padx=15, pady=10)
        
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="请选择练习模式开始答题",
            font=ctk.CTkFont(size=12),
            text_color="#7f8c8d"
        )
        self.progress_label.pack(side="left")
        
        # 题目内容
        self.question_text = ctk.CTkLabel(
            question_frame,
            text="📋 暂无题目，请先导入题库或选择练习模式",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#2c3e50",
            wraplength=700,
            justify="left"
        )
        self.question_text.pack(fill="x", padx=15, pady=10)
        
        # 选项区域
        self.options_frame = ctk.CTkFrame(question_frame, fg_color="transparent")
        self.options_frame.pack(fill="x", padx=15, pady=10)
        
        self.option_vars = []
        self.option_buttons = []
        for i in range(4):
            var = ctk.StringVar(value="")
            self.option_vars.append(var)
            btn = ctk.CTkRadioButton(
                self.options_frame,
                text=f"{chr(65+i)}. 选项内容",
                variable=var,
                value=str(chr(65+i)),
                font=ctk.CTkFont(size=13),
                command=self._on_answer_select
            )
            btn.pack(anchor="w", pady=5)
            self.option_buttons.append(btn)
        
        # 填空题输入框（初始隐藏）
        self.fill_blank_frame = ctk.CTkFrame(question_frame, fg_color="transparent")
        self.fill_blank_frame.pack(fill="x", padx=15, pady=10)
        self.fill_blank_frame.pack_forget()
        
        ctk.CTkLabel(
            self.fill_blank_frame,
            text="✍️ 请输入答案:",
            font=ctk.CTkFont(size=13),
            text_color="#2c3e50"
        ).pack(anchor="w")
        
        self.fill_blank_entry = ctk.CTkEntry(
            self.fill_blank_frame,
            width=300,
            height=35,
            font=ctk.CTkFont(size=13)
        )
        self.fill_blank_entry.pack(pady=5)
        self.fill_blank_entry.bind('<Return>', lambda e: self._submit_answer())
        
        # 解析区域（初始隐藏）
        self.explanation_frame = ctk.CTkFrame(
            question_frame,
            fg_color="#f8f9fa",
            corner_radius=8
        )
        self.explanation_frame.pack(fill="x", padx=15, pady=10)
        self.explanation_frame.pack_forget()
        
        ctk.CTkLabel(
            self.explanation_frame,
            text="📖 解析",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#2c3e50"
        ).pack(anchor="w", padx=10, pady=5)
        
        self.explanation_text = ctk.CTkLabel(
            self.explanation_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#7f8c8d",
            wraplength=700,
            justify="left"
        )
        self.explanation_text.pack(fill="x", padx=10, pady=5)
        
        # 提交按钮
        submit_btn = ctk.CTkButton(
            question_frame,
            text="✅ 提交答案",
            width=120,
            height=35,
            command=self._submit_answer,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        submit_btn.pack(pady=10)
        self.submit_btn = submit_btn

    def _build_navigation(self):
        """底部导航按钮"""
        nav_frame = ctk.CTkFrame(self, fg_color="#ecf0f1", height=50)
        nav_frame.pack(fill="x", side="bottom", padx=10, pady=(0, 10))
        nav_frame.pack_propagate(False)
        
        self.prev_btn = ctk.CTkButton(
            nav_frame,
            text="⬅️ 上一题",
            width=100,
            height=35,
            command=self._prev_question,
            state="disabled",
            fg_color="#95a5a6"
        )
        self.prev_btn.pack(side="left", padx=15)
        
        self.next_btn = ctk.CTkButton(
            nav_frame,
            text="➡️ 下一题",
            width=100,
            height=35,
            command=self._next_question,
            state="disabled",
            fg_color="#95a5a6"
        )
        self.next_btn.pack(side="right", padx=15)
        
        self.finish_btn = ctk.CTkButton(
            nav_frame,
            text="📊 完成答题",
            width=100,
            height=35,
            command=self._finish_quiz,
            state="disabled",
            fg_color="#27ae60"
        )
        self.finish_btn.pack(side="right", padx=5)

    def _build_result_area(self):
        """结果统计区域（初始隐藏）"""
        result_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        result_frame.pack(fill="x", padx=10, pady=10)
        result_frame.pack_forget()
        
        self.result_title = ctk.CTkLabel(
            result_frame,
            text="📊 答题结果",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#2c3e50"
        )
        self.result_title.pack(pady=10)
        
        self.result_detail = ctk.CTkLabel(
            result_frame,
            text="",
            font=ctk.CTkFont(size=14),
            text_color="#7f8c8d"
        )
        self.result_detail.pack(pady=5)
        
        ctk.CTkButton(
            result_frame,
            text="🔄 再来一次",
            width=120,
            height=35,
            command=self._restart,
            fg_color="#3498db"
        ).pack(pady=10)

    # ===== 核心功能 =====
    def _start_quiz(self):
        """开始答题"""
        mode = self.mode_var.get()
        
        if not self.quiz_manager:
            messagebox.showwarning("提示", "请先配置题库管理器")
            return
        
        try:
            if mode == "随机抽题":
                self._start_random_quiz()
            elif mode == "按章节练习":
                self._start_chapter_quiz()
            elif mode == "错题复习":
                self._start_error_review()
        except Exception as e:
            messagebox.showerror("错误", f"开始练习失败: {e}")

    def _start_random_quiz(self, count: int = 10):
        """随机抽题练习"""
        # 获取所有学科
        subjects = self.quiz_manager.get_all_subjects()
        if not subjects:
            messagebox.showwarning("提示", "题库为空，请先导入题目")
            return
        
        # 用户选择学科和年级
        from tkinter import simpledialog
        subject = simpledialog.askstring("选择学科", "请输入学科名称:\n如: 数学, 物理, 化学", initialvalue=subjects[0])
        if not subject:
            return
        
        subject = subject.strip()
        if subject not in subjects:
            messagebox.showerror("错误", f"未找到学科: {subject}")
            return
        
        grades = self.quiz_manager.get_all_grades(subject)
        if not grades:
            messagebox.showwarning("提示", f"学科 {subject} 下没有题目")
            return
        
        grade = simpledialog.askstring("选择年级", f"请选择年级:\n{', '.join(grades)}", initialvalue=grades[0])
        if not grade:
            return
        
        grade = grade.strip()
        if grade not in grades:
            messagebox.showerror("错误", f"未找到年级: {grade}")
            return
        
        # 随机抽题
        questions = self.quiz_manager.get_random_questions(subject, grade, count)
        if not questions:
            messagebox.showwarning("提示", f"学科 {subject} 年级 {grade} 下没有足够题目")
            return
        
        self.current_questions = questions
        self._show_question(0)

    def _start_chapter_quiz(self):
        """按章节练习"""
        subjects = self.quiz_manager.get_all_subjects()
        if not subjects:
            messagebox.showwarning("提示", "题库为空，请先导入题目")
            return
        
        # 弹出选择对话框
        dialog = ChapterSelectDialog(self, subjects)
        self.wait_window(dialog.top)
        
        if dialog.result:
            subject, grade, chapter = dialog.result
            questions = self.quiz_manager.get_questions_by_chapter(subject, grade, chapter, 20)
            if not questions:
                messagebox.showwarning("提示", "该章节没有题目")
                return
            self.current_questions = questions
            self._show_question(0)

    def _start_error_review(self):
        """错题复习"""
        from core.storage.database import StudyDatabase
        db = StudyDatabase()
        errors = db.get_errors()
        
        if not errors:
            messagebox.showinfo("提示", "暂无错题记录，先去答题积累错题吧！")
            return
        
        # 转换为当前格式
        self.current_questions = []
        for err in errors[:10]:  # 最多10题
            q = {
                "id": err["id"],
                "subject": err["subject_code"],
                "grade": err["grade"],
                "chapter": err["chapter"],
                "question": err["question"],
                "options": err.get("options") or [],
                "answer": err["correct_answer"],
                "user_answer": err["user_answer"],
                "is_error": True
            }
            self.current_questions.append(q)
        
        self.is_review_mode = True
        self._show_question(0)

    def _show_question(self, index: int):
        """显示指定题目"""
        if index < 0 or index >= len(self.current_questions):
            return
        
        self.current_index = index
        q = self.current_questions[index]
        
        # 更新进度
        total = len(self.current_questions)
        self.progress_label.configure(text=f"第 {index+1}/{total} 题 | {q.get('subject','')} - {q.get('grade','')}")
        
        # 解析题目数据（question字段是JSON字符串）
        question_text, options = self._parse_question(q)
        self.question_text.configure(text=question_text)
        
        # 检测题型：有选项则显示单选，否则显示填空题
        has_options = len(options) > 0
        question_type = q.get('question_type', '')
        
        if has_options:
            # 选择题：显示选项按钮
            self.options_frame.pack()
            self.fill_blank_frame.pack_forget()
            for i, btn in enumerate(self.option_buttons):
                if i < len(options):
                    btn.configure(text=f"{chr(65+i)}. {options[i]}")
                    btn.pack()
                else:
                    btn.pack_forget()
        else:
            # 填空题/解答题：显示输入框
            self.options_frame.pack_forget()
            self.fill_blank_frame.pack()
            for btn in self.option_buttons:
                btn.pack_forget()
        
        # 重置选择
        for var in self.option_vars:
            var.set("")
        self.fill_blank_entry.delete(0, 'end')
        
        # 隐藏解析
        self.explanation_frame.pack_forget()
        
        # 更新导航按钮状态
        self.prev_btn.configure(state="disabled" if index == 0 else "normal")
        self.next_btn.configure(state="disabled" if index == total - 1 else "normal")
        self.finish_btn.configure(state="normal")
    
    def _parse_question(self, q: Dict):
        """
        解析题目数据，返回(题目文本, 选项列表)
        question字段可能是JSON字符串或dict对象
        """
        question_data = q.get("question", "")
        options_list = []
        
        try:
            # 如果question是字符串，尝试解析
            if isinstance(question_data, str):
                question_data = question_data.strip()
                if question_data.startswith('\ufeff'):
                    question_data = question_data[1:]
                try:
                    question_data = ast.literal_eval(question_data)
                except:
                    # 解析失败，尝试JSON
                    import json
                    question_data = json.loads(question_data)
            
            # 现在question_data应该是dict
            if not isinstance(question_data, dict):
                return str(question_data), []
            
            # 提取题目文本
            title = self._clean_question_text(question_data.get("title", "暂无题目"))
            
            # 提取选项（支持option_a/b/c/d格式，过滤无效占位符）
            option_keys = ["option_a", "option_b", "option_c", "option_d", "option_e"]
            for key in option_keys:
                opt = question_data.get(key, "").strip()
                # 跳过空值、占位符（如"..."）
                if opt and opt not in ['', '...', '（...）', '(...)']:
                    options_list.append(self._clean_question_text(opt))
            
            return title, options_list
            
        except Exception as e:
            # 解析失败，直接显示原文
            return str(question_data), []
    
    def _clean_question_text(self, text: str) -> str:
        """彻底清理LaTeX标记和特殊符号"""
        import re
        if not text:
            return ""
        
        # 清理外层数学环境标记 $$...$$ 或 \[...\]
        text = re.sub(r'^\$\$', '', text)
        text = re.sub(r'\$\$', '', text)
        text = text.replace('\\[', '').replace('\\]', '')
        
        # 1. 处理\begin{...}\end{...}结构
        text = re.sub(r'\\begin\{(\w+)\}', '', text)
        text = re.sub(r'\\end\{(\w+)\}', '', text)
        text = re.sub(r'\\overset\{([^}]*)\}\{([^}]*)\}', r'\2(\1)', text)
        
        # 2. 处理\frac和\dfrac - 转换为(a)/(b)格式
        def clean_frac(match):
            numerator = match.group(1)
            denominator = match.group(2)
            return f"({numerator})/({denominator})"
        
        text = re.sub(r'\\(?:d)?frac\{([^}]*)\}\{([^}]*)\}', clean_frac, text)
        
        # 3. 处理\sqrt
        def clean_sqrt(match):
            root = match.group(1) if match.group(1) else ''
            radicand = match.group(2)
            if root:
                return f"√[{root}] {radicand}"
            return f"√ {radicand}"
        
        text = re.sub(r'\\sqrt(?:\[([^\]]*)\])?\{([^}]+)\}', clean_sqrt, text)
        
        # 4. 处理\left和\right
        text = text.replace('\\left', '').replace('\\right', '')
        text = text.replace('\\left(', '(').replace('\\right)', ')')
        text = text.replace('\\left[', '[').replace('\\right]', ']')
        text = text.replace('\\left\{', '{').replace('\\right\}', '}')
        text = text.replace('\\left|', '|').replace('\\right|', '|')
        
        # 5. 希腊字母映射
        greek = {'\\alpha':'α','\\beta':'β','\\gamma':'γ','\\delta':'δ',
                 '\\epsilon':'ε','\\varepsilon':'ε','\\zeta':'ζ','\\eta':'η',
                 '\\theta':'θ','\\iota':'ι','\\kappa':'κ','\\lambda':'λ',
                 '\\mu':'μ','\\nu':'ν','\\xi':'ξ','\\pi':'π','\\rho':'ρ',
                 '\\sigma':'σ','\\tau':'τ','\\upsilon':'υ','\\phi':'φ',
                 '\\chi':'χ','\\psi':'ψ','\\omega':'ω'}
        for k, v in greek.items():
            text = text.replace(k, v)
        
        # 6. 关系运算符
        ops = {'\\leqslant':'≤','\\geqslant':'≥','\\neq':'≠','\\approx':'≈',
               '\\infty':'∞','\\pm':'±','\\div':'÷','\\times':'×',
               '\\cdot':'·','\\sim':'∼','\\parallel':'∥','\\perp':'⊥'}
        for k, v in ops.items():
            text = text.replace(k, v)
        
        # 7. 其他符号
        text = text.replace('\\because','∵').replace('\\therefore','∴')
        text = text.replace('\\in','∈').replace('\\notin','∉')
        text = text.replace('\\subset','⊂').replace('\\supset','⊃')
        text = text.replace('\\subseteq','⊆').replace('\\supseteq','⊇')
        text = text.replace('\\cup','∪').replace('\\cap','∩')
        text = text.replace('\\emptyset','∅').replace('\\varnothing','∅')
        text = text.replace('\\forall','∀').replace('\\exists','∃')
        text = text.replace('\\neg','¬').replace('\\land','∧').replace('\\lor','∨')
        text = text.replace('\\rightarrow','→').replace('\\leftarrow','←')
        text = text.replace('\\Rightarrow','⇒').replace('\\Leftarrow','⇐')
        text = text.replace('\\leftrightarrow','↔').replace('\\Leftrightarrow','⇔')
        text = text.replace('\\hat','̂').replace('\\bar','̄').replace('\\vec','⃗')
        text = text.replace('\\mathbb{R}','ℝ').replace('\\mathbb{N}','ℕ')
        text = text.replace('\\mathbb{Z}','ℤ').replace('\\mathbb{Q}','ℚ')
        text = text.replace('\\text','').replace('\\mathrm','')
        text = text.replace('\\mathbb','')
        
        # 8. 清理指数
        text = text.replace('^\{\{}','^').replace('^{}','^')
        text = re.sub(r'\^\{?(\d+)\}?', r'^\1', text)
        
        # 9. 清理花括号和转义符
        text = text.replace('{','').replace('}','')
        text = text.replace('\\','')
        
        # 10. 清理多余空格
        text = re.sub(r'\s+',' ',text).strip()
        
        return text

    def _on_answer_select(self):
        """选项被选中时"""
        pass
    
    def _check_fill_blank_answer(self, user_answer: str, correct_answer: str) -> bool:
        """判断填空题答案是否正确（模糊匹配）"""
        if not correct_answer or not user_answer:
            return False
        
        # 清理答案中的标记符号
        clean_correct = re.sub(r'[【】\[\]()（）]', '', correct_answer).strip()
        clean_user = re.sub(r'[【】\[\]()（）]', '', user_answer).strip()
        
        # 如果正确答案包含多个空（用空格或制表符分隔），尝试分别匹配
        if ' ' in clean_correct or '\t' in clean_correct:
            parts_correct = re.split(r'\s+', clean_correct)
            parts_user = re.split(r'\s+', clean_user)
            if len(parts_correct) == len(parts_user):
                return all(pc.strip() in pu for pc, pu in zip(parts_correct, parts_user))
            return False
        
        # 模糊匹配：用户答案包含正确答案关键词，或正确答案包含用户答案
        return clean_correct in clean_user or clean_user in clean_correct
    
    def _submit_answer(self):
        """提交答案"""
        if self.current_index >= len(self.current_questions):
            return
        
        q = self.current_questions[self.current_index]
        
        # 判断题型
        _, options = self._parse_question(q)
        has_options = len(options) > 0
        
        if has_options:
            selected = self.option_vars[self.current_index].get()
        else:
            selected = self.fill_blank_entry.get().strip()
        
        if not selected:
            messagebox.showwarning("提示", "请先填写答案")
            return
        
        # 获取正确答案
        correct = q.get("answer", "").strip()
        
        # 判断是否正确
        is_correct = False
        if has_options:
            # 选择题：比较选项字母
            if correct:
                if len(correct) == 1 and correct.isalpha():
                    is_correct = selected.upper() == correct
                elif len(correct) > 1:
                    is_correct = selected.upper() in correct.upper()
        else:
            # 填空题：模糊匹配答案关键词
            is_correct = self._check_fill_blank_answer(selected, correct)
        
        # 保存答案
        self.user_answers[str(q["id"])] = selected
        
        # 显示解析
        explanation = q.get("explanation", "")
        self.explanation_text.configure(text=explanation if explanation else "暂无解析")
        self.explanation_frame.pack(fill="x", padx=15, pady=10)
        
        # 高亮选项（仅选择题）
        if has_options:
            _, options_list = self._parse_question(q)
            for i, btn in enumerate(self.option_buttons):
                if i < len(options_list):
                    if chr(65+i) == correct.upper():
                        btn.configure(fg_color="#d5f5e3", text_color="#27ae60")
                    elif chr(65+i) == selected.upper() and not is_correct:
                        btn.configure(fg_color="#fadbd8", text_color="#e74c3c")
                    else:
                        btn.configure(fg_color="white", text_color="#2c3e50")
        else:
            # 填空题：如果正确，显示绿色提示
            if is_correct:
                self.fill_blank_entry.configure(fg_color="#27ae60", text_color="white")
            else:
                self.fill_blank_entry.configure(fg_color="#e74c3c", text_color="white")
        
        # 记录答题（如果是随机模式，记录到错题本）
        if not self.is_review_mode and not is_correct:
            self._record_error(q)

    def _record_error(self, question: Dict):
        """记录错题"""
        from core.storage.database import StudyDatabase
        db = StudyDatabase()
        db.add_error(
            subject=question.get("subject", ""),
            grade=question.get("grade", ""),
            chapter=question.get("chapter", ""),
            question=question.get("question", ""),
            options=question.get("options", []),
            correct=question.get("answer", ""),
            user_ans=self.user_answers.get(str(question["id"]), ""),
            analysis=question.get("explanation", "")
        )

    def _next_question(self):
        """下一题"""
        self._show_question(self.current_index + 1)

    def _prev_question(self):
        """上一题"""
        self._show_question(self.current_index - 1)

    def _finish_quiz(self):
        """完成答题，显示结果"""
        total = len(self.current_questions)
        answered = len([a for a in self.user_answers.values() if a])
        
        # 计算正确数（支持选择题和填空题）
        correct = 0
        for q in self.current_questions:
            user_ans = self.user_answers.get(str(q["id"]), "").strip()
            correct_ans = q.get("answer", "").strip()
            
            if not user_ans or not correct_ans:
                continue
            
            # 选择题：直接比较字母
            if len(correct_ans) <= 4 and correct_ans.isalpha():
                if user_ans.upper() == correct_ans.upper():
                    correct += 1
            # 填空题：使用模糊匹配
            else:
                if self._check_fill_blank_answer(user_ans, correct_ans):
                    correct += 1
        
        # 显示结果
        pct = round(correct / total * 100, 1) if total > 0 else 0
        result_text = f"共答 {total} 题，正确 {correct} 题，正确率 {pct}%"
        
        self.result_title.configure(text=f"📊 答题结果 - {result_text}")
        self.result_detail.configure(text=result_text)
        self.result_frame = self.master.nametowidget(self.result_frame.winfo_pathname()) if hasattr(self, 'result_frame') else None
        
        # 显示结果区域
        if hasattr(self, '_result_frame'):
            self._result_frame.pack(fill="x", padx=10, pady=10)
        
        # 禁用导航
        self.finish_btn.configure(state="disabled")
        self.next_btn.configure(state="disabled")
        self.prev_btn.configure(state="disabled")

    def _restart(self):
        """重新开始"""
        self.current_questions = []
        self.current_index = 0
        self.user_answers = {}
        self.is_review_mode = False
        
        # 重置UI
        self.progress_label.configure(text="请选择练习模式开始答题")
        self.question_text.configure(text="📋 暂无题目，请先导入题库或选择练习模式")
        self.explanation_frame.pack_forget()
        
        for var in self.option_vars:
            var.set("")
        for btn in self.option_buttons:
            btn.configure(fg_color="white", text_color="#2c3e50")
            btn.pack_forget()
        
        # 重置填空题输入框
        if hasattr(self, 'fill_blank_entry'):
            self.fill_blank_entry.delete(0, 'end')
            self.fill_blank_entry.configure(fg_color=None, text_color=None)
        
        self.next_btn.configure(state="disabled")
        self.prev_btn.configure(state="disabled")
        self.finish_btn.configure(state="disabled")
        
        if hasattr(self, '_result_frame'):
            self._result_frame.pack_forget()

    def _import_quiz(self):
        """导入题库"""
        from tkinter import filedialog
        filepath = filedialog.askopenfilename(
            title="选择题库文件",
            filetypes=[
                ("JSON文件", "*.json"),
                ("Excel文件", "*.xlsx *.xls"),
                ("Word文件", "*.docx *.doc"),
                ("PDF文件", "*.pdf"),
                ("所有文件", "*.*")
            ]
        )
        
        if not filepath:
            return
        
        if self.quiz_manager:
            result = self.quiz_manager.import_questions(filepath)
            if result["success"]:
                messagebox.showinfo("成功", f"已导入 {result['count']} 道题！")
            else:
                messagebox.showerror("失败", result.get("error", "导入失败"))
        else:
            messagebox.showwarning("提示", "请先配置题库管理器")


class ChapterSelectDialog:
    """章节选择对话框"""
    
    def __init__(self, parent, subjects: List[str]):
        self.top = ctk.CTkToplevel(parent)
        self.top.title("选择章节")
        self.top.geometry("400x300")
        self.top.grab_set()
        self.result = None
        
        self.subjects = subjects
        self.grades = []
        self.chapters = []
        
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(
            self.top,
            text="选择练习章节",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # 学科选择
        subject_frame = ctk.CTkFrame(self.top)
        subject_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(subject_frame, text="学科:", width=60).pack(side="left")
        self.subject_var = ctk.StringVar(value=self.subjects[0] if self.subjects else "")
        ctk.CTkOptionMenu(
            subject_frame,
            values=self.subjects,
            variable=self.subject_var,
            width=150
        ).pack(side="left", padx=10)
        
        # 年级选择
        grade_frame = ctk.CTkFrame(self.top)
        grade_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(grade_frame, text="年级:", width=60).pack(side="left")
        self.grade_var = ctk.StringVar(value="")
        ctk.CTkOptionMenu(
            grade_frame,
            values=[],
            variable=self.grade_var,
            width=150
        ).pack(side="left", padx=10)
        
        # 章节选择
        chapter_frame = ctk.CTkFrame(self.top)
        chapter_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(chapter_frame, text="章节:", width=60).pack(side="left")
        self.chapter_var = ctk.StringVar(value="")
        ctk.CTkOptionMenu(
            chapter_frame,
            values=[],
            variable=self.chapter_var,
            width=150
        ).pack(side="left", padx=10)
        
        # 按钮
        btn_frame = ctk.CTkFrame(self.top, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="确定",
            width=80,
            command=self._confirm,
            fg_color="#27ae60"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="取消",
            width=80,
            command=self.top.destroy,
            fg_color="#95a5a6"
        ).pack(side="left", padx=10)
        
        # 绑定学科变化事件
        self.subject_var.trace_add("write", self._on_subject_change)
        
        # 绑定年级变化事件
        self.grade_var.trace_add("write", self._on_grade_change)
        
        # 初始化年级列表
        self._on_subject_change()
    
    def _on_grade_change(self, *args):
        """年级变化时更新章节列表"""
        subject = self.subject_var.get()
        grade = self.grade_var.get()
        if not subject or not grade:
            return
        
        # 获取该年级的所有章节
        from core.engine.quiz_manager import QuizManager
        qm = QuizManager()
        chapters = qm.get_all_chapters(subject, grade)
        
        self.chapter_var.set("")
        
        # 更新章节选项
        for child in self.chapter_var.master.winfo_children():
            if isinstance(child, ctk.CTkOptionMenu):
                child.configure(values=chapters if chapters else [""])
                break

    def _on_subject_change(self, *args):
        """学科变化时更新年级列表"""
        subject = self.subject_var.get()
        if not subject:
            return
        
        # 动态获取该学科的所有年级
        from core.engine.quiz_manager import QuizManager
        qm = QuizManager()
        grades = qm.get_all_grades(subject)
        
        self.grade_var.set("")
        self.chapter_var.set("")
        
        # 更新年级选项
        for child in self.grade_var.master.winfo_children():
            if isinstance(child, ctk.CTkOptionMenu):
                child.configure(values=grades if grades else [""])
                break

    def _confirm(self):
        """确认选择"""
        subject = self.subject_var.get()
        grade = self.grade_var.get()
        chapter = self.chapter_var.get()
        
        if not subject:
            messagebox.showwarning("提示", "请选择学科")
            return
        if not grade:
            messagebox.showwarning("提示", "请选择年级")
            return
        
        self.result = (subject, grade, chapter)
        self.top.destroy()
