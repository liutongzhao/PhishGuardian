#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新163邮箱SMTP配置脚本
将163邮箱的SMTP从TLS端口587改为SSL端口465
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import EmailProvider

def update_163_smtp_config():
    """更新163邮箱SMTP配置"""
    
    app = create_app()
    
    with app.app_context():
        try:
            # 查找163邮箱提供商
            provider_163 = EmailProvider.query.filter_by(name='163').first()
            
            if not provider_163:
                print("❌ 未找到163邮箱提供商配置")
                return False
            
            print(f"📧 找到163邮箱配置: {provider_163.display_name}")
            print(f"当前SMTP配置: {provider_163.smtp_server}:{provider_163.smtp_port}")
            print(f"当前加密方式: {'SSL' if hasattr(provider_163, 'smtp_ssl') and provider_163.smtp_ssl else 'TLS' if provider_163.smtp_tls else '无加密'}")
            
            # 更新SMTP配置为SSL端口465
            provider_163.smtp_port = 465
            provider_163.smtp_tls = False  # 关闭TLS
            
            # 如果有smtp_ssl字段，设置为True
            if hasattr(provider_163, 'smtp_ssl'):
                provider_163.smtp_ssl = True
            else:
                # 如果没有smtp_ssl字段，需要先添加
                print("⚠️  检测到数据库中没有smtp_ssl字段，请先运行add_smtp_ssl_field.py脚本")
                return False
            
            # 提交更改
            db.session.commit()
            
            print("\n✅ 163邮箱SMTP配置更新成功！")
            print(f"新配置: {provider_163.smtp_server}:{provider_163.smtp_port} (SSL)")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ 更新失败: {str(e)}")
            return False

if __name__ == '__main__':
    print("🔧 开始更新163邮箱SMTP配置...")
    print("将SMTP端口从587(TLS)改为465(SSL)\n")
    
    success = update_163_smtp_config()
    
    if success:
        print("\n🎉 163邮箱SMTP配置更新完成！")
        print("现在163邮箱将使用SSL加密连接(端口465)")
    else:
        print("\n💥 163邮箱SMTP配置更新失败！")
        sys.exit(1)