from datetime import datetime, timedelta
from functools import wraps
from flask import current_app, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt, verify_jwt_in_request
)
import jwt


class JWTUtils:
    """JWT工具类"""
    
    jwt_manager = JWTManager()
    
    @classmethod
    def init_app(cls, app):
        """初始化JWT扩展"""
        cls.jwt_manager.init_app(app)
    
    @staticmethod
    def generate_token(user):
        """
        生成JWT token
        
        Args:
            user: 用户对象
            
        Returns:
            dict: 包含token和用户信息的字典
        """
        # 创建token载荷
        payload = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(days=1),  # 1天过期
            'iat': datetime.utcnow(),
            'type': 'access'
        }
        
        # 生成token
        token = jwt.encode(
            payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )
        
        return {
            'token': token,
            'expires_in': 86400,  # 24小时，单位秒
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }
    
    @staticmethod
    def verify_token(token):
        """
        验证JWT token
        
        Args:
            token: JWT token字符串
            
        Returns:
            dict: 解码后的载荷，如果验证失败返回None
        """
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256']
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None  # token已过期
        except jwt.InvalidTokenError:
            return None  # token无效
    
    @staticmethod
    def get_user_from_token(token):
        """
        从token中获取用户对象
        
        Args:
            token: JWT token字符串
            
        Returns:
            User: 用户对象，如果获取失败返回None
        """
        # 延迟导入避免循环导入
        from ..models.user import User
        
        payload = JWTUtils.verify_token(token)
        if payload:
            user_id = payload.get('user_id')
            if user_id:
                return User.query.get(user_id)
        return None


def token_required(f):
    """
    装饰器：要求请求携带有效的JWT token
    
    Args:
        f: 被装饰的函数
        
    Returns:
        function: 装饰后的函数
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 从请求头中获取token
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({
                    'success': False,
                    'message': 'Token格式错误，应为: Bearer <token>'
                }), 401
        
        if not token:
            return jsonify({
                'success': False,
                'message': '缺少访问token'
            }), 401
        
        # 验证token
        payload = JWTUtils.verify_token(token)
        if payload is None:
            return jsonify({
                'success': False,
                'message': 'Token无效或已过期'
            }), 401
        
        # 获取用户信息
        # 延迟导入避免循环导入
        from ..models.user import User
        
        current_user = User.query.get(payload['user_id'])
        if not current_user:
            return jsonify({
                'success': False,
                'message': '用户不存在'
            }), 401
        
        # 将当前用户信息传递给被装饰的函数
        return f(current_user, *args, **kwargs)
    
    return decorated


def init_jwt(app):
    """
    初始化JWT扩展
    
    Args:
        app: Flask应用实例
    """
    jwt_manager = JWTManager(app)
    
    # JWT错误处理
    @jwt_manager.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'success': False,
            'message': 'Token已过期'
        }), 401
    
    @jwt_manager.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'success': False,
            'message': 'Token无效'
        }), 401
    
    @jwt_manager.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'success': False,
            'message': '缺少访问token'
        }), 401
    
    return jwt_manager