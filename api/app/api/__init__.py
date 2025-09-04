from .health import health_bp
from .auth import auth_bp

# API蓝图模块
# 基础健康检查API和用户认证API

# 所有蓝图列表
blueprints = [
    health_bp,
    auth_bp
]

__all__ = [
    'health_bp',
    'auth_bp',
    'blueprints'
]