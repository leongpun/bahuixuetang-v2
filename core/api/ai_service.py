"""
AI DiagnosisService - CallSapiens AIPartAnalyzeStudyWeakness
"""
import json
import requests
from config.paths import APP_SETTINGS_PATH


class AIService:
    """AIStudyDiagnosisService"""

    PROMPT_TEMPLATE = """YouYesExperiencedJuniorHighTutor。StudentProcessingStudy{subject}，CurrentYes{grade}Grade{term}Term，ProcessingStudy"{chapter}"Chapter。

StudentMistakeQuestionRecord：{errors}

PleasePartAnalyze：
1. TheStudentKnowledgeKnowledgeWeakness
2. RecommendedStudyAgainPoint
3. ToolBodyPracticeSuggestion

PleaseConciseStructureizeFormatReply。"""

    def __init__(self, scanner=None):
        self.scanner = scanner
        from config.settings import load_settings
        self.settings = load_settings()
        self.api_key = self._load_api_key()
        # UseConfigureInAIEndpointPoint，DefaultSapiens AI
        self.base_url = self.settings.get("ai_endpoint", "https://api.sapiens.ai/v1/chat/completions")
        self.model = self.settings.get("ai_model", "deepseek-chat")

    def _load_api_key(self):
        """LoadAPISecret Key"""
        from config.settings import load_settings
        settings = load_settings()
        return settings.get('ai_api_key', '')

    def diagnose(self, subject, grade, term, chapter, errors=None, progress_data=None):
        """AI DiagnosisStudyWeakness"""
        if not self.api_key:
            return {"error": "API key not configured"}

        errors_text = json.dumps(errors, ensure_ascii=False) if errors else "NoMistakeQuestionRecord"

        prompt = self.PROMPT_TEMPLATE.format(
            subject=subject,
            grade=grade,
            term=term,
            chapter=chapter,
            errors=errors_text,
        )

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
            }
            resp = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            return {
                "weakness": result.get("choices", [{}])[0].get("message", {}).get("content", ""),
                "raw": result,
            }
        except Exception as e:
            return {"error": str(e)}

    def generate_quiz(self, subject, grade, topic, difficulty="medium"):
        """AIGeneratePracticeQuestion"""
        if not self.api_key:
            return {"error": "API key not configured"}

        prompt = f"PleaseFor{subject}{grade}Grade'{topic}'ChapterOutput5Questions{difficulty}DifficultySelectQuestion，EveryQuestion4ItemOption，LabelCorrectAnswerAndExplanation。Format：JSONCountGroup。"

        try:
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            payload = {"model": self.model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
            resp = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            # TryExplanationJSON
            try:
                import re
                json_match = re.search(r"\[.*\]", content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                return {"questions": content}
            except json.JSONDecodeError:
                return {"questions": content}
        except Exception as e:
            return {"error": str(e)}

    def set_api_key(self, key):
        self.api_key = key
        if APP_SETTINGS_PATH.exists():
            try:
                with open(APP_SETTINGS_PATH, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                settings["ai_api_key"] = key
                with open(APP_SETTINGS_PATH, "w", encoding="utf-8") as f:
                    json.dump(settings, f, ensure_ascii=False, indent=2)
            except Exception:
                pass
