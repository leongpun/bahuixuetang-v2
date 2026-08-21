# 柏慧学堂 v2 - 完整架构设计文档

## 项目概览
面向初中生的离线自学App，整合上海空中课堂视频+课本PDF+AI诊断。

## 技术栈
- Python 3.13 + CustomTkinter (GUI)
- SQLite (本地数据) + JSON (配置)
- PyInstaller (打包为exe)
- mpv / VLC (视频播放，通过subprocess)
- requests (线上下载)

## 目录结构
```
baihuixuetang_v2/
├── run_app.py                  # 主入口
├── build_app.py                # PyInstaller打包脚本
├── config/
│   ├── __init__.py
│   ├── paths.py                # 统一路径管理（IS_FROZEN检测）
│   ├── courses.py              # 课程数据结构（硬编码教材结构）
│   └── settings.py             # 应用设置默认值
├── core/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── local_scanner.py    # E盘资源扫描与索引构建
│   │   ├── airclass_downloader.py  # 上海空中课堂API下载
│   │   └── ai_service.py       # AI诊断服务（Sapiens API）
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── database.py         # SQLite封装（学习进度/错题本/收藏）
│   │   ├── resource_index.py   # 本地资源索引（缓存扫描结果）
│   │   └── user_config.py      # 用户配置（JSON持久化）
│   └── engine/
│       ├── __init__.py
│       ├── course_selector.py  # 课程选择逻辑（按年级/学科/学期）
│       ├── lesson_player.py    # 视频/文档播放器协调
│       └── progress_tracker.py # 学习进度追踪
├── ui/
│   ├── __init__.py
│   ├── main_window.py          # 主窗口（侧边栏导航）
│   ├── components/
│   │   ├── __init__.py
│   │   ├── course_tree.py      # 课程树组件（教材结构）
│   │   ├── video_player.py     # 视频播放组件（mpv嵌入）
│   │   ├── pdf_viewer.py       # PDF查看组件
│   │   ├── quiz_panel.py       # 题库练习面板
│   │   ├── ai_diagnosis.py     # AI诊断面板
│   │   ├── error_book.py       # 错题本面板
│   │   └── settings_panel.py   # 设置面板
│   └── styles.py               # 统一样式定义
├── tests/
│   ├── __init__.py
│   ├── test_scan.py            # 扫描测试
│   └── test_api.py             # API测试
└── resources/
    ├── icons/                  # UI图标
    └── templates/              # 配置文件模板
```

## 核心数据流

### 资源加载策略（优先本地）
```
用户选择课程 → 检查本地索引 → 找到→直接播放
                                    → 未找到→尝试网络下载→保存本地→播放
```

### 课程数据结构
```python
COURSE_STRUCTURE = {
    "math": {
        "name": "数学",
        "grade_levels": ["六年级", "七年级", "八年级", "九年级"],
        "terms": ["第一学期", "第二学期"],
        "chapters": [...]  # 从课本PDF提取的章节结构
    },
    ...
}
```

## 关键设计原则
1. **路径动态化**：所有路径通过 paths.py 统一管理，支持打包/未打包两种模式
2. **数据持久化**：学习进度用SQLite，用户配置用JSON
3. **离线优先**：本地资源库优先，网络下载作为补充
4. **模块化**：各模块独立可测，接口清晰
