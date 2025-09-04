from .health import health_bp
from .auth import auth_bp
from .email import email_bp

# API蓝图模块
# 基础健康检查API、用户认证API和邮箱管理API

# 所有蓝图列表
blueprints = [
    health_bp,
    auth_bp,
    email_bp
]

__all__ = [
    'health_bp',
    'auth_bp',
    'email_bp',
    'blueprints'
]