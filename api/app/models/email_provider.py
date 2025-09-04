from datetime import datetime
import pytz
from app import db


class EmailProvider(db.Model):
    """邮箱厂商模型"""
    __tablename__ = 'email_providers'
    
    # 基础字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='厂商唯一标识')
    name = db.Column(db.String(100), unique=True, nullable=False, index=True, comment='厂商名称')
    display_name = db.Column(db.String(100), nullable=False, comment='显示名称')
    
    # 邮箱配置
    email_suffix = db.Column(db.String(100), nullable=False, comment='邮箱后缀，如@gmail.com')
    
    # 服务器配置
    imap_server = db.Column(db.String(255), nullable=False, comment='IMAP服务器地址')
    imap_port = db.Column(db.Integer, nullable=False, default=993, comment='IMAP端口')
    imap_ssl = db.Column(db.Boolean, nullable=False, default=True, comment='是否使用SSL')
    
    smtp_server = db.Column(db.String(255), nullable=False, comment='SMTP服务器地址')
    smtp_port = db.Column(db.Integer, nullable=False, default=587, comment='SMTP端口')
    smtp_tls = db.Column(db.Boolean, nullable=False, default=True, comment='是否使用TLS')
    smtp_ssl = db.Column(db.Boolean, nullable=False, default=False, comment='是否使用SSL')
    
    # 状态字段
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True, comment='是否启用')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')), nullable=False, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')), onupdate=lambda: datetime.now(pytz.timezone('Asia/Shanghai')), nullable=False, comment='更新时间')
    
    # 软删除
    is_deleted = db.Column(db.Boolean, default=False, nullable=False, index=True, comment='是否已删除（软删除）')
    
    # 保留字段
    reserved_field_1 = db.Column(db.String(255), nullable=True, comment='保留字段1')
    reserved_field_2 = db.Column(db.String(255), nullable=True, comment='保留字段2')
    
    def __repr__(self):
        return f'<EmailProvider {self.name}>'
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'email_suffix': self.email_suffix,
            'imap_server': self.imap_server,
            'imap_port': self.imap_port,
            'imap_ssl': self.imap_ssl,
            'smtp_server': self.smtp_server,
            'smtp_port': self.smtp_port,
            'smtp_tls': self.smtp_tls,
            'smtp_ssl': self.smtp_ssl,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def soft_delete(self):
        """软删除厂商"""
        self.is_deleted = True
    
    def restore(self):
        """恢复已删除的厂商"""
        self.is_deleted = False
    
    def activate(self):
        """启用厂商"""
        self.is_active = True
    
    def deactivate(self):
        """停用厂商"""
        self.is_active = False
    
    @classmethod
    def get_active_providers(cls):
        """获取所有启用的厂商"""
        return cls.query.filter(
            cls.is_active == True,
            cls.is_deleted == False
        ).order_by(cls.name).all()
    
    @classmethod
    def find_by_name(cls, name):
        """根据名称查找厂商"""
        return cls.query.filter(
            cls.name == name,
            cls.is_deleted == False
        ).first()