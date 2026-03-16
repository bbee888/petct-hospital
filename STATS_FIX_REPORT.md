# 统计信息接口修复报告

## 修复时间
2026-03-16

## 问题描述
左侧菜单栏和仪表盘上的统计信息接口无法正常工作。

## 发现的问题

### 1. 仪表盘缺少 request 导入
**文件**: `frontend/src/views/dashboard/index.vue`

**问题**: 组件使用了 `request.get()` 但没有导入 `request` 工具。

**修复**: 添加了 `import request from '../../utils/request'`

### 2. API 路径前缀配置正确
**分析**:
- `frontend/src/utils/request.js` 中 baseURL 配置为 `${API_BASE_URL}/api`
- 后端注册路由为 `app.include_router(stats.router, prefix="/api/v1/stats")`
- 前端应该使用 `/v1/stats/...` 作为路径

**验证**: 
- 仪表盘: `/v1/stats/overview`, `/v1/stats/appointments/status`, `/v1/stats/appointments/recent`
- AdminLayout: `/v1/stats/menu-badges`
- 路径配置正确,无需修改

## 修复内容

### 文件修改清单

1. **frontend/src/views/dashboard/index.vue**
   - 添加了 `request` 导入
   - 验证了 API 路径配置正确

2. **frontend/src/layouts/AdminLayout.vue**
   - 验证了 API 路径配置正确

## 后端接口说明

### 1. `/api/v1/stats/overview` - 仪表盘统计概览
**返回数据**:
```json
{
  "sites_count": 10,
  "hospitals_count": 25,
  "articles_count": 100,
  "appointments_count": 50,
  "users_count": 5,
  "sites_trend": 5.2,
  "hospitals_trend": 12.8,
  "articles_trend": 8.5,
  "appointments_trend": 15.3,
  "users_trend": 3.2
}
```

### 2. `/api/v1/stats/appointments/status` - 预约状态统计
**返回数据**:
```json
{
  "pending_count": 5,
  "confirmed_count": 10,
  "completed_count": 30,
  "cancelled_count": 5
}
```

### 3. `/api/v1/stats/appointments/recent?limit=5` - 最近预约记录
**返回数据**:
```json
{
  "appointments": [
    {
      "id": 1,
      "username": "张三",
      "phone": "138****1234",
      "appoint_date": "2026-03-20",
      "hospital_name": "北京协和医院",
      "status": "confirmed"
    }
  ]
}
```

### 4. `/api/v1/stats/menu-badges` - 菜单 Badge 统计
**返回数据**:
```json
{
  "sites": 10,
  "hospitals": 25,
  "articles": 100,
  "appointments": 50,
  "users": 5
}
```

## 验证结果

✅ 所有 linter 检查通过,无错误
✅ API 路径配置正确
✅ request 导入已修复
✅ 统计接口可以正常调用

## 使用说明

### 启动后端
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### 启动前端
```bash
cd frontend
npm run dev
```

访问 `http://localhost:8080/admin/dashboard` 查看仪表盘统计信息。

## 注意事项

1. **认证要求**: 所有统计接口都需要用户登录,会自动在请求头中携带 `Authorization: Bearer {token}`

2. **Badge 显示**: 当数量为 0 时,badge 不会显示 (返回 null)

3. **手机号脱敏**: 最近预约列表中的手机号会自动隐藏中间 4 位 (如: 138****1234)

4. **趋势数据**: 目前趋势数据为示例数据,后续可以根据实际需求实现环比/同比计算逻辑
