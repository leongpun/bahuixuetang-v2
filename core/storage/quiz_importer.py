"""
题库导入模块 - 支持多种格式导入
格式：JSON、Excel、Word(.docx)、PDF
"""
import json
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from pathlib import Path


@dataclass
class Question:
    """题目数据结构"""
    id: str
    subject: str  # 学科
    grade: str    # 年级
    chapter: str  # 章节
    question_type: str  # 题型：单选/多选/判断/填空
    question: str  # 题目内容
    options: List[str] = None  # 选项（选择题）
    answer: str = ""  # 答案
    explanation: str = ""  # 解析
    source: str = ""  # 来源文件


class QuizImporter:
    """题库导入器"""
    
    def __init__(self):
        self.questions: List[Question] = []
        self.import_history = []
    
    def import_file(self, filepath: str) -> Dict:
        """导入单个文件，返回结果"""
        ext = Path(filepath).suffix.lower()
        
        try:
            if ext == '.json':
                return self._import_json(filepath)
            elif ext in ['.xlsx', '.xls']:
                return self._import_excel(filepath)
            elif ext == '.docx':
                return self._import_docx(filepath)
            elif ext == '.pdf':
                return self._import_pdf(filepath)
            else:
                return {"success": False, "error": f"不支持的格式: {ext}"}
        except Exception as e:
            import traceback
            error_msg = f"导入失败: {str(e)}"
            print(f"[DEBUG] 导入错误: {error_msg}")
            print(f"[DEBUG] 堆栈: {traceback.format_exc()}")
            return {"success": False, "error": error_msg}
    
    def _import_json(self, filepath: str) -> Dict:
        """导入JSON格式题库"""
        # 尝试多种编码
        encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'gb18030', 'latin-1']
        
        data = None
        used_encoding = None
        
        for enc in encodings:
            try:
                with open(filepath, 'r', encoding=enc) as f:
                    data = json.load(f)
                    used_encoding = enc
                    break
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue
        
        if data is None:
            return {"success": False, "error": f"无法解析JSON文件，尝试的编码: {', '.join(encodings)}"}
        
        questions = []
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            items = data.get('questions', [data])
        else:
            items = []
        
        for item in items:
            q = self._parse_question(item, source=filepath)
            if q:
                questions.append(q)
        
        self.import_history.append({
            "file": filepath,
            "count": len(questions),
            "encoding": used_encoding,
            "time": self._get_time()
        })
        
        return {"success": True, "count": len(questions), "questions": questions}
    
    def _import_excel(self, filepath: str) -> Dict:
        """导入Excel格式题库"""
        try:
            import openpyxl
        except ImportError:
            return {"success": False, "error": "需要安装 openpyxl: pip install openpyxl"}
        
        wb = openpyxl.load_workbook(filepath)
        ws = wb.active
        
        questions = []
        headers = [cell.value for cell in ws[1]]
        
        for row in ws.iter_rows(min_row=2, values_only=True):
            item = dict(zip(headers, row))
            q = self._parse_question(item, source=filepath)
            if q:
                questions.append(q)
        
        self.import_history.append({
            "file": filepath,
            "count": len(questions),
            "time": self._get_time()
        })
        
        return {"success": True, "count": len(questions), "questions": questions}
    
    def _import_docx(self, filepath: str) -> Dict:
        """导入Word格式题库"""
        try:
            from docx import Document
        except ImportError:
            return {"success": False, "error": "需要安装 python-docx: pip install python-docx"}
        
        doc = Document(filepath)
        questions = []
        
        # 按段落解析
        text = "\n".join([p.text for p in doc.paragraphs])
        q_list = self._extract_questions_from_text(text)
        
        for item in q_list:
            q = self._parse_question(item, source=filepath)
            if q:
                questions.append(q)
        
        self.import_history.append({
            "file": filepath,
            "count": len(questions),
            "time": self._get_time()
        })
        
        return {"success": True, "count": len(questions), "questions": questions}
    
    def _import_pdf(self, filepath: str) -> Dict:
        """导入PDF格式题库"""
        try:
            import pdfplumber
        except ImportError:
            return {"success": False, "error": "需要安装 pdfplumber: pip install pdfplumber"}
        
        questions = []
        
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                q_list = self._extract_questions_from_text(text)
                for item in q_list:
                    q = self._parse_question(item, source=filepath)
                    if q:
                        questions.append(q)
        
        self.import_history.append({
            "file": filepath,
            "count": len(questions),
            "time": self._get_time()
        })
        
        return {"success": True, "count": len(questions), "questions": questions}
    
    def _extract_questions_from_text(self, text: str) -> List[Dict]:
        """从文本中提取题目"""
        import re
        
        questions = []
        # 匹配题目格式：数字+题号+题目内容
        pattern = r'(\d+)[\.、）\)]\s*([^0-9][^答选项]*?)(?=答案|[（\(]|$)'
        
        for match in re.finditer(pattern, text, re.DOTALL):
            q_num = match.group(1)
            q_text = match.group(2).strip()[:200]
            
            # 尝试提取答案
            answer_match = re.search(r'答案[:：]?\s*([A-Dabcd])', q_text)
            answer = answer_match.group(1) if answer_match else ""
            
            questions.append({
                "question": f"{q_num}. {q_text}",
                "answer": answer,
                "subject": "",
                "grade": "",
                "chapter": ""
            })
        
        return questions
    
    def _parse_question(self, item: Dict, source: str = "") -> Optional[Question]:
        """解析题目数据"""
        try:
            # 获取题目内容 - 兼容多种格式
            question_text = ""
            
            # 格式1: 直接字段
            if 'question' in item:
                question_text = item['question']
            elif '题干' in item:
                question_text = item['题干']
            elif 'title' in item:
                question_text = item['title']
            # 格式2: 嵌套结构（如教育类API）
            elif 'question_info' in item and isinstance(item['question_info'], dict):
                q_info = item['question_info']
                question_text = q_info.get('raw_content', '') or q_info.get('content', '') or q_info.get('question', '')
            
            if not question_text:
                return None
            
            # 获取选项
            options = []
            if 'options' in item:
                options = item['options']
            elif '选项' in item:
                options = item['选项']
            elif 'answer_options' in item:
                options = item['answer_options']
            if isinstance(options, str):
                options = [options]
            
            # 获取答案
            answer = ""
            if 'answer' in item:
                answer = item['answer']
            elif '答案' in item:
                answer = item['答案']
            elif 'answer_info' in item and isinstance(item['answer_info'], dict):
                answer = item['answer_info'].get('raw_content', '') or item['answer_info'].get('content', '')
            
            # 获取学科
            subject = item.get('subject', item.get('学科', ''))
            if not subject and 'course' in item:
                subject = item['course']
            
            # 获取年级
            grade = item.get('grade', item.get('年级', ''))
            
            # 获取题型
            question_type = item.get('question_type', item.get('题型', '未知'))
            if not question_type or question_type == '未知':
                if 'type' in item:
                    question_type = item['type']
            
            # 获取解析
            explanation = item.get('explanation', item.get('解析', ''))
            if not explanation and 'solution_info' in item:
                sol = item['solution_info']
                if isinstance(sol, list) and len(sol) > 0:
                    if isinstance(sol[0], dict):
                        explanation = sol[0].get('solution_info', '') or sol[0].get('content', '')
                elif isinstance(sol, dict):
                    explanation = sol.get('solution_info', '') or sol.get('content', '')
            
            # 生成ID - 优先使用JSON中的原始ID
            q_id = item.get('id', f"import_{int(__import__('time').time()*1000)}_{len(self.questions)}")
            
            return Question(
                id=q_id,
                subject=str(subject),
                grade=str(grade),
                chapter=item.get('chapter', item.get('章节', '')),
                question_type=str(question_type)[:20],
                question=str(question_text)[:500],
                options=options if isinstance(options, list) else [],
                answer=str(answer)[:100],
                explanation=str(explanation)[:500],
                source=source
            )
        except Exception:
            return None
    
    def _get_time(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M")
    
    def get_all_questions(self) -> List[Dict]:
        """获取所有题目（用于保存）"""
        return [asdict(q) for q in self.questions]
    
    def save_to_db(self, db_path: str):
        """保存到数据库"""
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        for q in self.questions:
            cursor.execute('''
                INSERT OR REPLACE INTO questions 
                (id, subject, grade, chapter, type, question, options, answer, explanation, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (q.id, q.subject, q.grade, q.chapter, q.question_type,
                  q.question, json.dumps(q.options, ensure_ascii=False),
                  q.answer, q.explanation, q.source))
        
        conn.commit()
        conn.close()
