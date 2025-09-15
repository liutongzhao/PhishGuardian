#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时任务调度器
"""

import os
import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from flask import current_app

logger = logging.getLogger(__name__)


class TaskScheduler:
    """定时任务调度器类"""
    
    def __init__(self):
        self.scheduler = None
        self.app = None
        self._is_initialized = False
    
    def init_app(self, app):
        """
        初始化调度器
        """
        if self._is_initialized:
            return
            
        self.app = app
        
        # 在调试模式下，只在重启后的主进程中初始化调度器
        if app.debug:
            if not os.environ.get('WERKZEUG_RUN_MAIN'):
                return
        
        try:
            # 配置调度器
            jobstores = {
                'default': MemoryJobStore()
            }
            
            executors = {
                'default': ThreadPoolExecutor(20)
            }
            
            job_defaults = {
                'coalesce': False,
                'max_instances': 3
            }
            
            self.scheduler = BackgroundScheduler(
                jobstores=jobstores,
                executors=executors,
                job_defaults=job_defaults,
                timezone='Asia/Shanghai'
            )
            
            # 启动调度器
            self.scheduler.start()
            
            # 在应用上下文中设置任务
            with app.app_context():
                self._setup_jobs()
                
            print("定时任务调度器已启动")
            self._is_initialized = True
            
        except Exception as e:
            print(f"调度器初始化失败: {e}")
            raise
    
    def _setup_jobs(self):
        """
        设置定时任务
        """
        # 邮件获取任务已改为前端手动触发，不再使用定时任务
        # self.scheduler.add_job(
        #     func=self._fetch_emails_api,
        #     trigger="interval",
        #     seconds=20,
        #     id='fetch_emails',
        #     name='邮件获取任务',
        #     replace_existing=True
        # )
        
        print("定时任务设置完成（邮件获取任务已禁用）")
    
    def _fetch_emails_api(self):
        """
        邮件获取任务的API调用函数
        """
        try:
            # 导入API端点函数（避免循环导入）
            from app.api.email import fetch_emails
             
            # 在应用上下文中执行任务
            with self.app.app_context():
                # 直接调用API函数的逻辑部分
                from app.services.email_fetch_service import EmailFetchService
                result = EmailFetchService.fetch_emails()
                print(f"邮件获取定时任务执行完成: {result['message']}")
                
                # 推送消息给所有有邮箱绑定的用户
                if result.get('success') and result.get('data'):
                    self._push_email_notification(result['data'])
                 
        except Exception as e:
            print(f"邮件获取定时任务执行失败: {e}")
    
    def _push_email_notification(self, data):
        """
        推送邮件获取通知给用户
        """
        try:
            from app.services.websocket_service import WebSocketService
            from app.models.user_email_binding import UserEmailBinding
            
            # 获取所有有活跃邮箱绑定的用户
            active_users = UserEmailBinding.query.filter(
                UserEmailBinding.is_active == True,
                UserEmailBinding.is_deleted == False
            ).with_entities(UserEmailBinding.user_id).distinct().all()
            
            email_count = data.get('total_emails', 0)
            success_count = data.get('success_count', 0)
            error_count = data.get('error_count', 0)
            
            # 只有当有新邮件时才推送
            if email_count > 0:
                for user_tuple in active_users:
                    user_id = user_tuple[0]
                    WebSocketService.push_email_notification(
                        user_id=user_id,
                        email_count=email_count,
                        success_count=success_count,
                        error_count=error_count
                    )
                    print(f"已向用户 {user_id} 推送新邮件通知: {email_count} 封")
            else:
                print("本次邮件获取无新邮件，跳过推送")
                
        except Exception as e:
            print(f"推送邮件通知失败: {e}")
    

    
    def add_job(self, func, trigger, job_id, name=None, **kwargs):
        """
        添加新的定时任务
        
        Args:
            func: 要执行的函数
            trigger: 触发器
            job_id: 任务ID
            name: 任务名称
            **kwargs: 其他参数
        """
        if self.scheduler:
            self.scheduler.add_job(
                func=func,
                trigger=trigger,
                id=job_id,
                name=name,
                replace_existing=True,
                **kwargs
            )
            print(f"已添加定时任务: {name or job_id}")
    
    def remove_job(self, job_id):
        """
        移除定时任务
        
        Args:
            job_id: 任务ID
        """
        if self.scheduler:
            try:
                self.scheduler.remove_job(job_id)
                print(f"已移除定时任务: {job_id}")
            except Exception as e:
                print(f"移除定时任务失败: {e}")
    
    def get_jobs(self):
        """
        获取所有任务列表
        
        Returns:
            list: 任务列表
        """
        if self.scheduler:
            return self.scheduler.get_jobs()
        return []
    
    def pause_job(self, job_id):
        """
        暂停任务
        
        Args:
            job_id: 任务ID
        """
        if self.scheduler:
            try:
                self.scheduler.pause_job(job_id)
                print(f"已暂停任务: {job_id}")
            except Exception as e:
                print(f"暂停任务失败: {e}")
    
    def resume_job(self, job_id):
        """
        恢复任务
        
        Args:
            job_id: 任务ID
        """
        if self.scheduler:
            try:
                self.scheduler.resume_job(job_id)
                print(f"已恢复任务: {job_id}")
            except Exception as e:
                print(f"恢复任务失败: {e}")


# 全局调度器实例
scheduler = TaskScheduler()