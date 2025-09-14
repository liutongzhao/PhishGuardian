from flask import Blueprint, request, jsonify, current_app, Response
from app.services.rag_service import RAGService
from app.services.conversation_service import ConversationService
from app.utils.response import api_response
from app.utils.jwt_utils import token_required
import logging
import requests
import json
import time
import traceback

logger = logging.getLogger(__name__)

# 创建RAG蓝图
rag_bp = Blueprint('rag', __name__, url_prefix='/api/rag')

@rag_bp.route('/knowledge/text', methods=['GET'])
@token_required
def get_knowledge_text(current_user):
    """
    同步用户知识库到向量数据库
    """
    try:
        # 调用RAG服务获取并存储用户知识库
        result = RAGService.get_user_knowledge_text(current_user.id)
        
        if result['success']:
            return api_response(
                success=True,
                message=f'知识库同步成功，处理了{result["emails_count"]}封邮件和{result["bindings_count"]}个邮箱绑定',
                data={
                    'user_id': result['user_id'],
                    'emails_count': result['emails_count'],
                    'bindings_count': result['bindings_count'],
                    'vector_stored': result['vector_stored'],
                    'generated_at': result['generated_at']
                }
            )
        else:
            return api_response(
                success=False,
                message=f'知识库同步失败: {result["error"]}'
            ), 500
            
    except Exception as e:
        logger.error(f"同步知识库失败: {str(e)}")
        return api_response(
            success=False,
            message=f'同步知识库失败: {str(e)}'
        ), 500

def _call_ai_model(messages):
    """
    调用AI模型生成回复
    
    Args:
        messages: 消息列表
        
    Returns:
        Dict: AI模型响应结果
    """
    try:
        # 使用真实的GPT API调用
        api_url = "https://yunwu.ai/v1/chat/completions"
        api_key = "sk-BJyJEGSpGrNS2G0eFCscVgjBEp34Hb4FzCagVv56H7qrSSIl"
        model = "deepseek-v3-search"
        
        # 构建API请求
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0,
            "stream": False
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 发送API请求
        response = requests.post(api_url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        
        # 解析响应
        api_response = response.json()
        
        if 'choices' in api_response and len(api_response['choices']) > 0:
            content = api_response['choices'][0]['message']['content']
            
            # 计算token使用量
            usage = api_response.get('usage', {})
            token_count = usage.get('total_tokens', 0)
            
            return {
                'success': True,
                'content': content,
                'token_count': token_count
            }
        else:
            logger.error(f"AI API响应格式异常: {api_response}")
            return {
                'success': False,
                'error': 'AI API响应格式异常'
            }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"AI API请求失败: {str(e)}")
        return {
            'success': False,
            'error': f'AI API请求失败: {str(e)}'
        }
    except Exception as e:
        logger.error(f"AI模型调用失败: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


def _generate_fallback_response(message, rag_sources):
    """
    生成备用回复（当AI模型不可用时）
    
    Args:
        message: 用户消息
        rag_sources: RAG检索结果
        
    Returns:
        str: 备用回复内容
    """
    if rag_sources:
        response = f"根据您的问题\"{message}\"，我找到了以下相关信息：\n\n"
        for i, source in enumerate(rag_sources[:2], 1):
            content = source.get('content', '')[:200]  # 限制长度
            response += f"{i}. {content}...\n\n"
        response += "如需更详细的分析，请稍后重试或联系管理员。"
    else:
        response = f"感谢您的问题\"{message}\"。目前没有找到直接相关的信息，建议您：\n\n1. 检查邮件发送方是否可信\n2. 注意邮件中的可疑链接\n3. 验证邮件内容的真实性\n\n如需更详细的帮助，请稍后重试。"
    
    return response




@rag_bp.route('/chat/stream', methods=['POST'])
@token_required
def rag_chat_stream(current_user):
    return _rag_chat_stream_impl(current_user)

def _rag_chat_stream_impl(current_user):
    """
    RAG流式聊天接口
    
    接收用户消息，进行RAG检索，调用AI模型生成流式回复
    
    Returns:
        SSE流式响应
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return Response(
                f"data: {json.dumps({'error': '请求数据不能为空'})}\n\n",
                mimetype='text/plain'
            ), 400
            
        message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id')
        
        if not message:
            return Response(
                f"data: {json.dumps({'error': '消息内容不能为空'})}\n\n",
                mimetype='text/plain'
            ), 400
            
        # 获取当前用户ID
        current_user_id = current_user.id
        
        # 获取当前应用实例
        app = current_app._get_current_object()
        
        def generate_stream():
            nonlocal conversation_id  # 声明使用外部变量
            with app.app_context():
                try:
                    # 发送开始信号
                    yield f"data: {json.dumps({'type': 'start', 'message': '开始处理您的问题...'})}\n\n"
                    
                    # 1. 进行RAG检索
                    yield f"data: {json.dumps({'type': 'status', 'message': '正在检索相关信息...'})}\n\n"
                    
                    # RAG搜索（在应用上下文中）
                    search_result = RAGService.search_knowledge_base(
                        user_id=current_user_id,
                        query=message,
                        top_k=5
                    )
                    
                    rag_sources = []
                    rag_context = ""
                    
                    if search_result['success'] and search_result['results']:
                        # 构建RAG上下文
                        rag_sources = search_result['results']
                        context_parts = []
                        for i, result in enumerate(rag_sources[:3]):  # 只使用前3个最相关的结果
                            context_parts.append(f"参考信息{i+1}: {result.get('content', '')}")
                        rag_context = "\n\n".join(context_parts)
                    
                    # 2. 获取对话历史上下文
                    yield f"data: {json.dumps({'type': 'status', 'message': '正在分析对话历史...'})}\n\n"
                    
                    conversation_context = []
                    if conversation_id:
                        # 在应用上下文中执行数据库操作
                        conversation_context = ConversationService.get_conversation_context(
                            conversation_id=conversation_id,
                            max_messages=5
                        )
                    
                    # 3. 构建AI模型的prompt
                    system_prompt = """你是一个专业的邮件安全助手，专门帮助用户回答相关问题。请基于提供的上下文信息回答用户问题。
                            回答要求：
                            1. 准确、专业、有帮助
                            2.如果有相关的数据信息需要结合数据来回答，不要直接列举给你的数据，你需要对给定的数据进行自己的处理后回答用户的信息，注意数据的准确性和完整性
                            3.对于那些不需要提供数据回答的问题可以根据你的能力来帮助用户解决问题
                            4.尽可能详细的向用户解释
                            5.不要什么信息都依据我给的上下文内容，基于客观事实回答"""
                    
                    # 构建消息历史
                    messages = [{"role": "system", "content": system_prompt}]
                    
                    # 添加对话历史
                    for ctx in conversation_context[-4:]:  # 只保留最近4轮对话
                        messages.append({
                            "role": ctx['role'],
                            "content": ctx['content']
                        })
                    
                    # 添加当前用户消息（包含RAG上下文）
                    user_message = message
                    if rag_context:
                        user_message = f"参考以下信息回答问题：\n\n{rag_context}\n\n用户问题：{message}"
                    
                    messages.append({
                        "role": "user",
                        "content": user_message
                    })
                    
                    # 4. 调用AI模型进行流式生成
                    yield f"data: {json.dumps({'type': 'status', 'message': 'AI正在思考中...'})}\n\n"
                    
                    # 调用流式AI模型
                    full_content = ""
                    token_count = 0
                    logger.info(f"开始调用AI模型流式生成，消息数量: {len(messages)}")
                    
                    for chunk in _call_ai_model_stream(messages):
                        logger.debug(f"收到AI流式响应块: {chunk}")
                        if chunk['success']:
                            if chunk.get('content'):
                                content = chunk['content']
                                full_content += content
                                logger.debug(f"发送内容块: {repr(content)}")
                                yield f"data: {json.dumps({'type': 'content', 'content': content})}\n\n"
                            if chunk.get('token_count'):
                                token_count = chunk['token_count']
                                logger.info(f"AI生成完成，总内容长度: {len(full_content)}, token数量: {token_count}")
                        else:
                            error_msg = chunk.get('error', '生成失败')
                            logger.error(f"AI流式生成错误: {error_msg}")
                            yield f"data: {json.dumps({'type': 'error', 'message': error_msg})}\n\n"
                            return
                    
                    # 保存对话到数据库
                    try:
                        # 如果没有对话ID，创建新对话
                        if not conversation_id:
                            from app.models import ConversationType
                            conversation = ConversationService.create_conversation(
                                user_id=current_user_id,
                                title=message[:20] + '...' if len(message) > 20 else message,
                                conversation_type=ConversationType.EMAIL_ASSISTANT
                            )
                            conversation_id = conversation.id
                            yield f"data: {json.dumps({'type': 'conversation_created', 'conversation_id': conversation_id})}\n\n"
                        
                        # 保存用户消息
                        from app.models import MessageRole
                        ConversationService.add_message(
                            conversation_id=conversation_id,
                            role=MessageRole.USER,
                            content=message,
                            has_rag_context=len(rag_sources) > 0,
                            rag_sources=rag_sources
                        )
                        
                        # 保存助手回复
                        ConversationService.add_message(
                            conversation_id=conversation_id,
                            role=MessageRole.ASSISTANT,
                            content=full_content,
                            model_name="gpt-4o",
                            token_count=token_count,
                            has_rag_context=len(rag_sources) > 0,
                            rag_sources=rag_sources
                        )
                        
                        logger.info(f"对话保存成功: conversation_id={conversation_id}, user_message_len={len(message)}, assistant_message_len={len(full_content)}")
                        
                    except Exception as save_error:
                        logger.error(f"保存对话失败: {str(save_error)}")
                        logger.error(f"保存异常堆栈: {traceback.format_exc()}")
                        # 不中断流式响应，只记录错误
                    
                    # 发送完成信号
                    yield f"data: {json.dumps({'type': 'done', 'sources': rag_sources, 'token_count': token_count, 'has_rag_context': len(rag_sources) > 0, 'conversation_id': conversation_id})}\n\n"
                    
                except Exception as e:
                    logger.error(f"流式生成异常: {str(e)}")
                    logger.error(f"异常堆栈: {traceback.format_exc()}")
                    error_msg = f"服务器内部错误: {str(e)}"
                    yield f"data: {json.dumps({'type': 'error', 'message': error_msg})}\n\n"
        
        return Response(
            generate_stream(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            }
        )
        
    except Exception as e:
        logger.error(f"RAG流式聊天接口异常: {str(e)}")
        return Response(
            f"data: {json.dumps({'type': 'error', 'message': '服务器内部错误'})}\n\n",
            mimetype='text/event-stream'
        ), 500


def _call_ai_model_stream(messages):
    """
    调用AI模型进行流式生成
    
    Args:
        messages: 消息列表
        
    Yields:
        Dict: AI模型流式响应结果
    """
    try:
        # 使用真实的GPT API调用
        api_url = "https://yunwu.ai/v1/chat/completions"
        api_key = "sk-BJyJEGSpGrNS2G0eFCscVgjBEp34Hb4FzCagVv56H7qrSSIl"
        model = "deepseek-v3-search"
        
        # 构建API请求
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0,
            "stream": True  # 启用流式响应
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 发送API请求
        response = requests.post(api_url, json=payload, headers=headers, timeout=120, stream=True)
        response.raise_for_status()
        
        # 解析流式响应
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data_str = line[6:]  # 移除 'data: ' 前缀
                    
                    if data_str.strip() == '[DONE]':
                        break
                    
                    try:
                        data = json.loads(data_str)
                        if 'choices' in data and len(data['choices']) > 0:
                            choice = data['choices'][0]
                            
                            # 处理流式内容
                            if 'delta' in choice:
                                delta = choice['delta']
                                if 'content' in delta and delta['content']:
                                    content = delta['content']
                                    logger.debug(f"AI流式内容: {repr(content)}")
                                    yield {
                                        'success': True,
                                        'content': content
                                    }
                            
                            # 检查是否完成
                            if choice.get('finish_reason') == 'stop':
                                # 计算token使用量（如果有的话）
                                usage = data.get('usage', {})
                                token_count = usage.get('total_tokens', 0)
                                logger.info(f"AI流式生成完成，token使用量: {token_count}")
                                yield {
                                    'success': True,
                                    'token_count': token_count
                                }
                                break
                                
                    except json.JSONDecodeError:
                        continue
        
    except requests.exceptions.RequestException as e:
        logger.error(f"AI API流式请求失败: {str(e)}")
        yield {
            'success': False,
            'error': f'AI API请求失败: {str(e)}'
        }
    except Exception as e:
        logger.error(f"AI模型流式调用失败: {str(e)}")
        yield {
            'success': False,
            'error': str(e)
        }