"""
AnswerQuestionPracticePanel - SelectQuestionDisplay And Interaction
"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from typing import List, Dict, Optional
import random
import ast
import re


class QuizPanel(ctk.CTkFrame):
    """AnswerQuestionPracticePanel"""

    def __init__(self, parent, quiz_manager=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.quiz_manager = quiz_manager
        self.current_questions: List[Dict] = []
        self.current_index = 0
        self.user_answers: Dict[str, str] = {}
        self.is_review_mode = False  # Review Mode（ShowMistakeQuestion）
        
        self._build_ui()

    def _build_ui(self):
        """Build Interface"""
        # Top Control Bar
        self._build_toolbar()
        
        # Question Area
        self._build_question_area()
        
        # Navigation Buttons
        self._build_navigation()
        
        # Result Statistics Area（Show After Answering）
        self._build_result_area()

    def _build_toolbar(self):
        """Top Toolbar"""
        toolbar = ctk.CTkFrame(self, fg_color="#2c3e50", height=50)
        toolbar.pack(fill="x", padx=0, pady=(0, 10))
        toolbar.pack_propagate(False)
        
        # Title
        ctk.CTkLabel(
            toolbar,
            text="📝 AnswerQuestionPractice",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        ).pack(side="left", padx=15, pady=10)
        
        # Mode Switch
        self.mode_var = ctk.StringVar(value="random")
        mode_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        mode_frame.pack(side="right", padx=10)
        
        ctk.CTkOptionMenu(
            mode_frame,
            values=["RandomQuestion", "ByChapterPractice", "Review Mistakes"],
            variable=self.mode_var,
            width=120,
            height=30,
            fg_color="#34495e",
            button_hover_color="#3d566e",
            text_color="white"
        ).pack(side="left", padx=5)
        
        # StartByButton
        ctk.CTkButton(
            toolbar,
            text="▶️ StartPractice",
            width=100,
            height=30,
            command=self._start_quiz,
            fg_color="#27ae60",
            hover_color="#219a52"
        ).pack(side="right", padx=10)
        
        # ImportByButton
        ctk.CTkButton(
            toolbar,
            text="📂 ImportQuestion Bank",
            width=100,
            height=30,
            command=self._import_quiz,
            fg_color="#8e44ad",
            hover_color="#7d3c98"
        ).pack(side="right", padx=5)

    def _build_question_area(self):
        """QuestionShowArea"""
        question_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        question_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # QuestionNumberAndProgress
        progress_frame = ctk.CTkFrame(question_frame, fg_color="transparent")
        progress_frame.pack(fill="x", padx=15, pady=10)
        
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="Please selectPracticeModeStartAnswerQuestion",
            font=ctk.CTkFont(size=12),
            text_color="#7f8c8d"
        )
        self.progress_label.pack(side="left")
        
        # QuestionInsideContent
        self.question_text = ctk.CTkLabel(
            question_frame,
            text="📋 NoQuestion，Please firstImportQuestion BankOrSelectPracticeMode",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#2c3e50",
            wraplength=700,
            justify="left"
        )
        self.question_text.pack(fill="x", padx=15, pady=10)
        
        # OptionArea
        self.options_frame = ctk.CTkFrame(question_frame, fg_color="transparent")
        self.options_frame.pack(fill="x", padx=15, pady=10)
        
        self.option_vars = []
        self.option_buttons = []
        for i in range(4):
            var = ctk.StringVar(value="")
            self.option_vars.append(var)
            btn = ctk.CTkRadioButton(
                self.options_frame,
                text=f"{chr(65+i)}. Option Content",
                variable=var,
                value=str(chr(65+i)),
                font=ctk.CTkFont(size=13),
                command=self._on_answer_select
            )
            btn.pack(anchor="w", pady=5)
            self.option_buttons.append(btn)
        
        # Fill-in-blank Input（Initially Hidden）
        self.fill_blank_frame = ctk.CTkFrame(question_frame, fg_color="transparent")
        self.fill_blank_frame.pack(fill="x", padx=15, pady=10)
        self.fill_blank_frame.pack_forget()
        
        ctk.CTkLabel(
            self.fill_blank_frame,
            text="✍️ Please enterAnswer:",
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
        
        # ExplanationArea（Initially Hidden）
        self.explanation_frame = ctk.CTkFrame(
            question_frame,
            fg_color="#f8f9fa",
            corner_radius=8
        )
        self.explanation_frame.pack(fill="x", padx=15, pady=10)
        self.explanation_frame.pack_forget()
        
        ctk.CTkLabel(
            self.explanation_frame,
            text="📖 Explanation",
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
        
        # SubmitByButton
        submit_btn = ctk.CTkButton(
            question_frame,
            text="✅ SubmitAnswer",
            width=120,
            height=35,
            command=self._submit_answer,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        submit_btn.pack(pady=10)
        self.submit_btn = submit_btn

    def _build_navigation(self):
        """BottomNavigation Buttons"""
        nav_frame = ctk.CTkFrame(self, fg_color="#ecf0f1", height=50)
        nav_frame.pack(fill="x", side="bottom", padx=10, pady=(0, 10))
        nav_frame.pack_propagate(False)
        
        self.prev_btn = ctk.CTkButton(
            nav_frame,
            text="⬅️ Previous",
            width=100,
            height=35,
            command=self._prev_question,
            state="disabled",
            fg_color="#95a5a6"
        )
        self.prev_btn.pack(side="left", padx=15)
        
        self.next_btn = ctk.CTkButton(
            nav_frame,
            text="➡️ Next",
            width=100,
            height=35,
            command=self._next_question,
            state="disabled",
            fg_color="#95a5a6"
        )
        self.next_btn.pack(side="right", padx=15)
        
        self.finish_btn = ctk.CTkButton(
            nav_frame,
            text="📊 DoneAnswerQuestion",
            width=100,
            height=35,
            command=self._finish_quiz,
            state="disabled",
            fg_color="#27ae60"
        )
        self.finish_btn.pack(side="right", padx=5)

    def _build_result_area(self):
        """Result Statistics Area（Initially Hidden）"""
        result_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        result_frame.pack(fill="x", padx=10, pady=10)
        result_frame.pack_forget()
        
        self.result_title = ctk.CTkLabel(
            result_frame,
            text="📊 Answer Result",
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
            text="🔄 Try Again",
            width=120,
            height=35,
            command=self._restart,
            fg_color="#3498db"
        ).pack(pady=10)

    # ===== Core Feature =====
    def _start_quiz(self):
        """StartAnswerQuestion"""
        mode = self.mode_var.get()
        
        if not self.quiz_manager:
            messagebox.showwarning("Tip", "Please firstConfigureQuestion BankManager")
            return
        
        try:
            if mode == "RandomQuestion":
                self._start_random_quiz()
            elif mode == "ByChapterPractice":
                self._start_chapter_quiz()
            elif mode == "Review Mistakes":
                self._start_error_review()
        except Exception as e:
            messagebox.showerror("Error", f"StartPracticeFailed: {e}")

    def _start_random_quiz(self, count: int = 10):
        """RandomQuestionPractice"""
        # Get AllSubject
        subjects = self.quiz_manager.get_all_subjects()
        if not subjects:
            messagebox.showwarning("Tip", "Question BankEmpty，Please firstImportQuestion")
            return
        
        # UserSelectSubjectAndGrade
        from tkinter import simpledialog
        subject = simpledialog.askstring("SelectSubject", "Please enterSubjectName:\nSuch As: Math, Physics, Chemistry", initialvalue=subjects[0])
        if not subject:
            return
        
        subject = subject.strip()
        if subject not in subjects:
            messagebox.showerror("Error", f"Not yetFoundSubject: {subject}")
            return
        
        grades = self.quiz_manager.get_all_grades(subject)
        if not grades:
            messagebox.showwarning("Tip", f"Subject {subject} No InQuestion")
            return
        
        grade = simpledialog.askstring("SelectGrade", f"Please selectGrade:\n{', '.join(grades)}", initialvalue=grades[0])
        if not grade:
            return
        
        grade = grade.strip()
        if grade not in grades:
            messagebox.showerror("Error", f"Not yetFoundGrade: {grade}")
            return
        
        # RandomQuestion
        questions = self.quiz_manager.get_random_questions(subject, grade, count)
        if not questions:
            messagebox.showwarning("Tip", f"Subject {subject} Grade {grade} No InEnoughQuestion")
            return
        
        self.current_questions = questions
        self._show_question(0)

    def _start_chapter_quiz(self):
        """ByChapterPractice"""
        subjects = self.quiz_manager.get_all_subjects()
        if not subjects:
            messagebox.showwarning("Tip", "Question BankEmpty，Please firstImportQuestion")
            return
        
        # Pop UpSelectDialog
        dialog = ChapterSelectDialog(self, subjects)
        self.wait_window(dialog.top)
        
        if dialog.result:
            subject, grade, chapter = dialog.result
            questions = self.quiz_manager.get_questions_by_chapter(subject, grade, chapter, 20)
            if not questions:
                messagebox.showwarning("Tip", "TheChapterNot HaveHaveQuestion")
                return
            self.current_questions = questions
            self._show_question(0)

    def _start_error_review(self):
        """Review Mistakes"""
        from core.storage.database import StudyDatabase
        db = StudyDatabase()
        errors = db.get_errors()
        
        if not errors:
            messagebox.showinfo("Tip", "NoMistakeQuestionRecord，FirstAnswerQuestionAccumulateMistakeQuestion！")
            return
        
        # Convert ToCurrentFormat
        self.current_questions = []
        for err in errors[:10]:  # Max10Question
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
        """ShowPointDefineQuestion"""
        if index < 0 or index >= len(self.current_questions):
            return
        
        self.current_index = index
        q = self.current_questions[index]
        
        # MoreNewProgress
        total = len(self.current_questions)
        self.progress_label.configure(text=f"Th {index+1}/{total} Question | {q.get('subject','')} - {q.get('grade','')}")
        
        # ExplanationQuestionData（questionFieldYesJSONString）
        question_text, options = self._parse_question(q)
        self.question_text.configure(text=question_text)
        
        # DetectQuestionType：HaveOptionThenShowSingle Choice，NoThenShowFill-in-blankQuestion
        has_options = len(options) > 0
        question_type = q.get('question_type', '')
        
        if has_options:
            # SelectQuestion：ShowOptionByButton
            self.options_frame.pack()
            self.fill_blank_frame.pack_forget()
            for i, btn in enumerate(self.option_buttons):
                if i < len(options):
                    btn.configure(text=f"{chr(65+i)}. {options[i]}")
                    btn.pack()
                else:
                    btn.pack_forget()
        else:
            # Fill-in-blankQuestion/AnswerQuestion：ShowInputBox
            self.options_frame.pack_forget()
            self.fill_blank_frame.pack()
            for btn in self.option_buttons:
                btn.pack_forget()
        
        # ResetSelect
        for var in self.option_vars:
            var.set("")
        self.fill_blank_entry.delete(0, 'end')
        
        # HideExplanation
        self.explanation_frame.pack_forget()
        
        # MoreNewNavigation ButtonsStatus
        self.prev_btn.configure(state="disabled" if index == 0 else "normal")
        self.next_btn.configure(state="disabled" if index == total - 1 else "normal")
        self.finish_btn.configure(state="normal")
    
    def _parse_question(self, q: Dict):
        """
        ExplanationQuestionData，Back(Question Text, OptionList)
        questionFieldMayYesJSONStringOrdictObject
        """
        question_data = q.get("question", "")
        options_list = []
        
        try:
            # Such AsResultquestionYesString，TryExplanation
            if isinstance(question_data, str):
                question_data = question_data.strip()
                if question_data.startswith('\ufeff'):
                    question_data = question_data[1:]
                try:
                    question_data = ast.literal_eval(question_data)
                except:
                    # ExplanationFailed，TryJSON
                    import json
                    question_data = json.loads(question_data)
            
            # Nowquestion_dataShouldTheYesdict
            if not isinstance(question_data, dict):
                return str(question_data), []
            
            # ExtractQuestion Text
            title = self._clean_question_text(question_data.get("title", "NoQuestion"))
            
            # Extract Options（Supportoption_a/b/c/dFormat，FilterInvalidPlaceholder）
            option_keys = ["option_a", "option_b", "option_c", "option_d", "option_e"]
            for key in option_keys:
                opt = question_data.get(key, "").strip()
                # Skip Null Values、Placeholder（Such As"..."）
                if opt and opt not in ['', '...', '（...）', '(...)']:
                    options_list.append(self._clean_question_text(opt))
            
            return title, options_list
            
        except Exception as e:
            # ExplanationFailed，DirectShowOriginal Text
            return str(question_data), []
    
    def _clean_question_text(self, text: str) -> str:
        """ThoroughCleanLaTeXMarks and Special Symbols"""
        import re
        if not text:
            return ""
        
        # CleanOuter LayerMathEnvironment Mark $$...$$ Or \[...\]
        text = re.sub(r'^\$\$', '', text)
        text = re.sub(r'\$\$', '', text)
        text = text.replace('\\[', '').replace('\\]', '')
        
        # 1. Process\begin{...}\end{...}Structure
        text = re.sub(r'\\begin\{(\w+)\}', '', text)
        text = re.sub(r'\\end\{(\w+)\}', '', text)
        text = re.sub(r'\\overset\{([^}]*)\}\{([^}]*)\}', r'\2(\1)', text)
        
        # 2. Process\fracAnd\dfrac - Convert To(a)/(b)Format
        def clean_frac(match):
            numerator = match.group(1)
            denominator = match.group(2)
            return f"({numerator})/({denominator})"
        
        text = re.sub(r'\\(?:d)?frac\{([^}]*)\}\{([^}]*)\}', clean_frac, text)
        
        # 3. Process\sqrt
        def clean_sqrt(match):
            root = match.group(1) if match.group(1) else ''
            radicand = match.group(2)
            if root:
                return f"√[{root}] {radicand}"
            return f"√ {radicand}"
        
        text = re.sub(r'\\sqrt(?:\[([^\]]*)\])?\{([^}]+)\}', clean_sqrt, text)
        
        # 4. Process\leftAnd\right
        text = text.replace('\\left', '').replace('\\right', '')
        text = text.replace('\\left(', '(').replace('\\right)', ')')
        text = text.replace('\\left[', '[').replace('\\right]', ']')
        text = text.replace('\\left\{', '{').replace('\\right\}', '}')
        text = text.replace('\\left|', '|').replace('\\right|', '|')
        
        # 5. Greek Letter Mapping
        greek = {'\\alpha':'α','\\beta':'β','\\gamma':'γ','\\delta':'δ',
                 '\\epsilon':'ε','\\varepsilon':'ε','\\zeta':'ζ','\\eta':'η',
                 '\\theta':'θ','\\iota':'ι','\\kappa':'κ','\\lambda':'λ',
                 '\\mu':'μ','\\nu':'ν','\\xi':'ξ','\\pi':'π','\\rho':'ρ',
                 '\\sigma':'σ','\\tau':'τ','\\upsilon':'υ','\\phi':'φ',
                 '\\chi':'χ','\\psi':'ψ','\\omega':'ω'}
        for k, v in greek.items():
            text = text.replace(k, v)
        
        # 6. Relational Operators
        ops = {'\\leqslant':'≤','\\geqslant':'≥','\\neq':'≠','\\approx':'≈',
               '\\infty':'∞','\\pm':'±','\\div':'÷','\\times':'×',
               '\\cdot':'·','\\sim':'∼','\\parallel':'∥','\\perp':'⊥'}
        for k, v in ops.items():
            text = text.replace(k, v)
        
        # 7. Other Symbols
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
        
        # 8. CleanPointCount
        text = text.replace('^\{\{}','^').replace('^{}','^')
        text = re.sub(r'\^\{?(\d+)\}?', r'^\1', text)
        
        # 9. Clean Braces and Escapes
        text = text.replace('{','').replace('}','')
        text = text.replace('\\','')
        
        # 10. CleanExtra Spaces
        text = re.sub(r'\s+',' ',text).strip()
        
        return text

    def _on_answer_select(self):
        """OptionWhen Selected"""
        pass
    
    def _check_fill_blank_answer(self, user_answer: str, correct_answer: str) -> bool:
        """JudgeFill-in-blankQuestionAnswerYesNoCorrect（Fuzzy Match）"""
        if not correct_answer or not user_answer:
            return False
        
        # CleanAnswerSymbols in
        clean_correct = re.sub(r'[【】\[\]()（）]', '', correct_answer).strip()
        clean_user = re.sub(r'[【】\[\]()（）]', '', user_answer).strip()
        
        # Such AsResultCorrectAnswerContains Multiple Blanks（With SpaceOrSystemTableSymbolPartSeparate），TryPartOtherMatch
        if ' ' in clean_correct or '\t' in clean_correct:
            parts_correct = re.split(r'\s+', clean_correct)
            parts_user = re.split(r'\s+', clean_user)
            if len(parts_correct) == len(parts_user):
                return all(pc.strip() in pu for pc, pu in zip(parts_correct, parts_user))
            return False
        
        # Fuzzy Match：UserAnswerIncludeCorrectAnswerKeyword，OrCorrectAnswerIncludeUserAnswer
        return clean_correct in clean_user or clean_user in clean_correct
    
    def _submit_answer(self):
        """SubmitAnswer"""
        if self.current_index >= len(self.current_questions):
            return
        
        q = self.current_questions[self.current_index]
        
        # JudgeQuestionType
        _, options = self._parse_question(q)
        has_options = len(options) > 0
        
        if has_options:
            selected = self.option_vars[self.current_index].get()
        else:
            selected = self.fill_blank_entry.get().strip()
        
        if not selected:
            messagebox.showwarning("Tip", "Please firstFillAnswer")
            return
        
        # GetCorrectAnswer
        correct = q.get("answer", "").strip()
        
        # JudgeYesNoCorrect
        is_correct = False
        if has_options:
            # SelectQuestion：CompareOptionCharacterMother
            if correct:
                if len(correct) == 1 and correct.isalpha():
                    is_correct = selected.upper() == correct
                elif len(correct) > 1:
                    is_correct = selected.upper() in correct.upper()
        else:
            # Fill-in-blankQuestion：Fuzzy MatchAnswerKeyword
            is_correct = self._check_fill_blank_answer(selected, correct)
        
        # SaveAnswer
        self.user_answers[str(q["id"])] = selected
        
        # ShowExplanation
        explanation = q.get("explanation", "")
        self.explanation_text.configure(text=explanation if explanation else "NoExplanation")
        self.explanation_frame.pack(fill="x", padx=15, pady=10)
        
        # Highlight Option（OnlySelectQuestion）
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
            # Fill-in-blankQuestion：Such AsResultCorrect，ShowGreenTip
            if is_correct:
                self.fill_blank_entry.configure(fg_color="#27ae60", text_color="white")
            else:
                self.fill_blank_entry.configure(fg_color="#e74c3c", text_color="white")
        
        # Record Answers（Such AsResultYesRandom Mode，Record ToError Book）
        if not self.is_review_mode and not is_correct:
            self._record_error(q)

    def _record_error(self, question: Dict):
        """Record Mistakes"""
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
        """Next"""
        self._show_question(self.current_index + 1)

    def _prev_question(self):
        """Previous"""
        self._show_question(self.current_index - 1)

    def _finish_quiz(self):
        """DoneAnswerQuestion，ShowResult"""
        total = len(self.current_questions)
        answered = len([a for a in self.user_answers.values() if a])
        
        # CalculateCorrectCount（SupportSelectQuestionAndFill-in-blankQuestion）
        correct = 0
        for q in self.current_questions:
            user_ans = self.user_answers.get(str(q["id"]), "").strip()
            correct_ans = q.get("answer", "").strip()
            
            if not user_ans or not correct_ans:
                continue
            
            # SelectQuestion：Directly Compare Letters
            if len(correct_ans) <= 4 and correct_ans.isalpha():
                if user_ans.upper() == correct_ans.upper():
                    correct += 1
            # Fill-in-blankQuestion：Use Fuzzy Matching
            else:
                if self._check_fill_blank_answer(user_ans, correct_ans):
                    correct += 1
        
        # ShowResult
        pct = round(correct / total * 100, 1) if total > 0 else 0
        result_text = f"Total Answered {total} Question，Correct {correct} Question，CorrectRate {pct}%"
        
        self.result_title.configure(text=f"📊 Answer Result - {result_text}")
        self.result_detail.configure(text=result_text)
        self.result_frame = self.master.nametowidget(self.result_frame.winfo_pathname()) if hasattr(self, 'result_frame') else None
        
        # ShowResultArea
        if hasattr(self, '_result_frame'):
            self._result_frame.pack(fill="x", padx=10, pady=10)
        
        # Disable Navigation
        self.finish_btn.configure(state="disabled")
        self.next_btn.configure(state="disabled")
        self.prev_btn.configure(state="disabled")

    def _restart(self):
        """AgainNewStart"""
        self.current_questions = []
        self.current_index = 0
        self.user_answers = {}
        self.is_review_mode = False
        
        # ResetUI
        self.progress_label.configure(text="Please selectPracticeModeStartAnswerQuestion")
        self.question_text.configure(text="📋 NoQuestion，Please firstImportQuestion BankOrSelectPracticeMode")
        self.explanation_frame.pack_forget()
        
        for var in self.option_vars:
            var.set("")
        for btn in self.option_buttons:
            btn.configure(fg_color="white", text_color="#2c3e50")
            btn.pack_forget()
        
        # ResetFill-in-blank Input
        if hasattr(self, 'fill_blank_entry'):
            self.fill_blank_entry.delete(0, 'end')
            self.fill_blank_entry.configure(fg_color=None, text_color=None)
        
        self.next_btn.configure(state="disabled")
        self.prev_btn.configure(state="disabled")
        self.finish_btn.configure(state="disabled")
        
        if hasattr(self, '_result_frame'):
            self._result_frame.pack_forget()

    def _import_quiz(self):
        """ImportQuestion Bank"""
        from tkinter import filedialog
        filepath = filedialog.askopenfilename(
            title="SelectQuestion BankFile",
            filetypes=[
                ("JSONFile", "*.json"),
                ("ExcelFile", "*.xlsx *.xls"),
                ("WordFile", "*.docx *.doc"),
                ("PDFFile", "*.pdf"),
                ("All Files", "*.*")
            ]
        )
        
        if not filepath:
            return
        
        if self.quiz_manager:
            result = self.quiz_manager.import_questions(filepath)
            if result["success"]:
                messagebox.showinfo("Success", f"AlreadyImport {result['count']} Questions！")
            else:
                messagebox.showerror("Failed", result.get("error", "ImportFailed"))
        else:
            messagebox.showwarning("Tip", "Please firstConfigureQuestion BankManager")


class ChapterSelectDialog:
    """ChapterSelectDialog"""
    
    def __init__(self, parent, subjects: List[str]):
        self.top = ctk.CTkToplevel(parent)
        self.top.title("SelectChapter")
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
            text="SelectPracticeChapter",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # SubjectSelect
        subject_frame = ctk.CTkFrame(self.top)
        subject_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(subject_frame, text="Subject:", width=60).pack(side="left")
        self.subject_var = ctk.StringVar(value=self.subjects[0] if self.subjects else "")
        ctk.CTkOptionMenu(
            subject_frame,
            values=self.subjects,
            variable=self.subject_var,
            width=150
        ).pack(side="left", padx=10)
        
        # GradeSelect
        grade_frame = ctk.CTkFrame(self.top)
        grade_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(grade_frame, text="Grade:", width=60).pack(side="left")
        self.grade_var = ctk.StringVar(value="")
        ctk.CTkOptionMenu(
            grade_frame,
            values=[],
            variable=self.grade_var,
            width=150
        ).pack(side="left", padx=10)
        
        # ChapterSelect
        chapter_frame = ctk.CTkFrame(self.top)
        chapter_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(chapter_frame, text="Chapter:", width=60).pack(side="left")
        self.chapter_var = ctk.StringVar(value="")
        ctk.CTkOptionMenu(
            chapter_frame,
            values=[],
            variable=self.chapter_var,
            width=150
        ).pack(side="left", padx=10)
        
        # ByButton
        btn_frame = ctk.CTkFrame(self.top, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="Confirm",
            width=80,
            command=self._confirm,
            fg_color="#27ae60"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=80,
            command=self.top.destroy,
            fg_color="#95a5a6"
        ).pack(side="left", padx=10)
        
        # BindSubjectChange Event
        self.subject_var.trace_add("write", self._on_subject_change)
        
        # BindGradeChange Event
        self.grade_var.trace_add("write", self._on_grade_change)
        
        # InitializeGradeList
        self._on_subject_change()
    
    def _on_grade_change(self, *args):
        """GradeOn ChangeMoreNewChapterList"""
        subject = self.subject_var.get()
        grade = self.grade_var.get()
        if not subject or not grade:
            return
        
        # GetTheGrade's AllChapter
        from core.engine.quiz_manager import QuizManager
        qm = QuizManager()
        chapters = qm.get_all_chapters(subject, grade)
        
        self.chapter_var.set("")
        
        # MoreNewChapterOption
        for child in self.chapter_var.master.winfo_children():
            if isinstance(child, ctk.CTkOptionMenu):
                child.configure(values=chapters if chapters else [""])
                break

    def _on_subject_change(self, *args):
        """SubjectOn ChangeMoreNewGradeList"""
        subject = self.subject_var.get()
        if not subject:
            return
        
        # DynamicGetTheSubject's AllGrade
        from core.engine.quiz_manager import QuizManager
        qm = QuizManager()
        grades = qm.get_all_grades(subject)
        
        self.grade_var.set("")
        self.chapter_var.set("")
        
        # MoreNewGradeOption
        for child in self.grade_var.master.winfo_children():
            if isinstance(child, ctk.CTkOptionMenu):
                child.configure(values=grades if grades else [""])
                break

    def _confirm(self):
        """ConfirmSelect"""
        subject = self.subject_var.get()
        grade = self.grade_var.get()
        chapter = self.chapter_var.get()
        
        if not subject:
            messagebox.showwarning("Tip", "Please selectSubject")
            return
        if not grade:
            messagebox.showwarning("Tip", "Please selectGrade")
            return
        
        self.result = (subject, grade, chapter)
        self.top.destroy()
