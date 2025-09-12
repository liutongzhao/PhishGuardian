import re
import json
import requests
from typing import Dict, Any, List


class TextAgent:
    def __init__(self, api_url: str, api_key: str, model: str = "gpt-4o", temperature: float = 0, timeout: int = 60):
        self.api_url = api_url
        self.model = model
        self.temperature = temperature
        self.timeout = timeout
        
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
        
        self.strict_json_note = (
            'Return ONLY ONE LINE of MINIFIED JSON with EXACT keys and values, '
            'no extra text, no code fences:\n'
            '{"verdict":"Phishing"|"Legitimate","phishing_probability":0-1,"confidence":0-1,"reasons":"Chinese explanation"}'
        )
        
        self.system_prompt = f"""You are a cybersecurity expert specializing in phishing.
Focus ONLY on the email BODY text cues (lottery/donation claims, money requests, urgency, grammar anomalies).
{self.strict_json_note}"""
    
    def call_llm_api(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "stream": False
        }
        try:
            resp = self._session.post(self.api_url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            print(f"API请求错误: {e}")
            return {}
    
    def _postfix_schema(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if "reasons" not in data and "reason" in data:
            data["reasons"] = data["reason"]
        if "phishing_probability" not in data:
            for k in ("probability", "score", "phish_prob", "phishing_score"):
                if k in data:
                    data["phishing_probability"] = data[k]
                    break

        data.setdefault("verdict", "Phishing")
        for k, dv in (("phishing_probability", 0.5), ("confidence", 0.5)):
            try:
                v = float(data.get(k, dv))
            except Exception:
                v = dv
            data[k] = max(0.0, min(1.0, v))
        data.setdefault("reasons", "（无）")

        if data["verdict"] not in ("Phishing", "Legitimate"):
            data["verdict"] = "Phishing" if data["phishing_probability"] >= 0.5 else "Legitimate"
        return data
    
    def safe_parse_agent_json(self, api_json: Dict[str, Any]) -> Dict[str, Any]:
        default = {"verdict": "Phishing", "phishing_probability": 0.5, "confidence": 0.3, "reasons": "解析失败，使用中性概率"}
        try:
            content = api_json["choices"][0]["message"]["content"]
        except Exception:
            return default

        s = content.strip()
        s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s, flags=re.I)

        if s.startswith("{") and s.rstrip().endswith("}"):
            try:
                return self._postfix_schema(json.loads(s))
            except Exception as e:
                print("raw loads failed:", e, "\nSTR:", repr(s))

        m = re.search(r"\{[\s\S]*?\}", s)
        if m:
            s = m.group(0)

        s = s.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029").replace("\ufeff", "")
        s = re.sub(r",\s*([}\]])", r"\1", s)

        try:
            return self._postfix_schema(json.loads(s))
        except Exception:
            print("JSON解析失败，repr：", repr(s))
            return default
    
    def build_messages(self, body: str) -> List[Dict[str, str]]:
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": "以下为邮件正文，仅根据正文文本判断（不要考虑URL和元数据）：\n\n" + body}
        ]
    
    def analyze(self, body: str) -> Dict[str, Any]:
        if not body or not body.strip():
            return {
                "verdict": "Legitimate",
                "phishing_probability": 0.1,
                "confidence": 0.3,
                "reasons": "邮件正文为空，无法进行文本分析"
            }
        
        messages = self.build_messages(body)
        api_response = self.call_llm_api(messages)
        
        if not api_response:
            return {
                "verdict": "Phishing",
                "phishing_probability": 0.5,
                "confidence": 0.3,
                "reasons": "API调用失败，使用中性概率"
            }
        
        return self.safe_parse_agent_json(api_response)


def analyze_text(body: str, api_url: str, api_key: str, 
                model: str = "gpt-4o", temperature: float = 0, timeout: int = 60) -> Dict[str, Any]:
    agent = TextAgent(api_url, api_key, model, temperature, timeout)
    return agent.analyze(body)