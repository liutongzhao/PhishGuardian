#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加SMTP SSL字段并更新数据库结构
为了更准确地表示SSL和TLS配置，添加smtp_ssl字段
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import EmailProvider
from sqlalchemy import text

def add_smtp_ssl_field():
    """添加smtp_ssl字段到EmailProvider表"""
    
    app = create_app('development')
    
    with app.app_context():
        print("开始添加SMTP SSL字段...")
        
        try:
            # 检查字段是否已存在
            result = db.session.execute(text("PRAGMA table_info(email_providers)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'smtp_ssl' in columns:
                print("smtp_ssl字段已存在，跳过添加")
            else:
                # 添加新字段
                print("添加smtp_ssl字段...")
                db.session.execute(text(
                    "ALTER TABLE email_providers ADD COLUMN smtp_ssl BOOLEAN DEFAULT 0 NOT NULL"
                ))
                print("✓ smtp_ssl字段添加成功")
            
            # 更新所有记录的smtp_ssl字段
            print("\n更新SMTP SSL配置...")
            providers = EmailProvider.query.all()
            
            for provider in providers:
                # 根据端口判断是否使用SSL
                if provider.smtp_port == 465:
                    provider.smtp_ssl = True
                    provider.smtp_tls = False  # SSL和TLS互斥
                    print(f"✓ {provider.display_name}: 设置为SSL (端口465)")
                elif provider.smtp_port == 587:
                    provider.smtp_ssl = False
                    provider.smtp_tls = True   # 使用STARTTLS
                    print(f"✓ {provider.display_name}: 设置为TLS (端口587)")
                else:
                    # 其他端口保持原有配置
                    provider.smtp_ssl = False
                    print(f"✓ {provider.display_name}: 保持原有配置 (端口{provider.smtp_port})")
            
            db.session.commit()
            print("\n✓ 所有邮箱提供商的SSL/TLS配置更新完成")
            
            # 显示更新后的配置
            print("\n当前配置:")
            for provider in EmailProvider.query.all():
                ssl_type = "SSL" if provider.smtp_ssl else ("TLS" if provider.smtp_tls else "无加密")
                print(f"  {provider.display_name}: SMTP {provider.smtp_server}:{provider.smtp_port} ({ssl_type})")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"\n✗ 操作失败: {str(e)}")
            return False

if __name__ == '__main__':
    success = add_smtp_ssl_field()
    if success:
        print("\nSMTP SSL字段添加和配置更新完成！")
    else:
        print("\nSMTP SSL字段添加失败！")
        sys.exit(1)