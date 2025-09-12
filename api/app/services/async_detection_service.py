import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, Optional
from app import db
from app.models.email_detection_detail import EmailDetectionDetail, DetectionStatus

from app.models.email import Email
import logging

# 获取日志记录器（不配置全局basicConfig以避免影响其他日志格式）
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AsyncDetectionService:
    """异步检测服务"""
    
    def __init__(self, max_workers: int = 3):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self._running_tasks = {}  # 存储正在运行的任务
        self._lock = threading.Lock()
    
    def submit_detection_task(self, email_id: int, detection_type: str, detection_func, *args, **kwargs):
        """提交检测任务
        
        Args:
            email_id: 邮件ID
            detection_type: 检测类型 ('content', 'url', 'metadata')
            detection_func: 检测函数
            *args, **kwargs: 传递给检测函数的参数
        
        Returns:
            Future对象
        """
        task_key = f"{email_id}_{detection_type}"
        
        with self._lock:
            if task_key in self._running_tasks:
                print(f"任务 {task_key} 已在运行中")
                return self._running_tasks[task_key]
            
            # 提交任务
            future = self.executor.submit(
                self._execute_detection_with_callback,
                email_id, detection_type, detection_func, *args, **kwargs
            )
            
            self._running_tasks[task_key] = future
            
            return future
    
    def _execute_detection_with_callback(self, email_id: int, detection_type: str, detection_func, *args, **kwargs):
        """执行检测并处理回调"""
        task_key = f"{email_id}_{detection_type}"
        
        try:
            # 获取当前Flask应用实例
            from flask import current_app
            from app import create_app
            
            # 尝试获取当前应用，如果没有则创建新的
            try:
                app = current_app._get_current_object()
            except RuntimeError:
                app = create_app()
            
            # 在Flask应用上下文中执行检测和数据库操作
            with app.app_context():
                # 执行检测
                result = detection_func(*args, **kwargs)
                
                # 更新检测结果
                self._update_detection_result(email_id, detection_type, result)
                
                # 检查是否所有检测都已完成，如果是则发送WebSocket通知
                detail = EmailDetectionDetail.find_by_email_id(email_id)
                if detail and self._is_all_detection_completed(detail):
                    self._send_websocket_notification(email_id, detail)
                
                # 检测完成
            
            return result
            
        except Exception as e:
            print(f"检测任务失败: {task_key}, 错误: {str(e)}")
            # 在Flask应用上下文中更新失败状态
            try:
                from flask import current_app
                from app import create_app
                try:
                    app = current_app._get_current_object()
                except RuntimeError:
                    app = create_app()
                    
                with app.app_context():
                    self._update_detection_error(email_id, detection_type, str(e))
            except Exception as update_error:
                print(f"更新错误状态也失败了: {str(update_error)}")
            raise
        
        finally:
            # 清理任务记录
            with self._lock:
                self._running_tasks.pop(task_key, None)
    
    def _update_detection_result(self, email_id: int, detection_type: str, result: Dict[str, Any]):
        """更新检测结果到数据库"""
        try:
            detail = EmailDetectionDetail.find_by_email_id(email_id)
            if not detail:
                print(f"未找到邮件检测详情: email_id={email_id}")
                return
            
            # 提取结果数据
            phishing_probability = result.get('phishing_probability', 0.5)
            confidence = result.get('confidence', 0.5)
            is_phishing = result.get('verdict', 'Phishing') == 'Phishing'
            reason = result.get('reasons', '检测完成')
            
            # 根据检测类型更新相应字段
            if detection_type == 'content':
                detail.update_content_detection(
                    weight=detail.content_weight,
                    probability=phishing_probability,
                    confidence=confidence,
                    is_phishing=is_phishing,
                    reason=reason
                )
                detail.content_detection_status = DetectionStatus.COMPLETED.value
                
            elif detection_type == 'url':
                detail.update_url_detection(
                    weight=detail.url_weight,
                    probability=phishing_probability,
                    confidence=confidence,
                    is_phishing=is_phishing,
                    reason=reason
                )
                detail.url_detection_status = DetectionStatus.COMPLETED.value
                
            elif detection_type == 'metadata':
                detail.update_metadata_detection(
                    weight=detail.metadata_weight,
                    probability=phishing_probability,
                    confidence=confidence,
                    is_phishing=is_phishing,
                    reason=reason
                )
                detail.metadata_detection_status = DetectionStatus.COMPLETED.value
            
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            print(f"更新检测结果失败: {str(e)}")
    

    
    def _update_detection_error(self, email_id: int, detection_type: str, error_msg: str):
        """更新检测错误状态"""
        try:
            detail = EmailDetectionDetail.find_by_email_id(email_id)
            if not detail:
                return
            
            # 设置错误状态和原因
            if detection_type == 'content':
                detail.content_detection_status = DetectionStatus.COMPLETED.value
                detail.content_reason = f"检测失败: {error_msg}"
            elif detection_type == 'url':
                detail.url_detection_status = DetectionStatus.COMPLETED.value
                detail.url_reason = f"检测失败: {error_msg}"
            elif detection_type == 'metadata':
                detail.metadata_detection_status = DetectionStatus.COMPLETED.value
                detail.metadata_reason = f"检测失败: {error_msg}"
            
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            print(f"更新错误状态失败: {str(e)}")
    
    def _is_all_detection_completed(self, detection_detail) -> bool:
        """检查是否所有检测都已完成"""
        # 检查所有检测状态是否都是完成(2)或无需检测(3)
        statuses = [
            detection_detail.content_detection_status,
            detection_detail.url_detection_status,
            detection_detail.metadata_detection_status
        ]
        
        return all(status in [2, 3] for status in statuses)
    
    def _send_websocket_notification(self, email_id: int, detection_detail):
        """发送WebSocket通知"""
        try:
            from app.utils.websocket import send_websocket_message
            
            # 构造消息数据
            message_data = {
                'email_id': email_id,
                'detection_detail': {
                    'id': detection_detail.id,
                    'detection_stage': detection_detail.detection_stage,
                    'content_detection_status': detection_detail.content_detection_status,
                    'url_detection_status': detection_detail.url_detection_status,
                    'metadata_detection_status': detection_detail.metadata_detection_status
                },
                'message': f'邮件 {email_id} 检测完成'
            }
            
            # 发送WebSocket消息
            send_websocket_message('detection_completed', message_data)
            
        except Exception as e:
            print(f"发送WebSocket通知失败: {str(e)}")
    
    def get_task_status(self, email_id: int, detection_type: str) -> Optional[str]:
        """获取任务状态"""
        task_key = f"{email_id}_{detection_type}"
        
        with self._lock:
            if task_key in self._running_tasks:
                future = self._running_tasks[task_key]
                if future.done():
                    return 'completed'
                else:
                    return 'running'
            return None
    
    def shutdown(self):
        """关闭服务"""
        print("正在关闭异步检测服务...")
        self.executor.shutdown(wait=True)
        print("异步检测服务已关闭")

# 全局异步检测服务实例
async_detection_service = AsyncDetectionService()