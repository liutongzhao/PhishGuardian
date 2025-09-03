from flask import jsonify
from typing import Any


def api_response(success: bool, message: str, data: Any = None) -> tuple:
    """统一API响应函数
    
    Args:
        success: 是否成功
        message: 响应消息
        data: 响应数据
        
    Returns:
        tuple: (响应JSON, 状态码)
    """
    response = {
        'success': success,
        'message': message,
        'data': data
    }
    
    return jsonify(response)