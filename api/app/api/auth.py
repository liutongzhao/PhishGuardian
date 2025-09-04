from flask import Blueprint, request, jsonify
from app.utils import api_response, validate_email, validate_password, validate_username
from app.models.user import User, RegistrationType
from app.utils.jwt_utils import JWTUtils, token_required
from app import db
import re
from datetime import datetime, timedelta
import pytz
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# 创建认证蓝图
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/check-username', methods=['POST'])
def check_username():
    """检查用户名是否可用"""
    try:
        data = request.get_json()
        if not data or 'username' not in data:
            return api_response(
                success=False,
                message='用户名不能为空'
            )
        
        username = data['username'].strip()
        
        # 验证用户名格式
        validation_result = validate_username(username)
        if not validation_result['valid']:
            return api_response(
                success=True,
                message=validation_result['message'],
                data={'available': False, 'reason': 'format_error'}
            )
        
        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=username, is_deleted=False).first()
        if existing_user:
            return api_response(
                success=True,
                message='用户名已被使用',
                data={'available': False, 'reason': 'already_exists'}
            )
        
        return api_response(
            success=True,
            message='用户名可用',
            data={'available': True, 'reason': 'valid'}
        )
        
    except Exception as e:
        return api_response(
            success=False,
            message=f'服务器错误: {str(e)}'
        )


@auth_bp.route('/send-verification-code', methods=['POST'])
def send_verification_code():
    """发送邮箱验证码"""
    try:
        data = request.get_json()
        if not data or 'email' not in data:
            return api_response(
                success=False,
                message='邮箱不能为空'
            )
        
        email = data['email'].strip().lower()
        
        # 验证邮箱格式
        if not validate_email(email):
            return api_response(
                success=False,
                message='邮箱格式不正确'
            )
        
        # 检查邮箱是否已被激活的用户使用
        existing_user = User.query.filter_by(email=email, is_deleted=False, is_activated=True).first()
        if existing_user:
            return api_response(
                success=False,
                message='该邮箱已被注册'
            )
        
        # 查找或创建未激活的用户记录
        user = User.query.filter_by(email=email, is_deleted=False, is_activated=False).first()
        if not user:
            # 创建新的未激活用户记录
            user = User(
                username='',  # 临时为空，注册时填写
                email=email,
                github='',  # 临时为空
                wechat='',  # 临时为空
                registration_method=RegistrationType.EMAIL,
                is_activated=False
            )
            db.session.add(user)
        
        # 生成验证码
        verification_code = user.generate_verification_code()
        
        # 发送邮件
        try:
            send_email_verification_code(email, verification_code)
        except Exception as e:
            print(f"邮件发送错误详情: {str(e)}")  # 添加调试日志
            return api_response(
                success=False,
                message=f'发送邮件失败: {str(e)}'
            )
        
        # 保存到数据库
        db.session.commit()
        
        return api_response(
            success=True,
            message='验证码已发送到您的邮箱，请查收',
            data={'expires_in': 600}  # 10分钟有效期
        )
        
    except Exception as e:
        db.session.rollback()
        return api_response(
            success=False,
            message=f'服务器错误: {str(e)}'
        )


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.get_json()
        required_fields = ['username', 'password', 'email', 'verification_code']
        
        # 检查必填字段
        for field in required_fields:
            if not data or field not in data or not data[field]:
                return api_response(
                    success=False,
                    message=f'{field} 不能为空'
                )
        
        username = data['username'].strip()
        password = data['password']
        email = data['email'].strip().lower()
        verification_code = data['verification_code'].strip()
        
        # 验证用户名
        username_validation = validate_username(username)
        if not username_validation['valid']:
            return api_response(
                success=False,
                message=username_validation['message']
            )
        
        # 验证密码（修改为6-20位，必须包含字母和数字）
        if not validate_password_format(password):
            return api_response(
                success=False,
                message='密码必须为6-20位，且包含字母和数字'
            )
        
        # 验证邮箱格式
        if not validate_email(email):
            return api_response(
                success=False,
                message='邮箱格式不正确'
            )
        
        # 检查用户名是否已被使用
        existing_username = User.query.filter_by(username=username, is_deleted=False).first()
        if existing_username:
            return api_response(
                success=False,
                message='用户名已被使用'
            )
        
        # 检查邮箱是否已被激活用户使用
        existing_email = User.query.filter_by(email=email, is_deleted=False, is_activated=True).first()
        if existing_email:
            return api_response(
                success=False,
                message='该邮箱已被注册'
            )
        
        # 查找未激活的用户记录
        user = User.query.filter_by(email=email, is_deleted=False, is_activated=False).first()
        if not user:
            return api_response(
                success=False,
                message='请先获取验证码'
            )
        
        # 验证验证码
        if not user.is_verification_code_valid(verification_code):
            return api_response(
                success=False,
                message='验证码无效或已过期'
            )
        
        # 更新用户信息并激活
        user.username = username
        user.set_password(password)
        user.activate()
        user.verification_code = None  # 清除验证码
        user.verification_code_expires = None
        
        db.session.commit()
        
        return api_response(
            success=True,
            message='注册成功',
            data={
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            }
        )
        
    except Exception as e:
        db.session.rollback()
        return api_response(
            success=False,
            message=f'服务器错误: {str(e)}'
        )


def validate_password_format(password):
    """验证密码格式（6-20位，包含字母和数字）"""
    if not password or len(password) < 6 or len(password) > 20:
        return False
    
    # 必须包含字母
    has_letter = bool(re.search(r'[a-zA-Z]', password))
    # 必须包含数字
    has_digit = bool(re.search(r'\d', password))
    
    return has_letter and has_digit


def send_email_verification_code(email, code):
    """发送邮箱验证码"""
    # 邮件配置（需要在环境变量中设置）
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.163.com')
    smtp_port = int(os.getenv('SMTP_PORT', '25'))  # 网易邮箱使用25端口
    smtp_username = os.getenv('SMTP_USERNAME', '15209828080@163.com')
    smtp_password = os.getenv('SMTP_PASSWORD')  # 网易邮箱授权码
    
    print(f"邮件配置: server={smtp_server}, port={smtp_port}, username={smtp_username}, password={'***' if smtp_password else 'None'}")
    
    if not smtp_username or not smtp_password:
        raise Exception('邮件服务配置不完整')
    
    # 创建邮件内容
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = email
    msg['Subject'] = 'PhishGuard 注册验证码'
    
    body = f"""
    您好！
    
    您正在注册 PhishGuard 账户，验证码为：{code}
    
    验证码有效期为10分钟，请及时使用。
    
    如果这不是您的操作，请忽略此邮件。
    
    PhishGuard 团队
    """
    
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # 发送邮件
    try:
        print(f"正在连接SMTP服务器: {smtp_server}:{smtp_port}")
        server = smtplib.SMTP(smtp_server, smtp_port)
        print("SMTP连接成功，开始TLS加密")
        server.starttls()
        print("TLS加密成功，开始登录")
        server.login(smtp_username, smtp_password)
        print("登录成功，开始发送邮件")
        text = msg.as_string()
        server.sendmail(smtp_username, email, text)
        print("邮件发送成功")
        server.quit()
    except Exception as e:
        print(f"邮件发送详细错误: {str(e)}")
        raise Exception(f'邮件发送失败: {str(e)}')


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        if not data:
            return api_response(
                success=False,
                message='请求数据不能为空'
            )
        
        # 获取登录凭据（用户名或邮箱）和密码
        credential = data.get('username', '').strip()  # 可以是用户名或邮箱
        password = data.get('password', '')
        
        if not credential or not password:
            return api_response(
                success=False,
                message='用户名/邮箱和密码不能为空'
            )
        
        # 验证密码格式
        if not validate_password_format(password):
            return api_response(
                success=False,
                message='密码格式不正确'
            )
        
        # 查找用户（通过用户名或邮箱）
        user = None
        if '@' in credential:
            # 如果包含@符号，按邮箱查找
            if not validate_email(credential.lower()):
                return api_response(
                    success=False,
                    message='邮箱格式不正确'
                )
            user = User.query.filter_by(
                email=credential.lower(),
                is_deleted=False,
                is_activated=True
            ).first()
        else:
            # 否则按用户名查找
            user = User.query.filter_by(
                username=credential,
                is_deleted=False,
                is_activated=True
            ).first()
        
        # 验证用户存在性和密码
        if not user or not user.check_password(password):
            return api_response(
                success=False,
                message='用户名/邮箱或密码错误'
            )
        
        # 生成JWT token
        token_data = JWTUtils.generate_token(user)
        
        # 更新最后登录时间
        user.last_login = datetime.now(pytz.timezone('Asia/Shanghai'))
        db.session.commit()
        
        return api_response(
            success=True,
            message='登录成功',
            data={
                'token': token_data['token'],
                'expires_in': token_data['expires_in'],
                'user': token_data['user']
            }
        )
        
    except Exception as e:
        db.session.rollback()
        return api_response(
            success=False,
            message=f'服务器错误: {str(e)}'
        )


@auth_bp.route('/verify-token', methods=['POST'])
@token_required
def verify_token(current_user):
    """验证token有效性"""
    try:
        return api_response(
            success=True,
            message='Token有效',
            data={
                'user': {
                    'id': current_user.id,
                    'username': current_user.username,
                    'email': current_user.email
                }
            }
        )
    except Exception as e:
        return api_response(
            success=False,
            message=f'服务器错误: {str(e)}'
        )


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """用户登出"""
    try:
        # 这里可以添加token黑名单逻辑，目前简单返回成功
        return api_response(
            success=True,
            message='登出成功'
        )
    except Exception as e:
        return api_response(
            success=False,
            message=f'服务器错误: {str(e)}'
        )