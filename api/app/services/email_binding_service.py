import imaplib
import smtplib
import ssl
import socket
from typing import Dict, Tuple
from app.models import EmailProvider, UserEmailBinding
from app import db


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
            print(f"开始测试SMTP连接: {provider.smtp_server}:{provider.smtp_port}")
            # 设置socket超时时间为5秒
            original_timeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(5.0)
            
            # 根据smtp_ssl字段和端口选择连接方式
            if hasattr(provider, 'smtp_ssl') and provider.smtp_ssl:
                # 使用SSL连接（明确配置为SSL）
                print(f"使用SSL连接SMTP服务器...")
                context = ssl.create_default_context()
                smtp = smtplib.SMTP_SSL(provider.smtp_server, provider.smtp_port, timeout=5, context=context)
                print(f"SMTP SSL连接建立成功")
            elif provider.smtp_port == 465:
                # 端口465默认使用SSL
                print(f"使用SSL连接SMTP服务器（端口465）...")
                context = ssl.create_default_context()
                smtp = smtplib.SMTP_SSL(provider.smtp_server, provider.smtp_port, timeout=5, context=context)
                print(f"SMTP SSL连接建立成功")
            else:
                # 使用普通连接然后STARTTLS（端口587等）
                print(f"正在连接SMTP服务器...")
                smtp = smtplib.SMTP(provider.smtp_server, provider.smtp_port, timeout=5)
                print(f"SMTP连接建立成功")
                
                # 启用TLS加密
                if provider.smtp_tls:
                    print(f"启用TLS加密...")
                    smtp.starttls()
                    print(f"TLS加密成功")
            
            # 尝试登录
            print(f"尝试SMTP登录...")
            smtp.login(email, auth_code)
            print(f"SMTP登录成功")
            
            # 登录成功，关闭连接
            smtp.quit()
            
            # 恢复原始超时设置
            socket.setdefaulttimeout(original_timeout)
            
            return True, "SMTP连接成功"
            
        except socket.timeout:
            print(f"SMTP连接超时")
            socket.setdefaulttimeout(original_timeout)
            return False, "SMTP连接超时，请检查网络或服务器设置"
        except smtplib.SMTPAuthenticationError as e:
            print(f"SMTP认证失败: {str(e)}")
            socket.setdefaulttimeout(original_timeout)
            return False, f"SMTP认证失败: {str(e)}"
        except Exception as e:
            print(f"SMTP连接错误: {str(e)}")
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
        print(imap_message,imap_success)
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
        else:
            failed_services = []
            if not imap_success:
                failed_services.append('IMAP')
            if not smtp_success:
                failed_services.append('SMTP')
            
            result['message'] = f'邮箱验证失败，{"、".join(failed_services)}连接失败'
        
        return result
    
    @staticmethod
    def create_email_binding(user_id: int, provider_id: int, email: str, auth_code: str) -> Tuple[bool, str, UserEmailBinding]:
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