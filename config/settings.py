"""应用默认设置"""
import json
from .paths import APP_SETTINGS_PATH

DEFAULT_SETTINGS = {
    "app_name": "柏慧学堂",
    "version": "2.0.0",
    "theme": "light",
    "video_quality": "default",
    "auto_download": False,
    "download_path": "",  # 空=使用默认视频目录
    "ai_api_key": "",
    "ai_model": "default",
    "language": "zh-CN",
    "external_resource_paths": [
        r"E:\\空中课堂",
        r"E:\\初中课本"
    ],
}

def load_settings():
    """加载用户设置"""
    if APP_SETTINGS_PATH.exists():
        try:
            with open(APP_SETTINGS_PATH, "r", encoding="utf-8") as f:
                user_settings = json.load(f)
            DEFAULT_SETTINGS.update(user_settings)
        except Exception:
            pass
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """保存用户设置"""
    with open(APP_SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)
