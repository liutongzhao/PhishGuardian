#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PhishGuardian API 启动脚本
提供开发、生产、测试等不同环境的启动选项
"""

import os
import sys
import click
from flask.cli import with_appcontext
from app import create_app, db
# 模型导入区域 - 当前无模型需要导入
from config.config import DevelopmentConfig, ProductionConfig, TestingConfig

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def get_config_class(env):
    """根据环境名称获取配置类"""
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    return config_map.get(env.lower(), DevelopmentConfig)


@click.group()
def cli():
    """PhishGuardian API 管理命令"""
    pass


@cli.command()
@click.option('--env', '-e', default='development', 
              type=click.Choice(['development', 'production', 'testing']),
              help='运行环境 (development/production/testing)')
@click.option('--host', '-h', default='127.0.0.1', help='绑定主机地址')
@click.option('--port', '-p', default=5000, type=int, help='端口号')
@click.option('--debug', '-d', is_flag=True, help='启用调试模式')
def run(env, host, port, debug):
    """启动Flask应用"""
    # 设置环境变量
    os.environ['FLASK_ENV'] = env
    
    # 创建应用
    app = create_app(env)
    
    # 启动应用
    click.echo(f'启动PhishGuardian API服务...')
    click.echo(f'环境: {env}')
    click.echo(f'地址: http://{host}:{port}')
    click.echo(f'调试模式: {debug or env == "development"}')
    
    # 使用Flask运行
    app.run(
        host=host,
        port=port,
        debug=debug or env == 'development'
    )


@cli.command()
@click.option('--env', '-e', default='development',
              type=click.Choice(['development', 'production', 'testing']),
              help='运行环境')
def init_db(env):
    """初始化数据库"""
    os.environ['FLASK_ENV'] = env
    app = create_app(env)
    
    with app.app_context():
        click.echo('创建数据库表...')
        db.create_all()
        click.echo('数据库初始化完成！')


@cli.command()
@click.option('--env', '-e', default='development',
              type=click.Choice(['development', 'production', 'testing']),
              help='运行环境')
def drop_db(env):
    """删除所有数据库表"""
    if click.confirm('确定要删除所有数据库表吗？此操作不可恢复！'):
        os.environ['FLASK_ENV'] = env
        app = create_app(env)
        
        with app.app_context():
            click.echo('删除数据库表...')
            db.drop_all()
            click.echo('数据库表删除完成！')


@cli.command()
@click.option('--env', '-e', default='development',
              type=click.Choice(['development', 'production', 'testing']),
              help='运行环境')
def reset_db(env):
    """重置数据库（删除后重新创建）"""
    if click.confirm('确定要重置数据库吗？所有数据将丢失！'):
        os.environ['FLASK_ENV'] = env
        app = create_app(env)
        
        with app.app_context():
            click.echo('删除现有数据库表...')
            db.drop_all()
            click.echo('创建新的数据库表...')
            db.create_all()
            click.echo('数据库重置完成！')


# create_admin命令已移除，因为没有用户模型


@cli.command()
@click.option('--env', '-e', default='development',
              type=click.Choice(['development', 'production', 'testing']),
              help='运行环境')
def db_status(env):
    """查看数据库状态"""
    os.environ['FLASK_ENV'] = env
    app = create_app(env)
    
    with app.app_context():
        try:
            # 检查数据库连接
            with db.engine.connect() as connection:
                connection.execute(db.text('SELECT 1'))
            click.echo('✓ 数据库连接正常')
            click.echo('\n当前为干净的服务器，无业务数据表')
            
        except Exception as e:
            click.echo(f'✗ 数据库连接失败: {str(e)}')


@cli.command()
@click.option('--env', '-e', default='development',
              type=click.Choice(['development', 'production', 'testing']),
              help='运行环境')
@click.option('--workers', '-w', default=4, type=int, help='工作进程数')
@click.option('--bind', '-b', default='127.0.0.1:5000', help='绑定地址')
def gunicorn(env, workers, bind):
    """使用Gunicorn启动生产服务器"""
    os.environ['FLASK_ENV'] = env
    
    cmd = f'gunicorn -w {workers} -b {bind} "app:create_app()"'
    click.echo(f'启动Gunicorn服务器: {cmd}')
    os.system(cmd)


@cli.command()
@click.option('--env', '-e', default='development',
              type=click.Choice(['development', 'production', 'testing']),
              help='运行环境')
def shell(env):
    """启动Flask Shell"""
    os.environ['FLASK_ENV'] = env
    config_class = get_config_class(env)
    app = create_app(config_class)
    
    with app.app_context():
        # 导入常用模块到shell环境
        import_dict = {
            'app': app,
            'db': db,
            'User': User,
            'EmailAccount': EmailAccount,
            'EmailMessage': EmailMessage
        }
        
        click.echo('PhishGuardian API Shell')
        click.echo('可用对象: app, db, User, EmailAccount, EmailMessage')
        
        # 启动IPython或普通Python shell
        try:
            from IPython import embed
            embed(user_ns=import_dict)
        except ImportError:
            import code
            code.interact(local=import_dict)


@cli.command()
def install():
    """安装项目依赖"""
    click.echo('安装Python依赖包...')
    os.system('pip install -r requirements.txt')
    click.echo('依赖安装完成！')


@cli.command()
def test():
    """运行测试"""
    click.echo('运行测试用例...')
    os.system('python -m pytest tests/ -v')


if __name__ == '__main__':
    cli()