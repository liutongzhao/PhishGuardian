from datetime import datetime
import pytz
from app import db


class UserEmailBinding(db.Model):
    """用户邮箱绑定模型"""
    __tablename__ = 'user_email_bindings'
    
    # 基础字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='绑定记录唯一标识')
    user_id = db.Column(db.Integer, nullable=False, index=True, comment='用户ID')
    provider_id = db.Column(db.Integer, nullable=False, index=True, comment='邮箱厂商ID')
    
    # 邮箱信息
    provider_display_name = db.Column(db.String(100), nullable=False, comment='邮箱厂商显示名称')
    email_address = db.Column(db.String(255), nullable=False, index=True, comment='邮箱地址')
    auth_code = db.Column(db.String(500), nullable=False, comment='授权码')
    
    # 服务器配置（冗余存储，避免厂商配置变更影响已绑定邮箱）
    imap_server = db.Column(db.String(255), nullable=False, comment='IMAP服务器地址')
    smtp_server = db.Column(db.String(255), nullable=False, comment='SMTP服务器地址')
    
    # 状态字段
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True, comment='是否启用')
    is_deleted = db.Column(db.Boolean, default=False, nullable=False, index=True, comment='是否删除')
    
    # 保留字段
    reserved_field1 = db.Column(db.String(255), comment='保留字段1')
    reserved_field2 = db.Column(db.String(255), comment='保留字段2')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')), nullable=False, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')), onupdate=lambda: datetime.now(pytz.timezone('Asia/Shanghai')), nullable=False, comment='更新时间')
    
    def __repr__(self):
        return f'<UserEmailBinding {self.email_address}>'
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'provider_id': self.provider_id,
            'provider_display_name': self.provider_display_name,
            'email_address': self.email_address,
            'auth_code': self.auth_code,
            'imap_server': self.imap_server,
            'smtp_server': self.smtp_server,
            'is_active': self.is_active,
            'reserved_field1': self.reserved_field1,
            'reserved_field2': self.reserved_field2,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def soft_delete(self):
        """软删除"""
        self.is_deleted = True
        self.is_active = False
        self.updated_at = datetime.now(pytz.timezone('Asia/Shanghai'))
    
    @classmethod
    def get_user_bindings(cls, user_id, active_only=True):
        """获取用户的邮箱绑定列表"""
        query = cls.query.filter(
            cls.user_id == user_id,
            cls.is_deleted == False
        )
        
        if active_only:
            query = query.filter(cls.is_active == True)
        
        return query.order_by(cls.created_at.desc()).all()
    
    @classmethod
    def find_by_email(cls, email_address, active_only=True):
        """根据邮箱地址查找绑定记录"""
        query = cls.query.filter(
            cls.email_address == email_address,
            cls.is_deleted == False
        )
        
        if active_only:
            query = query.filter(cls.is_active == True)
        
        return query.first()
    
    @classmethod
    def find_user_provider_binding(cls, user_id, provider_id, active_only=True):
        """查找用户在指定厂商的绑定记录"""
        query = cls.query.filter(
            cls.user_id == user_id,
            cls.provider_id == provider_id,
            cls.is_deleted == False
        )
        
        if active_only:
            query = query.filter(cls.is_active == True)
        
        return query.first()