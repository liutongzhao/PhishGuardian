from flask import Blueprint, request, jsonify, g
from app.middleware.auth import jwt_required
from app.services.conversation_service import ConversationService
from app.models import ConversationType, MessageRole
from app.utils import api_response
import logging

logger = logging.getLogger(__name__)

# 创建蓝图
conversation_bp = Blueprint('conversation', __name__, url_prefix='/api/conversation')

@conversation_bp.route('/list', methods=['GET'])
@jwt_required
def get_conversations():
    """获取用户对话列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        result = ConversationService.get_user_conversations(
            user_id=g.current_user.id,
            page=page,
            per_page=per_page
        )
        
        return api_response(
            success=True,
            data=result,
            message="获取对话列表成功"
        )
        
    except Exception as e:
        logger.error(f"获取对话列表失败: {e}")
        return api_response(success=False, message="获取对话列表失败")

@conversation_bp.route('/create', methods=['POST'])
@jwt_required
def create_conversation():
    """创建新对话"""
    try:
        data = request.get_json()
        title = data.get('title', '新对话')
        conversation_type = data.get('type', 'email_assistant')
        
        # 转换对话类型
        try:
            conv_type = ConversationType(conversation_type)
        except ValueError:
            conv_type = ConversationType.EMAIL_ASSISTANT
        
        conversation = ConversationService.create_conversation(
            user_id=g.current_user.id,
            title=title,
            conversation_type=conv_type
        )
        
        return api_response(
            success=True,
            data=conversation.to_dict(),
            message="创建对话成功"
        )
        
    except Exception as e:
        logger.error(f"创建对话失败: {e}")
        return api_response(success=False, message="创建对话失败")

@conversation_bp.route('/<int:conversation_id>/messages', methods=['GET'])
@jwt_required
def get_messages(conversation_id):
    """获取对话消息列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        result = ConversationService.get_conversation_messages(
            conversation_id=conversation_id,
            page=page,
            per_page=per_page
        )
        
        return api_response(
            success=True,
            data=result,
            message="获取消息列表成功"
        )
        
    except Exception as e:
        logger.error(f"获取消息列表失败: {e}")
        return api_response(success=False, message="获取消息列表失败")

@conversation_bp.route('/<int:conversation_id>/messages', methods=['POST'])
@jwt_required
def add_message(conversation_id):
    """添加消息到对话"""
    try:
        data = request.get_json()
        role = data.get('role', 'user')
        content = data.get('content', '')
        model_name = data.get('model_name')
        token_count = data.get('token_count', 0)
        has_rag_context = data.get('has_rag_context', False)
        rag_sources = data.get('rag_sources', [])
        
        if not content.strip():
            return api_response(success=False, message="消息内容不能为空")
        
        # 转换消息角色
        try:
            msg_role = MessageRole(role)
        except ValueError:
            msg_role = MessageRole.USER
        
        message = ConversationService.add_message(
            conversation_id=conversation_id,
            role=msg_role,
            content=content,
            model_name=model_name,
            token_count=token_count,
            has_rag_context=has_rag_context,
            rag_sources=rag_sources
        )
        
        return api_response(
            success=True,
            data=message.to_dict(),
            message="添加消息成功"
        )
        
    except Exception as e:
        logger.error(f"添加消息失败: {e}")
        return api_response(success=False, message="添加消息失败")

@conversation_bp.route('/<int:conversation_id>/title', methods=['PUT'])
@jwt_required
def update_title(conversation_id):
    """更新对话标题"""
    try:
        data = request.get_json()
        title = data.get('title', '')
        
        if not title.strip():
            return api_response(success=False, message="标题不能为空")
        
        success = ConversationService.update_conversation_title(
            conversation_id=conversation_id,
            title=title
        )
        
        if success:
            return api_response(success=True, message="更新标题成功")
        else:
            return api_response(success=False, message="对话不存在")
        
    except Exception as e:
        logger.error(f"更新标题失败: {e}")
        return api_response(success=False, message="更新标题失败")

@conversation_bp.route('/<int:conversation_id>', methods=['DELETE'])
@jwt_required
def delete_conversation(conversation_id):
    """删除对话"""
    try:
        success = ConversationService.delete_conversation(
            conversation_id=conversation_id,
            user_id=g.current_user.id
        )
        
        if success:
            return api_response(success=True, message="删除对话成功")
        else:
            return api_response(success=False, message="对话不存在或无权限删除")
        
    except Exception as e:
        logger.error(f"删除对话失败: {e}")
        return api_response(success=False, message="删除对话失败")

@conversation_bp.route('/<int:conversation_id>/archive', methods=['PUT'])
@jwt_required
def archive_conversation(conversation_id):
    """归档对话"""
    try:
        success = ConversationService.archive_conversation(
            conversation_id=conversation_id,
            user_id=g.current_user.id
        )
        
        if success:
            return api_response(success=True, message="归档对话成功")
        else:
            return api_response(success=False, message="对话不存在或无权限归档")
        
    except Exception as e:
        logger.error(f"归档对话失败: {e}")
        return api_response(success=False, message="归档对话失败")

@conversation_bp.route('/<int:conversation_id>/context', methods=['GET'])
@jwt_required
def get_context(conversation_id):
    """获取对话上下文"""
    try:
        max_messages = request.args.get('max_messages', 10, type=int)
        
        context = ConversationService.get_conversation_context(
            conversation_id=conversation_id,
            max_messages=max_messages
        )
        
        return api_response(
            success=True,
            data={'context': context},
            message="获取上下文成功"
        )
        
    except Exception as e:
        logger.error(f"获取上下文失败: {e}")
        return api_response(success=False, message="获取上下文失败")