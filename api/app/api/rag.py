from flask import Blueprint, request, jsonify, current_app
from app.services.rag_service import RAGService
from app.utils.response import api_response
from app.utils.jwt_utils import token_required
import logging

logger = logging.getLogger(__name__)

# 创建RAG蓝图
rag_bp = Blueprint('rag', __name__, url_prefix='/api/rag')


@rag_bp.route('/knowledge/text', methods=['GET'])
@token_required
def get_user_knowledge_text(current_user):
    """
    获取当前用户的知识库文本
    
    Returns:
        JSON: 包含用户知识库文本的响应
    """
    try:
        # 获取当前用户ID
        current_user_id = current_user.id
        
        # 获取用户知识库文本
        result = RAGService.get_user_knowledge_text(current_user_id)
        
        if result['success']:
            # 在控制台打印知识库文本
            print("\n" + "="*80)
            print(f"用户 {current_user_id} 的知识库文本 - API调用")
            print("="*80)
            print(result['knowledge_text'])
            print("="*80)
            print(f"统计信息: 邮箱绑定 {result['bindings_count']} 个，邮件 {result['emails_count']} 封")
            print(f"生成时间: {result['generated_at']}")
            print("="*80 + "\n")
            
            return api_response(
                success=True,
                message="用户知识库文本获取成功，已在控制台打印",
                data={
                    'user_id': result['user_id'],
                    'bindings_count': result['bindings_count'],
                    'emails_count': result['emails_count'],
                    'generated_at': result['generated_at'],
                    'knowledge_text_length': len(result['knowledge_text'])
                }
            )
        else:
            logger.error(f"获取用户 {current_user_id} 知识库失败: {result['error']}")
            return api_response(
                success=False,
                message=f"获取知识库失败: {result['error']}"
            ), 500
            
    except Exception as e:
        logger.error(f"获取用户知识库文本接口异常: {str(e)}")
        return api_response(
            success=False,
            message="服务器内部错误"
        ), 500


@rag_bp.route('/knowledge/print', methods=['POST'])
@token_required
def print_user_knowledge(current_user):
    """
    在控制台打印当前用户的知识库文本
    
    Returns:
        JSON: 操作结果响应
    """
    try:
        # 获取当前用户ID
        current_user_id = current_user.id
        
        # 打印用户知识库
        RAGService.print_user_knowledge(current_user_id)
        
        return api_response(
            success=True,
            message="用户知识库已在控制台打印",
            data={'user_id': current_user_id}
        )
        
    except Exception as e:
        logger.error(f"打印用户知识库接口异常: {str(e)}")
        return api_response(
            success=False,
            message="服务器内部错误"
        ), 500


@rag_bp.route('/knowledge/stats', methods=['GET'])
@token_required
def get_user_knowledge_stats(current_user):
    """
    获取当前用户的知识库统计信息
    
    Returns:
        JSON: 用户知识库统计信息
    """
    try:
        # 获取当前用户ID
        current_user_id = current_user.id
        
        # 获取用户知识库文本（仅用于统计）
        result = RAGService.get_user_knowledge_text(current_user_id)
        
        if result['success']:
            return api_response(
                success=True,
                message="用户知识库统计信息获取成功",
                data={
                    'user_id': result['user_id'],
                    'bindings_count': result['bindings_count'],
                    'emails_count': result['emails_count'],
                    'knowledge_text_length': len(result['knowledge_text']),
                    'generated_at': result['generated_at']
                }
            )
        else:
            logger.error(f"获取用户 {current_user_id} 知识库统计失败: {result['error']}")
            return api_response(
                success=False,
                message=f"获取知识库统计失败: {result['error']}"
            ), 500
            
    except Exception as e:
        logger.error(f"获取用户知识库统计接口异常: {str(e)}")
        return api_response(
            success=False,
            message="服务器内部错误"
        ), 500