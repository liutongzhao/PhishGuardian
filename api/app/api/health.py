from flask import Blueprint, jsonify
from app.utils import api_response

# 创建健康检查蓝图
health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return api_response(
        success=True,
        message='服务运行正常',
        data={
            'status': 'healthy',
            'service': 'PhishGuardian API',
            'version': '1.0.0'
        }
    )


@health_bp.route('/ping', methods=['GET'])
def ping():
    """简单的ping接口"""
    return jsonify({'message': 'pong'})