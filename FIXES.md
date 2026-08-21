# 柏慧学堂v2 关键修复记录
# 日期: 2026-08-20

## 问题1: AI无法回答
### 根因
- AIService的base_url硬编码为"sapiens.ai"，但settings中配置的可能不同
- 未使用load_settings()读取配置的AI端点

### 修复
- 文件: core/api/ai_service.py
- 修改: __init__方法，从settings读取base_url和model
```python
self.base_url = self.settings.get("ai_endpoint", "https://api.sapiens.ai/v1/chat/completions")
self.model = self.settings.get("ai_model", "deepseek-chat")
```

## 问题2: 学习进度未显示章节数量
### 根因
- get_dashboard()统计total_chapters时直接计算所有进度记录数
- 跨电脑迁移后章节数据可能重复或不一致

### 修复
- 文件: core/engine/progress_tracker.py
- 修改: 统计唯一章节组合（subject+grade+term+chapter）
```python
chapter_keys = set()
for p in all_progress:
    key = f"{p['subject']}|{p['grade']}|{p['term']}|{p['chapter']}"
    chapter_keys.add(key)
stats["total_chapters"] = len(chapter_keys)
```

## 问题3: 跨电脑无法选择章节/播放视频
### 根因
- CourseSelector._get_term_path()硬编码固定目录层级
- 不同电脑目录结构可能不同（如E:\空中课堂\初中数学_沪教育\七年级\第一学期）
- 只匹配精确目录名，无法适配变体

### 修复
- 文件: core/engine/course_selector.py
- 重写_get_term_path()为递归搜索
- 从settings读取external_resource_paths配置
- 使用os.walk()递归查找匹配关键词的目录

```python
def _get_term_path(self, subject_code, grade, term):
    """动态查找学期目录路径 - 支持任意目录层级"""
    from config.settings import load_settings
    from pathlib import Path
    
    subject_name = SUBJECTS.get(subject_code, {}).get("name", subject_code)
    settings = load_settings()
    
    # 从配置获取搜索路径
    search_paths = settings.get("external_resource_paths", [
        r"E:\空中课堂",
        r"E:\初中课本"
    ])
    
    # 匹配学期名称变体
    term_variants = [term, "第一学期", "第二学期", "上学期", "下学期"]
    
    for base_path in search_paths:
        base_path = Path(base_path).expanduser()
        if not base_path.exists():
            continue
        
        # 递归查找匹配的目录
        for root, dirs, files in os.walk(base_path):
            root_str = str(root).replace('\\', '/')
            
            # 检查是否包含所有关键词
            if (subject_name in root_str and 
                grade in root_str and
                any(t in root_str for t in term_variants)):
                return root
    
    return None
```

## 验证结果
- course_selector: ✅ 测试通过，能找到E:\空中课堂\初中数学_沪教育\七年级\第一学期
- ai_service: ✅ base_url从settings读取
- progress_tracker: ✅ 统计唯一章节组合

## 下一步
- 打包exe进行测试