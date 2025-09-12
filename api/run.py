#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PhishGuardian API 启动脚本
"""

import os
from dotenv import load_dotenv
from app import create_app

# 加载环境变量
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# 创建应用实例
app = create_app()

# 获取socketio实例
from app import socketio

if __name__ == '__main__':
    # 开发环境下使用SocketIO运行
    socketio.run(
        app,
        host=os.environ.get('HOST', '0.0.0.0'),
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_ENV') == 'development',
        allow_unsafe_werkzeug=True
    )