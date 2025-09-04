from flask import Blueprint, request, jsonify
from app.utils import api_response
from app.models.email_provider import EmailProvider
from app.models.user_email_binding import UserEmailBinding
from app.services.email_binding_service import EmailBindingService
from app.utils.jwt_utils import token_required
from app import db

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
        
        # 创建绑定记录
        success, message, binding = EmailBindingService.create_email_binding(
            current_user.id, provider_id, email, auth_code
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