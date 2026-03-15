# 医院CMS系统启动指南

## 项目概述
这是一个多站点医院内容管理系统，包含前端（Vue 3 + Element Plus）和后端（FastAPI + SQLAlchemy）。

## 环境要求
- Python 3.13+
- Node.js 18+
- MySQL 8.0+
- 数据库名称：`petct_manage_db`
- 数据库用户名：`root`
- 数据库密码：`root`

## 后端启动

### 1. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置数据库
数据库连接已配置在 `backend/.env` 文件中：
```
DATABASE_URL=mysql+aiomysql://root:root@localhost:3306/petct_manage_db
```

### 3. 初始化数据库
```bash
python init_db.py
```
这将创建超级管理员账号：`admin / admin123`

### 4. 创建测试数据
```bash
python create_test_data.py
```
这将创建测试站点：`petct.com`

### 5. 启动后端服务
```bash
python start.py
```
后端服务将在 `http://localhost:8000` 启动

### 6. 访问API文档
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 前端启动

### 1. 安装依赖
```bash
cd frontend
npm install
```

### 2. 启动开发服务器
```bash
npm run dev
```
前端服务将在 `http://localhost:5173` 启动

### 3. 访问系统
- 登录页面：`http://localhost:5173/login`
- 默认账号：`admin`
- 默认密码：`admin123`

## 已修复的问题

### 1. 域名中间件问题
**问题**：域名中间件对所有请求都进行域名验证，包括根路径和API文档路径
**修复**：在 `backend/app/middleware/domain_middleware.py` 中添加了白名单路径：
- `/`
- `/docs`
- `/redoc`
- `/openapi.json`
- `/api/v1/auth/login`

### 2. 登录接口格式问题
**问题**：后端登录接口使用 `OAuth2PasswordRequestForm`，期望 `application/x-www-form-urlencoded` 格式，但前端发送的是JSON格式
**修复**：
- 在 `frontend/src/utils/request.js` 中创建了专门的 `loginRequest` 实例
- 在 `frontend/src/views/Login.vue` 中使用 `URLSearchParams` 构建表单数据

### 3. 数据库连接和依赖
**问题**：缺少必要的Python依赖包
**修复**：
- 安装了 `aiomysql` 和 `python-slugify`
- 更新了 `requirements.txt`，移除了版本锁定以兼容Python 3.13

## API端点

### 认证相关
- `POST /api/v1/auth/login` - 用户登录

### 站点管理
- `GET /api/v1/sites/` - 获取所有站点
- `POST /api/v1/sites/` - 创建站点
- `GET /api/v1/sites/{site_id}` - 获取站点详情
- `PUT /api/v1/sites/{site_id}` - 更新站点
- `DELETE /api/v1/sites/{site_id}` - 删除站点

### 医院管理
- `GET /api/v1/hospitals/` - 获取医院列表（需要域名header）
- `POST /api/v1/hospitals/` - 创建医院
- `GET /api/v1/hospitals/{hospital_id}` - 获取医院详情
- `PUT /api/v1/hospitals/{hospital_id}` - 更新医院
- `DELETE /api/v1/hospitals/{hospital_id}` - 删除医院

### 文章管理
- `GET /api/v1/articles/` - 获取文章列表
- `POST /api/v1/articles/` - 创建文章
- `GET /api/v1/articles/{article_id}` - 获取文章详情
- `PUT /api/v1/articles/{article_id}` - 更新文章
- `DELETE /api/v1/articles/{article_id}` - 删除文章

### 预约管理
- `GET /api/v1/appointments/` - 获取预约列表
- `POST /api/v1/appointments/` - 创建预约
- `GET /api/v1/appointments/{appointment_id}` - 获取预约详情
- `PUT /api/v1/appointments/{appointment_id}` - 更新预约
- `DELETE /api/v1/appointments/{appointment_id}` - 删除预约

### 标签管理
- `GET /api/v1/tags/` - 获取所有标签
- `POST /api/v1/tags/` - 创建标签

## 项目结构

### 后端结构
```
backend/
├── app/
│   ├── api/
│   │   ├── routes/          # API路由
│   │   └── deps.py          # 依赖注入
│   ├── core/
│   │   └── security.py      # 安全相关（密码加密、JWT）
│   ├── db/
│   │   ├── base.py          # 数据库基类
│   │   └── session.py       # 数据库会话
│   ├── middleware/
│   │   └── domain_middleware.py  # 域名中间件
│   ├── models/              # 数据模型
│   ├── schemas/             # Pydantic模式
│   ├── services/            # 业务逻辑
│   └── main.py              # FastAPI应用入口
├── .env                     # 环境变量
├── init_db.py              # 数据库初始化脚本
├── create_test_data.py     # 创建测试数据
├── start.py                # 启动脚本
└── requirements.txt        # Python依赖
```

### 前端结构
```
frontend/
├── src/
│   ├── views/              # 页面组件
│   ├── components/         # 通用组件
│   ├── stores/             # Pinia状态管理
│   ├── router/             # Vue Router配置
│   ├── utils/              # 工具函数
│   ├── App.vue             # 根组件
│   └── main.js             # 入口文件
├── public/                 # 静态资源
├── vite.config.js          # Vite配置
└── package.json            # Node.js依赖
```

## 注意事项

1. **多站点架构**：系统使用域名隔离数据，每个请求需要包含正确的 `Host` header
2. **认证**：大部分API需要JWT token认证，登录后token会存储在localStorage中
3. **数据库**：确保MySQL服务正在运行，并且数据库 `petct_manage_db` 已创建
4. **端口冲突**：如果8000或5173端口被占用，需要修改相应的配置文件

## 故障排除

### 后端无法启动
- 检查MySQL服务是否运行
- 检查数据库连接配置是否正确
- 检查Python依赖是否安装完整

### 前端无法连接后端
- 检查后端服务是否在 `http://localhost:8000` 运行
- 检查 `frontend/vite.config.js` 中的代理配置
- 检查浏览器控制台的错误信息

### 登录失败
- 确认数据库中存在admin用户
- 确认密码是 `admin123`
- 检查网络连接和后端服务状态