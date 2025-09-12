#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件检测服务
处理邮件检测相关的业务逻辑
"""

from app import db
from app.models.email import Email
from app.models.email_detection_detail import EmailDetectionDetail
from app.services.weight_calculator import calculate_email_weights
from typing import Dict, Optional


class EmailDetectionService:
    """
    邮件检测服务类
    处理邮件检测的初始化、权重计算等功能
    """
    
    @staticmethod
    def initialize_detection_weights(email_id: int) -> Dict:
        """
        初始化邮件检测权重
        
        Args:
            email_id: 邮件ID
            
        Returns:
            包含操作结果的字典
        """
        try:
            # 获取邮件信息
            email = Email.query.get(email_id)
            if not email:
                return {
                    'success': False,
                    'message': '邮件不存在'
                }
            
            # 检查邮件是否已经有检测详情记录
            existing_detail = EmailDetectionDetail.find_by_email_id(email_id)
            if existing_detail:
                return {
                    'success': False,
                    'message': '该邮件已经初始化过检测权重'
                }
            
            # 计算权重
            weights = calculate_email_weights(
                body=email.content or "",
                headers=email.headers or ""
            )
            # 权重计算完成
            
            # 根据权重确定检测状态
            content_status = 3 if weights.get('text', 0.0) == 0.0 else 0  # 无需检测 : 未检测
            url_status = 3 if weights.get('url', 0.0) == 0.0 else 0
            metadata_status = 3 if weights.get('metadata', 0.0) == 0.0 else 0
            
            # 创建检测详情记录
            detection_detail = EmailDetectionDetail(
                email_id=email_id,
                content_weight=weights.get('text', 0.0),
                metadata_weight=weights.get('metadata', 0.0),
                url_weight=weights.get('url', 0.0),
                content_detection_status=content_status,
                url_detection_status=url_status,
                metadata_detection_status=metadata_status
            )
            
            # 保存到数据库
            db.session.add(detection_detail)
            db.session.commit()
            
            return {
                'success': True,
                'message': '权重设置成功',
                'data': {
                    'email_id': email_id,
                    'weights': weights,
                    'detection_detail_id': detection_detail.id
                }
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'权重设置失败: {str(e)}'
            }
    
    @staticmethod
    def get_detection_detail(email_id: int) -> Optional[EmailDetectionDetail]:
        """
        获取邮件检测详情
        
        Args:
            email_id: 邮件ID
            
        Returns:
            检测详情对象或None
        """
        return EmailDetectionDetail.find_by_email_id(email_id)