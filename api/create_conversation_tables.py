#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建对话相关数据库表的脚本
"""

import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import Conversation, ConversationMessage

# 加载环境变量
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

def create_tables():
    """创建对话相关表"""
    app = create_app()
    
    with app.app_context():
        try:
            # 创建表
            db.create_all()
            print("✅ 对话相关数据库表创建成功！")
            print("已创建的表:")
            print("- conversations (对话会话表)")
            print("- conversation_messages (对话消息表)")
            
        except Exception as e:
            print(f"❌ 创建表时发生错误: {e}")
            raise

if __name__ == '__main__':
    create_tables()