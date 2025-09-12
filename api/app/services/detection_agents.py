import os
from typing import Dict, Any

from .text_agent import analyze_text
from .url_agent import analyze_urls_from_text
from .metadata_agent import analyze_metadata

class DetectionAgents:
    """检测代理集成服务"""
    
    def __init__(self, api_url: str, api_key: str, model: str = "gpt-4o", temperature: float = 0, timeout: int = 60):
        self.api_url = api_url
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.timeout = timeout
    
    def analyze_content(self, body: str) -> Dict[str, Any]:
        """分析邮件内容文本
        
        Args:
            body: 邮件正文内容
            
        Returns:
            检测结果字典
        """
        try:
            return analyze_text(
                body=body,
                api_url=self.api_url,
                api_key=self.api_key,
                model=self.model,
                temperature=self.temperature,
                timeout=self.timeout
            )
        except Exception as e:
            return {
                "verdict": "Phishing",
                "phishing_probability": 0.5,
                "confidence": 0.3,
                "reasons": f"文本检测失败: {str(e)}"
            }
    
    def analyze_urls(self, body: str) -> Dict[str, Any]:
        """分析邮件中的URL
        
        Args:
            body: 邮件正文内容
            
        Returns:
            检测结果字典
        """
        try:
            return analyze_urls_from_text(
                body=body,
                api_url=self.api_url,
                api_key=self.api_key,
                model=self.model,
                temperature=self.temperature,
                timeout=self.timeout
            )
        except Exception as e:
            return {
                "verdict": "Phishing",
                "phishing_probability": 0.5,
                "confidence": 0.3,
                "reasons": f"URL检测失败: {str(e)}"
            }
    
    def analyze_metadata(self, headers: Dict[str, str]) -> Dict[str, Any]:
        """分析邮件元数据
        
        Args:
            headers: 邮件头部信息字典
            
        Returns:
            检测结果字典
        """
        try:
            return analyze_metadata(
                headers=headers,
                api_url=self.api_url,
                api_key=self.api_key,
                model=self.model,
                temperature=self.temperature,
                timeout=self.timeout
            )
        except Exception as e:
            return {
                "verdict": "Phishing",
                "phishing_probability": 0.5,
                "confidence": 0.3,
                "reasons": f"元数据检测失败: {str(e)}"
            }

# 默认配置
DEFAULT_API_URL = "https://yunwu.ai/v1/chat/completions"
DEFAULT_API_KEY = "sk-BJyJEGSpGrNS2G0eFCscVgjBEp34Hb4FzCagVv56H7qrSSIl"
DEFAULT_MODEL = "gpt-4o"

# 全局检测代理实例
detection_agents = DetectionAgents(
    api_url=DEFAULT_API_URL,
    api_key=DEFAULT_API_KEY,
    model=DEFAULT_MODEL
)