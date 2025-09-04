from datetime import datetime
import pytz
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import secrets
import string

class RegistrationType(Enum):
    EMAIL = 'email'
    GITHUB = 'github'
    WECHAT = 'wechat'

class User(db.Model):
    __tablename__ = 'users'
    
    # 基础字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户唯一标识')
    username = db.Column(db.String(80), unique=True, nullable=False, index=True, comment='用户名，唯一且非空')
    email = db.Column(db.String(120), unique=True, nullable=True, index=True, comment='邮箱地址，唯一但可为空')
    github = db.Column(db.String(100), unique=True, nullable=True, index=True, comment='GitHub用户名，唯一但可为空')
    wechat = db.Column(db.String(100), unique=True, nullable=True, index=True, comment='微信号，唯一但可为空')
    
    # 注册方式
    registration_method = db.Column(db.Enum(RegistrationType), nullable=False, default=RegistrationType.EMAIL, comment='注册方式')
    
    # 密码
    password = db.Column(db.String(255), nullable=True, comment='密码哈希值')
    
    # 验证码
    verification_code = db.Column(db.String(10), nullable=True, comment='验证码')
    verification_code_expires = db.Column(db.DateTime, nullable=True, comment='验证码过期时间')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')), nullable=False, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')), onupdate=lambda: datetime.now(pytz.timezone('Asia/Shanghai')), nullable=False, comment='更新时间')
    last_login = db.Column(db.DateTime, nullable=True, comment='最后登录时间')
    
    # 软删除
    is_deleted = db.Column(db.Boolean, default=False, nullable=False, index=True, comment='是否已删除（软删除）')
    
    # 激活状态
    is_activated = db.Column(db.Boolean, default=False, nullable=False, index=True, comment='是否已激活')
    
    # 保留字段
    reserved_field_1 = db.Column(db.String(255), nullable=True, comment='保留字段1')
    reserved_field_2 = db.Column(db.String(255), nullable=True, comment='保留字段2')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """设置密码"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        if not self.password:
            return False
        return check_password_hash(self.password, password)
    
    def generate_verification_code(self):
        """生成验证码"""
        code = ''.join(secrets.choice(string.digits) for _ in range(6))
        self.verification_code = code
        from datetime import timedelta
        self.verification_code_expires = datetime.utcnow() + timedelta(minutes=10)
        return code
    
    def is_verification_code_valid(self, code):
        """验证验证码是否有效"""
        if not self.verification_code or not self.verification_code_expires:
            return False
        if datetime.utcnow() > self.verification_code_expires:
            return False
        return self.verification_code == code
    
    def soft_delete(self):
        """软删除用户"""
        self.is_deleted = True
    
    def restore(self):
        """恢复已删除的用户"""
        self.is_deleted = False
    
    def activate(self):
        """激活用户"""
        self.is_activated = True
    
    def deactivate(self):
        """停用用户"""
        self.is_activated = False
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'github': self.github,
            'wechat': self.wechat,
            'registration_method': self.registration_method.value,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_deleted': self.is_deleted,
            'is_activated': self.is_activated,
        }
    
    @classmethod
    def find_by_username_or_email(cls, identifier):
        """通过用户名或邮箱查找用户"""
        return cls.query.filter(
            db.or_(
                cls.username == identifier,
                cls.email == identifier
            )
        ).filter(cls.is_deleted == False).first()
    
    @classmethod
    def find_active_users(cls):
        """查找所有活跃用户"""
        return cls.query.filter(
            cls.is_deleted == False
        ).all()