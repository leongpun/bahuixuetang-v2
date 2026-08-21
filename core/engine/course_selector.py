"""
课程选择器 - 基于实际目录结构
结构: 学科 -> 年级 -> 学期 -> 章(子目录) -> 课时(mp4文件)
"""
import os
import re
from pathlib import Path
from config.courses import SUBJECTS, TERMS
from core.api.local_scanner import LocalResourceScanner
from config.settings import load_settings


class CourseSelector:
    """基于目录结构的课程选择器"""

    def __init__(self, scanner=None):
        self.scanner = scanner or LocalResourceScanner()
        self.settings = load_settings()

    # ========== 基础信息 ==========
    def get_subjects(self):
        return list(SUBJECTS.keys())

    def get_grade_levels(self, subject_code):
        return SUBJECTS.get(subject_code, {}).get("grades", [])

    def get_terms(self):
        return TERMS

    # ========== 核心方法 ==========
    def _get_all_mp4_recursive(self, dir_path):
        """递归扫描目录下所有mp4文件"""
        mp4_files = []
        if not os.path.exists(dir_path):
            return mp4_files
        
        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            if os.path.isfile(item_path) and item.lower().endswith('.mp4'):
                mp4_files.append(item)
            elif os.path.isdir(item_path):
                # 递归扫描子目录
                mp4_files.extend(self._get_all_mp4_recursive(item_path))
        
        return sorted(mp4_files)

    def get_chapters(self, subject_code, grade, term):
        """获取章节列表（扫描学期目录下的子目录）"""
        # 构建学期目录路径
        term_path = self._get_term_path(subject_code, grade, term)
        if not term_path or not os.path.exists(term_path):
            return []
        
        chapters = []
        
        # 扫描子目录作为章节
        for item in sorted(os.listdir(term_path)):
            item_path = os.path.join(term_path, item)
            
            # 只处理目录
            if not os.path.isdir(item_path):
                continue
            
            # 统计该目录下的mp4文件（递归扫描）
            mp4_files = self._get_all_mp4_recursive(item_path)
            
            if mp4_files:
                chapters.append({
                    "number": self._extract_number(item),
                    "title": item,  # 直接使用目录名作为章节标题
                    "videos": [
                        {
                            "title": f.replace('.mp4', ''),
                            "path": self._find_mp4_path(item_path, f)
                        }
                        for f in mp4_files
                    ]
                })
        
        return chapters

    def _get_term_path(self, subject_code, grade, term):
        """动态查找学期目录路径 - 支持任意目录层级"""
        from config.settings import load_settings
        
        subject_name = SUBJECTS.get(subject_code, {}).get("name", subject_code)
        settings = load_settings()
        
        # 从配置获取搜索路径
        search_paths = settings.get("external_resource_paths", [
            r"E:\空中课堂",
            r"E:\初中课本"
        ])
        
        # 匹配学期名称变体
        term_variants = [term, "第一学期", "第二学期", "上学期", "下学期"]
        
        for base_path in search_paths:
            base_path = Path(base_path).expanduser()
            if not base_path.exists():
                continue
            
            # 递归查找匹配的目录
            for root, dirs, files in os.walk(base_path):
                root_str = str(root).replace('\\', '/')
                
                # 检查是否包含所有关键词
                if (subject_name in root_str and 
                    grade in root_str and
                    any(t in root_str for t in term_variants)):
                    return root
        
        return None

    def _extract_number(self, name):
        """从目录名提取数字编号"""
        match = re.search(r'^(\d+)', name)
        return match.group(1) if match else "999"

    def _find_mp4_path(self, base_dir, filename):
        """递归查找mp4文件的完整路径"""
        if not os.path.exists(base_dir):
            return None
        
        # 直接在当前目录查找
        full_path = os.path.join(base_dir, filename)
        if os.path.exists(full_path):
            return full_path
        
        # 在子目录中查找
        for item in os.listdir(base_dir):
            item_path = os.path.join(base_dir, item)
            if os.path.isdir(item_path):
                result = self._find_mp4_path(item_path, filename)
                if result:
                    return result
        
        return None

    # ========== 兼容接口 ==========
    def get_available_lessons(self, subject_code, grade, term):
        """兼容旧接口"""
        return self.get_chapters(subject_code, grade, term)

    def get_lesson_details(self, subject_code, grade, term, chapter_key):
        """获取单章节详情"""
        for ch in self.get_chapters(subject_code, grade, term):
            if ch["number"] == chapter_key or ch["title"] == chapter_key:
                return ch
        return None
