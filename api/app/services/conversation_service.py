from datetime import datetime
from typing import List, Dict, Any, Optional
from app import db
from app.models import Conversation, ConversationMessage, ConversationType, MessageRole, User
from sqlalchemy import desc
import logging

logger = logging.getLogger(__name__)

class ConversationService:
    """对话服务类"""
    
    @staticmethod
    def create_conversation(user_id: int, title: str = "新对话", 
                          conversation_type: ConversationType = ConversationType.EMAIL_ASSISTANT) -> Conversation:
        """创建新对话
        
        Args:
            user_id: 用户ID
            title: 对话标题
            conversation_type: 对话类型
            
        Returns:
            Conversation: 创建的对话对象
        """
        try:
            conversation = Conversation(
                user_id=user_id,
                title=title,
                conversation_type=conversation_type
            )
            
            db.session.add(conversation)
            db.session.commit()
            
            logger.info(f"创建新对话成功: user_id={user_id}, conversation_id={conversation.id}")
            return conversation
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"创建对话失败: {e}")
            raise
    
    @staticmethod
    def get_user_conversations(user_id: int, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """获取用户的对话列表
        
        Args:
            user_id: 用户ID
            page: 页码
            per_page: 每页数量
            
        Returns:
            Dict: 分页的对话列表
        """
        try:
            conversations = Conversation.query.filter_by(
                user_id=user_id,
                is_active=True,
                is_archived=False
            ).order_by(desc(Conversation.last_message_at)).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            return {
                'conversations': [conv.to_dict() for conv in conversations.items],
                'pagination': {
                    'page': conversations.page,
                    'per_page': conversations.per_page,
                    'total': conversations.total,
                    'pages': conversations.pages,
                    'has_prev': conversations.has_prev,
                    'has_next': conversations.has_next
                }
            }
            
        except Exception as e:
            logger.error(f"获取用户对话列表失败: {e}")
            raise
    
    @staticmethod
    def get_conversation_messages(conversation_id: int, page: int = 1, per_page: int = 50) -> Dict[str, Any]:
        """获取对话消息列表
        
        Args:
            conversation_id: 对话ID
            page: 页码
            per_page: 每页数量
            
        Returns:
            Dict: 分页的消息列表
        """
        try:
            messages = ConversationMessage.query.filter_by(
                conversation_id=conversation_id,
                is_deleted=False
            ).order_by(ConversationMessage.created_at).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            return {
                'messages': [msg.to_dict() for msg in messages.items],
                'pagination': {
                    'page': messages.page,
                    'per_page': messages.per_page,
                    'total': messages.total,
                    'pages': messages.pages,
                    'has_prev': messages.has_prev,
                    'has_next': messages.has_next
                }
            }
            
        except Exception as e:
            logger.error(f"获取对话消息失败: {e}")
            raise
    
    @staticmethod
    def add_message(conversation_id: int, role: MessageRole, content: str,
                   model_name: str = None, token_count: int = 0,
                   has_rag_context: bool = False, rag_sources: List[Dict] = None) -> ConversationMessage:
        """添加消息到对话
        
        Args:
            conversation_id: 对话ID
            role: 消息角色
            content: 消息内容
            model_name: 模型名称
            token_count: token数量
            has_rag_context: 是否包含RAG上下文
            rag_sources: RAG源文档信息
            
        Returns:
            ConversationMessage: 创建的消息对象
        """
        try:
            # 创建消息
            message = ConversationMessage(
                conversation_id=conversation_id,
                role=role,
                content=content,
                model_name=model_name,
                token_count=token_count,
                has_rag_context=has_rag_context,
                rag_sources=rag_sources or []
            )
            
            db.session.add(message)
            
            # 更新对话信息
            conversation = Conversation.query.get(conversation_id)
            if conversation:
                conversation.message_count += 1
                conversation.last_message_at = datetime.utcnow()
                
                # 如果是第一条用户消息，更新对话标题
                if role == MessageRole.USER and conversation.message_count == 1:
                    title = content[:20] + '...' if len(content) > 20 else content
                    conversation.title = title
            
            db.session.commit()
            
            logger.info(f"添加消息成功: conversation_id={conversation_id}, role={role.value}")
            return message
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"添加消息失败: {e}")
            raise
    
    @staticmethod
    def update_conversation_title(conversation_id: int, title: str) -> bool:
        """更新对话标题
        
        Args:
            conversation_id: 对话ID
            title: 新标题
            
        Returns:
            bool: 是否更新成功
        """
        try:
            conversation = Conversation.query.get(conversation_id)
            if not conversation:
                return False
            
            conversation.title = title
            db.session.commit()
            
            logger.info(f"更新对话标题成功: conversation_id={conversation_id}")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"更新对话标题失败: {e}")
            return False
    
    @staticmethod
    def delete_conversation(conversation_id: int, user_id: int) -> bool:
        """删除对话（软删除）
        
        Args:
            conversation_id: 对话ID
            user_id: 用户ID（用于权限验证）
            
        Returns:
            bool: 是否删除成功
        """
        try:
            conversation = Conversation.query.filter_by(
                id=conversation_id,
                user_id=user_id
            ).first()
            
            if not conversation:
                return False
            
            conversation.is_active = False
            db.session.commit()
            
            logger.info(f"删除对话成功: conversation_id={conversation_id}")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"删除对话失败: {e}")
            return False
    
    @staticmethod
    def archive_conversation(conversation_id: int, user_id: int) -> bool:
        """归档对话
        
        Args:
            conversation_id: 对话ID
            user_id: 用户ID（用于权限验证）
            
        Returns:
            bool: 是否归档成功
        """
        try:
            conversation = Conversation.query.filter_by(
                id=conversation_id,
                user_id=user_id
            ).first()
            
            if not conversation:
                return False
            
            conversation.is_archived = True
            db.session.commit()
            
            logger.info(f"归档对话成功: conversation_id={conversation_id}")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"归档对话失败: {e}")
            return False
    
    @staticmethod
    def get_conversation_context(conversation_id: int, max_messages: int = 10) -> List[Dict[str, Any]]:
        """获取对话上下文（用于RAG）
        
        Args:
            conversation_id: 对话ID
            max_messages: 最大消息数量
            
        Returns:
            List[Dict]: 消息上下文列表
        """
        try:
            messages = ConversationMessage.query.filter_by(
                conversation_id=conversation_id,
                is_deleted=False
            ).order_by(desc(ConversationMessage.created_at)).limit(max_messages).all()
            
            # 反转顺序，使其按时间正序排列
            messages.reverse()
            
            context = []
            for msg in messages:
                context.append({
                    'role': msg.role.value,
                    'content': msg.content,
                    'timestamp': msg.created_at.isoformat()
                })
            
            return context
            
        except Exception as e:
            logger.error(f"获取对话上下文失败: {e}")
            return []