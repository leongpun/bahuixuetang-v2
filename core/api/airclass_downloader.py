"""
OnSeaAirClassInLineDownload
"""
import requests
import os
import json
import time
from pathlib import Path
from urllib.parse import quote


class AirClassDownloader:
    """OnSeaAirClassVideoDownload"""

    BASE_URL = "https://shd-assets.eduyun.cn/onlineClass"

    def __init__(self, save_dir=None, timeout=30):
        self.save_dir = Path(save_dir) if save_dir else Path.home() / "柏慧学堂Data" / "videos"
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.timeout = timeout
        self.session = requests.Session()
        self.session.verify = False  # OnSeaEducation CloudPlatformCertificateAskQuestion
        self.session.trust_env = False

    def get_course_list(self, stage, subject):
        """GetCourseList"""
        try:
            url = f"{self.BASE_URL}/stage/stageInfo"
            params = {"stage": stage, "subject": subject}
            resp = self.session.get(url, params=params, timeout=self.timeout)
            data = resp.json()
            if data.get("code") == 200:
                return data.get("data", [])
            return []
        except Exception as e:
            print(f"GetCourseListFailed: {e}")
            return []

    def get_resource_url(self, resource_id):
        """GetResourceDownloadAddress"""
        try:
            url = f"{self.BASE_URL}/resource/resourceInfo"
            params = {"resourceId": resource_id}
            resp = self.session.get(url, params=params, timeout=self.timeout)
            data = resp.json()
            if data.get("code") == 200:
                return data.get("data", {})
            return {}
        except Exception as e:
            print(f"GetResourceInfoFailed: {e}")
            return {}

    def download_video(self, lesson_info, output_path=None):
        """DownloadSingleItemVideo"""
        try:
            # lesson_info should contain the download URL
            video_url = lesson_info.get("url") or lesson_info.get("downloadUrl")
            if not video_url:
                return False, "No download URL found"

            if output_path is None:
                filename = lesson_info.get("title", "lesson") + ".mp4"
                output_path = self.save_dir / filename

            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Download with progress
            resp = self.session.get(video_url, stream=True, timeout=self.timeout)
            total = int(resp.headers.get("content-length", 0))
            downloaded = 0
            with open(output_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total > 0:
                            pct = downloaded * 100 // total
                            print(f"  Download: {pct}% ({downloaded}/{total})")

            return True, str(output_path)
        except Exception as e:
            return False, str(e)

    def update_courses(self, grade, subject, term="Term 1"):
        """MoreNewSomeItemGradeSomeSubjectCourse"""
        stage_map = {"Grade 6": "6", "Grade 7": "7", "Grade 8": "8", "Grade 9": "9"}
        stage = stage_map.get(grade)
        if not stage:
            return []

        courses = self.get_course_list(stage, subject)
        results = []
        for course in courses:
            title = course.get("title", "")
            # Skip if already downloaded
            existing = self.save_dir / f"{title}.mp4"
            if existing.exists():
                results.append({"title": title, "status": "exists", "path": str(existing)})
                continue
            # Download
            ok, path = self.download_video(course)
            results.append({"title": title, "status": "downloaded" if ok else "failed", "path": path if ok else ""})
            if ok:
                time.sleep(1)  # AvoidPleaseRequest Too Fast
        return results
