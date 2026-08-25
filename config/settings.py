"""ShouldUseDefaultSettings"""
import json
from .paths import APP_SETTINGS_PATH

DEFAULT_SETTINGS = {
    "app_name": "柏慧学堂",
    "version": "2.0.0",
    "theme": "light",
    "video_quality": "default",
    "auto_download": False,
    "download_path": "",  # Empty=UseDefaultVideoDirectory
    "ai_api_key": "",
    "ai_model": "default",
    "language": "zh-CN",
    "external_resource_paths": [
        r"E:\\AirClass",
        r"E:\\JuniorHighTextbook"
    ],
}

def load_settings():
    """LoadUserSettings"""
    if APP_SETTINGS_PATH.exists():
        try:
            with open(APP_SETTINGS_PATH, "r", encoding="utf-8") as f:
                user_settings = json.load(f)
            DEFAULT_SETTINGS.update(user_settings)
        except Exception:
            pass
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """SaveUserSettings"""
    with open(APP_SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)
