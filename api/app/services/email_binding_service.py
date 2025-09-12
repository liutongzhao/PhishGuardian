import imaplib
import smtplib
import ssl
import socket
from typing import Dict, Tuple, Optional
from app.models import EmailProvider, UserEmailBinding
from app import db
import logging

logger = logging.getLogger(__name__)


class EmailBindingService:
    """邮箱绑定服务类"""
    
    @staticmethod
    def validate_email_format(email: str, provider: EmailProvider) -> bool:
        """验证邮箱格式是否匹配厂商"""
        if not email or not provider.email_suffix:
            return False
        
        return email.lower().endswith(provider.email_suffix.lower())
    
    @staticmethod
    def test_imap_connection(email: str, auth_code: str, provider: EmailProvider) -> Tuple[bool, str]:
        """测试IMAP连接"""
        try:
            # 设置socket超时时间为5秒
            original_timeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(5.0)
            
            # 创建IMAP连接
            if provider.imap_ssl:
                # 使用SSL连接
                imap = imaplib.IMAP4_SSL(provider.imap_server, provider.imap_port)
            else:
                # 使用普通连接
                imap = imaplib.IMAP4(provider.imap_server, provider.imap_port)
                if provider.imap_port == 143:  # 如果是143端口，尝试STARTTLS
                    imap.starttls()
            
            # 尝试登录
            result = imap.login(email, auth_code)
            
            # 登录成功，关闭连接
            imap.logout()
            
            # 恢复原始超时设置
            socket.setdefaulttimeout(original_timeout)
            
            return True, "IMAP连接成功"
            
        except socket.timeout:
            socket.setdefaulttimeout(original_timeout)
            return False, "IMAP连接超时，请检查网络或服务器设置"
        except imaplib.IMAP4.error as e:
            socket.setdefaulttimeout(original_timeout)
            return False, f"IMAP认证失败: {str(e)}"
        except Exception as e:
            socket.setdefaulttimeout(original_timeout)
            return False, f"IMAP连接错误: {str(e)}"
    
    @staticmethod
    def test_smtp_connection(email: str, auth_code: str, provider: EmailProvider) -> Tuple[bool, str]:
        """测试SMTP连接"""
        try:
            # 设置socket超时时间为5秒
            original_timeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(5.0)
            
            # 根据smtp_ssl字段和端口选择连接方式
            if hasattr(provider, 'smtp_ssl') and provider.smtp_ssl:
                # 使用SSL连接（明确配置为SSL）
                context = ssl.create_default_context()
                smtp = smtplib.SMTP_SSL(provider.smtp_server, provider.smtp_port, timeout=5, context=context)
            elif provider.smtp_port == 465:
                # 端口465默认使用SSL
                context = ssl.create_default_context()
                smtp = smtplib.SMTP_SSL(provider.smtp_server, provider.smtp_port, timeout=5, context=context)
            else:
                # 使用普通连接然后STARTTLS（端口587等）
                smtp = smtplib.SMTP(provider.smtp_server, provider.smtp_port, timeout=5)
                # 启用TLS加密
                if provider.smtp_tls:
                    smtp.starttls()
            
            # 尝试登录
            smtp.login(email, auth_code)
            
            # 登录成功，关闭连接
            smtp.quit()
            
            # 恢复原始超时设置
            socket.setdefaulttimeout(original_timeout)
            
            return True, "SMTP连接成功"
            
        except socket.timeout:
            socket.setdefaulttimeout(original_timeout)
            return False, "SMTP连接超时，请检查网络或服务器设置"
        except smtplib.SMTPAuthenticationError as e:
            socket.setdefaulttimeout(original_timeout)
            return False, f"SMTP认证失败: {str(e)}"
        except Exception as e:
            socket.setdefaulttimeout(original_timeout)
            return False, f"SMTP连接错误: {str(e)}"
    
    @staticmethod
    def validate_email_binding(email: str, auth_code: str, provider: EmailProvider) -> Dict:
        """验证邮箱绑定"""
        result = {
            'success': False,
            'message': '',
            'details': {
                'email_format_valid': False,
                'imap_success': False,
                'smtp_success': False,
                'imap_message': '',
                'smtp_message': ''
            }
        }
        
        # 1. 验证邮箱格式
        if not EmailBindingService.validate_email_format(email, provider):
            result['message'] = f'邮箱格式不匹配，应该以 {provider.email_suffix} 结尾'
            return result
        
        result['details']['email_format_valid'] = True
        
        # 2. 测试IMAP连接
        imap_success, imap_message = EmailBindingService.test_imap_connection(email, auth_code, provider)
        # IMAP连接测试完成
        result['details']['imap_success'] = imap_success
        result['details']['imap_message'] = imap_message
        
        # 3. 测试SMTP连接
        smtp_success, smtp_message = EmailBindingService.test_smtp_connection(email, auth_code, provider)
        result['details']['smtp_success'] = smtp_success
        result['details']['smtp_message'] = smtp_message
        
        # 4. 判断整体结果
        if imap_success and smtp_success:
            result['success'] = True
            result['message'] = '邮箱验证成功，IMAP和SMTP连接均正常'
            
            # 5. 获取最新邮件UID
            latest_uid = EmailBindingService.get_latest_email_uid(email, auth_code, provider)
            if latest_uid is not None:
                result['details']['uid_success'] = True
                result['details']['uid_message'] = '获取UID成功'
                result['details']['latest_uid'] = str(latest_uid)
            else:
                result['details']['uid_success'] = False
                result['details']['uid_message'] = '获取UID失败'
                result['details']['latest_uid'] = None
                # 获取UID失败
        else:
            failed_services = []
            if not imap_success:
                failed_services.append('IMAP')
            if not smtp_success:
                failed_services.append('SMTP')
            
            result['message'] = f'邮箱验证失败，{"、".join(failed_services)}连接失败'
        
        return result
    
    @staticmethod
    def create_email_binding(user_id: int, provider_id: int, email: str, auth_code: str, last_uid: Optional[str] = None) -> Tuple[bool, str, UserEmailBinding]:
        """创建邮箱绑定记录"""
        try:
            # 获取邮箱厂商信息
            provider = EmailProvider.query.filter(
                EmailProvider.id == provider_id,
                EmailProvider.is_deleted == False,
                EmailProvider.is_active == True
            ).first()
            
            if not provider:
                return False, '邮箱厂商不存在或已禁用', None
            
            # 检查是否已经绑定过该邮箱
            existing_binding = UserEmailBinding.find_by_email(email)
            if existing_binding:
                return False, '该邮箱已被绑定', None
            
            # 检查用户是否已经绑定过该厂商
            existing_provider_binding = UserEmailBinding.find_user_provider_binding(user_id, provider_id)
            if existing_provider_binding:
                return False, f'您已经绑定过{provider.display_name}邮箱', None
            
            # 创建绑定记录
            binding = UserEmailBinding(
                user_id=user_id,
                provider_id=provider_id,
                provider_display_name=provider.display_name,
                email_address=email,
                auth_code=auth_code,
                imap_server=provider.imap_server,
                smtp_server=provider.smtp_server,
                last_uid=last_uid,
                is_active=True
            )
            
            db.session.add(binding)
            db.session.commit()
            
            return True, '邮箱绑定成功', binding
            
        except Exception as e:
            db.session.rollback()
            return False, f'绑定失败: {str(e)}', None
    
    @staticmethod
    def get_user_bindings(user_id: int) -> list:
        """获取用户的邮箱绑定列表"""
        return UserEmailBinding.get_user_bindings(user_id)
    
    @staticmethod
    def delete_email_binding(user_id: int, binding_id: int) -> Tuple[bool, str]:
        """删除邮箱绑定"""
        try:
            binding = UserEmailBinding.query.filter(
                UserEmailBinding.id == binding_id,
                UserEmailBinding.user_id == user_id,
                UserEmailBinding.is_deleted == False
            ).first()
            
            if not binding:
                return False, '绑定记录不存在'
            
            binding.soft_delete()
            db.session.commit()
            
            return True, '邮箱绑定删除成功'
            
        except Exception as e:
            db.session.rollback()
            return False, f'删除失败: {str(e)}'
    
    @staticmethod
    def get_latest_email_uid(email: str, auth_code: str, provider: EmailProvider) -> Optional[int]:
        """根据邮箱厂商获取最新邮件的UID"""
        # 根据邮箱厂商选择不同的获取策略
        if 'qq.com' in email.lower():
            return EmailBindingService._get_qq_email_uid(email, auth_code, provider)
        elif '163.com' in email.lower():
            return EmailBindingService._get_163_email_uid(email, auth_code, provider)
        elif 'gmail.com' in email.lower():
            return EmailBindingService._get_gmail_uid(email, auth_code, provider)
        else:
            # 默认使用通用方法
            return EmailBindingService._get_generic_email_uid(email, auth_code, provider)
    
    @staticmethod
    def _get_qq_email_uid(email: str, auth_code: str, provider: EmailProvider) -> Optional[int]:
        """获取QQ邮箱最新邮件的UID - QQ邮箱专用方法"""
        try:
            # 连接到IMAP服务器
            imap = imaplib.IMAP4_SSL(provider.imap_server, provider.imap_port)
            imap.login(email, auth_code)
            
            # 选择收件箱
            imap.select('INBOX')
            
            # QQ邮箱使用UID SEARCH命令直接获取UID
            status, uid_data = imap.uid('search', None, 'ALL')
            if status == 'OK' and uid_data[0]:
                # 解析UID列表
                uid_list = uid_data[0].decode().split()
                if uid_list:
                    latest_uid = int(uid_list[-1])  # 最后一个UID是最新的
                    print(f"QQ邮箱获取到最新UID: {latest_uid}")
                    imap.logout()
                    return latest_uid
            
            print("QQ邮箱收件箱中没有邮件")
            imap.logout()
            return 0
                
        except Exception as e:
            print(f"获取QQ邮箱最新邮件UID时发生错误: {e}")
            return None
    
    @staticmethod
    def _get_163_email_uid(email: str, auth_code: str, provider: EmailProvider) -> Optional[int]:
        """获取163邮箱最新邮件的UID - 163邮箱专用方法"""
        try:
            # 连接IMAP服务器
            mail = imaplib.IMAP4_SSL(provider.imap_server, provider.imap_port)
            
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
            
            # 登录邮箱
            mail.login(email, auth_code)
            
            # 选择收件箱
            select_status, select_data = mail.select('INBOX')
            if select_status != 'OK':
                print(f"163邮箱选择收件箱失败: {select_data}")
                mail.logout()
                return None
            
            # 搜索所有邮件的UID
            status, uid_data = mail.uid('search', None, 'ALL')
            
            if status != 'OK' or not uid_data[0]:
                print(f"163邮箱搜索邮件失败: {status}, {uid_data}")
                mail.logout()
                return None
            
            # 获取UID列表
            uid_list = uid_data[0].decode().split()
            
            if not uid_list:
                print("163邮箱中没有邮件")
                mail.logout()
                return None
            
            # 获取最新的UID（列表中的最后一个）
            latest_uid = int(uid_list[-1])
            print(f"163邮箱成功获取最新UID: {latest_uid}")
            
            # 关闭连接
            mail.logout()
            
            return latest_uid
                
        except Exception as e:
            print(f"获取163邮箱最新邮件UID时发生错误: {e}")
            return None
    
    @staticmethod
    def _get_gmail_uid(email: str, auth_code: str, provider: EmailProvider) -> Optional[int]:
        """获取Gmail最新邮件的UID - Gmail专用方法"""
        try:
            # 连接到IMAP服务器
            imap = imaplib.IMAP4_SSL(provider.imap_server, provider.imap_port)
            imap.login(email, auth_code)
            
            # 选择收件箱
            imap.select('INBOX')
            
            # Gmail使用UID SEARCH命令
            status, uid_data = imap.uid('search', None, 'ALL')
            if status == 'OK' and uid_data[0]:
                uid_list = uid_data[0].decode().split()
                if uid_list:
                    latest_uid = int(uid_list[-1])
                    print(f"Gmail获取到最新UID: {latest_uid}")
                    imap.logout()
                    return latest_uid
            
            print("Gmail收件箱中没有邮件")
            imap.logout()
            return 0
                
        except Exception as e:
            print(f"获取Gmail最新邮件UID时发生错误: {e}")
            return None
    
    @staticmethod
    def _get_generic_email_uid(email: str, auth_code: str, provider: EmailProvider) -> Optional[int]:
        """通用邮箱UID获取方法 - 作为备用方案"""
        try:
            # 连接到IMAP服务器
            imap = imaplib.IMAP4_SSL(provider.imap_server, provider.imap_port)
            imap.login(email, auth_code)
            
            # 选择收件箱
            imap.select('INBOX')
            
            # 先尝试UID SEARCH方法
            try:
                status, uid_data = imap.uid('search', None, 'ALL')
                if status == 'OK' and uid_data[0]:
                    uid_list = uid_data[0].decode().split()
                    if uid_list:
                        latest_uid = int(uid_list[-1])
                        print(f"通用方法(UID SEARCH)获取到最新UID: {latest_uid}")
                        imap.logout()
                        return latest_uid
            except Exception:
                print("UID SEARCH方法失败，尝试传统方法")
            
            # 备用方法：传统的SEARCH + FETCH
            status, messages = imap.search(None, 'ALL')
            if status != 'OK' or not messages[0]:
                print("通用方法收件箱中没有邮件")
                imap.logout()
                return 0
            
            message_ids = messages[0].split()
            latest_msg_id = message_ids[-1]
            
            # 尝试不同的FETCH方法
            for fetch_cmd in ['UID', '(UID)']:
                try:
                    status, uid_data = imap.uid('fetch', latest_msg_id, fetch_cmd)
                    if status == 'OK' and uid_data[0]:
                        import re
                        uid_response = uid_data[0].decode('utf-8')
                        uid_match = re.search(r'UID (\d+)', uid_response)
                        if uid_match:
                            latest_uid = int(uid_match.group(1))
                            print(f"通用方法(FETCH {fetch_cmd})获取到最新UID: {latest_uid}")
                            imap.logout()
                            return latest_uid
                except Exception:
                    continue
            
            imap.logout()
            return None
                
        except Exception as e:
            print(f"通用方法获取最新邮件UID时发生错误: {e}")
            return None
                
        except socket.timeout:
            socket.setdefaulttimeout(original_timeout)
            return False, 'IMAP连接超时', None
        except imaplib.IMAP4.error as e:
            socket.setdefaulttimeout(original_timeout)
            return False, f'IMAP错误: {str(e)}', None
        except Exception as e:
            socket.setdefaulttimeout(original_timeout)
            return False, f'获取UID失败: {str(e)}', None