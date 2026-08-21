"""
课程结构配置模块
基于上海课本结构 + 空中课堂资源映射
"""

# ===== 学科定义 =====
# 格式: {code: {"name": 显示名, "edition": 版本, "grades": 年级列表}}
SUBJECTS = {
    "math":     {"name": "数学",     "edition": "沪教版",     "grades": ["六年级", "七年级", "八年级", "九年级"]},
    "chinese":  {"name": "语文",     "edition": "统编五四版", "grades": ["六年级", "七年级", "八年级", "九年级"]},
    "english":  {"name": "英语",     "edition": "沪教版",     "grades": ["六年级", "七年级", "八年级"]},
    "physics":  {"name": "物理",     "edition": "沪科技版",   "grades": ["八年级", "九年级"]},
    "chemistry":{"name": "化学",     "edition": "沪科技版",   "grades": ["九年级"]},
    "biology":  {"name": "生物",     "edition": "沪教版",     "grades": ["七年级", "八年级"]},
    "science":  {"name": "科学",     "edition": "沪科技版",   "grades": ["六年级"]},
    "morality": {"name": "道德与法治","edition": "统编五四版","grades": ["六年级", "七年级", "八年级", "九年级"]},
    "art":      {"name": "美术",     "edition": "沪书画版",   "grades": ["六年级", "七年级", "八年级"]},
    "music":    {"name": "音乐",     "edition": "沪音版",     "grades": ["六年级", "七年级", "八年级"]},
    "dance":    {"name": "舞蹈",     "edition": "沪教版",     "grades": ["八年级"]},
}

# ===== 学期 =====
TERMS = ["第一学期", "第二学期"]

# ===== 空中课堂资源路径映射 =====
# {学科code: {"local_path": E盘路径前缀, "api_base": API基础URL}}
AIRCLASS_CONFIG = {
    "math": {
        "local_path": r"E:\空中课堂\初中数学_沪教育",
        "api_base": "https://shd-assets.eduyun.cn/onlineClass/stage/stageInfo",
        "grade_map": {"六年级": "6", "七年级": "7", "八年级": "8", "九年级": "9"},
    },
    "chinese": {
        "local_path": r"E:\空中课堂\初中语文",
        "api_base": "https://shd-assets.eduyun.cn/onlineClass/stage/stageInfo",
        "grade_map": {"六年级": "6", "七年级": "7", "八年级": "8", "九年级": "9"},
    },
    "english": {
        "local_path": r"E:\空中课堂\初中英语",
        "api_base": "https://shd-assets.eduyun.cn/onlineClass/stage/stageInfo",
        "grade_map": {"六年级": "6", "七年级": "7", "八年级": "8"},
    },
}

# ===== 课本PDF路径 =====
TEXTBOOK_PDFS = {
    "math": {
        "path": r"E:\初中课本\数学\沪教版",
        "files": {
            "六年级": ["六年级上册（2024新版）.pdf", "六年级下册（2024新版）.pdf"],
            "七年级": ["七年级上册（2024新版）.pdf", "七年级下册（2024新版）.pdf"],
            "八年级": ["八年级上册（2024新版）.pdf", "八年级下册（2024新版）.pdf"],
            "九年级": [],  # 无单独九年级PDF
        }
    },
    "chinese": {
        "path": r"E:\初中课本\语文\统编五四版",
        "files": {
            "六年级": ["六年级上册（2024新版）.pdf", "六年级下册（2024新版）.pdf"],
            "七年级": ["七年级上册（2024新版）.pdf", "七年级下册（2024新版）.pdf"],
            "八年级": ["八年级上册（2024新版）.pdf", "八年级下册（2024新版）.pdf"],
            "九年级": ["九年级上册（现行版）.pdf", "九年级下册（现行版）.pdf"],
        }
    },
    "english": {
        "path": r"E:\初中课本\英语\沪教版",
        "files": {
            "六年级": ["六年级上册（2024新版）.pdf", "六年级下册（2024新版）.pdf"],
            "七年级": ["七年级上册（2024新版）.pdf", "七年级下册（2024新版）.pdf"],
            "八年级": ["八年级上册（2024新版）.pdf", "八年级下册（2024新版）.pdf"],
        }
    },
    "physics": {
        "path": r"E:\初中课本\物理\沪科技版",
        "files": {
            "八年级": ["八年级上册（2024新版）.pdf", "八年级下册（2024新版）.pdf"],
            "九年级": ["九年级上册（2024新版）.pdf", "九年级下册（2024新版）.pdf"],
        }
    },
    "chemistry": {
        "path": r"E:\初中课本\化学\沪科技版",
        "files": {
            "九年级": ["九年级全一册（2024新版）.pdf", "八年级全一册（2024新版）.pdf"],
        }
    },
    "biology": {
        "path": r"E:\初中课本\生物\沪教版",
        "files": {
            "七年级": ["七年级上册（2024新版）.pdf", "七年级下册（2024新版）.pdf"],
            "八年级": ["八年级上册（2024新版）.pdf", "八年级下册（2024新版）.pdf"],
        }
    },
    "science": {
        "path": r"E:\初中课本\科学\沪科技版",
        "files": {
            "六年级": ["六年级上册（2024新版）.pdf", "六年级下册（2024新版）.pdf"],
        }
    },
    "morality": {
        "path": r"E:\初中课本\道德与法治\统编五四版",
        "files": {
            "六年级": ["六年级全一册（2024新版）.pdf", "六年级下册（2024新版）.pdf"],
            "七年级": ["七年级全一册（2024新版）.pdf"],
            "八年级": ["八年级上册（2024新版）.pdf", "八年级下册（2024新版）.pdf"],
            "九年级": ["九年级上册（现行版）.pdf", "九年级下册（现行版）.pdf"],
        }
    },
    "art": {
        "path": r"E:\初中课本\美术\沪书画版",
        "files": {
            "六年级": ["六年级上册（2024新版）.pdf", "六年级下册（2024新版）.pdf"],
            "七年级": ["七年级上册（2024新版）.pdf", "七年级下册（2024新版）.pdf"],
            "八年级": ["八年级上册（2024新版）.pdf", "八年级下册（2024新版）.pdf"],
        }
    },
    "music": {
        "path": r"E:\初中课本\音乐\沪音版",
        "files": {
            "六年级": ["六年级上册（2024新版）.pdf", "六年级下册（2024新版）.pdf"],
            "七年级": ["七年级上册（2024新版）.pdf", "七年级下册（2024新版）.pdf"],
            "八年级": ["八年级上册（2024新版）.pdf"],
        }
    },
    "dance": {
        "path": r"E:\初中课本\舞蹈\沪教版",
        "files": {
            "八年级": ["八年级下册（2024新版）.pdf"],
        }
    },
}

# ===== 章节结构模板 =====
# 各学科按课本章节组织，这里提供通用模板
# 实际章节从课本PDF解析获取
CHAPTER_TEMPLATES = {
    "math": {
        "六年级": {
            "第一学期": ["第1章 数表", "第2章 比和比例", "第3章 分数和百分数（一）", "第4章 分数和百分数（二）", "第5章 整数和小数的加减法", "第6章 整数和小数的乘除法", "第7章 简易方程"],
            "第二学期": ["第1章 多边的面积计算", "第2章 几何小实践", "第3章 整数的整除", "第4章 分数和百分数（三）", "第5章 有理数", "第6章 线段、角的再认识"],
        },
        "七年级": {
            "第一学期": ["第1章 整式", "第2章 因式分解", "第3章 一次方程（组）", "第4章 一次不等式（组）", "第5章 线段、角 平行与垂直"],
            "第二学期": ["第1章 分式", "第2章 二次根式", "第3章 数据整理与平稳随机事件", "第4章 几何图形的初步认识", "第5章 实数"],
        },
        "八年级": {
            "第一学期": ["第1章 二次根式", "第2章 函数初步", "第3章 平行四边形", "第4章 数据分析初步"],
            "第二学期": ["第1章 一元二次方程", "第2章 相似三角形", "第3章 圆的初步认识", "第4章 统计初步"],
        },
        "九年级": {
            "第一学期": ["第1章 二次函数", "第2章 圆与扇形", "第3章 锐角三角比", "第4章 概率初步"],
            "第二学期": ["第1章 相似三角形", "第2章 锐角三角比", "第3章 二次函数", "第4章 统计"],
        },
    },
    "chinese": {
        "六年级": {
            "第一学期": ["第一单元 四季美景", "第二单元 亲情家人", "第三单元 阅读指南", "第四单元 动物世界", "第五单元 古代故事", "第六单元 诗歌欣赏", "第七单元 写作训练"],
            "第二学期": ["第一单元 民俗风情", "第二单元 童年往事", "第三单元 读书指导", "第四单元 自然科学", "第五单元 古诗研读", "第六单元 文言启蒙", "第七单元 综合实践"],
        },
        "七年级": {
            "第一学期": ["第一单元 四季景色", "第二单元 亲情时光", "第三单元 学习指导", "第四单元 人生历程", "第五单元 动物天地", "第六单元 想象世界", "第七单元 古诗积累", "第八单元 文言初探"],
            "第二学期": ["第一单元 自然之美", "第二单元 人文情怀", "第三单元 阅读方法", "第四单元 科学探索", "第五单元 古代文化", "第六单元 写作训练", "第七单元 古诗专题", "第八单元 文言进阶"],
        },
        "八年级": {
            "第一学期": ["第一单元 新闻阅读", "第二单元 回忆性散文", "第三单元 古诗文", "第四单元 事理说明文", "第五单元 文言文", "第六单元 古诗", "第七单元 写作", "第八单元 综合性学习"],
            "第二学期": ["第一单元 游记", "第二单元 事物说明文", "第三单元 古诗文", "第四单元 小说", "第五单元 文言文", "第六单元 古诗", "第七单元 写作", "第八单元 综合性学习"],
        },
        "九年级": {
            "第一学期": ["第一单元 自然吟唱", "第二单元 人间情怀", "第三单元 阅读方法", "第四单元 议论文章", "第五单元 古诗文", "第六单元 小说", "第七单元 文言", "第八单元 写作"],
            "第二学期": ["第一单元 人物风采", "第二单元 生命赞歌", "第三单元 古诗文研读", "第四单元 小说鉴赏", "第五单元 议论文", "第六单元 文言", "第七单元 写作", "第八单元 综合性学习"],
        },
    },
    "english": {
        "六年级": {
            "第一学期": ["Unit 1 My school life", "Unit 2 Our home", "Unit 3 Food and diet", "Unit 4 Travel", "Unit 5 Shopping", "Unit 6 Outdoor fun", "Unit 7 Festivals", "Module revision"],
            "第二学期": ["Unit 1 Welcome to Shanghai", "Unit 2 At home", "Unit 3 Going out", "Unit 4 Food and shopping", "Unit 5 Healthy lifestyle", "Unit 6 Entertainment", "Unit 7 Computer world", "Module revision"],
        },
        "七年级": {
            "第一学期": ["Unit 1 People and places", "Unit 2 Daily life", "Unit 3 Food and drink", "Unit 4 Life in the past", "Unit 5 Sports", "Unit 6 Weather", "Unit 7 Special occasions", "Module revision"],
            "第二学期": ["Unit 1 Culture and traditions", "Unit 2 Nature and environment", "Unit 3 Technology", "Unit 4 Careers and dreams", "Unit 5 Health and fitness", "Unit 6 Travel and transport", "Unit 7 Communication", "Module revision"],
        },
        "八年级": {
            "第一学期": ["Unit 1 Personal experiences", "Unit 2 Hobbies and interests", "Unit 3 Geography and environment", "Unit 4 History and culture", "Unit 5 Science and future", "Unit 6 Society and community", "Unit 7 Problems and solutions", "Module revision"],
            "第二学期": ["Unit 1 Education and learning", "Unit 2 Family and relationships", "Unit 3 Media and information", "Unit 4 Arts and literature", "Unit 5 Economy and business", "Unit 6 Health and medicine", "Unit 7 Global issues", "Module revision"],
        },
    },
}


def get_subjects():
    """获取所有学科列表"""
    return SUBJECTS

def get_grade_levels(subject_code):
    """获取某学科的所有年级"""
    return SUBJECTS.get(subject_code, {}).get("grades", [])

def get_chapters(subject_code, grade, term):
    """获取某年级某学期的章节列表"""
    templates = CHAPTER_TEMPLATES.get(subject_code, {})
    grade_chapters = templates.get(grade, {})
    return grade_chapters.get(term, [f"第{i+1}章" for i in range(10)])

def get_textbook_pdf(subject_code, grade):
    """获取课本PDF文件列表"""
    tf = TEXTBOOK_PDFS.get(subject_code, {})
    files = tf.get("files", {}).get(grade, [])
    base_path = tf.get("path", "")
    return [os.path.join(base_path, f) for f in files if os.path.exists(os.path.join(base_path, f))]

def get_airclass_local_path(subject_code):
    """获取空中课堂本地路径"""
    cfg = AIRCLASS_CONFIG.get(subject_code, {})
    return cfg.get("local_path", "")

def get_airclass_api_params(subject_code, grade, term):
    """获取API请求参数"""
    cfg = AIRCLASS_CONFIG.get(subject_code, {})
    grade_map = cfg.get("grade_map", {})
    api_base = cfg.get("api_base", "")
    stage = grade_map.get(grade, "")
    return {"stage": stage, "term": term}

import os
