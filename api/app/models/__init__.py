# 数据库模型模块
from .user import User, RegistrationType
from .email_provider import EmailProvider
from .user_email_binding import UserEmailBinding
from .email import Email, EmailDetectionStatus
from .email_detection_detail import EmailDetectionDetail, UrgencyLevel, ImportanceLevel
from .conversation import Conversation, ConversationMessage, ConversationType, MessageRole

__all__ = [
    'User',
    'RegistrationType',
    'EmailProvider',
    'UserEmailBinding',
    'Email',
    'EmailDetectionStatus',
    'EmailDetectionDetail',
    'UrgencyLevel',
    'ImportanceLevel',
    'Conversation',
    'ConversationMessage',
    'ConversationType',
    'MessageRole'
]