import re
import json
import requests
from typing import Dict, Any, List


class MetadataAgent:
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
Focus ONLY on email metadata analysis (sender reputation, SPF/DKIM/DMARC, routing anomalies).
{self.strict_json_note}"""
        
        self.header_keys_pattern = re.compile(
            r'^(from|to|cc|bcc|subject|date|message-id|received|return-path|'
            r'reply-to|sender|x-originating-ip|x-mailer|user-agent|'
            r'authentication-results|received-spf|dkim-signature|dmarc|'
            r'x-spam-score|x-spam-status|precedence|list-unsubscribe)$',
            re.IGNORECASE
        )
    
    def extract_valid_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        if not headers:
            return {}
        
        valid_headers = {}
        for key, value in headers.items():
            if self.header_keys_pattern.match(key):
                clean_value = re.sub(r'\s+', ' ', str(value).strip())
                valid_headers[key.lower()] = clean_value
        
        return valid_headers
    
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
    
    def build_messages(self, headers: Dict[str, str]) -> List[Dict[str, str]]:
        if not headers:
            header_content = "无有效邮件头部信息"
        else:
            header_lines = []
            for key, value in headers.items():
                header_lines.append(f"{key}: {value}")
            header_content = "\n".join(header_lines)
        
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": "以下为邮件头部元数据，仅根据元数据判断（不要考虑正文和URL）：\n\n" + header_content}
        ]
    
    def analyze(self, headers: Dict[str, str]) -> Dict[str, Any]:
        valid_headers = self.extract_valid_headers(headers)
        
        if not valid_headers:
            return {
                "verdict": "Legitimate",
                "phishing_probability": 0.2,
                "confidence": 0.5,
                "reasons": "邮件头部信息不足，无法进行元数据分析"
            }
        
        messages = self.build_messages(valid_headers)
        api_response = self.call_llm_api(messages)
        
        if not api_response:
            return {
                "verdict": "Phishing",
                "phishing_probability": 0.5,
                "confidence": 0.3,
                "reasons": "API调用失败，使用中性概率"
            }
        
        return self.safe_parse_agent_json(api_response)


def analyze_metadata(headers: Dict[str, str], api_url: str, api_key: str, 
                    model: str = "gpt-4o", temperature: float = 0, timeout: int = 60) -> Dict[str, Any]:
    agent = MetadataAgent(api_url, api_key, model, temperature, timeout)
    return agent.analyze(headers)