from datetime import datetime
from app import db
from enum import Enum

class ConversationType(Enum):
    """对话类型枚举"""
    EMAIL_ASSISTANT = 'email_assistant'  # 邮件助手对话
    PHISHING_DETECTION = 'phishing_detection'  # 钓鱼邮件检测对话
    GENERAL_INQUIRY = 'general_inquiry'  # 一般咨询

class MessageRole(Enum):
    """消息角色枚举"""
    USER = 'user'  # 用户消息
    ASSISTANT = 'assistant'  # 助手消息
    SYSTEM = 'system'  # 系统消息

class Conversation(db.Model):
    """对话会话表"""
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False, default='新对话')
    conversation_type = db.Column(db.Enum(ConversationType), nullable=False, default=ConversationType.EMAIL_ASSISTANT)
    
    # 对话状态
    is_active = db.Column(db.Boolean, default=True)  # 是否活跃
    is_archived = db.Column(db.Boolean, default=False)  # 是否归档
    
    # 对话统计
    message_count = db.Column(db.Integer, default=0)  # 消息数量
    last_message_at = db.Column(db.DateTime, default=datetime.utcnow)  # 最后消息时间
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关联关系
    user = db.relationship('User', backref=db.backref('conversations', lazy=True))
    messages = db.relationship('ConversationMessage', backref='conversation', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'conversation_type': self.conversation_type.value,
            'is_active': self.is_active,
            'is_archived': self.is_archived,
            'message_count': self.message_count,
            'last_message_at': self.last_message_at.isoformat() if self.last_message_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Conversation {self.id}: {self.title}>'

class ConversationMessage(db.Model):
    """对话消息表"""
    __tablename__ = 'conversation_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    
    # 消息内容
    role = db.Column(db.Enum(MessageRole), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # 消息元数据
    token_count = db.Column(db.Integer, default=0)  # token数量
    model_name = db.Column(db.String(100))  # 使用的模型名称
    
    # RAG相关字段
    has_rag_context = db.Column(db.Boolean, default=False)  # 是否包含RAG上下文
    rag_sources = db.Column(db.JSON)  # RAG检索的源文档信息
    
    # 消息状态
    is_deleted = db.Column(db.Boolean, default=False)  # 是否已删除
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'role': self.role.value,
            'content': self.content,
            'token_count': self.token_count,
            'model_name': self.model_name,
            'has_rag_context': self.has_rag_context,
            'rag_sources': self.rag_sources,
            'is_deleted': self.is_deleted,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<ConversationMessage {self.id}: {self.role.value}>'