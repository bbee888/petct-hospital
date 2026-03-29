# 医院列表页面数据加载修复说明

## 📋 问题描述

在 www.yypetct.com 的医院列表页面（/hospitals），后台数据库有 2 条医院记录，但前端页面显示为空。

## 🔍 问题分析

### 1. 后端 API 问题

#### 修改前的问题
```python
# ❌ 问题 1: 不支持分页参数
@router.get("/", response_model=List[HospitalSchema])
async def get_hospitals(
    title: Optional[str] = None,
    # ... 其他参数
):
    # ❌ 问题 2: 直接返回数组，不是分页格式
    return result_data
```

**具体问题：**
- 没有 `page` 和 `size` 分页参数
- 返回格式是数组 `[]`，而不是 `{ items: [], total: N }`
- 前端无法正确解析数据和总数

### 2. 前端调用问题

#### 修改前的问题
```javascript
// ❌ 问题 1: 传递了错误的参数名
const data = await get('/v1/hospitals', {
  params: {
    status: 1,        // ❌ 后端不支持 status 参数
    page_size: 10     // ❌ 后端参数名是 size 不是 page_size
  }
})

// ❌ 问题 2: 期望从 items 获取数据
hospitals.value = data.items || []
```

**具体问题：**
- 传递了 `status: 1`，但后端医院模型没有 status 字段
- 传递了 `page_size`，但后端期望的参数名是 `size`
- 后端返回数组，前端期望 `{ items: [...] }` 格式

## ✅ 修复方案

### 1. 后端 API 修复

**文件**: `backend/app/api/routes/hospitals.py`

#### 添加分页支持
```python
from fastapi import Query
from sqlalchemy import func

@router.get("/")
async def get_hospitals(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    title: Optional[str] = None,
    province_id: Optional[int] = None,
    city_id: Optional[int] = None,
    level: Optional[str] = None,
    is_cooperation: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # 构建基础查询
    query = select(Hospital).options(
        joinedload(Hospital.province),
        joinedload(Hospital.city)
    )

    # 添加筛选条件
    conditions = []
    if title:
        conditions.append(Hospital.title.like(f"%{title}%"))
    if province_id:
        conditions.append(Hospital.province_id == province_id)
    if city_id:
        conditions.append(Hospital.city_id == city_id)
    if level:
        conditions.append(Hospital.level == level)
    if is_cooperation is not None:
        conditions.append(Hospital.is_cooperation == is_cooperation)

    if conditions:
        query = query.where(*conditions)

    # 获取总数
    total_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(total_query)
    total = total_result.scalar() or 0

    # 获取分页数据
    offset = (page - 1) * size
    paginated_query = query.offset(offset).limit(size)
    result = await db.execute(paginated_query)
    hospitals = result.scalars().all()

    # 构造响应数据
    result_data = []
    for hospital in hospitals:
        hospital_dict = {
            **hospital.__dict__,
            'province_name': hospital.province.name if hospital.province else None,
            'city_name': hospital.city.name if hospital.city else None
        }
        result_data.append(HospitalSchema(**hospital_dict))

    # ✅ 返回分页格式
    return {
        "items": result_data,
        "total": total,
        "page": page,
        "size": size
    }
```

**关键改动：**
- ✅ 添加 `page` 和 `size` 参数
- ✅ 使用 `func.count()` 统计总数
- ✅ 使用 `offset()` 和 `limit()` 实现分页
- ✅ 返回标准的分页响应格式

### 2. 前端调用修复

**文件**: `www.yypetct.com/pages/hospitals/index.vue`

#### 修正 API 调用
```javascript
const fetchHospitals = async () => {
  try {
    loading.value = true
    const data = await get<any>('/v1/hospitals', {
      params: {
        province_id: selectedProvince.value || undefined,
        city_id: selectedCity.value || undefined,
        is_cooperation: 1,  // ✅ 使用正确的参数名
        page: currentPage.value,
        size: itemsPerPage  // ✅ 参数名改为 size
      }
    })
    hospitals.value = data.items || []
  } catch (error) {
    console.error('Failed to fetch hospitals:', error)
  } finally {
    loading.value = false
  }
}
```

**关键改动：**
- ✅ 将 `status: 1` 改为 `is_cooperation: 1`
- ✅ 将 `page_size` 改为 `size`
- ✅ 保持从 `data.items` 提取数据

## 📊 API 接口格式

### 请求格式
```
GET /v1/hospitals?
  page=1&
  size=10&
  province_id=1&
  city_id=10&
  is_cooperation=1
Authorization: Bearer <token>
```

### 响应格式
```json
{
  "items": [
    {
      "id": 1,
      "title": "北京协和医院",
      "level": "三级甲等",
      "price": 8500,
      "province_id": 1,
      "city_id": 10,
      "address": "北京市东城区",
      "device": "PET/CT",
      "is_cooperation": 1,
      "province_name": "北京市",
      "city_name": "北京市"
    },
    {
      "id": 2,
      "title": "上海华山医院",
      "level": "三级甲等",
      "price": 9000,
      "province_id": 2,
      "city_id": 20,
      "address": "上海市静安区",
      "device": "PET-MR",
      "is_cooperation": 1,
      "province_name": "上海市",
      "city_name": "上海市"
    }
  ],
  "total": 2,
  "page": 1,
  "size": 10
}
```

## 🎯 数据流程

```
页面加载 (onMounted)
  ↓
fetchProvinces() - 获取省份列表
fetchHospitals() - 获取医院列表
  ↓
GET /v1/hospitals?page=1&size=10&is_cooperation=1
  ↓
后端执行 SQL 查询
  ├─ SELECT COUNT(*) FROM hospitals WHERE is_cooperation=1
  └─ SELECT * FROM hospitals WHERE is_cooperation=1 LIMIT 10 OFFSET 0
  ↓
返回 { items: [...], total: 2 }
  ↓
前端更新 hospitals.value
  ↓
filteredHospitals computed 处理
  ↓
模板渲染医院卡片
  ↓
显示"正常营业"标签（如果 status===1）
```

## 📝 字段映射说明

### 医院模型字段
```typescript
interface Hospital {
  id: number
  title: string
  level: string
  price: number
  province_id: number
  city_id: number
  address: string
  device: string | null
  advantage: string | null
  ks_intro: string | null
  content: string | null
  cover: string | null
  view_count: number
  is_published: boolean
  create_at: string
  seo_title: string | null
  tags: string | null
  seo_description: string | null
  is_cooperation: number  // ✅ 合作标记：0=未合作，1=合作
  province_name?: string | null
  city_name?: string | null
}
```

### 筛选参数
| 参数名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| page | number | 页码 | 1 |
| size | number | 每页数量 | 10 |
| province_id | number | 省份 ID | - |
| city_id | number | 城市 ID | - |
| level | string | 医院等级 | - |
| is_cooperation | number | 是否合作 | - |
| title | string | 医院名称（模糊搜索） | - |

## 🚀 功能特点

### 1. 分页功能
- ✅ 支持页码切换
- ✅ 支持每页数量设置（最大 100）
- ✅ 返回总记录数

### 2. 筛选功能
- ✅ 按省份筛选
- ✅ 按城市筛选
- ✅ 按医院等级筛选
- ✅ 按合作状态筛选
- ✅ 按医院名称搜索

### 3. 数据展示
- ✅ 显示医院基本信息
- ✅ 显示省份和城市名称
- ✅ 显示合作医院标识
- ✅ 支持图片占位符

## ⚠️ 注意事项

### 1. 数据库索引
确保以下字段有索引以提升查询性能：
- `hospitals.province_id`
- `hospitals.city_id`
- `hospitals.is_cooperation`
- `hospitals.title` (全文索引或 LIKE 优化)

### 2. 参数验证
- `page >= 1`
- `size >= 1` 且 `size <= 100`
- `is_cooperation`: 0 或 1

### 3. 错误处理
```javascript
try {
  const data = await get('/v1/hospitals', { params })
  hospitals.value = data.items || []
} catch (error) {
  console.error('Failed to fetch hospitals:', error)
  // TODO: 显示错误提示给用户
} finally {
  loading.value = false
}
```

### 4. 空状态处理
```vue
<div v-else-if="filteredHospitals.length === 0" class="text-center py-12">
  <svg>...</svg>
  <p>暂无匹配的医院</p>
  <button @click="resetFilters">重置筛选</button>
</div>
```

## 🔧 调试技巧

### 1. 查看 API 请求
打开浏览器开发者工具，查看 Network 面板：
```
Request URL: /v1/hospitals?page=1&size=12&is_cooperation=1
Response: { items: [...], total: 2 }
```

### 2. 查看控制台日志
```javascript
console.log('获取到的医院数据:', hospitals.value)
console.log('过滤后的医院:', filteredHospitals.value)
```

### 3. 检查后端日志
```python
print(f"Page: {page}, Size: {size}")
print(f"Total: {total}")
print(f"Items count: {len(result_data)}")
```

## 📈 性能优化建议

### 短期优化
1. **添加缓存**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   async def get_cached_hospitals(page: int, size: int, ...):
       # ... 查询逻辑
   ```

2. **预加载关联数据**
   ```python
   query = select(Hospital).options(
       joinedload(Hospital.province),
       joinedload(Hospital.city)
   )
   ```

### 长期优化
1. **Redis 缓存**
   - 缓存热门地区的医院列表
   - 设置合理的过期时间

2. **搜索引擎**
   - 使用 Elasticsearch 进行全文搜索
   - 支持更复杂的搜索条件

3. **CDN 加速**
   - 医院图片使用 CDN 分发
   - 静态资源缓存

---

**修复日期**: 2026-03-19  
**版本**: v1.0.3  
**状态**: ✅ 已修复并测试
