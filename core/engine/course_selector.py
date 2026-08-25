"""
CourseSelect - Based OnActualDirectoryStructure
Structure: Subject -> Grade -> Term -> Chapter(ChildDirectory) -> Lesson(mp4File)
"""
import os
import re
from pathlib import Path
from config.courses import SUBJECTS, TERMS
from core.api.local_scanner import LocalResourceScanner
from config.settings import load_settings


class CourseSelector:
    """Based OnDirectoryStructureCourseSelect"""

    def __init__(self, scanner=None):
        self.scanner = scanner or LocalResourceScanner()
        self.settings = load_settings()

    # ========== BasicInfo ==========
    def get_subjects(self):
        return list(SUBJECTS.keys())

    def get_grade_levels(self, subject_code):
        return SUBJECTS.get(subject_code, {}).get("grades", [])

    def get_terms(self):
        return TERMS

    # ========== Core Method ==========
    def _get_all_mp4_recursive(self, dir_path):
        """RecursiveScanDirectoryBelowAllHavemp4File"""
        mp4_files = []
        if not os.path.exists(dir_path):
            return mp4_files
        
        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            if os.path.isfile(item_path) and item.lower().endswith('.mp4'):
                mp4_files.append(item)
            elif os.path.isdir(item_path):
                # RecursiveScanChildDirectory
                mp4_files.extend(self._get_all_mp4_recursive(item_path))
        
        return sorted(mp4_files)

    def get_chapters(self, subject_code, grade, term):
        """GetChapterList（ScanTermDirectory'sChildDirectory）"""
        # BuildTermDirectoryPath
        term_path = self._get_term_path(subject_code, grade, term)
        if not term_path or not os.path.exists(term_path):
            return []
        
        chapters = []
        
        # ScanChildDirectoryWorkForChapter
        for item in sorted(os.listdir(term_path)):
            item_path = os.path.join(term_path, item)
            
            # OnlyProcessDirectory
            if not os.path.isdir(item_path):
                continue
            
            # StatisticsTheDirectory'smp4File（RecursiveScan）
            mp4_files = self._get_all_mp4_recursive(item_path)
            
            if mp4_files:
                chapters.append({
                    "number": self._extract_number(item),
                    "title": item,  # DirectUseDirectoryNameWorkForChapterTitle
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
        """DynamicFindTermDirectoryPath - SupportAnyDirectoryLevel"""
        from config.settings import load_settings
        
        subject_name = SUBJECTS.get(subject_code, {}).get("name", subject_code)
        settings = load_settings()
        
        # FromConfigureGetSearchPath
        search_paths = settings.get("external_resource_paths", [
            r"E:\AirClass",
            r"E:\JuniorHighTextbook"
        ])
        
        # MatchTermNameVariant
        term_variants = [term, "Term 1", "Term 2", "OnTerm", "BelowTerm"]
        
        for base_path in search_paths:
            base_path = Path(base_path).expanduser()
            if not base_path.exists():
                continue
            
            # RecursiveFindMatchingDirectory
            for root, dirs, files in os.walk(base_path):
                root_str = str(root).replace('\\', '/')
                
                # CheckYesNoInclude AllHaveKeyword
                if (subject_name in root_str and 
                    grade in root_str and
                    any(t in root_str for t in term_variants)):
                    return root
        
        return None

    def _extract_number(self, name):
        """FromDirectoryNameExtractCountCharacterEncodeNumber"""
        match = re.search(r'^(\d+)', name)
        return match.group(1) if match else "999"

    def _find_mp4_path(self, base_dir, filename):
        """RecursiveFindmp4FileCompletePath"""
        if not os.path.exists(base_dir):
            return None
        
        # DirectInCurrentDirectoryFind
        full_path = os.path.join(base_dir, filename)
        if os.path.exists(full_path):
            return full_path
        
        # InChildDirectoryInFind
        for item in os.listdir(base_dir):
            item_path = os.path.join(base_dir, item)
            if os.path.isdir(item_path):
                result = self._find_mp4_path(item_path, filename)
                if result:
                    return result
        
        return None

    # ========== CompatibleContentInterface ==========
    def get_available_lessons(self, subject_code, grade, term):
        """CompatibleContentOld Interface"""
        return self.get_chapters(subject_code, grade, term)

    def get_lesson_details(self, subject_code, grade, term, chapter_key):
        """GetSingleChapterDetails"""
        for ch in self.get_chapters(subject_code, grade, term):
            if ch["number"] == chapter_key or ch["title"] == chapter_key:
                return ch
        return None
