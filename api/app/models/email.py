from datetime import datetime
import pytz
from enum import Enum
from app import db


class EmailDetectionStatus(Enum):
    """邮件检测状态枚举"""
    PENDING = 0      # 待检测
    DETECTING = 1    # 检测中
    SUCCESS = 2      # 检测成功
    FAILED = 3       # 检测失败


class Email(db.Model):
    """邮件信息模型"""
    __tablename__ = 'emails'
    
    # 基础字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='邮件唯一标识')
    binding_id = db.Column(db.Integer, nullable=False, index=True, comment='绑定邮箱ID')
    provider_id = db.Column(db.Integer, nullable=True, index=True, comment='邮箱厂商ID')
    user_id = db.Column(db.Integer, nullable=False, index=True, comment='用户ID')
    
    # 邮箱信息
    provider_display_name = db.Column(db.String(100), nullable=True, comment='邮箱厂商显示名称')
    email_address = db.Column(db.String(255), nullable=True, index=True, comment='邮箱地址')
    
    # 邮件基础信息
    email_uid = db.Column(db.String(50), nullable=True, index=True, comment='邮件UID')
    subject = db.Column(db.Text, nullable=True, comment='邮件主题')
    sender = db.Column(db.String(255), nullable=True, comment='邮件发送方')
    email_date = db.Column(db.DateTime, nullable=True, comment='邮件日期')
    content = db.Column(db.Text, nullable=True, comment='邮件正文')
    headers = db.Column(db.Text, nullable=True, comment='邮件完整头信息')
    
    # 检测状态
    detection_status = db.Column(db.Integer, default=EmailDetectionStatus.PENDING.value, nullable=False, index=True, comment='检测状态：0-待检测，1-检测中，2-检测成功，3-检测失败')
    
    # 状态字段
    is_deleted = db.Column(db.Boolean, default=False, nullable=False, index=True, comment='是否删除')
    
    # 保留字段
    reserved_field1 = db.Column(db.String(255), nullable=True, comment='保留字段1')
    reserved_field2 = db.Column(db.String(255), nullable=True, comment='保留字段2')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')), nullable=False, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')), onupdate=lambda: datetime.now(pytz.timezone('Asia/Shanghai')), nullable=False, comment='更新时间')
    
    def __repr__(self):
        return f'<Email {self.subject} from {self.sender}>'
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'binding_id': self.binding_id,
            'provider_id': self.provider_id,
            'user_id': self.user_id,
            'provider_display_name': self.provider_display_name,
            'email_address': self.email_address,
            'email_uid': self.email_uid,
            'subject': self.subject,
            'sender': self.sender,
            'email_date': self.email_date.isoformat() if self.email_date else None,
            'content': self.content,
            'headers': self.headers,
            'detection_status': self.detection_status,
            'detection_status_name': EmailDetectionStatus(self.detection_status).name,
            'is_deleted': self.is_deleted,
            'reserved_field1': self.reserved_field1,
            'reserved_field2': self.reserved_field2,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def soft_delete(self):
        """软删除邮件"""
        self.is_deleted = True
    
    def restore(self):
        """恢复已删除的邮件"""
        self.is_deleted = False
    
    def update_detection_status(self, status: EmailDetectionStatus):
        """更新检测状态"""
        self.detection_status = status.value
        db.session.commit()
    
    @classmethod
    def find_by_uid(cls, binding_id, email_uid):
        """根据绑定ID和邮件UID查找邮件"""
        return cls.query.filter(
            cls.binding_id == binding_id,
            cls.email_uid == email_uid,
            cls.is_deleted == False
        ).first()
    
    @classmethod
    def get_user_emails(cls, user_id, active_only=True):
        """获取用户的所有邮件"""
        query = cls.query.filter(cls.user_id == user_id)
        
        if active_only:
            query = query.filter(cls.is_deleted == False)
        
        return query.order_by(cls.email_date.desc()).all()
    
    @classmethod
    def get_binding_emails(cls, binding_id, active_only=True):
        """获取指定绑定邮箱的所有邮件"""
        query = cls.query.filter(cls.binding_id == binding_id)
        
        if active_only:
            query = query.filter(cls.is_deleted == False)
        
        return query.order_by(cls.email_date.desc()).all()
    
    @classmethod
    def get_pending_detection_emails(cls, limit=None):
        """获取待检测的邮件"""
        query = cls.query.filter(
            cls.detection_status == EmailDetectionStatus.PENDING.value,
            cls.is_deleted == False
        ).order_by(cls.created_at.asc())
        
        if limit:
            query = query.limit(limit)
            
        return query.all()
    
    @classmethod
    def get_detecting_emails(cls, limit=None):
        """获取检测中的邮件"""
        query = cls.query.filter(
            cls.detection_status == EmailDetectionStatus.DETECTING.value,
            cls.is_deleted == False
        ).order_by(cls.created_at.asc())
        
        if limit:
            query = query.limit(limit)
            
        return query.all()
    
    @classmethod
    def count_by_status(cls, user_id=None, status=None, binding_id=None):
        """按状态统计邮件数量"""
        query = cls.query.filter(cls.is_deleted == False)
        
        if user_id:
            query = query.filter(cls.user_id == user_id)
        
        if binding_id:
            query = query.filter(cls.binding_id == binding_id)
        
        if status is not None:
            if isinstance(status, EmailDetectionStatus):
                query = query.filter(cls.detection_status == status.value)
            else:
                query = query.filter(cls.detection_status == status)
        
        return query.count()