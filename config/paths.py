"""
路径管理模块 - 所有路径的统一入口
遵循：打包后使用用户目录，开发时使用项目目录
"""
import sys
import json
from pathlib import Path

# ===== 判断运行模式 =====
IS_FROZEN = getattr(sys, "frozen", False)
if IS_FROZEN:
    # 打包后：使用用户AppData目录
    APPLICATION_PATH = Path.home() / "柏慧学堂数据"
else:
    # 开发模式：优先使用用户目录，兼容测试
    APPLICATION_PATH = Path.home() / "柏慧学堂数据"

# ===== 数据目录 =====
DATA_DIR = APPLICATION_PATH / "data"
VIDEOS_DIR = DATA_DIR / "videos"
PDFS_DIR = DATA_DIR / "pdfs"
STUDY_LOG_DIR = DATA_DIR / "study_logs"
INDEX_DIR = DATA_DIR / "index"
CACHE_DIR = DATA_DIR / "cache"

# ===== 配置目录 =====
CONFIG_DIR = APPLICATION_PATH / "config"
USER_CONFIG_PATH = CONFIG_DIR / "user_config.json"
APP_SETTINGS_PATH = CONFIG_DIR / "app_settings.json"

# ===== 确保目录存在 =====
for d in [DATA_DIR, VIDEOS_DIR, PDFS_DIR, STUDY_LOG_DIR, INDEX_DIR, CACHE_DIR, CONFIG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ===== 外部资源路径（可配置）=====
EXTERNAL_RESOURCE_PATHS = [
    Path("~/空中课堂").expanduser(),
    Path("~/初中课本").expanduser(),
]

# ===== 数据库路径 =====
STUDY_DB_PATH = DATA_DIR / "study.db"

# ===== 工具函数 =====
def get_app_dir():
    """获取应用根目录"""
    return APPLICATION_PATH

def get_data_file(relative_path):
    """获取数据文件完整路径"""
    return DATA_DIR / relative_path

def is_local_resource_available(path):
    """检查本地资源是否存在"""
    p = Path(path)
    return p.exists() and p.is_file()

def ensure_dirs():
    """确保所有必要目录存在"""
    for d in [DATA_DIR, VIDEOS_DIR, PDFS_DIR, STUDY_LOG_DIR, INDEX_DIR, CACHE_DIR, CONFIG_DIR]:
        d.mkdir(parents=True, exist_ok=True)
