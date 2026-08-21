"""
SQLite数据库封装 - 学习进度、错题本、收藏
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime
from config.paths import STUDY_DB_PATH


class StudyDatabase:
    def __init__(self, db_path=None):
        self.db_path = Path(db_path) if db_path else STUDY_DB_PATH
        self._init_tables()

    def _get_conn(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_tables(self):
        """初始化所有表"""
        with self._get_conn() as conn:
            # 学习进度表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS study_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject_code TEXT NOT NULL,
                    grade TEXT NOT NULL,
                    term TEXT NOT NULL,
                    chapter TEXT NOT NULL,
                    lesson_name TEXT NOT NULL,
                    resource_path TEXT,
                    status TEXT DEFAULT 'pending',
                    progress_pct REAL DEFAULT 0,
                    last_watched TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(subject_code, grade, term, chapter, lesson_name)
                )
            """)
            # 错题本表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS error_book (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject_code TEXT NOT NULL,
                    grade TEXT NOT NULL,
                    chapter TEXT TEXT,
                    question TEXT NOT NULL,
                    options TEXT,
                    correct_answer TEXT,
                    user_answer TEXT,
                    analysis TEXT,
                    difficulty INTEGER DEFAULT 1,
                    count_wrong INTEGER DEFAULT 1,
                    last_wrong TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    resolved BOOLEAN DEFAULT 0
                )
            """)
            # 收藏表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS favorites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject_code TEXT NOT NULL,
                    grade TEXT NOT NULL,
                    term TEXT NOT NULL,
                    lesson_name TEXT NOT NULL,
                    resource_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(subject_code, grade, term, lesson_name)
                )
            """)
            # AI诊断记录表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ai_diagnosis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject_code TEXT,
                    grade TEXT,
                    weakness_area TEXT,
                    diagnosis_result TEXT,
                    suggested_topics TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    # ===== 学习进度操作 =====
    def save_progress(self, subject, grade, term, chapter, lesson, resource_path=None, status="in_progress", pct=0):
        with self._get_conn() as conn:
            conn.execute("""
                INSERT INTO study_progress (subject_code, grade, term, chapter, lesson_name, resource_path, status, progress_pct, last_watched)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(subject_code, grade, term, chapter, lesson_name)
                DO UPDATE SET status=excluded.status, progress_pct=excluded.progress_pct, last_watched=excluded.last_watched, updated_at=CURRENT_TIMESTAMP
            """, (subject, grade, term, chapter, lesson, resource_path, status, pct, datetime.now()))
            conn.commit()

    def get_progress(self, subject, grade, term=None):
        with self._get_conn() as conn:
            if term:
                rows = conn.execute(
                    "SELECT * FROM study_progress WHERE subject_code=? AND grade=? AND term=?",
                    (subject, grade, term)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM study_progress WHERE subject_code=? AND grade=?",
                    (subject, grade)
                ).fetchall()
            return [dict(r) for r in rows]

    def get_all_progress(self):
        with self._get_conn() as conn:
            rows = conn.execute("SELECT * FROM study_progress ORDER BY last_watched DESC").fetchall()
            return [dict(r) for r in rows]

    def get_completion_rate(self, subject, grade, term=None):
        progress = self.get_progress(subject, grade, term)
        if not progress:
            return 0
        completed = sum(1 for p in progress if p["status"] == "completed" and p["progress_pct"] >= 100)
        return round(completed / len(progress) * 100, 1)

    # ===== 错题本操作 =====
    def add_error(self, subject, grade, chapter, question, options=None, correct=None, user_ans=None, analysis=None, difficulty=1):
        with self._get_conn() as conn:
            conn.execute("""
                INSERT INTO error_book (subject_code, grade, chapter, question, options, correct_answer, user_answer, analysis, difficulty)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (subject, grade, chapter, question, json.dumps(options) if options else None, correct, user_ans, analysis, difficulty))
            conn.commit()

    def get_errors(self, subject=None, resolved=False):
        with self._get_conn() as conn:
            if subject:
                rows = conn.execute("SELECT * FROM error_book WHERE subject_code=? AND resolved=0 ORDER BY last_wrong DESC", (subject,)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM error_book WHERE resolved=0 ORDER BY last_wrong DESC").fetchall()
            result = []
            for r in rows:
                d = dict(r)
                if d.get("options"):
                    try: d["options"] = json.loads(d["options"])
                    except: pass
                result.append(d)
            return result

    def resolve_error(self, error_id):
        with self._get_conn() as conn:
            conn.execute("UPDATE error_book SET resolved=1, count_wrong=count_wrong+1 WHERE id=?", (error_id,))
            conn.commit()

    def get_error_stats(self):
        with self._get_conn() as conn:
            row = conn.execute("""
                SELECT subject_code, COUNT(*) as total, SUM(count_wrong) as total_wrong
                FROM error_book WHERE resolved=0 GROUP BY subject_code
            """).fetchone()
            return dict(row) if row else {}

    # ===== 收藏操作 =====
    def toggle_favorite(self, subject, grade, term, lesson, resource_path=None):
        with self._get_conn() as conn:
            try:
                conn.execute(
                    "INSERT INTO favorites (subject_code, grade, term, lesson_name, resource_path) VALUES (?,?,?,?,?)",
                    (subject, grade, term, lesson, resource_path)
                )
                return True
            except sqlite3.IntegrityError:
                conn.execute("DELETE FROM favorites WHERE subject_code=? AND grade=? AND term=? AND lesson_name=?",
                             (subject, grade, term, lesson))
                return False

    def get_favorites(self):
        with self._get_conn() as conn:
            rows = conn.execute("SELECT * FROM favorites ORDER BY created_at DESC").fetchall()
            return [dict(r) for r in rows]

    # ===== AI诊断操作 =====
    def save_diagnosis(self, subject, grade, weakness, result, topics):
        with self._get_conn() as conn:
            conn.execute("""
                INSERT INTO ai_diagnosis (subject_code, grade, weakness_area, diagnosis_result, suggested_topics)
                VALUES (?, ?, ?, ?, ?)
            """, (subject, grade, weakness, result, json.dumps(topics) if topics else None))
            conn.commit()

    def get_diagnosis_history(self, subject=None):
        with self._get_conn() as conn:
            if subject:
                rows = conn.execute("SELECT * FROM ai_diagnosis WHERE subject_code=? ORDER BY created_at DESC LIMIT 10", (subject,)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM ai_diagnosis ORDER BY created_at DESC LIMIT 20").fetchall()
            result = []
            for r in rows:
                d = dict(r)
                if d.get("suggested_topics"):
                    try: d["suggested_topics"] = json.loads(d["suggested_topics"])
                    except: pass
                result.append(d)
            return result
