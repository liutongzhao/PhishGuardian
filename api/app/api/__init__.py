from .health import health_bp

# API蓝图模块
# 基础健康检查API

# 所有蓝图列表
blueprints = [
    health_bp
]

__all__ = [
    'health_bp',
    'blueprints'
]