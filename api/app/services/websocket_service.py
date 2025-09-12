#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebSocket消息推送服务
"""

import json
import logging
from typing import Dict, List, Any
from flask import current_app
from flask_socketio import SocketIO, emit, join_room, leave_room
from app.utils.jwt_utils import JWTUtils

logger = logging.getLogger(__name__)

# 全局SocketIO实例
socketio = None

# 存储用户连接信息
user_connections: Dict[int, List[str]] = {}  # user_id -> [session_ids]


class WebSocketService:
    """WebSocket消息推送服务类"""
    
    @staticmethod
    def init_app(app):
        """初始化WebSocket服务"""
        global socketio
        socketio = SocketIO(
            app,
            cors_allowed_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5174"],
            async_mode='threading'
        )
        
        # 注册事件处理器
        WebSocketService._register_handlers()
        
        return socketio
    
    @staticmethod
    def _register_handlers():
        """注册WebSocket事件处理器"""
        
        @socketio.on('connect')
        def handle_connect(auth):
            """处理客户端连接"""
            try:
                # 验证JWT token
                if not auth or 'token' not in auth:
                    print("WebSocket连接缺少认证token")
                    return False
                
                token = auth['token']
                user_data = JWTUtils.verify_token(token)
                
                if not user_data:
                    print("WebSocket连接token无效")
                    return False
                
                user_id = user_data['user_id']
                session_id = request.sid
                
                # 加入用户房间
                user_room = f"user_{user_id}"
                join_room(user_room)
                
                # 记录用户连接
                if user_id not in user_connections:
                    user_connections[user_id] = []
                user_connections[user_id].append(session_id)
                
                print(f"用户 {user_id} 已连接WebSocket，会话ID: {session_id}")
                
                # 发送连接成功消息
                emit('connected', {'message': '连接成功', 'user_id': user_id})
                
            except Exception as e:
                print(f"WebSocket连接处理错误: {str(e)}")
                return False
        
        @socketio.on('disconnect')
        def handle_disconnect():
            """处理客户端断开连接"""
            try:
                session_id = request.sid
                
                # 从用户连接记录中移除
                disconnected_user = None
                for user_id, sessions in list(user_connections.items()):
                    if session_id in sessions:
                        sessions.remove(session_id)
                        disconnected_user = user_id
                        
                        if not sessions:  # 如果用户没有其他连接，删除记录
                            del user_connections[user_id]
                        
                        print(f"用户 {user_id} 断开WebSocket连接，会话ID: {session_id}")
                        break
                        
            except Exception as e:
                print(f"WebSocket断开连接处理错误: {str(e)}")
        

    
    @staticmethod
    def send_new_email_notification(user_id: int, email_count: int):
        """向指定用户发送新邮件通知"""
        try:
            print(f"开始发送WebSocket通知 - 用户ID: {user_id}, 邮件数量: {email_count}")
            
            if not socketio:
                print("SocketIO未初始化，无法发送消息")
                return
            
            # 检查用户是否在线
            is_connected = WebSocketService.is_user_connected(user_id)
            print(f"用户 {user_id} 连接状态: {is_connected}")
            print(f"当前连接的用户: {list(user_connections.keys())}")
            
            message = {
                'type': 'new_emails',
                'message': f'检测到 {email_count} 封新邮件',
                'email_count': email_count,
                'timestamp': datetime.now().isoformat()
            }
            
            # 发送到用户房间
            user_room = f"user_{user_id}"
            print(f"发送WebSocket消息到房间: {user_room}, 消息内容: {message}")
            socketio.emit('new_email_notification', message, room=user_room)
            
            print(f"已向用户 {user_id} 发送新邮件通知: {email_count} 封")
            
        except Exception as e:
            print(f"发送新邮件通知错误: {str(e)}")
    
    @staticmethod
    def send_detection_completed(user_id: int, data: dict):
        """发送检测完成消息到用户房间（通过新邮件通知机制）"""
        try:
            print(f"开始发送检测完成通知 - 用户ID: {user_id}, 邮件ID: {data.get('email_id')}")
            
            if not socketio:
                print("SocketIO未初始化，无法发送消息")
                return
            
            # 检查用户是否在线
            is_connected = WebSocketService.is_user_connected(user_id)
            print(f"用户 {user_id} 连接状态: {is_connected}")
            print(f"当前连接的用户: {list(user_connections.keys())}")
            
            # 构造消息（使用新邮件通知的格式，但添加检测完成的标识）
            message = {
                'type': 'detection_completed',  # 标识这是检测完成消息
                'email_id': data.get('email_id'),
                'detection_detail': data.get('detection_detail'),
                'message': data.get('message', '邮件检测完成'),
                'timestamp': datetime.now().isoformat()
            }
            
            # 发送到用户房间（使用new_email_notification事件，前端可以根据type字段区分）
            user_room = f"user_{user_id}"
            print(f"发送检测完成消息到房间: {user_room}, 消息内容: {message}")
            socketio.emit('new_email_notification', message, room=user_room)
            
            print(f"已向用户 {user_id} 发送检测完成消息: 邮件 {data.get('email_id')}")
            
        except Exception as e:
            print(f"发送检测完成消息错误: {str(e)}")
    

    @staticmethod
    def get_connected_users() -> List[int]:
        """获取当前连接的用户列表"""
        return list(user_connections.keys())
    
    @staticmethod
    def is_user_connected(user_id: int) -> bool:
        """检查用户是否在线"""
        return user_id in user_connections and len(user_connections[user_id]) > 0


# 导入必要的模块
from datetime import datetime
from flask import request