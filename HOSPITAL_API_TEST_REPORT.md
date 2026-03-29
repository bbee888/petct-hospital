# 医院列表页 API 测试报告

## 📋 测试目标

验证医院列表页的 API 集成是否正常工作，确保前端能够正确获取和展示后端数据。

---

## 🔧 测试环境准备

### Step 1: 检查后端服务

```bash
# 进入后端目录
cd /Users/shangxb/fastapi-vue3/petct-hospital/backend

# 启动后端服务
python3 start.py
```

**预期输出**:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: 访问 API 文档

打开浏览器访问：http://localhost:8000/docs

**检查项**:
- ✅ Swagger UI 页面正常显示
- ✅ 看到 `/api/hospitals` 接口
- ✅ 可以点击 "Try it out" 测试接口

### Step 3: 启动前端服务

```bash
# 进入前端目录
cd /Users/shangxb/fastapi-vue3/petct-hospital/cnpetct

# 启动开发服务器
npm run dev
```

**预期输出**:
```
Nuxt 3.x.x with Vite 7.x.x is ready in xxx ms
➜ Local:    http://localhost:3001/
```

---

## 🧪 手动测试步骤

### 测试 1: 直接访问 API（使用 curl）

```bash
# 测试基础查询
curl "http://localhost:8000/api/hospitals?page=1&size=10"

# 测试合作医院筛选
curl "http://localhost:8000/api/hospitals?page=1&size=5&is_cooperation=1"

# 测试搜索功能
curl "http://localhost:8000/api/hospitals?page=1&size=10&title=协和"
```

**预期响应**:
```json
{
  "items": [
    {
      "id": 1,
      "name": "北京协和医院",
      "level": "三甲",
      "price": 9800,
      ...
    }
  ],
  "total": 100,
  "page": 1,
  "size": 10
}
```

**检查项**:
- ✅ 返回 JSON 格式数据
- ✅ 包含 `items`, `total`, `page`, `size` 字段
- ✅ `items` 数组中有医院数据

---

### 测试 2: 使用 Swagger UI 测试

1. 访问 http://localhost:8000/docs
2. 找到 `GET /api/hospitals` 接口
3. 点击 "Try it out"
4. 填写参数:
   - page: 1
   - size: 10
   - is_cooperation: 1
5. 点击 "Execute"
6. 查看响应

**检查项**:
- ✅ 状态码 200
- ✅ 响应数据结构正确
- ✅ 数据内容符合预期

---

### 测试 3: 前端页面测试

#### 3.1 访问医院列表页

打开浏览器访问：http://localhost:3001/hospitals

**检查项**:
- ✅ 页面正常加载
- ✅ 顶部导航栏显示"全国医院列表"
- ✅ 搜索框可见
- ✅ 筛选栏可见（地区、等级、排序）

#### 3.2 检查浏览器控制台

按 F12 打开开发者工具，查看 Console

**应该看到的日志**:
```javascript
API 响应：{
  items: [...],
  total: 100,
  page: 1,
  size: 10
}
```

**不应该看到的错误**:
- ❌ `Failed to fetch`
- ❌ `Network Error`
- ❌ `CORS policy`

#### 3.3 检查网络请求

在开发者工具的 Network 标签页:

1. 过滤 "hospitals"
2. 查看请求详情

**检查项**:
- ✅ 请求 URL: `http://localhost:8000/api/hospitals?page=1&size=10&is_cooperation=1`
- ✅ 状态码：200
- ✅ 响应大小：合理（几 KB 到几十 KB）
- ✅ 响应时间：< 500ms

---

### 测试 4: 功能交互测试

#### 4.1 滚动加载更多

1. 向下滚动页面
2. 观察是否自动加载更多
3. 或点击"加载更多"按钮

**检查项**:
- ✅ 触发加载时显示 loading 提示
- ✅ 新数据追加到列表末尾
- ✅ 页码自动递增
- ✅ 到达底部时显示"没有更多了"

#### 4.2 搜索功能

1. 在搜索框输入"协和"
2. 观察列表变化

**检查项**:
- ✅ 列表实时更新（或按回车后更新）
- ✅ 只显示名称包含"协和"的医院
- ✅ 清空搜索后恢复全部列表

#### 4.3 降级方案测试

1. 停止后端服务（Ctrl+C）
2. 刷新前端页面

**检查项**:
- ✅ 页面仍能显示医院列表（模拟数据）
- ✅ 控制台显示错误日志
- ✅ 无白屏或崩溃

---

## 📊 测试结果记录表

### API 测试结果

| 测试项 | 状态 | 说明 |
|--------|------|------|
| **后端服务启动** | ⏳ 待测试 | 需要手动执行 |
| **Swagger UI 访问** | ⏳ 待测试 | 需要手动执行 |
| **基础查询接口** | ⏳ 待测试 | GET /api/hospitals |
| **合作医院筛选** | ⏳ 待测试 | is_cooperation=1 |
| **搜索功能** | ⏳ 待测试 | title 参数 |
| **等级筛选** | ⏳ 待测试 | level 参数 |
| **分页功能** | ⏳ 待测试 | page, size 参数 |
| **CORS 跨域** | ⏳ 待测试 | 前端访问是否正常 |

### 前端测试结果

| 测试项 | 状态 | 说明 |
|--------|------|------|
| **页面加载** | ⏳ 待测试 | http://localhost:3001/hospitals |
| **API 调用** | ⏳ 待测试 | 控制台日志检查 |
| **数据展示** | ⏳ 待测试 | 医院列表渲染 |
| **图片加载** | ⏳ 待测试 | 医院图片显示 |
| **滚动加载** | ⏳ 待测试 | 分页功能 |
| **搜索交互** | ⏳ 待测试 | 实时筛选 |
| **降级方案** | ⏳ 待测试 | API 失败时的处理 |

---

## 🐛 常见问题及解决方案

### 问题 1: 后端服务无法启动

**现象**:
```
Error: Address already in use
```

**解决方案**:
```bash
# 查找占用端口的进程
lsof -i :8000

# 杀死进程
kill -9 <PID>

# 重新启动
python3 start.py
```

---

### 问题 2: CORS 跨域错误

**现象** (前端控制台):
```
Access to fetch at 'http://localhost:8000/api/hospitals' from origin 'http://localhost:3001' has been blocked by CORS policy.
```

**解决方案**:

编辑 `backend/app/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### 问题 3: 401 Unauthorized

**现象**:
```json
{
  "detail": "Not authenticated"
}
```

**解决方案** (临时禁用认证):

编辑 `backend/app/api/routes/hospitals.py`:

```python
# 注释掉认证依赖
# current_user: User = Depends(get_current_active_user)
```

或者实现完整的登录流程获取 token。

---

### 问题 4: 数据库为空

**现象**:
```json
{
  "items": [],
  "total": 0
}
```

**解决方案**:

```bash
# 初始化数据库
cd backend
python3 init_db.py

# 或者创建测试数据
python3 create_test_data.py
```

---

### 问题 5: price 字段为 null

**现象**:
```json
{
  "price": null
}
```

**解决方案**:

参考之前的经验，编辑 `backend/app/models/hospital.py`:

```python
# 添加 ORM 序列化配置
class Hospital(Base):
    __tablename__ = "hospitals"
    
    # ... 其他字段
    
    price = Column(Integer, nullable=False)
    
    # 添加 model_config
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
```

并在 Schema 中确保 price 字段不是 Optional。

---

## ✅ 测试通过标准

### API 层面

- [ ] 后端服务正常启动
- [ ] Swagger UI 可访问
- [ ] GET /api/hospitals 返回 200
- [ ] 响应包含完整字段（items, total, page, size）
- [ ] items 数组非空
- [ ] 医院数据包含必要字段（id, name, price, level 等）
- [ ] CORS 配置正确
- [ ] 搜索、筛选、分页功能正常

### 前端层面

- [ ] 页面正常加载（无白屏）
- [ ] 医院列表正确渲染
- [ ] 图片正常显示
- [ ] 价格格式正确（¥9,800）
- [ ] 滚动加载正常工作
- [ ] 搜索功能可用
- [ ] 控制台无错误日志
- [ ] API 失败时降级到模拟数据

### 用户体验层面

- [ ] 加载速度快（首屏 < 2 秒）
- [ ] 滚动流畅不卡顿
- [ ] 交互反馈及时
- [ ] 无明显 UI 问题
- [ ] 移动端适配良好

---

## 📈 性能基准测试

### 使用 Lighthouse 测试

1. 打开 Chrome DevTools
2. 切换到 Lighthouse 标签
3. 选择 "Mobile"
4. 点击 "Analyze page load"

**目标分数**:
- Performance: ≥ 90
- Accessibility: ≥ 90
- Best Practices: ≥ 90
- SEO: ≥ 90

### 使用 Network 面板

1. 打开 Network 标签
2. 刷新页面
3. 查看各项指标

**目标值**:
- Finish: < 2s
- DOMContentLoaded: < 1s
- Load: < 3s

### 内存占用测试

1. 打开 Memory 标签
2. 录制一段时间
3. 查看内存使用

**目标值**:
- Heap Size: < 50MB
- 无明显内存泄漏

---

## 🎯 下一步行动

### 如果测试通过 ✅

1. **继续集成其他页面**
   - 医院详情页
   - 预约表单页
   - 文章列表页

2. **实施优化**
   - 骨架屏加载
   - 空状态提示
   - 图片懒加载

3. **准备部署**
   - 环境变量配置
   - 生产构建测试
   - 性能优化

### 如果测试失败 ❌

1. **记录问题**
   - 详细错误信息
   - 复现步骤
   - 截图/录屏

2. **逐项修复**
   - 优先解决阻塞性问题
   - 先 API 后前端
   - 先功能后体验

3. **重新测试**
   - 修复后再次执行测试
   - 确保所有项目通过

---

## 📝 测试报告模板

### 基本信息

- **测试日期**: YYYY-MM-DD HH:MM
- **测试人员**: [姓名]
- **测试环境**: 
  - 操作系统：macOS / Windows / Linux
  - 浏览器：Chrome xx.x / Safari xx.x
  - Node.js: vxx.x.x
  - Python: vxx.x.x

### 测试结果

**总体评价**: ✅ 通过 / ⚠️ 部分通过 / ❌ 失败

**通过率统计**:
- API 测试：x/x (xx%)
- 前端测试：x/x (xx%)
- 用户体验：x/x (xx%)

### 发现的问题

| 序号 | 问题描述 | 严重程度 | 状态 |
|------|---------|---------|------|
| 1 | 问题 1 描述 | 高/中/低 | 待修复/已修复 |
| 2 | 问题 2 描述 | 高/中/低 | 待修复/已修复 |

### 改进建议

1. 性能优化建议
2. 用户体验改进
3. 代码质量提升

---

## 🔗 相关资源

### 文档
- [API 集成指南](./API_INTEGRATION_GUIDE.md)
- [医院列表页 API 集成报告](./API_INTEGRATION_HOSPITAL_LIST.md)
- [医院列表页测试与优化方案](./HOSPITAL_LIST_TEST_PLAN.md)

### 工具
- [自动化测试脚本](./test_hospital_api.py)
- [Shell 测试脚本](./test_hospital_api.sh)

### 源码
- [医院列表页组件](./cnpetct/src/pages/hospitals/index.vue)
- [医院 API 服务](./cnpetct/src/api/hospitals.ts)
- [HTTP 请求封装](./cnpetct/src/utils/request.ts)

---

**报告生成时间**: 2026-03-21  
**测试状态**: ⏳ 准备就绪，等待执行测试  
**建议**: 按照本文档逐步执行测试，并记录结果
