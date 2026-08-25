"""
Local ResourcesScan - DynamicScanEDiskExternalPath
"""
import os
import json
from pathlib import Path
from datetime import datetime


class LocalResourceScanner:
    """ScanLocalVideo/PDFResource，BuildCourse-FileMap"""

    def __init__(self):
        self._cache = {}
        self._last_scan_time = 0
        self._search_paths = [
            Path(r"E:\AirClass"),
            Path(r"E:\JuniorHighTextbook"),
        ]

    def set_search_paths(self, paths):
        """DynamicSettingsSearchPath（SupportUserConfigure）"""
        self._search_paths = [Path(p) for p in paths if Path(p).exists()]

    def scan(self):
        """Execute CompleteScan"""
        result = {"videos": [], "pdfs": [], "scanned_at": datetime.now().isoformat(), "stats": {}}
        path_stats = {}
        for base_path in self._search_paths:
            if not base_path.exists():
                continue
            count = {"videos": 0, "pdfs": 0}
            for root, dirs, files in os.walk(base_path):
                rel = os.path.relpath(root, base_path)
                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    full_path = os.path.join(root, f)
                    entry = {
                        "filename": f,
                        "path": full_path,
                        "relative": rel,
                        "parent_dir": os.path.basename(root),
                        "size_mb": round(os.path.getsize(full_path) / 1024 / 1024, 1),
                    }
                    if ext == ".mp4":
                        entry["type"] = "video"
                        result["videos"].append(entry)
                        count["videos"] += 1
                    elif ext == ".pdf":
                        entry["type"] = "pdf"
                        result["pdfs"].append(entry)
                        count["pdfs"] += 1
            path_stats[str(base_path)] = count
        result["stats"] = path_stats
        result["total_videos"] = len(result["videos"])
        result["total_pdfs"] = len(result["pdfs"])
        self._cache = result
        self._last_scan_time = datetime.now()
        return result

    def find_videos_by_subject_grade_term(self, subject, grade, term=None):
        """BySubject/Grade/TermFilterVideo"""
        self._ensure_scanned()
        # subject code -> Chinese name mapping
        subject_name_map = {"math": "Math", "chinese": "Chinese", "english": "English"}
        subject_cn = subject_name_map.get(subject, subject)
        results = []
        for v in self._cache.get("videos", []):
            path = v["path"]
            # Match by Chinese subject name, grade, and optionally term
            if (subject_cn in path and
                grade in path and
                (term is None or term in path)):
                results.append(v)
        return results

    def find_pdf_by_subject_grade(self, subject, grade):
        """BySubject/GradeFindTextbookPDF"""
        self._ensure_scanned()
        results = []
        for p in self._cache.get("pdfs", []):
            if subject.lower() in p["path"].lower() and grade.lower() in p["path"].lower():
                results.append(p)
        return results

    def get_video(self, path):
        """GetSingleItemVideo"""
        self._ensure_scanned()
        for v in self._cache.get("videos", []):
            if v["path"] == path:
                return v
        # AlsoMayNotInCacheStoreIn，DirectCheck
        if os.path.exists(path):
            return {"filename": os.path.basename(path), "path": path, "type": "video", "size_mb": round(os.path.getsize(path) / 1024 / 1024, 1)}
        return None

    def _ensure_scanned(self):
        """LazyLoadScan"""
        if not self._cache:
            self.scan()

    def refresh(self):
        """ForceSystemAgainNewScan"""
        self._cache = {}
        return self.scan()
