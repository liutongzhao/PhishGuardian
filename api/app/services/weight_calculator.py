#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
权重计算模块
用于根据邮件内容和头部信息计算各代理的权重
"""

import re
from typing import Dict, List, Optional


class WeightCalculator:
    """
    权重计算器类
    根据邮件内容特征计算各代理权重
    """
    
    # 默认权重配置
    DEFAULT_WEIGHTS = {
        "text": 0.5,
        "url": 0.3,
        "metadata": 0.2
    }
    
    # 邮件头部关键字段正则表达式
    HEADER_KEYS_PATTERN = r"^(from|subject|to|date|reply-to|return-path|message-id|mime-version|content-type|content-transfer-encoding|received|dkim-signature):"
    
    def __init__(self, custom_weights: Optional[Dict[str, float]] = None):
        """
        初始化权重计算器
        
        Args:
            custom_weights: 自定义权重配置，如果不提供则使用默认权重
        """
        self.base_weights = custom_weights or self.DEFAULT_WEIGHTS.copy()
        
    def extract_urls(self, text: str) -> List[str]:
        """
        从文本中提取URL
        
        Args:
            text: 输入文本
            
        Returns:
            URL列表
        """
        url_pattern = r'https?://[^\s<>"]+'  
        return re.findall(url_pattern, text, re.IGNORECASE)
    
    def has_valid_headers(self, headers: str) -> bool:
        """
        检查是否包含有效的邮件头部信息
        
        Args:
            headers: 邮件头部字符串
            
        Returns:
            是否包含有效头部
        """
        if not headers or not headers.strip():
            return False
        
        # 检查是否包含关键邮件头部字段
        lines = headers.strip().split('\n')
        for line in lines:
            if re.match(self.HEADER_KEYS_PATTERN, line.strip(), re.IGNORECASE):
                return True
        return False
    
    def normalize_weights(self, active_agents: List[str]) -> Dict[str, float]:
        """
        标准化权重，确保总和为1.0
        
        Args:
            active_agents: 活跃代理列表
            
        Returns:
            标准化后的权重字典
        """
        # 计算活跃代理的权重总和
        total_weight = sum(self.base_weights[agent] for agent in active_agents if agent in self.base_weights)
        
        # 标准化：按比例重新分配权重
        if total_weight > 0:
            normalized = {agent: self.base_weights[agent] / total_weight 
                         for agent in active_agents if agent in self.base_weights}
        else:
            # 如果总权重为0，平均分配
            normalized = {agent: 1.0 / len(active_agents) for agent in active_agents}
        
        return normalized
    
    def get_weights_for_email(self, body: str, headers: str) -> Dict[str, float]:
        """
        为给定邮件计算权重
        
        Args:
            body: 邮件正文
            headers: 邮件头部
            
        Returns:
            标准化权重字典
        """
        # 提取URL
        urls = self.extract_urls(body or "")
        
        # 确定哪些代理可用
        agent_availability = {
            "text": True,  # 文本代理始终可用
            "url": len(urls) > 0,  # URL代理需要有URL
            "metadata": self.has_valid_headers(headers)  # 元数据代理需要有效头部
        }
        
        # 获取活跃代理列表
        active_agents = [agent for agent, available in agent_availability.items() if available]
        
        # 标准化权重
        return self.normalize_weights(active_agents)


# 便捷函数
def calculate_email_weights(body: str, headers: str, 
                          custom_weights: Optional[Dict[str, float]] = None) -> Dict[str, float]:
    """
    便捷函数：为邮件计算权重
    
    Args:
        body: 邮件正文
        headers: 邮件头部
        custom_weights: 自定义基础权重
        
    Returns:
        标准化后的权重字典
    """
    calculator = WeightCalculator(custom_weights)
    return calculator.get_weights_for_email(body, headers)