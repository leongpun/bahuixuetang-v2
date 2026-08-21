"""
AI诊断服务 - 调用Sapiens AI分析学习薄弱点
"""
import json
import requests
from config.paths import APP_SETTINGS_PATH


class AIService:
    """AI学习诊断服务"""

    PROMPT_TEMPLATE = """你是一位经验丰富的初中辅导老师。学生正在学习{subject}，当前是{grade}年级{term}学期，正在学习"{chapter}"章节。

学生的错题记录：{errors}

请分析：
1. 该学生的知识薄弱点
2. 推荐的学习重点
3. 具体的练习建议

请以简洁的结构化格式回复。"""

    def __init__(self, scanner=None):
        self.scanner = scanner
        from config.settings import load_settings
        self.settings = load_settings()
        self.api_key = self._load_api_key()
        # 使用配置中的AI端点，默认Sapiens AI
        self.base_url = self.settings.get("ai_endpoint", "https://api.sapiens.ai/v1/chat/completions")
        self.model = self.settings.get("ai_model", "deepseek-chat")

    def _load_api_key(self):
        """加载API密钥"""
        from config.settings import load_settings
        settings = load_settings()
        return settings.get('ai_api_key', '')

    def diagnose(self, subject, grade, term, chapter, errors=None, progress_data=None):
        """AI诊断学习薄弱点"""
        if not self.api_key:
            return {"error": "API key not configured"}

        errors_text = json.dumps(errors, ensure_ascii=False) if errors else "暂无错题记录"

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
        """AI生成练习题"""
        if not self.api_key:
            return {"error": "API key not configured"}

        prompt = f"请为{subject}{grade}年级'{topic}'章节出5道{difficulty}难度的选择题，每题4个选项，标注正确答案和解析。格式：JSON数组。"

        try:
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            payload = {"model": self.model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
            resp = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            # 尝试解析JSON
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
