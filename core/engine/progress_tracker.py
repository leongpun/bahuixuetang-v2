"""
学习进度追踪
"""
from datetime import datetime
from core.storage.database import StudyDatabase


class ProgressTracker:
    """学习进度追踪器"""

    def __init__(self, db=None):
        self.db = db or StudyDatabase()

    def start_lesson(self, subject, grade, term, chapter, lesson, resource_path=None):
        self.db.save_progress(subject, grade, term, chapter, lesson, resource_path, "in_progress", 0)

    def update_progress(self, subject, grade, term, chapter, lesson, pct):
        self.db.save_progress(subject, grade, term, chapter, lesson, None, "in_progress", pct)

    def complete_lesson(self, subject, grade, term, chapter, lesson):
        self.db.save_progress(subject, grade, term, chapter, lesson, None, "completed", 100)

    def get_dashboard(self):
        """获取学习仪表盘数据"""
        all_progress = self.db.get_all_progress()
        completed = sum(1 for p in all_progress if p["status"] == "completed")
        in_progress = sum(1 for p in all_progress if p["status"] == "in_progress")
        recent = sorted(all_progress, key=lambda x: x.get("last_watched", ""), reverse=True)[:10]
        
        # 统计章节总数（唯一章节组合）
        chapter_keys = set()
        for p in all_progress:
            key = (p["subject_code"], p["grade"], p["term"], p["chapter"])
            chapter_keys.add(key)
        
        stats = {
            "total_chapters": len(chapter_keys),
            "total_lessons": len(all_progress),
            "completed": completed,
            "in_progress": in_progress,
            "pending": len(all_progress) - completed - in_progress,
            "recent": recent,
        }
        return stats
