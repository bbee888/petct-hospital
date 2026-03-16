# 医院 CMS 系统

多站点医院内容管理系统

## 项目启动说明

### 前置要求
- Python 3.10+
- Node.js 16+
- MySQL 8.0+

### 数据库配置
确保MySQL已启动并创建了数据库：
- 数据库名：petct_manage_db
- 用户名：root
- 密码：123456

### 后端启动

1. 进入后端目录：
```bash
cd backend
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 初始化数据库（创建表和管理员账号）：
```bash
python init_db.py
```

4. 启动后端服务：
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端API地址：http://localhost:8000
API文档：http://localhost:8000/docs

默认管理员账号：
- 用户名：admin
- 密码：admin123

### 前端启动

1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
```

3. 配置环境变量(可选):
```bash
# 开发环境配置已默认设置,如需修改后端地址请编辑:
# frontend/.env.development
```

环境变量说明:
- `VITE_API_BASE_URL`: 后端API地址(不含/api路径),默认 `http://localhost:8001`
- `VITE_APP_PORT`: 前端应用端口,默认 `8080`

详细配置说明请参考: [frontend/ENV_CONFIG.md](frontend/ENV_CONFIG.md)

4. 启动前端开发服务器：
```bash
npm run dev
```

前端地址：http://localhost:8080

### 项目结构

```
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── middleware/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── init_db.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── layouts/
│   │   ├── router/
│   │   ├── stores/
│   │   ├── utils/
│   │   └── views/
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
└── petct.sql
```

### 技术栈

**后端：**
- FastAPI
- SQLAlchemy (Async)
- Pydantic V2
- Uvicorn
- MySQL (aiomysql)

**前端：**
- Vue 3 (Composition API)
- JavaScript
- Element Plus
- Pinia
- Vue Router
- Vite
- UnoCSS
