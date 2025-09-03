import re
from typing import Dict, Any


def validate_email(email: str) -> bool:
    """验证邮箱格式
    
    Args:
        email: 邮箱地址
        
    Returns:
        bool: 是否为有效邮箱格式
    """
    if not email or not isinstance(email, str):
        return False
    
    # 基本邮箱格式验证
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False
    
    # 长度检查
    if len(email) > 254:  # RFC 5321 限制
        return False
    
    # 本地部分和域名部分长度检查
    local, domain = email.rsplit('@', 1)
    if len(local) > 64 or len(domain) > 253:
        return False
    
    return True


def validate_password(password: str) -> Dict[str, Any]:
    """验证密码强度
    
    Args:
        password: 密码
        
    Returns:
        Dict: 包含验证结果和消息的字典
    """
    if not password or not isinstance(password, str):
        return {
            'valid': False,
            'message': 'Password is required',
            'score': 0
        }
    
    errors = []
    score = 0
    
    # 长度检查
    if len(password) < 8:
        errors.append('Password must be at least 8 characters long')
    elif len(password) >= 8:
        score += 1
        if len(password) >= 12:
            score += 1
    
    # 包含小写字母
    if re.search(r'[a-z]', password):
        score += 1
    else:
        errors.append('Password must contain at least one lowercase letter')
    
    # 包含大写字母
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        errors.append('Password must contain at least one uppercase letter')
    
    # 包含数字
    if re.search(r'\d', password):
        score += 1
    else:
        errors.append('Password must contain at least one digit')
    
    # 包含特殊字符
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        errors.append('Password must contain at least one special character')
    
    # 检查常见弱密码
    weak_passwords = [
        'password', '123456', '123456789', 'qwerty', 'abc123',
        'password123', 'admin', 'letmein', 'welcome', '123123'
    ]
    
    if password.lower() in weak_passwords:
        errors.append('Password is too common')
        score = max(0, score - 2)
    
    # 检查重复字符
    if len(set(password)) < len(password) * 0.6:
        errors.append('Password contains too many repeated characters')
        score = max(0, score - 1)
    
    is_valid = len(errors) == 0 and score >= 4
    
    return {
        'valid': is_valid,
        'message': '; '.join(errors) if errors else 'Password is valid',
        'score': score,
        'strength': get_password_strength(score)
    }


def get_password_strength(score: int) -> str:
    """根据评分获取密码强度描述
    
    Args:
        score: 密码评分
        
    Returns:
        str: 强度描述
    """
    if score <= 2:
        return 'Weak'
    elif score <= 4:
        return 'Medium'
    elif score <= 5:
        return 'Strong'
    else:
        return 'Very Strong'


def validate_username(username: str) -> Dict[str, Any]:
    """验证用户名
    
    Args:
        username: 用户名
        
    Returns:
        Dict: 包含验证结果和消息的字典
    """
    if not username or not isinstance(username, str):
        return {
            'valid': False,
            'message': 'Username is required'
        }
    
    username = username.strip()
    
    # 长度检查
    if len(username) < 3:
        return {
            'valid': False,
            'message': 'Username must be at least 3 characters long'
        }
    
    if len(username) > 50:
        return {
            'valid': False,
            'message': 'Username must be no more than 50 characters long'
        }
    
    # 字符检查
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return {
            'valid': False,
            'message': 'Username can only contain letters, numbers and underscores'
        }
    
    # 不能以数字开头
    if username[0].isdigit():
        return {
            'valid': False,
            'message': 'Username cannot start with a number'
        }
    
    # 不能全是数字
    if username.isdigit():
        return {
            'valid': False,
            'message': 'Username cannot be all numbers'
        }
    
    # 检查保留用户名
    reserved_usernames = [
        'admin', 'administrator', 'root', 'system', 'user',
        'test', 'guest', 'anonymous', 'null', 'undefined',
        'api', 'www', 'mail', 'ftp', 'support'
    ]
    
    if username.lower() in reserved_usernames:
        return {
            'valid': False,
            'message': 'Username is reserved'
        }
    
    return {
        'valid': True,
        'message': 'Username is valid'
    }


def validate_phone(phone: str) -> Dict[str, Any]:
    """验证手机号码
    
    Args:
        phone: 手机号码
        
    Returns:
        Dict: 包含验证结果和消息的字典
    """
    if not phone:
        return {
            'valid': True,  # 手机号码是可选的
            'message': 'Phone number is optional'
        }
    
    if not isinstance(phone, str):
        return {
            'valid': False,
            'message': 'Phone number must be a string'
        }
    
    phone = phone.strip().replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    
    # 基本格式检查
    if not re.match(r'^\+?[1-9]\d{1,14}$', phone):
        return {
            'valid': False,
            'message': 'Invalid phone number format'
        }
    
    # 长度检查
    if len(phone) < 7 or len(phone) > 15:
        return {
            'valid': False,
            'message': 'Phone number must be between 7 and 15 digits'
        }
    
    return {
        'valid': True,
        'message': 'Phone number is valid'
    }


def validate_url(url: str) -> bool:
    """验证URL格式
    
    Args:
        url: URL地址
        
    Returns:
        bool: 是否为有效URL格式
    """
    if not url or not isinstance(url, str):
        return False
    
    # 基本URL格式验证
    pattern = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$'
    
    return bool(re.match(pattern, url))


def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """验证文件扩展名
    
    Args:
        filename: 文件名
        allowed_extensions: 允许的扩展名列表
        
    Returns:
        bool: 是否为允许的文件类型
    """
    if not filename or not isinstance(filename, str):
        return False
    
    if not allowed_extensions:
        return True
    
    # 获取文件扩展名
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    
    return ext in [ext.lower() for ext in allowed_extensions]


def validate_file_size(file_size: int, max_size: int) -> bool:
    """验证文件大小
    
    Args:
        file_size: 文件大小（字节）
        max_size: 最大允许大小（字节）
        
    Returns:
        bool: 是否在允许的大小范围内
    """
    if not isinstance(file_size, int) or file_size < 0:
        return False
    
    if not isinstance(max_size, int) or max_size <= 0:
        return False
    
    return file_size <= max_size


def sanitize_input(text: str, max_length: int = None) -> str:
    """清理用户输入
    
    Args:
        text: 输入文本
        max_length: 最大长度限制
        
    Returns:
        str: 清理后的文本
    """
    if not text or not isinstance(text, str):
        return ''
    
    # 去除首尾空格
    text = text.strip()
    
    # 移除控制字符
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
    
    # 长度限制
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text