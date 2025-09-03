# PhishGuardian API - 干净服务器版本

PhishGuardian API 的简化版本，提供一个干净的Flask服务器基础架构，移除了所有业务相关功能，只保留核心框架和工具类。

## 当前功能

- ✅ **基础Flask应用** - 完整的Flask应用工厂模式
- ✅ **健康检查API** - 基础的健康检查和ping接口
- ✅ **工具类库** - 数据验证、响应格式化、数据库工具
- ✅ **配置管理** - 多环境配置支持
- ✅ **数据库支持** - SQLAlchemy ORM集成
- ✅ **CORS支持** - 跨域请求处理

## 已移除的功能

- ❌ 用户认证系统 (JWT, 登录注册)
- ❌ 邮件相关功能 (邮箱管理, 邮件分析)
- ❌ 业务数据模型 (User, EmailAccount, EmailMessage)
- ❌ Redis缓存
- ❌ 邮件处理工具

## 技术栈

- **框架**: Flask 2.3.3
- **数据库**: MySQL (通过SQLAlchemy ORM)
- **API文档**: Swagger (Flasgger)
- **工具**: 数据验证、响应格式化、数据库操作

## 项目结构

```
api/
├── app/                    # 应用主目录
│   ├── __init__.py        # Flask应用工厂
│   ├── api/               # API蓝图
│   │   ├── __init__.py    # 蓝图管理
│   │   └── health.py      # 健康检查API
│   ├── models/            # 数据模型 (当前为空)
│   │   └── __init__.py    # 模型管理
│   ├── utils/             # 工具类
│   │   ├── validators.py  # 数据验证
│   │   ├── response.py    # 响应格式化
│   │   └── database.py    # 数据库工具
│   └── services/          # 业务服务层 (当前为空)
├── config/                # 配置文件
│   └── config.py         # 应用配置
├── migrations/            # 数据库迁移文件
├── tests/                 # 测试文件
├── .env.example          # 环境变量模板
├── requirements.txt      # Python依赖 (已简化)
├── start.py             # 管理命令脚本
└── README.md            # 项目说明
```

## 快速开始

### 1. 环境准备

- Python 3.8+
- MySQL 5.7+

### 2. 项目克隆

```bash
git clone <repository-url>
cd PhishGuardian/api
```

### 3. 安装依赖

```bash
# 使用管理脚本安装
python start.py install

# 或手动安装
pip install -r requirements.txt
```

### 4. 环境变量配置

复制 `.env.example` 为 `.env` 并配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/phishguardian

# Flask配置
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

### 5. 数据库初始化

```bash
# 初始化数据库
python start.py init-db

# 查看数据库状态
python start.py db-status
```

### 6. 启动服务

```bash
# 开发环境启动
python start.py run

# 指定端口和主机
python start.py run --host 0.0.0.0 --port 8000

# 生产环境启动
python start.py gunicorn --env production
```

## API接口

### 健康检查

```bash
# 健康检查
GET /api/v1/health

# 简单ping
GET /api/v1/ping
```

响应示例：

```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "service": "PhishGuardian API",
    "version": "1.0.0"
  },
  "message": "服务运行正常"
}
```

## 管理命令

```bash
# 查看所有可用命令
python start.py --help

# 启动开发服务器
python start.py run

# 数据库管理
python start.py init-db      # 初始化数据库
python start.py drop-db      # 删除数据库
python start.py reset-db     # 重置数据库
python start.py db-status    # 查看数据库状态

# 生产环境
python start.py gunicorn     # 使用Gunicorn启动

# 开发工具
python start.py shell        # 启动Flask Shell
python start.py install      # 安装依赖
python start.py test         # 运行测试
```

## 配置说明

支持多环境配置：

- `development` - 开发环境（默认）
- `production` - 生产环境
- `testing` - 测试环境

## 扩展开发

这个干净的服务器为后续开发提供了良好的基础：

1. **添加新的API** - 在 `app/api/` 目录下创建新的蓝图文件
2. **添加数据模型** - 在 `app/models/` 目录下创建模型文件
3. **添加业务服务** - 在 `app/services/` 目录下创建服务文件
4. **使用工具类** - 利用现有的验证、响应、数据库工具类

## 开发指南

### 代码规范

- 使用 Black 进行代码格式化
- 使用 Flake8 进行代码检查
- 遵循 PEP 8 编码规范

### 测试

```bash
# 运行测试
python start.py test

# 或使用pytest
pytest tests/
```

## 部署

### 生产环境部署

```bash
# 使用Gunicorn
python start.py gunicorn --env production --workers 4 --bind 0.0.0.0:5000
```

### Docker部署

可以根据需要创建Dockerfile进行容器化部署。

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查数据库服务是否启动
   - 验证 `.env` 文件中的数据库配置

2. **端口被占用**
   - 使用 `--port` 参数指定其他端口

3. **依赖安装失败**
   - 确保Python版本 >= 3.8
   - 使用虚拟环境

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交Issue或Pull Request。