"""
题库管理模块 - 题目管理、检索、统计
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
    """题目统计数据"""
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
    """题库管理器"""
    
    def __init__(self, db_path=None):
        self.db_path = Path(db_path) if db_path else Path.home() / "柏慧学堂_data" / "quiz.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_tables()
    
    def _get_conn(self):
        """获取数据库连接"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_tables(self):
        """初始化数据库表"""
        with self._get_conn() as conn:
            # 题目表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    id TEXT PRIMARY KEY,
                    subject TEXT NOT NULL,
                    grade TEXT NOT NULL,
                    chapter TEXT,
                    question_type TEXT DEFAULT '未知',
                    question TEXT NOT NULL,
                    options TEXT,
                    answer TEXT,
                    explanation TEXT,
                    source TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # 导入历史表
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
    
    # ===== 导入相关 =====
    def import_questions(self, filepath: str) -> Dict:
        """导入题目文件，返回结果"""
        from core.storage.quiz_importer import QuizImporter
        
        importer = QuizImporter()
        result = importer.import_file(filepath)
        
        if not result["success"]:
            return result
        
        questions = result.get("questions", [])
        
        # 保存到数据库
        saved = self._save_questions(questions)
        
        # 记录导入历史
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
        """保存题目到数据库"""
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
                    print(f"保存题目失败: {e}")
        return saved
    
    # ===== 查询相关 =====
    def get_question(self, question_id: str) -> Optional[Dict]:
        """获取单个题目"""
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
        """查询题目列表（支持筛选）"""
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
        """搜索题目（按关键词）"""
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
    
    # ===== 统计相关 =====
    def get_stats(self) -> QuizStats:
        """获取题目统计信息"""
        stats = QuizStats()
        
        with self._get_conn() as conn:
            # 总数
            row = conn.execute("SELECT COUNT(*) as count FROM questions").fetchone()
            stats.total = row["count"] if row else 0
            
            # 按学科统计
            rows = conn.execute("SELECT subject, COUNT(*) as count FROM questions GROUP BY subject").fetchall()
            stats.by_subject = {r["subject"]: r["count"] for r in rows}
            
            # 按年级统计
            rows = conn.execute("SELECT grade, COUNT(*) as count FROM questions GROUP BY grade").fetchall()
            stats.by_grade = {r["grade"]: r["count"] for r in rows}
            
            # 按章节统计
            rows = conn.execute("SELECT chapter, COUNT(*) as count FROM questions WHERE chapter IS NOT NULL AND chapter != '' GROUP BY chapter").fetchall()
            stats.by_chapter = {r["chapter"]: r["count"] for r in rows}
            
            # 按题型统计
            rows = conn.execute("SELECT question_type, COUNT(*) as count FROM questions GROUP BY question_type").fetchall()
            stats.by_type = {r["question_type"]: r["count"] for r in rows}
        
        return stats
    
    def get_subject_stats(self, subject: str) -> Dict:
        """获取学科维度的统计"""
        with self._get_conn() as conn:
            # 各年级数量
            rows = conn.execute(
                "SELECT grade, COUNT(*) as count FROM questions WHERE subject=? GROUP BY grade",
                (subject,)
            ).fetchall()
            by_grade = {r["grade"]: r["count"] for r in rows}
            
            # 各题型数量
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
    
    # ===== 随机抽题 =====
    def get_random_questions(
        self,
        subject: str,
        grade: str,
        count: int = 10,
        exclude_ids: Optional[List[str]] = None
    ) -> List[Dict]:
        """随机抽取题目"""
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
        """获取指定章节的题目"""
        with self._get_conn() as conn:
            rows = conn.execute(
                """SELECT * FROM questions 
                   WHERE subject=? AND grade=? AND chapter=? 
                   ORDER BY id ASC LIMIT ?""",
                (subject, grade, chapter, limit)
            ).fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    # ===== 删除相关 =====
    def delete_question(self, question_id: str) -> bool:
        """删除题目"""
        with self._get_conn() as conn:
            cursor = conn.execute("DELETE FROM questions WHERE id=?", (question_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_questions_by_source(self, source: str) -> int:
        """按来源删除题目"""
        with self._get_conn() as conn:
            cursor = conn.execute("DELETE FROM questions WHERE source=?", (source,))
            conn.commit()
            return cursor.rowcount
    
    # ===== 导入历史 =====
    def get_import_history(self, limit: int = 20) -> List[Dict]:
        """获取导入历史记录"""
        with self._get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM import_history ORDER BY imported_at DESC LIMIT ?",
                (limit,)
            ).fetchall()
            return [dict(r) for r in rows]
    
    def clear_import_history(self):
        """清空导入历史"""
        with self._get_conn() as conn:
            conn.execute("DELETE FROM import_history")
            conn.commit()
    
    # ===== 工具方法 =====
    def _row_to_dict(self, row: sqlite3.Row) -> Dict:
        """将数据库行转换为字典"""
        d = dict(row)
        if d.get("options"):
            try:
                d["options"] = json.loads(d["options"])
            except:
                pass
        return d
    
    def question_exists(self, question_id: str) -> bool:
        """检查题目是否存在"""
        with self._get_conn() as conn:
            row = conn.execute("SELECT 1 FROM questions WHERE id=?", (question_id,)).fetchone()
            return row is not None
    
    def get_all_subjects(self) -> List[str]:
        """获取所有学科列表"""
        with self._get_conn() as conn:
            rows = conn.execute("SELECT DISTINCT subject FROM questions WHERE subject!='' ORDER BY subject").fetchall()
            return [r["subject"] for r in rows]
    
    def get_all_grades(self, subject: Optional[str] = None) -> List[str]:
        """获取所有年级列表"""
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
        """获取指定学科年级的所有章节"""
        with self._get_conn() as conn:
            rows = conn.execute(
                "SELECT DISTINCT chapter FROM questions WHERE subject=? AND grade=? AND chapter!='' ORDER BY chapter",
                (subject, grade)
            ).fetchall()
            return [r["chapter"] for r in rows]
