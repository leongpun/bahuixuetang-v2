"""
PathManageModule - Unified Entry for All Paths
Follow：After PackagingUse UserDirectory，During DevelopmentUseProjectDirectory
"""
import sys
import json
from pathlib import Path

# ===== JudgeRunMode =====
IS_FROZEN = getattr(sys, "frozen", False)
if IS_FROZEN:
    # After Packaging：Use UserAppDataDirectory
    APPLICATION_PATH = Path.home() / "柏慧学堂Data"
else:
    # Development Mode：PriorityUse UserDirectory，Compatibility Test
    APPLICATION_PATH = Path.home() / "柏慧学堂Data"

# ===== DataDirectory =====
DATA_DIR = APPLICATION_PATH / "data"
VIDEOS_DIR = DATA_DIR / "videos"
PDFS_DIR = DATA_DIR / "pdfs"
STUDY_LOG_DIR = DATA_DIR / "study_logs"
INDEX_DIR = DATA_DIR / "index"
CACHE_DIR = DATA_DIR / "cache"

# ===== ConfigureDirectory =====
CONFIG_DIR = APPLICATION_PATH / "config"
USER_CONFIG_PATH = CONFIG_DIR / "user_config.json"
APP_SETTINGS_PATH = CONFIG_DIR / "app_settings.json"

# ===== EnsureDirectoryStoreIn =====
for d in [DATA_DIR, VIDEOS_DIR, PDFS_DIR, STUDY_LOG_DIR, INDEX_DIR, CACHE_DIR, CONFIG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ===== External Resource Paths（CanConfigure）=====
EXTERNAL_RESOURCE_PATHS = [
    Path("~/AirClass").expanduser(),
    Path("~/JuniorHighTextbook").expanduser(),
]

# ===== DataLibraryPath =====
STUDY_DB_PATH = DATA_DIR / "study.db"

# ===== ToolsFunction =====
def get_app_dir():
    """Get App RootDirectory"""
    return APPLICATION_PATH

def get_data_file(relative_path):
    """Get Complete Path for Data Files"""
    return DATA_DIR / relative_path

def is_local_resource_available(path):
    """CheckLocal ResourcesYesNoStoreIn"""
    p = Path(path)
    return p.exists() and p.is_file()

def ensure_dirs():
    """Ensure All NecessaryDirectoryStoreIn"""
    for d in [DATA_DIR, VIDEOS_DIR, PDFS_DIR, STUDY_LOG_DIR, INDEX_DIR, CACHE_DIR, CONFIG_DIR]:
        d.mkdir(parents=True, exist_ok=True)
