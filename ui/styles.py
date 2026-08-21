"""
统一样式定义
"""
# ===== 配色方案 =====
COLORS = {
    "primary": "#3498db",       # 主色-蓝色
    "secondary": "#9b59b6",     # 辅色-紫色
    "accent": "#e67e22",        # 强调色-橙色
    "success": "#27ae60",       # 成功-绿色
    "warning": "#f39c12",       # 警告-黄色
    "error": "#e74c3c",         # 错误-红色
    "bg_dark": "#2c3e50",       # 深色背景
    "bg_light": "#ffffff",      # 浅色背景-白色
    "text_primary": "#2c3e50",  # 主文字-深蓝
    "text_secondary": "#7f8c8d", # 次要文字
    "white": "#ffffff",
    "border": "#bdc3c7",
}

# ===== 字体设置 =====
FONTS = {
    "title": ("Microsoft YaHei", 18, "bold"),
    "heading": ("Microsoft YaHei", 14, "bold"),
    "body": ("Microsoft YaHei", 11),
    "small": ("Microsoft YaHei", 9),
    "large": ("Microsoft YaHei", 24, "bold"),
}

# ===== 按钮样式 =====
BUTTON_CONFIG = {
    "hover_color": "#1a5276",
    "bg_color": "#2E86AB",
    "text_color": "#ffffff",
    "corner_radius": 8,
}

# ===== 侧边栏样式 =====
SIDEBAR = {
    "width": 220,
    "bg_color": "#2c3e50",      # 侧边栏背景-深蓝灰
    "text_color": "#ecf0f1",     # 白色文字
    "selected_bg": "#3498db",   # 选中背景-蓝色
    "icon_size": 20,
}
