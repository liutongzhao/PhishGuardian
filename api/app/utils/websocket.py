import logging

logger = logging.getLogger(__name__)

def send_websocket_message(event_name: str, data: dict):
    """
    发送WebSocket消息
    
    Args:
        event_name: 事件名称
        data: 要发送的数据
    """
    try:
        # 使用WebSocketService发送消息
        from app.services.websocket_service import WebSocketService
        
        if event_name == 'detection_completed':
            # 从data中提取必要信息
            email_id = data.get('email_id')
            message = data.get('message', '检测完成')
            
            # 从邮件记录中获取user_id
            from app.models.email import Email
            email = Email.query.get(email_id)
            if not email:
                print(f"未找到邮件记录: email_id={email_id}")
                return
            
            # 发送到用户房间
            from app.services.websocket_service import WebSocketService
            WebSocketService.send_detection_completed(email.user_id, data)
        else:
            # 其他类型的消息可以扩展
            print(f"未处理的WebSocket事件类型: {event_name}")
                
        print(f"WebSocket消息发送成功: {event_name}")
    except Exception as e:
        print(f"WebSocket消息发送失败: {str(e)}")
        raise