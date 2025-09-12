#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
163邮箱增量获取工具

根据上次记录的UID获取新增邮件

使用方法：
    from email_163_simple import get_new_emails
    
    result = get_new_emails(
        email_addr='your_email@163.com',
        password='your_password', 
        last_uid=12345
    )
"""

import imaplib
import email
import json
from datetime import datetime
import email.utils

def get_new_emails(email_addr, password, last_uid):
    """
    获取从指定UID之后的新邮件
    
    参数:
        email_addr (str): 163邮箱地址
        password (str): 163邮箱授权码
        last_uid (int): 上次记录的最大UID
    
    返回:
        dict: {
            "success": bool,
            "message": str,
            "data": list  # 新邮件列表
        }
    """
    
    def decode_subject(header):
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
    
    def extract_content(msg):
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
    
    def format_date(date_str):
        """格式化日期为标准格式"""
        if not date_str or date_str == '(无日期)':
            return '(无日期)'
        
        try:
            # 解析邮件日期
            email_dt = email.utils.parsedate_to_datetime(date_str)
            if email_dt:
                # 转换为本地时间并格式化
                if email_dt.tzinfo:
                    email_dt = email_dt.replace(tzinfo=None)
                return email_dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            pass
        
        return date_str
    
    try:
        # 连接163邮箱
        mail = imaplib.IMAP4_SSL('imap.163.com')
        mail.login(email_addr, password)
        
        # 163邮箱特殊处理 - 发送ID信息
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
        
        # 搜索UID大于last_uid的邮件
        search_criteria = f'UID {last_uid + 1}:*'
        status, messages = mail.uid('search', None, search_criteria)
        
        if status != 'OK' or not messages[0]:
            mail.logout()
            return {
                "success": True,
                "message": "没有新邮件",
                "data": []
            }
        
        # 获取新邮件的UID列表
        new_uids = [int(uid.decode()) for uid in messages[0].split()]
        
        if not new_uids:
            mail.logout()
            return {
                "success": True,
                "message": "没有新邮件",
                "data": []
            }
        
        # 获取每封邮件的详细信息
        emails_data = []
        
        for uid in new_uids:
            try:
                # 获取完整邮件信息
                status, msg_data = mail.uid('fetch', str(uid), '(RFC822)')
                
                if status == 'OK' and msg_data[0]:
                    msg = email.message_from_bytes(msg_data[0][1])
                    
                    email_info = {
                        'uid': uid,
                        'subject': decode_subject(msg.get('subject')),
                        'from': msg.get('from', '(未知发件人)'),
                        'date': format_date(msg.get('date', '(无日期)')),
                        'to': msg.get('to', '(未知收件人)'),
                        'content': extract_content(msg)
                    }
                    
                    emails_data.append(email_info)
                    
            except Exception as e:
                print(f"处理UID {uid} 时出错: {str(e)}")
                continue
        
        mail.logout()
        
        return {
            "success": True,
            "message": f"成功获取{len(emails_data)}封新邮件",
            "data": emails_data
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"获取邮件失败: {str(e)}",
            "data": []
        }

def main():
    """
    测试函数
    """
    # 测试配置（请修改为实际的邮箱信息）
    email_addr = '15209828080@163.com'
    password = 'YVuiB4Ty4QHzenTJ'
    last_uid = 1709006618  # 从UID 1开始获取所有邮件（用于测试）
    
    print(f"正在获取UID {last_uid + 1} 之后的新邮件...")
    result = get_new_emails(email_addr, password, last_uid)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if result['success'] and result['data']:
        print(f"\n最新的UID: {result['data'][-1]['uid']}")

if __name__ == '__main__':
    main()