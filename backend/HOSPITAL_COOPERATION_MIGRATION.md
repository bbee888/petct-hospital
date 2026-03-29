# 医院合作标记字段使用说明

## 修改内容

### 1. 数据库模型更新
- 在 `backend/app/models/hospital.py` 中添加了 `is_cooperation` 字段
- 字段类型：Integer
- 默认值：0（未合作）
- 合作医院值：1

### 2. 后端 API 更新
- 在 `backend/app/api/routes/stats.py` 中新增接口：
  - `GET /v1/stats/hospitals/cooperation` - 获取合作医院数量统计
- 在 `backend/app/api/routes/hospitals.py` 中支持按合作状态筛选：
  - `is_cooperation` 参数用于筛选合作/非合作医院

### 3. 前端页面更新
- 将"活跃医院"统计改为"合作医院"统计
- 统计卡片显示合作医院数量
- 在医院列表中显示"是否合作"列
- 新增 API 方法 `getCooperationCount()` 获取合作医院数量

## 数据库迁移步骤

### 步骤 1：运行迁移脚本添加字段
```bash
cd backend
python add_is_cooperation_field.py
```

### 步骤 2：初始化现有医院数据（可选）
如果需要将所有现有医院标记为合作医院，运行：
```bash
cd backend
python init_hospital_cooperation.py
```

### 步骤 3：重启后端服务
```bash
python start.py
```

## API 使用示例

### 获取合作医院数量
```javascript
const response = await request.get('/v1/stats/hospitals/cooperation')
// 返回：{ "cooperation_count": 10 }
```

### 按合作状态筛选医院
```javascript
// 获取所有合作医院
const response = await request.get('/v1/hospitals/', {
  params: { is_cooperation: 1 }
})

// 获取所有未合作医院
const response = await request.get('/v1/hospitals/', {
  params: { is_cooperation: 0 }
})
```

## 前端使用

在 Vue 组件中使用：
```vue
<template>
  <div class="stat-number">{{ cooperationHospitals }}</div>
  <div class="stat-label">合作医院</div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import request from '@/utils/request'

const cooperationCount = ref(0)

const cooperationHospitals = computed(() => cooperationCount.value)

const fetchCooperationCount = async () => {
  const response = await request.get('/v1/stats/hospitals/cooperation')
  cooperationCount.value = response.data?.cooperation_count || 0
}

onMounted(() => {
  fetchCooperationCount()
})
</script>
```

## 注意事项

1. 数据库迁移前请务必备份数据
2. 迁移脚本会自动检查字段是否已存在，避免重复添加
3. 初始化脚本会将所有现有医院标记为合作医院（is_cooperation=1）
4. 新增的医院默认为未合作状态（is_cooperation=0），需要在编辑时手动设置
