"""
Question BankManageModule - QuestionManage、Retrieve、Statistics
"""
import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from core.storage.quiz_importer import Question


@dataclass
class QuizStats:
    """QuestionStatisticsData"""
    total: int = 0
    by_subject: Dict[str, int] = None
    by_grade: Dict[str, int] = None
    by_chapter: Dict[str, int] = None
    by_type: Dict[str, int] = None
    
    def __post_init__(self):
        if self.by_subject is None:
            self.by_subject = {}
        if self.by_grade is None:
            self.by_grade = {}
        if self.by_chapter is None:
            self.by_chapter = {}
        if self.by_type is None:
            self.by_type = {}


class QuizManager:
    """Question BankManager"""
    
    def __init__(self, db_path=None):
        self.db_path = Path(db_path) if db_path else Path.home() / "柏慧学堂_data" / "quiz.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_tables()
    
    def _get_conn(self):
        """GetDataLibraryConnect"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_tables(self):
        """Initialize DataLibraryTable"""
        with self._get_conn() as conn:
            # QuestionTable
            conn.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    id TEXT PRIMARY KEY,
                    subject TEXT NOT NULL,
                    grade TEXT NOT NULL,
                    chapter TEXT,
                    question_type TEXT DEFAULT 'Not yetKnowledge',
                    question TEXT NOT NULL,
                    options TEXT,
                    answer TEXT,
                    explanation TEXT,
                    source TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # ImportHistoryTable
            conn.execute("""
                CREATE TABLE IF NOT EXISTS import_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT NOT NULL,
                    question_count INTEGER,
                    success BOOLEAN,
                    error_msg TEXT,
                    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    # ===== ImportRelated =====
    def import_questions(self, filepath: str) -> Dict:
        """ImportQuestionFile，BackResult"""
        from core.storage.quiz_importer import QuizImporter
        
        importer = QuizImporter()
        result = importer.import_file(filepath)
        
        if not result["success"]:
            return result
        
        questions = result.get("questions", [])
        
        # SaveToDataLibrary
        saved = self._save_questions(questions)
        
        # RecordImportHistory
        with self._get_conn() as conn:
            conn.execute("""
                INSERT INTO import_history (file_path, question_count, success, error_msg)
                VALUES (?, ?, ?, ?)
            """, (filepath, len(questions), True, None))
            conn.commit()
        
        return {
            "success": True,
            "count": len(questions),
            "saved": saved,
            "file": filepath
        }
    
    def _save_questions(self, questions: List[Question]) -> int:
        """SaveQuestionToDataLibrary"""
        saved = 0
        with self._get_conn() as conn:
            for q in questions:
                try:
                    conn.execute("""
                        INSERT OR REPLACE INTO questions 
                        (id, subject, grade, chapter, question_type, question, options, answer, explanation, source)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        q.id, q.subject, q.grade, q.chapter, q.question_type,
                        q.question, json.dumps(q.options, ensure_ascii=False) if q.options else None,
                        q.answer, q.explanation, q.source
                    ))
                    saved += 1
                except Exception as e:
                    print(f"SaveQuestionFailed: {e}")
        return saved
    
    # ===== QueryRelated =====
    def get_question(self, question_id: str) -> Optional[Dict]:
        """GetSingleItemQuestion"""
        with self._get_conn() as conn:
            row = conn.execute("SELECT * FROM questions WHERE id=?", (question_id,)).fetchone()
            if row:
                return self._row_to_dict(row)
        return None
    
    def get_questions(
        self,
        subject: Optional[str] = None,
        grade: Optional[str] = None,
        chapter: Optional[str] = None,
        question_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict]:
        """QueryQuestionList（SupportFilter）"""
        conditions = []
        params = []
        
        if subject:
            conditions.append("subject = ?")
            params.append(subject)
        if grade:
            conditions.append("grade = ?")
            params.append(grade)
        if chapter:
            conditions.append("chapter = ?")
            params.append(chapter)
        if question_type:
            conditions.append("question_type = ?")
            params.append(question_type)
        
        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        
        with self._get_conn() as conn:
            query = f"""
                SELECT * FROM questions 
                {where_clause}
                ORDER BY grade ASC, chapter ASC, id ASC
                LIMIT ? OFFSET ?
            """
            params.extend([limit, offset])
            rows = conn.execute(query, params).fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    def search_questions(self, keyword: str, subject: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """SearchQuestion（ByKeyword）"""
        with self._get_conn() as conn:
            query = """
                SELECT * FROM questions 
                WHERE question LIKE ? OR explanation LIKE ?
            """
            params = [f"%{keyword}%", f"%{keyword}%"]
            
            if subject:
                query += " AND subject = ?"
                params.append(subject)
            
            query += " LIMIT ?"
            params.append(limit)
            
            rows = conn.execute(query, params).fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    # ===== StatisticsRelated =====
    def get_stats(self) -> QuizStats:
        """GetQuestionStatisticsInfo"""
        stats = QuizStats()
        
        with self._get_conn() as conn:
            # TotalCount
            row = conn.execute("SELECT COUNT(*) as count FROM questions").fetchone()
            stats.total = row["count"] if row else 0
            
            # BySubjectStatistics
            rows = conn.execute("SELECT subject, COUNT(*) as count FROM questions GROUP BY subject").fetchall()
            stats.by_subject = {r["subject"]: r["count"] for r in rows}
            
            # ByGradeStatistics
            rows = conn.execute("SELECT grade, COUNT(*) as count FROM questions GROUP BY grade").fetchall()
            stats.by_grade = {r["grade"]: r["count"] for r in rows}
            
            # ByChapterStatistics
            rows = conn.execute("SELECT chapter, COUNT(*) as count FROM questions WHERE chapter IS NOT NULL AND chapter != '' GROUP BY chapter").fetchall()
            stats.by_chapter = {r["chapter"]: r["count"] for r in rows}
            
            # ByQuestionTypeStatistics
            rows = conn.execute("SELECT question_type, COUNT(*) as count FROM questions GROUP BY question_type").fetchall()
            stats.by_type = {r["question_type"]: r["count"] for r in rows}
        
        return stats
    
    def get_subject_stats(self, subject: str) -> Dict:
        """GetSubjectDimensionStatistics"""
        with self._get_conn() as conn:
            # EachGradeCountQuantity
            rows = conn.execute(
                "SELECT grade, COUNT(*) as count FROM questions WHERE subject=? GROUP BY grade",
                (subject,)
            ).fetchall()
            by_grade = {r["grade"]: r["count"] for r in rows}
            
            # EachQuestionTypeCountQuantity
            rows = conn.execute(
                "SELECT question_type, COUNT(*) as count FROM questions WHERE subject=? GROUP BY question_type",
                (subject,)
            ).fetchall()
            by_type = {r["question_type"]: r["count"] for r in rows}
            
            return {
                "total": sum(by_grade.values()),
                "by_grade": by_grade,
                "by_type": by_type
            }
    
    # ===== RandomQuestion =====
    def get_random_questions(
        self,
        subject: str,
        grade: str,
        count: int = 10,
        exclude_ids: Optional[List[str]] = None
    ) -> List[Dict]:
        """RandomFetchQuestion"""
        with self._get_conn() as conn:
            query = "SELECT * FROM questions WHERE subject=? AND grade=?"
            params = [subject, grade]
            
            if exclude_ids:
                placeholders = ",".join(["?"] * len(exclude_ids))
                query += f" AND id NOT IN ({placeholders})"
                params.extend(exclude_ids)
            
            query += " ORDER BY RANDOM() LIMIT ?"
            params.append(count)
            
            rows = conn.execute(query, params).fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    def get_questions_by_chapter(
        self,
        subject: str,
        grade: str,
        chapter: str,
        limit: int = 20
    ) -> List[Dict]:
        """GetPointDefineChapterQuestion"""
        with self._get_conn() as conn:
            rows = conn.execute(
                """SELECT * FROM questions 
                   WHERE subject=? AND grade=? AND chapter=? 
                   ORDER BY id ASC LIMIT ?""",
                (subject, grade, chapter, limit)
            ).fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    # ===== DeleteRelated =====
    def delete_question(self, question_id: str) -> bool:
        """DeleteQuestion"""
        with self._get_conn() as conn:
            cursor = conn.execute("DELETE FROM questions WHERE id=?", (question_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_questions_by_source(self, source: str) -> int:
        """BySourceDeleteQuestion"""
        with self._get_conn() as conn:
            cursor = conn.execute("DELETE FROM questions WHERE source=?", (source,))
            conn.commit()
            return cursor.rowcount
    
    # ===== ImportHistory =====
    def get_import_history(self, limit: int = 20) -> List[Dict]:
        """GetImportHistoryRecord"""
        with self._get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM import_history ORDER BY imported_at DESC LIMIT ?",
                (limit,)
            ).fetchall()
            return [dict(r) for r in rows]
    
    def clear_import_history(self):
        """ClearImportHistory"""
        with self._get_conn() as conn:
            conn.execute("DELETE FROM import_history")
            conn.commit()
    
    # ===== ToolsMethod =====
    def _row_to_dict(self, row: sqlite3.Row) -> Dict:
        """WillDataDB RowConvert ToCharacterExample"""
        d = dict(row)
        if d.get("options"):
            try:
                d["options"] = json.loads(d["options"])
            except:
                pass
        return d
    
    def question_exists(self, question_id: str) -> bool:
        """CheckQuestionYesNoStoreIn"""
        with self._get_conn() as conn:
            row = conn.execute("SELECT 1 FROM questions WHERE id=?", (question_id,)).fetchone()
            return row is not None
    
    def get_all_subjects(self) -> List[str]:
        """Get AllSubjectList"""
        with self._get_conn() as conn:
            rows = conn.execute("SELECT DISTINCT subject FROM questions WHERE subject!='' ORDER BY subject").fetchall()
            return [r["subject"] for r in rows]
    
    def get_all_grades(self, subject: Optional[str] = None) -> List[str]:
        """Get AllGradeList"""
        with self._get_conn() as conn:
            if subject:
                rows = conn.execute(
                    "SELECT DISTINCT grade FROM questions WHERE subject=? AND grade!='' ORDER BY grade",
                    (subject,)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT DISTINCT grade FROM questions WHERE grade!='' ORDER BY grade"
                ).fetchall()
            return [r["grade"] for r in rows]
    
    def get_all_chapters(self, subject: str, grade: str) -> List[str]:
        """GetPointDefineSubjectGrade's AllChapter"""
        with self._get_conn() as conn:
            rows = conn.execute(
                "SELECT DISTINCT chapter FROM questions WHERE subject=? AND grade=? AND chapter!='' ORDER BY chapter",
                (subject, grade)
            ).fetchall()
            return [r["chapter"] for r in rows]
