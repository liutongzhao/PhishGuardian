from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config.config import config
from app.utils.jwt_utils import JWTUtils
import os

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name=None):
    """应用工厂函数"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    
    # 初始化JWT
    JWTUtils.init_app(app)
    
    # 配置CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://localhost:5173", "http://localhost:5174"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # 注册蓝图
    from app.api import blueprints
    from app.api.health import health_bp
    from app.api.auth import auth_bp
    
    # 注册健康检查蓝图
    app.register_blueprint(health_bp, url_prefix='/api')
    
    # 注册认证蓝图
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app


# 模型导入区域
from app.models import User, RegistrationType