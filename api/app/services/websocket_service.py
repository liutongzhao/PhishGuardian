#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebSocket推送服务
"""

import logging
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import request
from app.utils.jwt_utils import JWTUtils

logger = logging.getLogger(__name__)

# 全局SocketIO实例
socketio = None
# 全局连接用户字典
connected_users = {}

class WebSocketService:
    """WebSocket推送服务类"""
    
    def __init__(self):
        pass
    
    @staticmethod
    def init_app(app):
        """初始化SocketIO"""
        global socketio
        socketio = SocketIO(
            app,
            cors_allowed_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5174"],
            async_mode='threading'
        )
        
        # 注册事件处理器
        websocket_service = WebSocketService()
        websocket_service._register_handlers()
        
        print("WebSocket服务已初始化")
        return socketio
    
    def _register_handlers(self):
        """注册WebSocket事件处理器"""
        global socketio
        
        @socketio.on('connect')
        def handle_connect(auth):
            """处理客户端连接"""
            try:
                # 验证JWT token
                print(f"WebSocket连接认证信息: {auth}")
                token = auth.get('token') if auth else None
                print(f"WebSocket接收到的token: {token[:50] if token else None}...")
                if not token:
                    print("WebSocket连接被拒绝：缺少token")
                    return False
                
                # 验证token并获取用户信息
                user_info = JWTUtils.verify_token(token)
                print(f"Token验证结果: {user_info}")
                if not user_info:
                    print("WebSocket连接被拒绝：无效token")
                    return False
                
                user_id = user_info.get('user_id')
                session_id = request.sid
                
                # 用户加入自己的房间
                join_room(f"user_{user_id}")
                
                # 记录连接的用户
                connected_users[user_id] = session_id
                
                print(f"用户 {user_id} 已连接WebSocket，session_id: {session_id}")
                
                # 发送连接成功消息
                emit('connected', {'message': '连接成功', 'user_id': user_id})
                
            except Exception as e:
                print(f"WebSocket连接处理失败: {e}")
                return False
        
        @socketio.on('disconnect')
        def handle_disconnect():
            """处理客户端断开连接"""
            try:
                session_id = request.sid
                # 找到断开连接的用户
                user_id = None
                for uid, sid in connected_users.items():
                    if sid == session_id:
                        user_id = uid
                        break
                
                if user_id:
                    # 离开房间
                    leave_room(f"user_{user_id}")
                    # 移除连接记录
                    del connected_users[user_id]
                    print(f"用户 {user_id} 已断开WebSocket连接")
                else:
                    print(f"未知用户断开WebSocket连接，session_id: {session_id}")
                    
            except Exception as e:
                print(f"WebSocket断开连接处理失败: {e}")
    
    @staticmethod
    def push_message(user_id, message_type, data):
        """向指定用户推送消息"""
        global socketio
        if not socketio:
            print("WebSocket服务未初始化")
            return False
        
        try:
            room = f"user_{user_id}"
            message = {
                'type': message_type,
                'data': data,
                'timestamp': int(__import__('time').time() * 1000)
            }
            
            socketio.emit('push_message', message, room=room)
            print(f"向用户 {user_id} 推送消息: {message_type}")
            return True
            
        except Exception as e:
            print(f"推送消息失败: {e}")
            return False
    
    @staticmethod
    def push_email_notification(user_id, email_count, success_count, error_count):
        """推送新邮件通知"""
        data = {
            'email_count': email_count,
            'success_count': success_count,
            'error_count': error_count,
            'message': f'成功获取 {email_count} 封新邮件'
        }
        return WebSocketService.push_message(user_id, 'new_emails', data)

# 全局WebSocket服务实例
websocket_service = WebSocketService()