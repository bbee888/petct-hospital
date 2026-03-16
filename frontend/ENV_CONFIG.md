# 环境变量配置说明

## 概述

前端项目使用环境变量来管理不同环境下的配置,避免硬编码,方便统一修改和部署。

## 环境文件说明

### 1. `.env.development` - 开发环境
用于本地开发,默认配置:
```bash
VITE_API_BASE_URL=http://localhost:8001
VITE_APP_PORT=8080
```

### 2. `.env.production` - 生产环境
用于生产部署,需要修改为实际生产环境地址:
```bash
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_APP_PORT=8080
```

### 3. `.env.local` - 本地覆盖(可选)
用于临时覆盖开发环境配置,不会被git提交:
```bash
# 示例: 连接到测试服务器
VITE_API_BASE_URL=http://test-server:8001
```

### 4. `.env.example` - 配置示例
包含所有可用的环境变量说明,供参考使用。

## 环境变量优先级

Vite按以下顺序加载环境变量(后面的覆盖前面的):

1. `.env` - 所有环境的基础配置
2. `.env.local` - 本地覆盖(被gitignore)
3. `.env.[mode]` - 特定环境配置(如development, production)
4. `.env.[mode].local` - 特定环境的本地覆盖

**示例**: 开发模式下的优先级:
```
.env -> .env.local -> .env.development -> .env.development.local
```

## 使用方法

### 修改API地址

#### 开发环境
编辑 `.env.development` 文件:
```bash
VITE_API_BASE_URL=http://your-backend-url:port
```

#### 生产环境
编辑 `.env.production` 文件:
```bash
VITE_API_BASE_URL=https://your-production-api.com
```

### 代码中使用环境变量

在JavaScript/Vue代码中访问环境变量:

```javascript
// Vite自动处理: 使用 import.meta.env 访问
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL
```

**重要**:
- ✅ 必须以 `VITE_` 开头才能在客户端代码中访问
- ❌ 不带 `VITE_` 前缀的环境变量只能在构建时使用

### 在request.js中的使用

```javascript
// src/utils/request.js
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8001'

const request = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  // ...
})
```

## 常见场景

### 场景1: 后端地址变更
只需修改对应环境文件中的 `VITE_API_BASE_URL`,无需修改代码。

### 场景2: 连接到远程开发服务器
创建 `.env.local` 文件:
```bash
VITE_API_BASE_URL=http://remote-server:8001
```

### 场景3: 多个开发环境
可以为不同的开发人员创建不同的 `.env.local`:
```bash
# 开发者A
VITE_API_BASE_URL=http://dev-a:8001

# 开发者B
VITE_API_BASE_URL=http://dev-b:8001
```

### 场景4: 生产部署前测试
修改 `.env.development` 临时指向测试服务器:
```bash
VITE_API_BASE_URL=http://staging-api.yourdomain.com
```

## 构建说明

### 开发构建
```bash
npm run dev
# 使用 .env.development 配置
```

### 生产构建
```bash
npm run build
# 使用 .env.production 配置
```

构建后,环境变量的值会被静态注入到构建产物中,无法运行时修改。

## 安全注意事项

### ⚠️ 不要在环境变量中存储敏感信息
- ✅ 可以存储: API地址、配置参数
- ❌ 不要存储: 密码、密钥、Token

### .gitignore 配置
确保以下文件不被提交:
```
.env.local
.env.*.local
.env
```

### 生产环境敏感信息
生产环境的密钥等敏感信息应该:
- 使用服务器端环境变量
- 通过CI/CD管道传递
- 不打包到前端代码中

## 环境变量列表

| 变量名 | 说明 | 开发环境默认值 | 必填 |
|--------|------|---------------|------|
| `VITE_API_BASE_URL` | 后端API地址(不含/api) | http://localhost:8001 | 是 |
| `VITE_APP_PORT` | 前端应用端口 | 8080 | 否 |

## 故障排除

### 问题1: 环境变量不生效
**解决**:
1. 检查变量名是否以 `VITE_` 开头
2. 确认文件名格式正确(如 `.env.development`)
3. 重启开发服务器
4. 清除浏览器缓存

### 问题2: 生产构建后API地址错误
**解决**:
1. 确认 `.env.production` 配置正确
2. 重新构建: `npm run build`
3. 检查构建产物中的配置

### 问题3: 开发和生产环境混乱
**解决**:
1. 确认当前运行模式: `npm run dev` 或 `npm run build`
2. 检查对应的环境文件
3. 查看 `import.meta.env.MODE` 确认当前模式

## 最佳实践

1. **始终使用环境变量**: 避免在代码中硬编码配置
2. **使用示例文件**: 通过 `.env.example` 说明可用配置
3. **本地配置隔离**: 使用 `.env.local` 存储个人配置
4. **文档化配置**: 记录每个环境变量的用途
5. **版本控制**: 将 `.env.example` 和 `.env.development` 提交到git
6. **敏感信息保护**: 密钥等通过服务器环境变量或CI/CD传递

## 相关文档

- [Vite环境变量](https://vitejs.dev/guide/env-and-mode.html)
- [Vue CLI环境变量](https://cli.vuejs.org/guide/mode-and-env.html)
- [.gitignore配置](https://git-scm.com/docs/gitignore)

## 更新日志

### 2024-03-16
- ✅ 统一使用环境变量管理API地址
- ✅ 更新request.js使用import.meta.env
- ✅ 添加详细的环境变量说明文档
- ✅ 配置开发、生产环境文件
