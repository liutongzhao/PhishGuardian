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
                # print('=================',result)
                # 更新检测结果
                self._update_detection_result(email_id, detection_type, result)
                
                # 检查是否所有检测都已完成
                # detail = EmailDetectionDetail.find_by_email_id(email_id)
                # if detail and self._is_all_detection_completed(detail):
                #     print(f"邮件 {email_id} 所有检测已完成")
                
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
            # print(result)
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
                
            elif detection_type == 'synthesis':
                # 处理第三阶段综合分析结果
                final_result = result.get('final', {})
                final_verdict = final_result.get('final_verdict', 'Safe')
                final_score = final_result.get('final_score', 0.5)
                explanation = result.get('explanation', '综合分析完成')
                
                # 判断是否为钓鱼邮件
                is_phishing = final_verdict == 'Phishing'
                
                # 更新最终结果
                detail.update_final_result(
                    fusion_score=final_score,
                    is_phishing=is_phishing,
                    reason=explanation
                )     
            elif detection_type == 'stage4_analysis':
                # 处理第四阶段邮件内容分析结果
                if result.get('success'):
                    # print(result)
                    analysis = result.get('analysis', {})
                    # print('analysis',analysis)
                    # 更新邮件分析字段
                    detail.email_summary = analysis.get('summary', '')
                    detail.email_type = analysis.get('email_type', '')
                    detail.urgency_level = analysis.get('urgency_level', '普通')
                    detail.importance_level = analysis.get('importance_level', '低')
                    
                    # 更新日程相关字段
                    detail.need_schedule = analysis.get('need_schedule', 0)
                    detail.schedule_name = analysis.get('schedule_name', '')
                    
                    # 处理日程时间字段
                    schedule_time_str = analysis.get('schedule_time', '')
                    if schedule_time_str:
                        try:
                            from datetime import datetime
                            # 尝试解析时间格式
                            if len(schedule_time_str) == 10:  # 格式：2025.09.15
                                detail.schedule_time = datetime.strptime(schedule_time_str, '%Y.%m.%d')
                            elif len(schedule_time_str) == 19:  # 格式：2025.09.15 12:00:00
                                detail.schedule_time = datetime.strptime(schedule_time_str, '%Y.%m.%d %H:%M:%S')
                            else:
                                detail.schedule_time = None
                        except ValueError:
                            detail.schedule_time = None
                    else:
                        detail.schedule_time = None
                    
                    # 设置reserved_field2为'2'表示分析完成
                    detail.reserved_field2 = '2'
                    
                    print(f"第四阶段分析完成，邮件ID: {email_id}")
                    print(f"摘要: {analysis.get('summary', '')}")
                    print(f"类型: {analysis.get('email_type', '')}")
                    print(f"紧急程度: {analysis.get('urgency_level', 1)}")
                    print(f"重要程度: {analysis.get('importance_level', 1)}")
                    print(f"需要日程: {analysis.get('need_schedule', 0)}")
                    print(f"日程名称: {analysis.get('schedule_name', '')}")
                    print(f"日程时间: {schedule_time_str}")
                    
                else:
                    # 分析失败，设置错误状态
                    detail.reserved_field2 = '0'  # 保持检测中状态
                    error_msg = result.get('error', '第四阶段分析失败')
                    print(f"第四阶段分析失败，邮件ID: {email_id}, 错误: {error_msg}")
            
            db.session.commit()
            

            print(f"{detection_type}检测任务已完成，邮件ID: {email_id}")
            
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
        
        all_completed = all(status in [2, 3] for status in statuses)
        
        # 如果所有检测都完成了，且当前是第二阶段，则设置parallel_detection_completed为True
        if all_completed and detection_detail.detection_stage == 2:
            detection_detail.parallel_detection_completed = True
            db.session.add(detection_detail)
            try:
                db.session.commit()
                print(f"邮件 {detection_detail.email_id} 第二阶段并行检测已全部完成")
            except Exception as e:
                db.session.rollback()
                print(f"更新parallel_detection_completed失败: {str(e)}")
        
        return all_completed
    
    
    
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