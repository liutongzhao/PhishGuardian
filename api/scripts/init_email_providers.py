#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮箱厂商数据初始化脚本
用于向数据库中插入常用的邮箱厂商配置信息
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import EmailProvider
from datetime import datetime

def init_email_providers():
    """初始化邮箱厂商数据"""
    
    # 常用邮箱厂商配置数据
    providers_data = [
        {
            'name': 'gmail',
            'display_name': 'Gmail',
            'email_suffix': '@gmail.com',
            'imap_server': 'imap.gmail.com',
            'imap_port': 993,
            'imap_ssl': True,
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'smtp_tls': True,
            'is_active': True
        },
        {
            'name': 'qq',
            'display_name': 'QQ邮箱',
            'email_suffix': '@qq.com',
            'imap_server': 'imap.qq.com',
            'imap_port': 993,
            'imap_ssl': True,
            'smtp_server': 'smtp.qq.com',
            'smtp_port': 587,
            'smtp_tls': True,
            'is_active': True
        },
        {
            'name': '163',
            'display_name': '网易163邮箱',
            'email_suffix': '@163.com',
            'imap_server': 'imap.163.com',
            'imap_port': 993,
            'imap_ssl': True,
            'smtp_server': 'smtp.163.com',
            'smtp_port': 587,
            'smtp_tls': True,
            'is_active': True
        },
        {
            'name': '126',
            'display_name': '网易126邮箱',
            'email_suffix': '@126.com',
            'imap_server': 'imap.126.com',
            'imap_port': 993,
            'imap_ssl': True,
            'smtp_server': 'smtp.126.com',
            'smtp_port': 587,
            'smtp_tls': True,
            'is_active': True
        },
        {
            'name': 'outlook',
            'display_name': 'Outlook/Hotmail',
            'email_suffix': '@outlook.com',
            'imap_server': 'outlook.office365.com',
            'imap_port': 993,
            'imap_ssl': True,
            'smtp_server': 'smtp-mail.outlook.com',
            'smtp_port': 587,
            'smtp_tls': True,
            'is_active': True
        },
        {
            'name': 'yahoo',
            'display_name': 'Yahoo Mail',
            'email_suffix': '@yahoo.com',
            'imap_server': 'imap.mail.yahoo.com',
            'imap_port': 993,
            'imap_ssl': True,
            'smtp_server': 'smtp.mail.yahoo.com',
            'smtp_port': 587,
            'smtp_tls': True,
            'is_active': True
        },
        {
            'name': 'sina',
            'display_name': '新浪邮箱',
            'email_suffix': '@sina.com',
            'imap_server': 'imap.sina.com',
            'imap_port': 993,
            'imap_ssl': True,
            'smtp_server': 'smtp.sina.com',
            'smtp_port': 587,
            'smtp_tls': True,
            'is_active': True
        },
        {
            'name': 'sohu',
            'display_name': '搜狐邮箱',
            'email_suffix': '@sohu.com',
            'imap_server': 'imap.sohu.com',
            'imap_port': 993,
            'imap_ssl': True,
            'smtp_server': 'smtp.sohu.com',
            'smtp_port': 587,
            'smtp_tls': True,
            'is_active': True
        }
    ]
    
    app = create_app('development')
    
    with app.app_context():
        print("开始初始化邮箱厂商数据...")
        
        # 检查是否已经有数据
        existing_count = EmailProvider.query.count()
        if existing_count > 0:
            print(f"数据库中已存在 {existing_count} 条邮箱厂商记录")
            if input("是否要清空现有数据并重新初始化？(y/N): ").lower() != 'y':
                print("操作已取消")
                return
            
            # 清空现有数据
            EmailProvider.query.delete()
            db.session.commit()
            print("已清空现有数据")
        
        # 插入新数据
        success_count = 0
        for provider_data in providers_data:
            try:
                provider = EmailProvider(**provider_data)
                db.session.add(provider)
                success_count += 1
                print(f"✓ 添加邮箱厂商: {provider_data['display_name']}")
            except Exception as e:
                print(f"✗ 添加邮箱厂商失败 {provider_data['display_name']}: {str(e)}")
        
        try:
            db.session.commit()
            print(f"\n成功初始化 {success_count} 个邮箱厂商配置")
            print("邮箱厂商数据初始化完成！")
        except Exception as e:
            db.session.rollback()
            print(f"\n数据库提交失败: {str(e)}")
            return False
    
    return True

if __name__ == '__main__':
    init_email_providers()