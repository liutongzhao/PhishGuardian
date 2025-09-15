#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件获取服务
"""

import imaplib
import email
import threading
import time
from datetime import datetime
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import email.utils
import logging
from flask import current_app

from app import db
from app.models import UserEmailBinding, Email, EmailDetectionStatus

logger = logging.getLogger(__name__)


class EmailFetchService:
    """邮件获取服务类"""
    
    # 线程锁，用于数据库操作
    _db_lock = threading.Lock()
    
    @staticmethod
    def fetch_emails():
        """
        获取所有启用邮箱的新邮件
        """
        start_time = datetime.now()
        
        try:
            # 1. 查询所有启用的邮箱绑定
            active_bindings = UserEmailBinding.query.filter(
                UserEmailBinding.is_active == True,
                UserEmailBinding.is_deleted == False
            ).all()
            
            if not active_bindings:
                return {'success': True, 'message': '没有启用的邮箱绑定'}
            
            # 2. 顺序获取邮件（避免多线程应用上下文问题）
            total_emails = 0
            success_count = 0
            error_count = 0
            
            for binding in active_bindings:
                try:
                    result = EmailFetchService._fetch_binding_emails(binding)
                    if result['success']:
                        success_count += 1
                        total_emails += result.get('email_count', 0)
                    else:
                        error_count += 1
                except Exception as e:
                    error_count += 1
                    print(f"处理邮箱 {binding.email_address} 时发生异常: {str(e)}")
            
            # 3. 输出处理结果
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            result_message = f"邮件获取任务完成 - 成功: {success_count}, 失败: {error_count}, 总邮件数: {total_emails}, 耗时: {duration:.2f}秒"
            
            return {
                'success': True, 
                'message': result_message,
                'data': {
                    'success_count': success_count,
                    'error_count': error_count,
                    'total_emails': total_emails,
                    'duration': duration
                }
            }
            
        except Exception as e:
            error_message = f"邮件获取任务执行失败: {str(e)}"
            print(error_message)
            return {'success': False, 'message': error_message}
    
    @staticmethod
    def _fetch_binding_emails(binding: UserEmailBinding) -> Dict[str, Any]:
        """
        获取单个邮箱绑定的新邮件
        
        Args:
            binding: 邮箱绑定记录
            
        Returns:
            Dict: 包含成功状态、消息和邮件数量的字典
        """
        try:
            # 根据邮箱类型选择获取方法
            if 'qq.com' in binding.email_address.lower():
                return EmailFetchService._fetch_qq_emails(binding)
            elif '163.com' in binding.email_address.lower():
                return EmailFetchService._fetch_163_emails(binding)
            else:
                return {
                    'success': False,
                    'message': f'不支持的邮箱类型: {binding.email_address}',
                    'email_count': 0
                }
                
        except Exception as e:
            print(f"获取邮箱 {binding.email_address} 的邮件时发生异常: {str(e)}")
            return {
                'success': False,
                'message': f'获取邮件异常: {str(e)}',
                'email_count': 0
            }
    
    @staticmethod
    def _fetch_qq_emails(binding: UserEmailBinding) -> Dict[str, Any]:
        """
        获取QQ邮箱的新邮件
        """
        return EmailFetchService._fetch_emails_generic(
            binding=binding,
            imap_server='imap.qq.com',
            use_id_extension=False
        )
    
    @staticmethod
    def _fetch_163_emails(binding: UserEmailBinding) -> Dict[str, Any]:
        """
        获取163邮箱的新邮件
        """
        return EmailFetchService._fetch_emails_generic(
            binding=binding,
            imap_server='imap.163.com',
            use_id_extension=True
        )
    
    @staticmethod
    def _fetch_emails_generic(binding: UserEmailBinding, imap_server: str, use_id_extension: bool = False) -> Dict[str, Any]:
        """
        通用的邮件获取方法
        
        Args:
            binding: 邮箱绑定记录
            imap_server: IMAP服务器地址
            use_id_extension: 是否使用ID扩展（163邮箱需要）
            
        Returns:
            Dict: 包含成功状态、消息和邮件数量的字典
        """
        mail = None
        try:
            # 1. 连接邮箱
            mail = imaplib.IMAP4_SSL(imap_server)
            mail.login(binding.email_address, binding.auth_code)
            
            # 2. 163邮箱特殊处理 - 发送ID信息
            if use_id_extension:
                try:
                    mail.send(b'ID01 ID ("name" "python_client" "version" "1.0" "vendor" "python_imaplib")\r\n')
                    mail.readline()
                    try:
                        mail.readline()
                    except:
                        pass
                except:
                    pass
            
            mail.select('INBOX')
            
            # 3. 确定搜索起始UID
            last_uid = int(binding.last_uid) if binding.last_uid else 0
            search_criteria = f'UID {last_uid + 1}:*'
            
            # 4. 搜索新邮件
            status, messages = mail.uid('search', None, search_criteria)
            
            if status != 'OK' or not messages[0]:
                mail.logout()
                return {
                    'success': True,
                    'message': '没有新邮件',
                    'email_count': 0
                }
            
            # 5. 获取新邮件的UID列表
            all_uids = [int(uid.decode()) for uid in messages[0].split()]
            # 过滤掉已经处理过的UID
            new_uids = [uid for uid in all_uids if uid > last_uid]
            
            if not new_uids:
                mail.logout()
                return {
                    'success': True,
                    'message': '没有新邮件',
                    'email_count': 0
                }
            
            # 6. 获取每封邮件的详细信息
            emails_data = []
            max_uid = last_uid
            
            for uid in new_uids:
                try:
                    # 获取完整邮件信息
                    status, msg_data = mail.uid('fetch', str(uid), '(RFC822)')
                    
                    if status == 'OK' and msg_data[0]:
                        msg = email.message_from_bytes(msg_data[0][1])
                        
                        # 获取原始header信息
                        headers_str = str(msg)
                        
                        email_info = {
                            'uid': uid,
                            'subject': EmailFetchService._decode_subject(msg.get('subject')),
                            'from': msg.get('from', '(未知发件人)'),
                            'date': EmailFetchService._format_date(msg.get('date', '(无日期)')),
                            'to': msg.get('to', '(未知收件人)'),
                            'content': EmailFetchService._extract_content(msg),
                            'headers': headers_str
                        }
                        
                        emails_data.append(email_info)
                        max_uid = max(max_uid, uid)
                        
                except Exception as e:
                    print(f"处理UID {uid} 时出错: {str(e)}")
                    continue
            
            mail.logout()
            
            # 7. 保存邮件到数据库
            if emails_data:
                EmailFetchService._save_emails_to_db(binding, emails_data, max_uid)
            
            return {
                'success': True,
                'message': f'成功获取{len(emails_data)}封新邮件',
                'email_count': len(emails_data)
            }
            
        except Exception as e:
            if mail:
                try:
                    mail.logout()
                except:
                    pass
            raise e
    
    @staticmethod
    def _decode_subject(header):
        """解码邮件主题"""
        if not header:
            return '(无主题)'
        
        subject = ''
        try:
            for part, encoding in email.header.decode_header(header):
                if isinstance(part, bytes):
                    if encoding:
                        subject += part.decode(encoding)
                    else:
                        subject += part.decode('utf-8', errors='ignore')
                else:
                    subject += str(part)
        except:
            subject = str(header)
        
        return subject.strip()
    
    @staticmethod
    def _extract_content(msg):
        """提取邮件正文内容"""
        content = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                if "attachment" in str(part.get("Content-Disposition")):
                    continue
                if part.get_content_type() == "text/plain":
                    try:
                        body = part.get_payload(decode=True)
                        if body:
                            charset = part.get_content_charset() or 'utf-8'
                            content += body.decode(charset, errors='ignore')
                    except:
                        continue
        else:
            try:
                body = msg.get_payload(decode=True)
                if body:
                    charset = msg.get_content_charset() or 'utf-8'
                    content = body.decode(charset, errors='ignore')
            except:
                content = str(msg.get_payload())
        
        content = ' '.join(content.split())
        return content if content else '(无内容)'
    
    @staticmethod
    def _format_date(date_str):
        """格式化日期为标准格式"""
        if not date_str or date_str == '(无日期)':
            return None
        
        try:
            # 解析邮件日期
            email_dt = email.utils.parsedate_to_datetime(date_str)
            if email_dt:
                # 转换为本地时间
                if email_dt.tzinfo:
                    email_dt = email_dt.replace(tzinfo=None)
                return email_dt
        except:
            pass
        
        return None
    
    @staticmethod
    def _save_emails_to_db(binding: UserEmailBinding, emails_data: List[Dict], max_uid: int):
        """
        保存邮件到数据库
        
        Args:
            binding: 邮箱绑定记录
            emails_data: 邮件数据列表
            max_uid: 最大UID
        """
        
        with EmailFetchService._db_lock:
            try:
                new_emails_count = 0
                
                # 开始数据库事务
                for email_info in emails_data:
                    # 检查邮件是否已存在
                    existing_email = Email.find_by_uid(binding.id, str(email_info['uid']))
                    if existing_email:
                        continue
                    
                    # 创建新邮件记录
                    new_email = Email(
                        binding_id=binding.id,
                        provider_id=binding.provider_id,
                        user_id=binding.user_id,
                        provider_display_name=binding.provider_display_name,
                        email_address=binding.email_address,
                        email_uid=str(email_info['uid']),
                        subject=email_info['subject'],
                        sender=email_info['from'],
                        email_date=email_info['date'],
                        content=email_info['content'],
                        headers=email_info['headers'],
                        detection_status=EmailDetectionStatus.PENDING.value
                    )
                    
                    db.session.add(new_email)
                    new_emails_count += 1
                
                # 更新绑定记录的last_uid
                binding.last_uid = str(max_uid)
                
                # 提交事务
                db.session.commit()
                
                # 新邮件处理完成
                if new_emails_count > 0:
                    print(f"成功获取 {new_emails_count} 封新邮件")
                
            except Exception as e:
                db.session.rollback()
                print(f"保存邮件到数据库时发生错误: {str(e)}")
                raise e