from functools import wraps
from flask import request, jsonify, g
from app.utils.jwt_utils import JWTUtils
from app.utils import api_response
from app.models.user import User


def jwt_required(f):
    """
    JWT认证装饰器
    用于保护需要认证的路由
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 获取Authorization头
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return api_response(
                success=False,
                message='缺少认证令牌'
            ), 401
        
        # 检查Bearer格式
        try:
            scheme, token = auth_header.split(' ', 1)
            if scheme.lower() != 'bearer':
                return api_response(
                    success=False,
                    message='认证令牌格式错误'
                ), 401
        except ValueError:
            return api_response(
                success=False,
                message='认证令牌格式错误'
            ), 401
        
        # 验证token
        try:
            payload = JWTUtils.verify_token(token)
            if not payload:
                return api_response(
                    success=False,
                    message='认证令牌无效'
                ), 401
            
            # 获取用户信息
            user = JWTUtils.get_user_from_token(token)
            if not user:
                return api_response(
                    success=False,
                    message='用户不存在或已被禁用'
                ), 401
            
            # 将用户信息存储到g对象中，供视图函数使用
            g.current_user = user
            g.token_payload = payload
            
        except Exception as e:
            return api_response(
                success=False,
                message=f'认证失败: {str(e)}'
            ), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


def optional_jwt(f):
    """
    可选JWT认证装饰器
    如果提供了token则验证，没有提供则继续执行
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 获取Authorization头
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            try:
                scheme, token = auth_header.split(' ', 1)
                if scheme.lower() == 'bearer':
                    # 验证token
                    payload = JWTUtils.verify_token(token)
                    if payload:
                        user = JWTUtils.get_user_from_token(token)
                        if user:
                            g.current_user = user
                            g.token_payload = payload
            except Exception:
                # 可选认证失败时不返回错误，继续执行
                pass
        
        return f(*args, **kwargs)
    
    return decorated_function


def admin_required(f):
    """
    管理员权限装饰器
    需要先通过jwt_required认证
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 检查是否已通过JWT认证
        if not hasattr(g, 'current_user') or not g.current_user:
            return api_response(
                success=False,
                message='需要认证'
            ), 401
        
        # 检查管理员权限（这里假设User模型有is_admin字段）
        # 如果没有is_admin字段，可以根据实际情况修改权限检查逻辑
        if not hasattr(g.current_user, 'is_admin') or not g.current_user.is_admin:
            return api_response(
                success=False,
                message='需要管理员权限'
            ), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


def get_current_user():
    """
    获取当前认证用户
    """
    return getattr(g, 'current_user', None)


def get_token_payload():
    """
    获取当前token的payload
    """
    return getattr(g, 'token_payload', None)