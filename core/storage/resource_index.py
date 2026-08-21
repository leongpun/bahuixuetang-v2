"""
本地资源索引 - 缓存E盘扫描结果，避免重复IO
"""
import json
import time
import os
from pathlib import Path
from datetime import datetime
from config.paths import INDEX_DIR


class ResourceIndex:
    def __init__(self, index_dir=None):
        self.index_dir = Path(index_dir) if index_dir else INDEX_DIR
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.index_dir / "resource_index.json"
        self._data = {}
        self._loaded = False

    def _load(self):
        if self._loaded:
            return
        if self.index_file.exists():
            try:
                with open(self.index_file, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception:
                self._data = {}
        self._loaded = True

    def _save(self):
        self.index_file.write_text(json.dumps(self._data, ensure_ascii=False, indent=2), encoding="utf-8")

    def scan_external_drives(self, search_paths):
        """扫描外部资源路径，构建索引"""
        index = {"scanned_at": datetime.now().isoformat(), "paths": {}, "videos": {}, "pdfs": {}}
        for base_path in search_paths:
            base = Path(base_path)
            if not base.exists():
                continue
            index["paths"][str(base)] = True
            for root, dirs, files in os.walk(base):
                rel = os.path.relpath(root, base)
                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    full_path = os.path.join(root, f)
                    key = f"{base}/{rel}/{f}"
                    if ext == ".mp4":
                        index["videos"][key] = {
                            "path": full_path,
                            "size_mb": round(os.path.getsize(full_path) / 1024 / 1024, 1),
                            "relative": f"{rel}/{f}",
                            "parent_dir": rel,
                        }
                    elif ext == ".pdf":
                        index["pdfs"][key] = {
                            "path": full_path,
                            "size_mb": round(os.path.getsize(full_path) / 1024 / 1024, 1),
                            "relative": f"{rel}/{f}",
                            "parent_dir": rel,
                        }
        # Merge with existing
        for k, v in index["videos"].items():
            self._data.setdefault("videos", {})[k] = v
        for k, v in index["pdfs"].items():
            self._data.setdefault("pdfs", {})[k] = v
        self._data["scanned_at"] = datetime.now().isoformat()
        self._save()
        return index

    def find_video(self, keyword):
        """按关键词搜索本地视频"""
        self._load()
        results = []
        for path, info in self._data.get("videos", {}).items():
            if keyword.lower() in path.lower() or keyword.lower() in info.get("relative", "").lower():
                results.append(info)
        return results

    def find_pdf(self, keyword):
        """按关键词搜索本地PDF"""
        self._load()
        results = []
        for path, info in self._data.get("pdfs", {}).items():
            if keyword.lower() in path.lower() or keyword.lower() in info.get("relative", "").lower():
                results.append(info)
        return results

    def get_all_videos(self):
        self._load()
        return list(self._data.get("videos", {}).values())

    def get_all_pdfs(self):
        self._load()
        return list(self._data.get("pdfs", {}).values())

    def is_available(self, path):
        """检查文件是否存在"""
        return os.path.exists(path)

    def refresh(self, search_paths):
        """强制刷新索引"""
        self._data = {}
        self._loaded = False
        return self.scan_external_drives(search_paths)
