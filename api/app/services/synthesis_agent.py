import re
import json
import requests
from typing import Dict, Any, List


class SynthesisAgent:
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
        
        # 总控提示词（用于把三路判定综合成自然语言解释）
        self.system_prompt = """You are an expert in cybersecurity with deep expertise in phishing.
Your task is to take the detailed technical explanations provided by the three specialized agents (text, URL, and metadata) for why an email is classified as phishing or legitimate, and synthesize them into one coherent, reliable, and complete explanation written in plain, everyday language. Ensure that your explanation is truthful, meaningful, and based solely on factual evidence—do not include any fabricated details. Avoid technical jargon, simplify complex concepts, and provide clear, concise reasons for the classification that accurately reflect the underlying data."""
        
        # 默认权重配置
        self.default_weights = {"text": 0.5, "url": 0.3, "metadata": 0.2}
        self.phishing_threshold = 0.6
    
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
        # 字段别名兜底
        if "reasons" not in data and "reason" in data:
            data["reasons"] = data["reason"]
        if "phishing_probability" not in data:
            for k in ("probability", "score", "phish_prob", "phishing_score"):
                if k in data:
                    data["phishing_probability"] = data[k]
                    break

        # 补全与数值裁剪
        data.setdefault("verdict", "Phishing")
        for k, dv in (("phishing_probability", 0.5), ("confidence", 0.5)):
            try:
                v = float(data.get(k, dv))
            except Exception:
                v = dv
            data[k] = max(0.0, min(1.0, v))
        data.setdefault("reasons", "（无）")

        # verdict 合法化
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
        # 去掉可能的代码围栏
        s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s, flags=re.I)

        # 情况 A：整体就是 JSON
        if s.startswith("{") and s.rstrip().endswith("}"):
            try:
                return self._postfix_schema(json.loads(s))
            except Exception as e:
                print("raw loads failed:", e, "\nSTR:", repr(s))

        # 情况 B：提取第一个 {...}（非贪婪）
        m = re.search(r"\{[\s\S]*?\}", s)
        if m:
            s = m.group(0)

        # 清洗不可见分隔符，避免解析报错
        s = s.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029").replace("\ufeff", "")
        # 尾逗号清理
        s = re.sub(r",\s*([}\]])", r"\1", s)

        try:
            return self._postfix_schema(json.loads(s))
        except Exception:
            print("JSON解析失败，repr：", repr(s))
            return default
    
    def normalize_weights(self, active_keys: List[str], weights: Dict[str, float]) -> Dict[str, float]:
        total = sum(weights[k] for k in active_keys)
        return {k: (weights[k] / total if total > 0 else 1.0 / len(active_keys)) for k in active_keys}
    
    def fuse_scores(self, results: Dict[str, Dict[str, Any]], weights: Dict[str, float]) -> Dict[str, Any]:
        """
        使用 组合分数 = Σ(权重 × 概率 × 置信度)
        """
        active = [k for k, v in results.items() if v is not None]
        if not active:
            return {"final_verdict": "Phishing", "final_score": 0.5, "threshold": self.phishing_threshold, "by_agent": []}

        w = self.normalize_weights(active, weights)
        combined = 0.0
        details = []
        for k in active:
            r = results[k]
            part = r["phishing_probability"] * r["confidence"]
            combined += w[k] * part
            details.append({
                "agent": k,
                "weight": w[k],
                "phishing_probability": r["phishing_probability"],
                "confidence": r["confidence"],
                "weighted_component": w[k] * part,
                "verdict": r.get("verdict", "")
            })

        final_verdict = "Phishing" if combined >= self.phishing_threshold else "Legitimate"
        return {"final_verdict": final_verdict, "final_score": round(combined, 4), "threshold": self.phishing_threshold, "by_agent": details}
    
    def build_messages(self, text_result: Dict[str, Any], url_result: Dict[str, Any], 
                      metadata_result: Dict[str, Any], fused_result: Dict[str, Any]) -> List[Dict[str, str]]:
        synthesis_user_content = (
            "请把三位代理的JSON结论综合为一段简明中文解释，避免术语，基于事实，不要捏造：\n\n"
            f"[Text]\n{json.dumps(text_result, ensure_ascii=False)}\n\n"
            f"[URL]\n{json.dumps(url_result, ensure_ascii=False)}\n\n"
            f"[Metadata]\n{json.dumps(metadata_result, ensure_ascii=False)}\n\n"
            f"融合分数：{fused_result['final_score']}，阈值：{fused_result['threshold']}，最终结论：{fused_result['final_verdict']}"
        )
        
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": synthesis_user_content}
        ]
    
    def synthesize(self, text_result: Dict[str, Any], url_result: Dict[str, Any], 
                  metadata_result: Dict[str, Any], weights: Dict[str, float] = None) -> Dict[str, Any]:
        # 使用传入的权重或默认权重
        if weights is None:
            weights = self.default_weights
        
        # 1) 融合打分
        results = {
            "text": text_result,
            "url": url_result,
            "metadata": metadata_result
        }
        fused = self.fuse_scores(results, weights)
        
        # 2) 生成自然语言解释
        messages = self.build_messages(text_result, url_result, metadata_result, fused)
        synth_resp = self.call_llm_api(messages)
        
        explanation = "（无法生成综合解释）"
        try:
            if synth_resp and "choices" in synth_resp:
                explanation = synth_resp["choices"][0]["message"]["content"]
        except Exception as e:
            print("生成综合解释失败：", e)
        
        # 3) 输出报告，包含权重信息
        return {
            "final": fused,
            "agents": results,
            "weights": weights,  # 添加权重信息
            "explanation": explanation
        }


def synthesize_results(text_result: Dict[str, Any], url_result: Dict[str, Any], 
                      metadata_result: Dict[str, Any], api_url: str, api_key: str,
                      weights: Dict[str, float] = None,  # 新增权重参数
                      model: str = "gpt-4o", temperature: float = 0, timeout: int = 60) -> Dict[str, Any]:
    """
    综合三个代理的分析结果，生成最终判定报告
    
    Args:
        text_result: 文本分析结果
        url_result: URL分析结果
        metadata_result: 元数据分析结果
        api_url: LLM API地址
        api_key: LLM API密钥
        weights: 权重配置，格式如 {"text": 0.5, "url": 0.3, "metadata": 0.2}
        model: 使用的模型
        temperature: 温度参数
        timeout: 超时时间
    
    Returns:
        包含最终判定、各代理结果和综合解释的字典
    """
    agent = SynthesisAgent(api_url, api_key, model, temperature, timeout)
    return agent.synthesize(text_result, url_result, metadata_result, weights)