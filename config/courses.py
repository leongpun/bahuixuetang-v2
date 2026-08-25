"""
CourseStructureConfigureModule
Based OnOnSeaTextbookStructure + AirClassResourceMap
"""

# ===== SubjectDefineMeaning =====
# Format: {code: {"name": Display Name, "edition": Edition, "grades": GradeList}}
SUBJECTS = {
    "math":     {"name": "Math",     "edition": "SH_Edu",     "grades": ["Grade 6", "Grade 7", "Grade 8", "Grade 9"]},
    "chinese":  {"name": "Chinese",     "edition": "Unified_Ed", "grades": ["Grade 6", "Grade 7", "Grade 8", "Grade 9"]},
    "english":  {"name": "English",     "edition": "SH_Edu",     "grades": ["Grade 6", "Grade 7", "Grade 8"]},
    "physics":  {"name": "Physics",     "edition": "SH_Tech",   "grades": ["Grade 8", "Grade 9"]},
    "chemistry":{"name": "Chemistry",     "edition": "SH_Tech",   "grades": ["Grade 9"]},
    "biology":  {"name": "Biology",     "edition": "SH_Edu",     "grades": ["Grade 7", "Grade 8"]},
    "science":  {"name": "Science",     "edition": "SH_Tech",   "grades": ["Grade 6"]},
    "morality": {"name": "Morality & Law","edition": "Unified_Ed","grades": ["Grade 6", "Grade 7", "Grade 8", "Grade 9"]},
    "art":      {"name": "Art",     "edition": "SH_Art",   "grades": ["Grade 6", "Grade 7", "Grade 8"]},
    "music":    {"name": "Music",     "edition": "SH_Music",     "grades": ["Grade 6", "Grade 7", "Grade 8"]},
    "dance":    {"name": "Dance",     "edition": "SH_Edu",     "grades": ["Grade 8"]},
}

# ===== Term =====
TERMS = ["Term 1", "Term 2"]

# ===== AirClassResourcePathMap =====
# {Subjectcode: {"local_path": EDrive Path Prefix, "api_base": API Base URL}}
AIRCLASS_CONFIG = {
    "math": {
        "local_path": r"E:\AirClass\JuniorHighMath_SH_Edu",
        "api_base": "https://shd-assets.eduyun.cn/onlineClass/stage/stageInfo",
        "grade_map": {"Grade 6": "6", "Grade 7": "7", "Grade 8": "8", "Grade 9": "9"},
    },
    "chinese": {
        "local_path": r"E:\AirClass\JuniorHighChinese",
        "api_base": "https://shd-assets.eduyun.cn/onlineClass/stage/stageInfo",
        "grade_map": {"Grade 6": "6", "Grade 7": "7", "Grade 8": "8", "Grade 9": "9"},
    },
    "english": {
        "local_path": r"E:\AirClass\JuniorHighEnglish",
        "api_base": "https://shd-assets.eduyun.cn/onlineClass/stage/stageInfo",
        "grade_map": {"Grade 6": "6", "Grade 7": "7", "Grade 8": "8"},
    },
}

# ===== TextbookPDFPath =====
TEXTBOOK_PDFS = {
    "math": {
        "path": r"E:\JuniorHighTextbook\Math\SH_Edu",
        "files": {
            "Grade 6": ["Grade 6OnVolume（2024NewEdition）.pdf", "Grade 6Volume 2（2024NewEdition）.pdf"],
            "Grade 7": ["Grade 7OnVolume（2024NewEdition）.pdf", "Grade 7Volume 2（2024NewEdition）.pdf"],
            "Grade 8": ["Grade 8OnVolume（2024NewEdition）.pdf", "Grade 8Volume 2（2024NewEdition）.pdf"],
            "Grade 9": [],  # NoneSingleUniqueGrade 9PDF
        }
    },
    "chinese": {
        "path": r"E:\JuniorHighTextbook\Chinese\Unified_Ed",
        "files": {
            "Grade 6": ["Grade 6OnVolume（2024NewEdition）.pdf", "Grade 6Volume 2（2024NewEdition）.pdf"],
            "Grade 7": ["Grade 7OnVolume（2024NewEdition）.pdf", "Grade 7Volume 2（2024NewEdition）.pdf"],
            "Grade 8": ["Grade 8OnVolume（2024NewEdition）.pdf", "Grade 8Volume 2（2024NewEdition）.pdf"],
            "Grade 9": ["Grade 9OnVolume（CurrentEdition）.pdf", "Grade 9Volume 2（CurrentEdition）.pdf"],
        }
    },
    "english": {
        "path": r"E:\JuniorHighTextbook\English\SH_Edu",
        "files": {
            "Grade 6": ["Grade 6OnVolume（2024NewEdition）.pdf", "Grade 6Volume 2（2024NewEdition）.pdf"],
            "Grade 7": ["Grade 7OnVolume（2024NewEdition）.pdf", "Grade 7Volume 2（2024NewEdition）.pdf"],
            "Grade 8": ["Grade 8OnVolume（2024NewEdition）.pdf", "Grade 8Volume 2（2024NewEdition）.pdf"],
        }
    },
    "physics": {
        "path": r"E:\JuniorHighTextbook\Physics\SH_Tech",
        "files": {
            "Grade 8": ["Grade 8OnVolume（2024NewEdition）.pdf", "Grade 8Volume 2（2024NewEdition）.pdf"],
            "Grade 9": ["Grade 9OnVolume（2024NewEdition）.pdf", "Grade 9Volume 2（2024NewEdition）.pdf"],
        }
    },
    "chemistry": {
        "path": r"E:\JuniorHighTextbook\Chemistry\SH_Tech",
        "files": {
            "Grade 9": ["Grade 9Complete Volume（2024NewEdition）.pdf", "Grade 8Complete Volume（2024NewEdition）.pdf"],
        }
    },
    "biology": {
        "path": r"E:\JuniorHighTextbook\Biology\SH_Edu",
        "files": {
            "Grade 7": ["Grade 7OnVolume（2024NewEdition）.pdf", "Grade 7Volume 2（2024NewEdition）.pdf"],
            "Grade 8": ["Grade 8OnVolume（2024NewEdition）.pdf", "Grade 8Volume 2（2024NewEdition）.pdf"],
        }
    },
    "science": {
        "path": r"E:\JuniorHighTextbook\Science\SH_Tech",
        "files": {
            "Grade 6": ["Grade 6OnVolume（2024NewEdition）.pdf", "Grade 6Volume 2（2024NewEdition）.pdf"],
        }
    },
    "morality": {
        "path": r"E:\JuniorHighTextbook\Morality & Law\Unified_Ed",
        "files": {
            "Grade 6": ["Grade 6Complete Volume（2024NewEdition）.pdf", "Grade 6Volume 2（2024NewEdition）.pdf"],
            "Grade 7": ["Grade 7Complete Volume（2024NewEdition）.pdf"],
            "Grade 8": ["Grade 8OnVolume（2024NewEdition）.pdf", "Grade 8Volume 2（2024NewEdition）.pdf"],
            "Grade 9": ["Grade 9OnVolume（CurrentEdition）.pdf", "Grade 9Volume 2（CurrentEdition）.pdf"],
        }
    },
    "art": {
        "path": r"E:\JuniorHighTextbook\Art\SH_Art",
        "files": {
            "Grade 6": ["Grade 6OnVolume（2024NewEdition）.pdf", "Grade 6Volume 2（2024NewEdition）.pdf"],
            "Grade 7": ["Grade 7OnVolume（2024NewEdition）.pdf", "Grade 7Volume 2（2024NewEdition）.pdf"],
            "Grade 8": ["Grade 8OnVolume（2024NewEdition）.pdf", "Grade 8Volume 2（2024NewEdition）.pdf"],
        }
    },
    "music": {
        "path": r"E:\JuniorHighTextbook\Music\SH_Music",
        "files": {
            "Grade 6": ["Grade 6OnVolume（2024NewEdition）.pdf", "Grade 6Volume 2（2024NewEdition）.pdf"],
            "Grade 7": ["Grade 7OnVolume（2024NewEdition）.pdf", "Grade 7Volume 2（2024NewEdition）.pdf"],
            "Grade 8": ["Grade 8OnVolume（2024NewEdition）.pdf"],
        }
    },
    "dance": {
        "path": r"E:\JuniorHighTextbook\Dance\SH_Edu",
        "files": {
            "Grade 8": ["Grade 8Volume 2（2024NewEdition）.pdf"],
        }
    },
}

# ===== ChapterStructureTemplate =====
# EachSubjectByTextbookChapterOrganization，HereSubmitProvidePassUseTemplate
# ActualChapterFromTextbookPDFExplanationGet
CHAPTER_TEMPLATES = {
    "math": {
        "Grade 6": {
            "Term 1": ["Th1Chapter CountTable", "Th2Chapter RatioAndRatioExample", "Th3Chapter PartCountAndHundredPartCount（One）", "Th4Chapter PartCountAndHundredPartCount（Two）", "Th5Chapter IntegerCountAndSmallCountAddition and Subtraction", "Th6Chapter IntegerCountAndSmallCountMultiplication and Division", "Th7Chapter Simple Equation"],
            "Term 2": ["Th1Chapter MoreEdgePageProductCalculate", "Th2Chapter GeometrySmallRealPractice", "Th3Chapter IntegerCountDivisible", "Th4Chapter PartCountAndHundredPartCount（Three）", "Th5Chapter HaveReasonCount", "Th6Chapter LineSection、Angle RecognitionKnowledge"],
        },
        "Grade 7": {
            "Term 1": ["Th1Chapter IntegerType", "Th2Chapter FactorTypePartSolve", "Th3Chapter OneTimesEquation（Group）", "Th4Chapter One TimeType（Group）", "Th5Chapter LineSection、Angle Parallel and Perpendicular"],
            "Term 2": ["Th1Chapter PartType", "Th2Chapter TwoTimesRootType", "Th3Chapter DataIntegerReasonand StabilityRandomEvent", "Th4Chapter GeometryIntroRecognizeKnowledge", "Th5Chapter RealCount"],
        },
        "Grade 8": {
            "Term 1": ["Th1Chapter TwoTimesRootType", "Th2Chapter FunctionIntro", "Th3Chapter ParallelogramEdgeShape", "Th4Chapter DataPartAnalyzeIntro"],
            "Term 2": ["Th1Chapter OneElementTwoTimesEquation", "Th2Chapter SimilarThreeAngleShape", "Th3Chapter Circle Introduction", "Th4Chapter StatisticsIntro"],
        },
        "Grade 9": {
            "Term 1": ["Th1Chapter TwoTimesFunction", "Th2Chapter Circle and Sector", "Th3Chapter Acute AngleThreeAngleRatio", "Th4Chapter ProbabilityIntro"],
            "Term 2": ["Th1Chapter SimilarThreeAngleShape", "Th2Chapter Acute AngleThreeAngleRatio", "Th3Chapter TwoTimesFunction", "Th4Chapter Statistics"],
        },
    },
    "chinese": {
        "Grade 6": {
            "Term 1": ["ThOneSingleElement Four Seasons Scenery", "ThTwoSingleElement Family", "ThThreeSingleElement ReadingPointSouth", "Unit 4 Animal WorldInterface", "ThFiveSingleElement Ancient Story", "ThSixSingleElement Poetry Appreciation", "ThSevenSingleElement WriteWorkTraining"],
            "Term 2": ["ThOneSingleElement Folk Customs", "ThTwoSingleElement Childhood Stories", "ThThreeSingleElement Reading BookPointGuide", "Unit 4 NatureScience", "ThFiveSingleElement Classical Poetry Study", "ThSixSingleElement Classical Chinese Intro", "ThSevenSingleElement Comprehensive Practice"],
        },
        "Grade 7": {
            "Term 1": ["ThOneSingleElement Four Seasons Scenery", "ThTwoSingleElement Family Time", "ThThreeSingleElement StudyPointGuide", "Unit 4 Life Journey", "ThFiveSingleElement Animal World", "ThSixSingleElement Imagination WorldInterface", "ThSevenSingleElement Classical Poetry Accumulation", "ThEightSingleElement Classical Chinese Intro"],
            "Term 2": ["ThOneSingleElement NatureBeauty", "ThTwoSingleElement Humanistic Sentiment", "ThThreeSingleElement ReadingMethod", "Unit 4 ScienceExplore", "ThFiveSingleElement Ancient Culture", "ThSixSingleElement WriteWorkTraining", "ThSevenSingleElement Classical PoetrySpecialQuestion", "ThEightSingleElement Classical ChineseAdvance"],
        },
        "Grade 8": {
            "Term 1": ["ThOneSingleElement NewHearReading", "ThTwoSingleElement Memoratory Essay", "ThThreeSingleElement Classical Poetry", "Unit 4 MatterReasonExpository Essay", "ThFiveSingleElement Classical Chinese", "ThSixSingleElement Classical Poetry", "ThSevenSingleElement WriteWork", "ThEightSingleElement ComprehensiveStudy"],
            "Term 2": ["ThOneSingleElement Travelogue", "ThTwoSingleElement ThingsExpository Essay", "ThThreeSingleElement Classical Poetry", "Unit 4 Novel", "ThFiveSingleElement Classical Chinese", "ThSixSingleElement Classical Poetry", "ThSevenSingleElement WriteWork", "ThEightSingleElement ComprehensiveStudy"],
        },
        "Grade 9": {
            "Term 1": ["ThOneSingleElement Natural Song", "ThTwoSingleElement Human Sentiments", "ThThreeSingleElement ReadingMethod", "Unit 4 Argumentative EssayChapter", "ThFiveSingleElement Classical Poetry", "ThSixSingleElement Novel", "ThSevenSingleElement Classical Chinese", "ThEightSingleElement WriteWork"],
            "Term 2": ["ThOneSingleElement Character Portrait", "ThTwoSingleElement Life Ode", "ThThreeSingleElement Classical PoetryStudy", "Unit 4 Novel Appreciation", "ThFiveSingleElement Argumentative Essay", "ThSixSingleElement Classical Chinese", "ThSevenSingleElement WriteWork", "ThEightSingleElement ComprehensiveStudy"],
        },
    },
    "english": {
        "Grade 6": {
            "Term 1": ["Unit 1 My school life", "Unit 2 Our home", "Unit 3 Food and diet", "Unit 4 Travel", "Unit 5 Shopping", "Unit 6 Outdoor fun", "Unit 7 Festivals", "Module revision"],
            "Term 2": ["Unit 1 Welcome to Shanghai", "Unit 2 At home", "Unit 3 Going out", "Unit 4 Food and shopping", "Unit 5 Healthy lifestyle", "Unit 6 Entertainment", "Unit 7 Computer world", "Module revision"],
        },
        "Grade 7": {
            "Term 1": ["Unit 1 People and places", "Unit 2 Daily life", "Unit 3 Food and drink", "Unit 4 Life in the past", "Unit 5 Sports", "Unit 6 Weather", "Unit 7 Special occasions", "Module revision"],
            "Term 2": ["Unit 1 Culture and traditions", "Unit 2 Nature and environment", "Unit 3 Technology", "Unit 4 Careers and dreams", "Unit 5 Health and fitness", "Unit 6 Travel and transport", "Unit 7 Communication", "Module revision"],
        },
        "Grade 8": {
            "Term 1": ["Unit 1 Personal experiences", "Unit 2 Hobbies and interests", "Unit 3 Geography and environment", "Unit 4 History and culture", "Unit 5 Science and future", "Unit 6 Society and community", "Unit 7 Problems and solutions", "Module revision"],
            "Term 2": ["Unit 1 Education and learning", "Unit 2 Family and relationships", "Unit 3 Media and information", "Unit 4 Arts and literature", "Unit 5 Economy and business", "Unit 6 Health and medicine", "Unit 7 Global issues", "Module revision"],
        },
    },
}


def get_subjects():
    """Get AllSubjectList"""
    return SUBJECTS

def get_grade_levels(subject_code):
    """GetSomeSubject's AllGrade"""
    return SUBJECTS.get(subject_code, {}).get("grades", [])

def get_chapters(subject_code, grade, term):
    """GetSomeGradeSomeTermChapterList"""
    templates = CHAPTER_TEMPLATES.get(subject_code, {})
    grade_chapters = templates.get(grade, {})
    return grade_chapters.get(term, [f"Th{i+1}Chapter" for i in range(10)])

def get_textbook_pdf(subject_code, grade):
    """GetTextbookPDFFileList"""
    tf = TEXTBOOK_PDFS.get(subject_code, {})
    files = tf.get("files", {}).get(grade, [])
    base_path = tf.get("path", "")
    return [os.path.join(base_path, f) for f in files if os.path.exists(os.path.join(base_path, f))]

def get_airclass_local_path(subject_code):
    """GetAirClassLocalPath"""
    cfg = AIRCLASS_CONFIG.get(subject_code, {})
    return cfg.get("local_path", "")

def get_airclass_api_params(subject_code, grade, term):
    """GetAPIPleaseSeek ParametersCount"""
    cfg = AIRCLASS_CONFIG.get(subject_code, {})
    grade_map = cfg.get("grade_map", {})
    api_base = cfg.get("api_base", "")
    stage = grade_map.get(grade, "")
    return {"stage": stage, "term": term}

import os
