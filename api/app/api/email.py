from flask import Blueprint, request, jsonify
from app.utils import api_response
from app.models.email_provider import EmailProvider
from app.models.user_email_binding import UserEmailBinding
from app.models.email import Email, EmailDetectionStatus
from app.models.email_detection_detail import EmailDetectionDetail
from app.services.email_binding_service import EmailBindingService
from app.services.email_fetch_service import EmailFetchService
from app.services.email_detection_service import EmailDetectionService
from app.utils.jwt_utils import token_required
from app import db
import logging

logger = logging.getLogger(__name__)

# 创建邮箱管理蓝图
email_bp = Blueprint('email', __name__)


@email_bp.route('/providers', methods=['GET'])
@token_required
def get_email_providers(current_user):
    """获取邮箱厂商列表"""
    try:
        # 获取所有启用的邮箱厂商
        providers = EmailProvider.get_active_providers()
        
        # 转换为字典格式
        providers_data = [provider.to_dict() for provider in providers]
        
        return api_response(
            success=True,
            message='获取邮箱厂商列表成功',
            data={
                'providers': providers_data,
                'total': len(providers_data)
            }
        )
        
    except Exception as e:
        return api_response(
            success=False,
            message=f'服务器错误: {str(e)}'
        )


@email_bp.route('/<int:email_id>/set-detection-status', methods=['POST'])
@token_required
def set_email_detection_status(current_user, email_id):
    """设置邮件检测状态为2（钓鱼邮件）"""
    
    try:
        # 获取邮件信息
        email = Email.query.get(email_id)
        print(email.detection_status)
        if not email:
            return api_response(
                success=False,
                message='邮件不存在'
            )
        
        # 检查邮件是否属于当前用户
        if email.user_id != current_user.id:
            return api_response(
                success=False,
                message='无权限访问该邮件'
            )
        
        # 设置邮件检测状态为2（完成）
        email.detection_status = 2
        
        # 获取检测详情并设置为第四阶段
        detail = EmailDetectionDetail.find_by_email_id(email_id)
        if detail:
            detail.detection_stage = 4
            detail.reserved_field2 = '2'  # 标记为钓鱼邮件，直接完成
            db.session.add(detail)
        
        db.session.add(email)
        db.session.commit()
        
        return api_response(
            success=True,
            message='邮件检测状态设置成功',
            data={
                'email_id': email_id,
                'detection_status': 2,
                'detection_stage': 4
            }
        )
        
    except Exception as e:
        db.session.rollback()
        return api_response(
            success=False,
            message=f'设置检测状态失败: {str(e)}'
        )


@email_bp.route('/<int:email_id>/start-stage4-detection', methods=['POST'])
@token_required
def start_stage4_detection(current_user, email_id):
    """开始第四阶段检测（邮件摘要分析）"""
    try:
        # 获取邮件信息
        email = Email.query.get(email_id)
        if not email:
            return api_response(
                success=False,
                message='邮件不存在'
            )
        
        # 检查邮件是否属于当前用户
        if email.user_id != current_user.id:
            return api_response(
                success=False,
                message='无权限访问该邮件'
            )
        
        # 获取检测详情
        detail = EmailDetectionDetail.find_by_email_id(email_id)
        if not detail:
            return api_response(
                success=False,
                message='邮件检测详情不存在'
            )
        
        # 设置检测阶段为第四阶段
        detail.detection_stage = 4
        detail.reserved_field2 = '0'  # 标记为检测中
        db.session.add(detail)
        db.session.commit()
        
        # 启动异步第四阶段检测任务
        from app.services.async_detection_service import async_detection_service
        from app.services.detection_agents import DEFAULT_API_URL, DEFAULT_API_KEY, DEFAULT_MODEL
        
        # 提交第四阶段分析任务
        async_detection_service.submit_detection_task(
            email_id, 'stage4_analysis',
            lambda content: _analyze_email_content_stage4(content, DEFAULT_API_URL, DEFAULT_API_KEY, DEFAULT_MODEL),
            email.content or ''
        )
        
        return api_response(
            success=True,
            message='第四阶段检测已启动',
            data={
                'email_id': email_id,
                'detection_stage': 4,
                'status': 'detecting'
            }
        )
        
    except Exception as e:
        db.session.rollback()
        return api_response(
            success=False,
            message=f'启动第四阶段检测失败: {str(e)}'
        )


def _analyze_email_content_stage4(content: str, api_url: str, api_key: str, model: str) -> dict:
    """第四阶段邮件内容分析"""
    import requests
    import json
    
    try:
        # 构建提示词
        prompt = f"""
请分析以下邮件内容，并以严格的JSON格式返回分析结果：

邮件内容：
{content}

请提取以下信息：
1. 邮件摘要（文本形式，不超过100字）
2. 紧急程度（"紧急" 或 "普通"）
3. 重要程度（"高"、"中" 或 "低"）
4. 邮件类型（不超过5个字概括，如：广告营销、会员续费、会议提醒等）
5. 是否需要添加日程（1表示需要，0表示不需要）
6. 如果需要添加日程，请提供日程名称

请严格按照以下JSON格式返回：
{{
  "summary": "邮件摘要",
  "urgency_level": "普通",
  "importance_level": "中",
  "email_type": "邮件类型",
  "need_schedule": 0,
  "schedule_name": "日程名称（如果需要的话）"
}}
"""
        
        # 调用大模型API
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        
        data = {
            'model': model,
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': 0,
            'max_tokens': 1000
        }
        
        response = requests.post(api_url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        content_text = result['choices'][0]['message']['content'].strip()
        
        # 尝试解析JSON响应
        try:
            # 提取JSON部分
            if '```json' in content_text:
                json_start = content_text.find('```json') + 7
                json_end = content_text.find('```', json_start)
                content_text = content_text[json_start:json_end].strip()
            elif '{' in content_text and '}' in content_text:
                json_start = content_text.find('{')
                json_end = content_text.rfind('}') + 1
                content_text = content_text[json_start:json_end]
            
            analysis_result = json.loads(content_text)
            
            return {
                'success': True,
                'analysis': analysis_result
            }
            
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {str(e)}, 原始内容: {content_text}")
            return {
                'success': False,
                'error': f'JSON解析失败: {str(e)}',
                'raw_content': content_text
            }
            
    except Exception as e:
        print(f"第四阶段分析失败: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


@email_bp.route('/update-detection-stage', methods=['POST'])
@token_required
def update_detection_stage(current_user):
    """更新检测阶段"""
    try:
        data = request.get_json()
        email_id = data.get('email_id')
        
        if not email_id:
            return api_response(
                success=False,
                message='邮件ID不能为空'
            )
        
        # 查找邮件检测详情
        detection_detail = EmailDetectionDetail.find_by_email_id(email_id)
        if not detection_detail:
            return api_response(
                success=False,
                message='未找到邮件检测详情'
            )
        
        # 验证邮件所有权
        email = Email.query.get(email_id)
        if not email or email.user_id != current_user.id:
            return api_response(
                success=False,
                message='无权限操作此邮件'
            )
        
        # 更新检测阶段为第三阶段，reserved_field1设置为0
        detection_detail.detection_stage = 3
        detection_detail.reserved_field1 = 0
        
        db.session.add(detection_detail)
        db.session.commit()
        
        return api_response(
            success=True,
            message='检测阶段更新成功',
            data={
                'email_id': email_id,
                'detection_stage': 3,
                'reserved_field1': 0
            }
        )
        
    except Exception as e:
        db.session.rollback()
        return api_response(
            success=False,
            message=f'更新检测阶段失败: {str(e)}'
        )





@email_bp.route('/fetch', methods=['GET'])
def fetch_emails():
    """简单的邮件获取接口"""
    try:
        result = EmailFetchService.fetch_emails()
        
        return jsonify({
            'success': True,
            'message': result['message']
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'邮件获取失败: {str(e)}'
        }), 500




@email_bp.route('/<int:email_id>/start-detection', methods=['POST'])
@token_required
def start_email_detection(current_user, email_id):
    """开始检测邮件"""
    try:
        # 获取邮件信息
        email = Email.query.get(email_id)
        if not email:
            return api_response(
                success=False,
                message='邮件不存在'
            )
        
        # 设置邮件检测状态为检测中
        email.detection_status = EmailDetectionStatus.DETECTING.value
        
        # 初始化检测权重
        result = EmailDetectionService.initialize_detection_weights(email_id)
        
        if result['success']:
            # 设置检测阶段为第二阶段
            detail = EmailDetectionDetail.find_by_email_id(email_id)
            if detail:
                detail.detection_stage = 2
                db.session.add(detail)
            
            # 提交数据库事务
            db.session.commit()
            
            # 启动异步检测任务
            from app.services.async_detection_service import async_detection_service
            from app.services.detection_agents import detection_agents
            from app.models.email_detection_detail import DetectionStatus
            
            # 获取邮件数据
            email = Email.query.get(email_id)
            if email and detail:
                # 根据权重决定是否启动检测任务
                if detail.content_weight > 0 and detail.content_detection_status != DetectionStatus.NO_NEED.value:
                    detail.content_detection_status = DetectionStatus.DETECTING.value
                    async_detection_service.submit_detection_task(
                        email_id, 'content', 
                        detection_agents.analyze_content,
                        email.content or ''
                    )
                
                if detail.url_weight > 0 and detail.url_detection_status != DetectionStatus.NO_NEED.value:
                    detail.url_detection_status = DetectionStatus.DETECTING.value
                    async_detection_service.submit_detection_task(
                        email_id, 'url',
                        detection_agents.analyze_urls,
                        email.content or ''
                    )
                
                if detail.metadata_weight > 0 and detail.metadata_detection_status != DetectionStatus.NO_NEED.value:
                    detail.metadata_detection_status = DetectionStatus.DETECTING.value
                    # 解析headers字符串为字典格式
                    headers_dict = {}
                    if email.headers and email.headers.strip():
                        try:
                            # 解析邮件头部字符串为字典
                            import email as email_parser
                            msg = email_parser.message_from_string(email.headers)
                            headers_dict = dict(msg.items())
                        except Exception as e:
                            print(f"解析邮件头部失败: {str(e)}")
                            headers_dict = {}
                    
                    async_detection_service.submit_detection_task(
                        email_id, 'metadata',
                        lambda headers: detection_agents.analyze_metadata(headers),
                        headers_dict
                    )
                
                # 更新检测状态到数据库
                db.session.add(detail)
                db.session.commit()
            
            return api_response(
                success=True,
                message='开始检测成功',
                data={
                    'email_id': email_id,
                    'detection_status': email.detection_status,
                    'weights': result['data']['weights'],
                    'detection_detail_id': result['data']['detection_detail_id']
                }
            )
        else:
            # 回滚事务
            db.session.rollback()
            return api_response(
                success=False,
                message=result['message']
            )
            
    except Exception as e:
        db.session.rollback()
        return api_response(
            success=False,
            message=f'开始检测失败: {str(e)}'
        )


@email_bp.route('/<int:email_id>/start-stage3-detection', methods=['POST'])
@token_required
def start_stage3_detection(current_user, email_id):
    """开始第三阶段检测（综合分析）"""
    try:
        # 获取邮件信息
        email = Email.query.get(email_id)
        if not email:
            return api_response(
                success=False,
                message='邮件不存在'
            )
        
        # 检查邮件是否属于当前用户
        if email.user_id != current_user.id:
            return api_response(
                success=False,
                message='无权限访问该邮件'
            )
        
        # 获取检测详情
        detail = EmailDetectionDetail.find_by_email_id(email_id)
        print("detail",detail)
        if not detail:
            return api_response(
                success=False,
                message='邮件检测详情不存在'
            )
        
        # 检查是否已完成第二阶段检测（检查所有并行检测状态）
        statuses = [
            detail.content_detection_status,
            detail.url_detection_status,
            detail.metadata_detection_status
        ]
        
        # 检查所有状态是否都是完成(2)或无需检测(3)
        all_completed = all(status in [2, 3] for status in statuses)
        
        if not all_completed:
            return api_response(
                success=False,
                message='第二阶段检测尚未完成，无法开始第三阶段检测'
            )
        
        # 设置检测阶段为第三阶段
        detail.detection_stage = 3
        db.session.add(detail)
        db.session.commit()
        
        # 准备传递给synthesize_results的参数
        text_result = {
            "verdict": "Phishing" if detail.content_is_phishing else "Safe",
            "phishing_probability": detail.content_phishing_probability,
            "confidence": detail.content_confidence,
            "reasons": detail.content_reason or "无检测原因"
        }
        
        url_result = {
            "verdict": "Phishing" if detail.url_is_phishing else "Safe",
            "phishing_probability": detail.url_phishing_probability,
            "confidence": detail.url_confidence,
            "reasons": detail.url_reason or "无检测原因"
        }
        
        metadata_result = {
            "verdict": "Phishing" if detail.metadata_is_phishing else "Safe",
            "phishing_probability": detail.metadata_phishing_probability,
            "confidence": detail.metadata_confidence,
            "reasons": detail.metadata_reason or "无检测原因"
        }
        
        weights = {
            "text": detail.content_weight,
            "url": detail.url_weight,
            "metadata": detail.metadata_weight
        }

        print("权重为：",weights)
        print("text_result",text_result)
        print("url_result",url_result)
        print("metadata_result",metadata_result)

        
        # 启动异步综合分析任务
        from app.services.async_detection_service import async_detection_service
        from app.services.synthesis_agent import synthesize_results
        from app.services.detection_agents import DEFAULT_API_URL, DEFAULT_API_KEY
        
        # 获取API配置
        api_url = DEFAULT_API_URL
        api_key = DEFAULT_API_KEY
        
        # 提交综合分析任务
        async_detection_service.submit_detection_task(
            email_id, 'synthesis',
            synthesize_results,
            text_result, url_result, metadata_result, api_url, api_key, weights
        )
        
        return api_response(
            success=True,
            message='第三阶段检测已启动',
            data={
                'email_id': email_id,
                'detection_stage': 3,
                'text_result': text_result,
                'url_result': url_result,
                'metadata_result': metadata_result,
                'weights': weights
            }
        )
        
    except Exception as e:
        db.session.rollback()
        return api_response(
            success=False,
            message=f'启动第三阶段检测失败: {str(e)}'
        )


@email_bp.route('/detection-overview', methods=['GET'])
@token_required
def get_detection_overview(current_user):
    """获取检测概览数据"""
    try:
        user_id = current_user.id
        
        # 查找正在检测的邮件
        detecting_email = Email.query.filter_by(
            user_id=user_id,
            detection_status=EmailDetectionStatus.DETECTING.value,
            is_deleted=False
        ).first()
        
        detecting_email_data = None
        detecting_detail = None
        if detecting_email:
            # 获取邮件基本信息
            detecting_email_data = detecting_email.to_dict()
            # 获取检测详情
            detail = EmailDetectionDetail.find_by_email_id(detecting_email.id)
            if detail:
                detecting_detail = detail.to_dict()
        
        # 查找待检测的邮件列表
        pending_emails = Email.query.filter_by(
            user_id=user_id,
            detection_status=EmailDetectionStatus.PENDING.value,
            is_deleted=False
        ).order_by(Email.created_at.asc()).all()
        
        # 转换为字典格式
        pending_emails_data = [email.to_dict() for email in pending_emails]
        
        return api_response(
            success=True,
            message='获取检测概览成功',
            data={
                'detecting_email': detecting_email_data,
                'detecting_detail': detecting_detail,
                'pending_emails': pending_emails_data
            }
        )
        
    except Exception as e:
        return api_response(
            success=False,
            message=f'获取检测概览失败: {str(e)}'
        )


@email_bp.route('/providers/<int:provider_id>', methods=['GET'])
@token_required
def get_email_provider(current_user, provider_id):
    """获取指定邮箱厂商详情"""
    try:
        provider = EmailProvider.query.filter(
            EmailProvider.id == provider_id,
            EmailProvider.is_deleted == False
        ).first()
        
        if not provider:
            return api_response(
                success=False,
                message='邮箱厂商不存在'
            )
        
        return api_response(
            success=True,
            message='获取邮箱厂商详情成功',
            data=provider.to_dict()
        )
        
    except Exception as e:
        return api_response(
            success=False,
            message=f'服务器错误: {str(e)}'
        )


@email_bp.route('/providers', methods=['POST'])
@token_required
def create_email_provider(current_user):
    """创建邮箱厂商（管理员功能）"""
    try:
        data = request.get_json()
        if not data:
            return api_response(
                success=False,
                message='请求数据不能为空'
            )
        
        # 验证必填字段
        required_fields = ['name', 'display_name', 'imap_server', 'smtp_server']
        for field in required_fields:
            if field not in data or not data[field]:
                return api_response(
                    success=False,
                    message=f'{field} 字段不能为空'
                )
        
        # 检查厂商名称是否已存在
        existing_provider = EmailProvider.find_by_name(data['name'])
        if existing_provider:
            return api_response(
                success=False,
                message='该厂商名称已存在'
            )
        
        # 创建新的邮箱厂商
        provider = EmailProvider(
            name=data['name'],
            display_name=data['display_name'],
            imap_server=data['imap_server'],
            imap_port=data.get('imap_port', 993),
            imap_ssl=data.get('imap_ssl', True),
            smtp_server=data['smtp_server'],
            smtp_port=data.get('smtp_port', 587),
            smtp_tls=data.get('smtp_tls', True),
            smtp_ssl=data.get('smtp_ssl', False),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(provider)
        db.session.commit()
        
        return api_response(
            success=True,
            message='邮箱厂商创建成功',
            data=provider.to_dict()
        )
        
    except Exception as e:
        db.session.rollback()
        return api_response(
            success=False,
            message=f'服务器错误: {str(e)}'
        )


@email_bp.route('/bindings/validate', methods=['POST'])
@token_required
def validate_email_binding(current_user):
    """验证邮箱绑定"""
    try:
        data = request.get_json()
        if not data:
            return api_response(
                success=False,
                message='请求数据不能为空'
            )
        
        # 验证必填字段
        required_fields = ['email', 'auth_code', 'provider_id']
        for field in required_fields:
            if field not in data or not data[field]:
                return api_response(
                    success=False,
                    message=f'{field} 字段不能为空'
                )
        
        email = data['email'].strip().lower()
        auth_code = data['auth_code'].strip()
        provider_id = data['provider_id']
        
        # 获取邮箱厂商信息
        provider = EmailProvider.query.filter(
            EmailProvider.id == provider_id,
            EmailProvider.is_deleted == False,
            EmailProvider.is_active == True
        ).first()
        
        if not provider:
            return api_response(
                success=False,
                message='邮箱厂商不存在或已禁用'
            )
        
        # 验证邮箱绑定
        validation_result = EmailBindingService.validate_email_binding(email, auth_code, provider)
        
        return api_response(
            success=validation_result['success'],
            message=validation_result['message'],
            data=validation_result['details']
        )
        
    except Exception as e:
        return api_response(
            success=False,
            message=f'服务器错误: {str(e)}'
        )


@email_bp.route('/bindings', methods=['POST'])
@token_required
def create_email_binding(current_user):
    """创建邮箱绑定"""
    try:
        data = request.get_json()
        if not data:
            return api_response(
                success=False,
                message='请求数据不能为空'
            )
        
        # 验证必填字段
        required_fields = ['email', 'auth_code', 'provider_id']
        for field in required_fields:
            if field not in data or not data[field]:
                return api_response(
                    success=False,
                    message=f'{field} 字段不能为空'
                )
        
        email = data['email'].strip().lower()
        auth_code = data['auth_code'].strip()
        provider_id = data['provider_id']
        
        # 获取邮箱厂商信息
        provider = EmailProvider.query.filter(
            EmailProvider.id == provider_id,
            EmailProvider.is_deleted == False,
            EmailProvider.is_active == True
        ).first()
        
        if not provider:
            return api_response(
                success=False,
                message='邮箱厂商不存在或已禁用'
            )
        
        # 先验证邮箱绑定
        validation_result = EmailBindingService.validate_email_binding(email, auth_code, provider)
        
        if not validation_result['success']:
            return api_response(
                success=False,
                message=validation_result['message'],
                data=validation_result['details']
            )
        
        # 从验证结果中获取UID
        latest_uid = validation_result['details'].get('latest_uid')
        
        # 创建绑定记录
        success, message, binding = EmailBindingService.create_email_binding(
            current_user.id, provider_id, email, auth_code, latest_uid
        )
        
        if success:
            return api_response(
                success=True,
                message=message,
                data=binding.to_dict() if binding else None
            )
        else:
            return api_response(
                success=False,
                message=message
            )
        
    except Exception as e:
        return api_response(
            success=False,
            message=f'服务器错误: {str(e)}'
        )


@email_bp.route('/bindings', methods=['GET'])
@token_required
def get_user_email_bindings(current_user):
    """获取用户的邮箱绑定列表"""
    try:
        bindings = EmailBindingService.get_user_bindings(current_user.id)
        
        bindings_data = [binding.to_dict() for binding in bindings]
        
        return api_response(
            success=True,
            message='获取邮箱绑定列表成功',
            data={
                'bindings': bindings_data,
                'total': len(bindings_data)
            }
        )
        
    except Exception as e:
        return api_response(
            success=False,
            message=f'服务器错误: {str(e)}'
        )


@email_bp.route('/bindings/<int:binding_id>', methods=['DELETE'])
@token_required
def delete_email_binding(current_user, binding_id):
    """删除邮箱绑定"""
    try:
        success, message = EmailBindingService.delete_email_binding(current_user.id, binding_id)
        
        return api_response(
            success=success,
            message=message
        )
        
    except Exception as e:
        return api_response(
            success=False,
            message=f'服务器错误: {str(e)}'
        )


@email_bp.route('/bindings/<int:binding_id>/status', methods=['PUT'])
@token_required
def update_email_binding_status(current_user, binding_id):
    """更新邮箱绑定状态"""
    try:
        data = request.get_json()
        if not data or 'is_active' not in data:
            return api_response(
                success=False,
                message='请求数据不能为空或缺少is_active字段'
            )
        
        # 查找绑定记录
        binding = UserEmailBinding.query.filter(
            UserEmailBinding.id == binding_id,
            UserEmailBinding.user_id == current_user.id,
            UserEmailBinding.is_deleted == False
        ).first()
        
        if not binding:
            return api_response(
                success=False,
                message='绑定记录不存在'
            )
        
        # 更新状态
        binding.is_active = bool(data['is_active'])
        db.session.commit()
        
        return api_response(
            success=True,
            message='状态更新成功',
            data=binding.to_dict()
        )
        
    except Exception as e:
        db.session.rollback()
        return api_response(
            success=False,
            message=f'服务器错误: {str(e)}'
        )


@email_bp.route('/providers/<int:provider_id>', methods=['PUT'])
@token_required
def update_email_provider(current_user, provider_id):
    """更新邮箱厂商（管理员功能）"""
    try:
        provider = EmailProvider.query.filter(
            EmailProvider.id == provider_id,
            EmailProvider.is_deleted == False
        ).first()
        
        if not provider:
            return api_response(
                success=False,
                message='邮箱厂商不存在'
            )
        
        data = request.get_json()
        if not data:
            return api_response(
                success=False,
                message='请求数据不能为空'
            )
        
        # 更新字段
        updatable_fields = [
            'display_name', 'imap_server', 'imap_port', 'imap_ssl',
            'smtp_server', 'smtp_port', 'smtp_tls', 'smtp_ssl', 'is_active'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(provider, field, data[field])
        
        db.session.commit()
        
        return api_response(
            success=True,
            message='邮箱厂商更新成功',
            data=provider.to_dict()
        )
        
    except Exception as e:
        db.session.rollback()
        return api_response(
            success=False,
            message=f'服务器错误: {str(e)}'
        )


@email_bp.route('/providers/<int:provider_id>', methods=['DELETE'])
@token_required
def delete_email_provider(current_user, provider_id):
    """删除邮箱厂商（软删除，管理员功能）"""
    try:
        provider = EmailProvider.query.filter(
            EmailProvider.id == provider_id,
            EmailProvider.is_deleted == False
        ).first()
        
        if not provider:
            return api_response(
                success=False,
                message='邮箱厂商不存在'
            )
        
        provider.soft_delete()
        db.session.commit()
        
        return api_response(
            success=True,
            message='邮箱厂商删除成功'
        )
        
    except Exception as e:
        db.session.rollback()
        return api_response(
            success=False,
            message=f'服务器错误: {str(e)}'
        )