# 医院合作统计功能 - 快速部署指南

## 📋 修改概述

已将前端页面的"活跃医院"统计改为"合作医院统计"，并实现了完整的后端支持。

## ✅ 已完成的修改

### 1. 数据库模型
- ✅ 添加 `is_cooperation` 字段到 hospitals 表
- ✅ 字段说明：0=未合作，1=合作，默认值=0

### 2. 后端 API
- ✅ 新增接口：`GET /v1/stats/hospitals/cooperation`（获取合作医院数量）
- ✅ 支持按合作状态筛选医院

### 3. 前端页面
- ✅ 统计卡片标签："活跃医院" → "合作医院"
- ✅ 新增合作医院数量统计显示
- ✅ 医院列表增加"是否合作"列
- ✅ 支持编辑医院合作状态

## 🚀 快速部署（推荐）

### 方式一：使用部署脚本

```bash
# 进入 backend 目录
cd /Users/shangxb/fastapi-vue3/petct-hospital/backend

# 运行部署脚本
./deploy_cooperation_feature.sh
```

脚本会自动执行以下步骤：
1. 备份数据库（可选）
2. 运行数据库迁移
3. 初始化现有数据（可选）
4. 提示重启服务

### 方式二：手动部署

#### 步骤 1：数据库迁移
```bash
cd backend
python3 add_is_cooperation_field.py
```

#### 步骤 2：初始化现有数据（可选）
```bash
python3 init_hospital_cooperation.py
```

#### 步骤 3：重启后端服务
```bash
python3 start.py
```

## 📝 验证功能

### 1. 检查数据库字段
```sql
-- 查看字段是否添加成功
DESCRIBE hospitals;
-- 应该看到 is_cooperation 字段
```

### 2. 测试 API 接口
```bash
# 获取合作医院数量
curl http://localhost:8000/v1/stats/hospitals/cooperation

# 筛选合作医院
curl http://localhost:8000/v1/hospitals/?is_cooperation=1
```

### 3. 检查前端页面
1. 访问医院管理页面
2. 查看统计卡片的"合作医院"数字
3. 检查医院列表的"是否合作"列
4. 测试编辑医院的合作状态

## 📊 文件清单

### 修改的文件
- `backend/app/models/hospital.py` - 添加 is_cooperation 字段
- `backend/app/api/routes/stats.py` - 新增统计接口
- `frontend/src/views/hospitals/index.vue` - 修改统计显示
- `frontend/src/api/hospitals.js` - 新增 API 方法

### 新增的文件
- `backend/add_is_cooperation_field.py` - 数据库迁移脚本
- `backend/init_hospital_cooperation.py` - 数据初始化脚本
- `backend/deploy_cooperation_feature.sh` - 自动化部署脚本
- `backend/HOSPITAL_COOPERATION_MIGRATION.md` - 详细文档
- `COOPERATION_FEATURE_SUMMARY.md` - 功能总结文档

## ⚠️ 注意事项

1. **数据备份**：部署前务必备份数据库
2. **测试环境**：建议先在测试环境验证
3. **权限控制**：API 需要登录后才能访问
4. **数据一致性**：新创建的医院默认为未合作状态

## 🔧 常见问题

### Q1: 字段已存在怎么办？
A: 迁移脚本会自动检测，如果字段已存在会跳过。

### Q2: 如何修改现有医院的合作状态？
A: 在医院列表中点击"编辑"，切换"是否合作"开关。

### Q3: 如何批量更新合作状态？
A: 可以运行 `init_hospital_cooperation.py` 脚本，或编写自定义 SQL。

### Q4: 部署后统计数字为 0 怎么办？
A: 运行 `init_hospital_cooperation.py` 将现有医院标记为合作医院。

## 📞 技术支持

如有问题，请查看详细文档：
- 功能总结：`COOPERATION_FEATURE_SUMMARY.md`
- 详细文档：`backend/HOSPITAL_COOPERATION_MIGRATION.md`

---

**最后更新时间**：2026-03-19
**版本**：v1.0.0
