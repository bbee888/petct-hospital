<template>
  <div class="hospital-management">
    <!-- 页面标题和操作 -->
    <div class="page-header">
      <div class="page-header-left">
        <h1 class="page-title">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>
            <path d="M15 8a3 3 0 1 0-6 0"/>
          </svg>
          医院管理
        </h1>
        <p class="page-subtitle">管理医院信息和PET-CT设备配置</p>
      </div>
      <div class="page-header-right">
        <el-button 
          type="primary" 
          @click="handleAdd"
          class="action-button"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="16"/>
            <line x1="8" y1="12" x2="16" y2="12"/>
          </svg>
          新增医院
        </el-button>
        
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card stat-primary">
        <div class="stat-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-number">{{ total }}</div>
          <div class="stat-label">医院总数</div>
        </div>
      </div>
      <div class="stat-card stat-success">
        <div class="stat-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-number">{{ cooperationHospitals }}</div>
          <div class="stat-label">合作医院</div>
        </div>
      </div>
      <div class="stat-card stat-warning">
        <div class="stat-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
            <line x1="8" y1="21" x2="16" y2="21"/>
            <line x1="12" y1="17" x2="12" y2="21"/>
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-number">{{ avgPrice.toFixed(0) }}</div>
          <div class="stat-label">平均价格(¥)</div>
        </div>
      </div>
      <div class="stat-card stat-info">
        <div class="stat-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="16" x2="12" y2="12"/>
            <line x1="12" y1="8" x2="12.01" y2="8"/>
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-number">{{ levelDistribution['三级甲等'] || 0 }}</div>
          <div class="stat-label">三甲医院</div>
        </div>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="filter-card" shadow="hover">
      <div class="filter-header">
        <h3>筛选医院</h3>
        <div class="filter-actions">
          <el-button 
            type="text" 
            @click="toggleAdvancedFilter"
            :icon="advancedFilter ? ArrowUp : ArrowDown"
          >
            {{ advancedFilter ? '收起筛选' : '高级筛选' }}
          </el-button>
          <el-button type="text" @click="handleReset">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
              <path d="M3 3v5h5"/>
            </svg>
            重置
          </el-button>
        </div>
      </div>
      
      <div class="filter-grid">
        <div class="filter-item">
          <label class="filter-label">医院名称</label>
          <el-input
            v-model="searchQuery"
            placeholder="输入医院名称搜索"
            :prefix-icon="Search"
            clearable
            @keyup.enter="fetchHospitals"
            class="filter-input"
          />
        </div>
        
        <div class="filter-item">
          <label class="filter-label">省份/城市</label>
          <div class="geo-filters">
            <el-select
              v-model="searchProvince"
              placeholder="选择省份"
              clearable
              @change="handleProvinceChange"
              class="geo-select"
            >
              <el-option
                v-for="province in provinces"
                :key="province.id"
                :label="province.name"
                :value="province.id"
              />
            </el-select>
            <el-select
              v-model="searchCity"
              placeholder="选择城市"
              clearable
              :disabled="!searchProvince"
              class="geo-select"
            >
              <el-option
                v-for="city in cities"
                :key="city.id"
                :label="city.name"
                :value="city.id"
              />
            </el-select>
          </div>
        </div>
        
        <div class="filter-item">
          <label class="filter-label">医院等级</label>
          <el-select
            v-model="searchLevel"
            placeholder="选择医院等级"
            clearable
            class="filter-input"
          >
            <el-option label="三级甲等" value="三级甲等" />
            <el-option label="三级乙等" value="三级乙等" />
            <el-option label="二级甲等" value="二级甲等" />
            <el-option label="二级乙等" value="二级乙等" />
            <el-option label="一级甲等" value="一级甲等" />
            <el-option label="一级乙等" value="一级乙等" />
            <el-option label="综合医院" value="综合医院" />
            <el-option label="影像中心" value="影像中心" />
          </el-select>
        </div>
        
        <div class="filter-item">
          <label class="filter-label">价格范围</label>
          <div class="price-range">
            <el-input-number
              v-model="minPrice"
              :min="0"
              :max="10000"
              placeholder="最低价"
              controls-position="right"
              class="price-input"
            />
            <span class="price-separator">至</span>
            <el-input-number
              v-model="maxPrice"
              :min="0"
              :max="10000"
              placeholder="最高价"
              controls-position="right"
              class="price-input"
            />
          </div>
        </div>
      </div>
      
      <transition name="slide-down">
        <div v-if="advancedFilter" class="advanced-filters">
          <div class="filter-grid">
            <div class="filter-item">
              <label class="filter-label">设备类型</label>
              <el-select
                v-model="searchDevice"
                placeholder="选择PET-CT设备"
                clearable
                class="filter-input"
              >
                <el-option label="PET/CT" value="PET/CT" />
                <el-option label="PET-MR" value="PET-MR" />
                <el-option label="SPECT/CT" value="SPECT/CT" />
              </el-select>
            </div>
            
            <div class="filter-item">
              <label class="filter-label">排序方式</label>
              <el-select
                v-model="sortBy"
                placeholder="选择排序方式"
                class="filter-input"
              >
                <el-option label="默认排序" value="id" />
                <el-option label="价格从低到高" value="price_asc" />
                <el-option label="价格从高到低" value="price_desc" />
                <el-option label="医院等级" value="level" />
                <el-option label="最近更新" value="updated_at" />
              </el-select>
            </div>
            
            <div class="filter-item">
              <label class="filter-label">显示字段</label>
              <el-select
                v-model="visibleColumns"
                placeholder="选择显示字段"
                multiple
                collapse-tags
                collapse-tags-tooltip
                class="filter-input"
              >
                <el-option label="ID" value="id" />
                <el-option label="医院名称" value="title" />
                <el-option label="省份城市" value="location" />
                <el-option label="价格" value="price" />
                <el-option label="等级" value="level" />
                <el-option label="地址" value="address" />
                <el-option label="设备" value="device" />
                <el-option label="优势" value="advantage" />
              </el-select>
            </div>
          </div>
        </div>
      </transition>
      
      <div class="filter-footer">
        <el-button 
          type="primary" 
          @click="fetchHospitals"
          class="search-button"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          搜索 ({{ hospitals.length }} 条结果)
        </el-button>
      </div>
    </el-card>

    <!-- 医院列表表格 -->
    <el-card class="table-card" shadow="hover">
      <div class="table-header">
        <h3>医院列表</h3>
        <div class="table-actions">
          <el-button 
            type="text" 
            @click="toggleTableView"
            :icon="tableView === 'table' ? Apple : Menu"
          >
            {{ tableView === 'table' ? '卡片视图' : '表格视图' }}
          </el-button>
          <el-button type="text" @click="refreshData">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18-5.5l3 2.5M22 12.5a10 10 0 0 1-18 5.5l-3-2.5"/>
            </svg>
            刷新
          </el-button>
        </div>
      </div>
      
      <div class="table-container">
        <!-- 表格视图 -->
        <transition name="fade" mode="out-in">
          <div v-if="tableView === 'table'" class="table-wrapper">
            <el-table 
              :data="hospitals" 
              style="width: 100%"
              :row-class-name="tableRowClassName"
              @row-click="handleRowClick"
            >
              <el-table-column type="selection" width="50" />
              
              <el-table-column prop="id" label="ID" width="80">
                <template #default="scope">
                  <span class="hospital-id">#{{ scope.row.id }}</span>
                </template>
              </el-table-column>
              
              <el-table-column label="医院信息" min-width="250">
                <template #default="scope">
                  <div class="hospital-info">
                    <div class="hospital-name">
                      <span class="hospital-title">{{ scope.row.title }}</span>
                      <!-- 医院图片图标 -->
                      <el-tooltip 
                        v-if="scope.row.cover" 
                        placement="top"
                        :offset="10"
                        class="hospital-cover-tooltip"
                      >
                        <template #content>
                          <div class="hospital-cover-preview">
                            <img :src="scope.row.cover" :alt="scope.row.title" />
                          </div>
                        </template>
                        <div class="hospital-cover-icon">
                          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                            <circle cx="8.5" cy="8.5" r="1.5"/>
                            <polyline points="21 15 16 10 5 21"/>
                          </svg>
                        </div>
                      </el-tooltip>
                    </div>
                    <div class="hospital-meta">
                      <span class="meta-item">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/>
                          <circle cx="12" cy="10" r="3"/>
                        </svg>
                        {{ scope.row.address }}
                      </span>
                      <span class="meta-divider">•</span>
                      <span class="meta-item">
                        {{ scope.row.province_name }} - {{ scope.row.city_name }}
                      </span>
                    </div>
                  </div>
                </template>
              </el-table-column>
                            
              <!-- 医院等级列 -->
              <el-table-column label="医院等级" prop="level" width="120" align="center">
                <template #default="scope">
                  <span class="hospital-level-badge" :class="getLevelClass(scope.row.level)">
                    {{ scope.row.level || '未分级' }}
                  </span>
                </template>
              </el-table-column>
                            
              <el-table-column label="PET-CT 设备" min-width="150">
                <template #default="scope">
                  <div class="device-info">
                    <div class="device-type">
                      {{ scope.row.device || '未配置' }}
                    </div>
                  </div>
                </template>
              </el-table-column>
              
              <el-table-column label="价格与状态" width="180">
                <template #default="scope">
                  <div class="price-status">
                    <div class="price-tag">
                      <span class="price-currency">¥</span>
                      <span class="price-value">{{ scope.row.price || 0 }}</span>
                    </div>
                    <div class="status-indicator">
                      <span class="status-dot" :class="getStatusClass(scope.row)"></span>
                      <span class="status-text">正常</span>
                    </div>
                  </div>
                </template>
              </el-table-column>
              
              <el-table-column label="是否合作" prop="is_cooperation" width="100">
                <template #default="scope">
                  <el-tag v-if="scope.row.is_cooperation === 1" type="success">合作</el-tag>
                  <el-tag v-else type="info">未合作</el-tag>
                </template>
              </el-table-column>
              
              <el-table-column label="操作" width="250" fixed="right">
                <template #default="scope">
                  <div class="table-actions-buttons">
                    <el-button 
                      type="primary" 
                      size="small" 
                      @click.stop="handleView(scope.row)"
                      class="action-btn view-btn"
                    >
                      查看
                    </el-button>
                    <el-button 
                      type="success" 
                      size="small" 
                      @click.stop="handleEdit(scope.row)"
                      class="action-btn edit-btn"
                    >
                      编辑
                    </el-button>
                    <el-button 
                      type="danger" 
                      size="small" 
                      @click.stop="handleDelete(scope.row.id)"
                      class="action-btn delete-btn"
                    >
                      删除
                    </el-button>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </div>
          
          <!-- 卡片视图 -->
          <div v-else class="cards-grid">
            <div 
              v-for="hospital in hospitals" 
              :key="hospital.id"
              class="hospital-card"
            >
              <div class="card-header">
                <div class="hospital-basic">
                  <h4 class="hospital-title">{{ hospital.title }}</h4>
                  <span class="hospital-level" :class="getLevelClass(hospital.level)">
                    {{ hospital.level || '未分级' }}
                  </span>
                </div>
                <div class="card-actions">
                  <el-button 
                    type="text" 
                    size="small" 
                    @click="handleEdit(hospital)"
                  >
                    编辑
                  </el-button>
                </div>
              </div>
              
              <div class="card-body">
                <div class="hospital-location">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/>
                    <circle cx="12" cy="10" r="3"/>
                  </svg>
                  {{ hospital.province_name }} {{ hospital.city_name }}
                </div>
                
                <div class="hospital-price">
                  <span class="price-label">全身价格:</span>
                  <span class="price-value">¥{{ hospital.price || '待定' }}</span>
                </div>
                
                <div class="hospital-device" v-if="hospital.device">
                  <span class="device-label">设备类型:</span>
                  <span class="device-value">{{ hospital.device }}</span>
                </div>
                
                <div class="hospital-address" v-if="hospital.address">
                  <span class="address-label">地  址:</span>
                  <span class="address-value">{{ hospital.address.slice(0, 50) }}...</span>
                </div>
              </div>
              
              <div class="card-footer">
                <el-button 
                  type="primary" 
                  size="small" 
                  @click="handleView(hospital)"
                >
                  查看详情
                </el-button>
                <el-button 
                  type="danger" 
                  size="small" 
                  @click="handleDelete(hospital.id)"
                >
                  删除
                </el-button>
              </div>
            </div>
          </div>
        </transition>
        
        <!-- 空状态 -->
        <div v-if="hospitals.length === 0" class="empty-state">
          <div class="empty-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="16" x2="12" y2="12"/>
              <line x1="12" y1="8" x2="12.01" y2="8"/>
            </svg>
          </div>
          <h3>暂无医院数据</h3>
          <p>点击"新增医院"按钮添加第一家医院</p>
          <el-button type="primary" @click="handleAdd">
            新增医院
          </el-button>
        </div>
      </div>
      
      <!-- 分页 -->
      <div class="table-footer">
        <div class="table-summary">
          显示 {{ (currentPage - 1) * pageSize + 1 }}-{{ Math.min(currentPage * pageSize, total) }} 条，共 {{ total }} 条记录
        </div>
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          class="pagination"
        />
      </div>
    </el-card>

    <!-- 医院编辑对话框组件 -->
    <HospitalForm
      v-model:visible="dialogVisible"
      :title="dialogTitle"
      :form-data="form"
      @save="handleSave"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { Search, ArrowUp, ArrowDown, Apple, Menu } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox, ElNotification } from 'element-plus'
import request from '../../utils/request'
import HospitalForm from './components/HospitalForm.vue'
import { announceToScreenReader } from '../../utils/accessibility'

// 数据状态
const hospitals = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const cooperationCount = ref(0)
const searchQuery = ref('')
const searchProvince = ref('')
const searchCity = ref('')
const searchLevel = ref('')
const minPrice = ref(null)
const maxPrice = ref(null)
const searchDevice = ref('')
const sortBy = ref('id')
const visibleColumns = ref(['id', 'title', 'location', 'price', 'level', 'address'])

// 界面状态
const dialogVisible = ref(false)
const dialogTitle = ref('新增医院')
const tableView = ref('table') // 'table' 或 'card'
const advancedFilter = ref(false)
const provinces = ref([])
const cities = ref([])

// 表单数据
const form = ref({
  id: '',
  title: '',
  level: '',
  price: '',
  province_id: '',
  city_id: '',
  address: '',
  device: '',
  advantage: '',
  ks_intro: '',
  content: '',
  cover: '',
  seo_title: '',
  seo_keywords: '',
  seo_description: '',
})

// 计算属性
const cooperationHospitals = computed(() => {
  return cooperationCount.value
})

const avgPrice = computed(() => {
  const validPrices = hospitals.value.filter(h => h.price).map(h => parseFloat(h.price))
  if (validPrices.length === 0) return 0
  const sum = validPrices.reduce((acc, price) => acc + price, 0)
  return sum / validPrices.length
})

const levelDistribution = computed(() => {
  const distribution = {}
  hospitals.value.forEach(hospital => {
    const level = hospital.level || '未分级'
    distribution[level] = (distribution[level] || 0) + 1
  })
  return distribution
})

const fetchHospitals = async () => {
  try {
    let params = {
      page: currentPage.value,
      size: pageSize.value
    }
    
    if (searchQuery.value) {
      params.title = searchQuery.value
    }
    if (searchProvince.value) {
      params.province_id = searchProvince.value
    }
    if (searchCity.value) {
      params.city_id = searchCity.value
    }
    if (searchLevel.value) {
      params.level = searchLevel.value
    }
    if (minPrice.value) {
      params.min_price = minPrice.value
    }
    if (maxPrice.value) {
      params.max_price = maxPrice.value
    }
    if (searchDevice.value) {
      params.device = searchDevice.value
    }
    if (sortBy.value && sortBy.value !== 'id') {
      params.sort = sortBy.value
    }

    const response = await request.get('/v1/hospitals/', { params })
    hospitals.value = response.data?.items || response.data || []
    total.value = response.data?.total || hospitals.value.length
    
    // 获取合作医院数量
    fetchCooperationCount()
    
    // 通知屏幕阅读器
    announceToScreenReader(`找到 ${hospitals.value.length} 家医院`)
    
    ElNotification.success({
      title: '搜索完成',
      message: `找到 ${hospitals.value.length} 家医院`,
      duration: 2000
    })
  } catch (error) {
    console.error('获取医院列表失败:', error)
    announceToScreenReader('获取医院列表失败，请检查网络连接')
    ElNotification.error({
      title: '获取医院列表失败',
      message: error.response?.data?.detail || '请检查网络连接后重试',
      duration: 3000
    })
  }
}

const fetchCooperationCount = async () => {
  try {
    const response = await request.get('/v1/stats/hospitals/cooperation')
    cooperationCount.value = response.data?.cooperation_count || 0
  } catch (error) {
    console.error('获取合作医院数量失败:', error)
  }
}

const fetchProvinces = async () => {
  try {
    const response = await request.get('/v1/geo/provinces')
    provinces.value = response.data || []
  } catch (error) {
    console.error('获取省份列表失败:', error)
  }
}

const fetchCities = async (provinceId) => {
  try {
    const response = await request.get(`/v1/geo/cities?province_id=${provinceId}`)
    cities.value = response.data || []
  } catch (error) {
    console.error('获取城市列表失败:', error)
  }
}

const handleProvinceChange = (provinceId) => {
  searchCity.value = ''
  if (provinceId) {
    fetchCities(provinceId)
  } else {
    cities.value = []
  }
}

const handleReset = () => {
  searchQuery.value = ''
  searchProvince.value = ''
  searchCity.value = ''
  searchLevel.value = ''
  cities.value = []
  fetchHospitals()
}

const handleAdd = () => {
  dialogTitle.value = '新增医院'
  form.value = {
    id: '',
    title: '',
    level: '',
    price: '',
    province_id: '',
    city_id: '',
    address: '',
    device: '',
    advantage: '',
    ks_intro: '',
    content: '',
    cover: '',
    seo_title: '',
    tags: '',
    seo_description: '',
  }
  nextTick(() => {
    dialogVisible.value = true
  })
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑医院'
  form.value = { ...row }
  dialogVisible.value = true
}

const handleSave = async (formData) => {
  try {
    if (formData.id) {
      await request.put(`/v1/hospitals/${formData.id}`, formData)
      ElMessage.success('医院更新成功')
    } else {
      await request.post('/v1/hospitals/', formData)
      ElMessage.success('医院创建成功')
    }
    dialogVisible.value = false
    fetchHospitals()
  } catch (error) {
    console.error('保存医院失败:', error)
    ElMessage.error(error.response?.data?.detail || '保存医院失败，请稍后重试')
  }
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该医院吗？删除后无法恢复。', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await request.delete(`/v1/hospitals/${id}`)
    ElMessage.success('医院删除成功')
    fetchHospitals()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除医院失败:', error)
      ElMessage.error(error.response?.data?.detail || '删除医院失败，请稍后重试')
    }
  }
}


// 新的功能函数
const toggleAdvancedFilter = () => {
  advancedFilter.value = !advancedFilter.value
  announceToScreenReader(advancedFilter.value ? '展开高级筛选' : '收起高级筛选')
}

const toggleTableView = () => {
  tableView.value = tableView.value === 'table' ? 'card' : 'table'
  announceToScreenReader(tableView.value === 'table' ? '切换到表格视图' : '切换到卡片视图')
}

const refreshData = () => {
  fetchHospitals()
  announceToScreenReader('刷新医院数据')
  ElNotification.info({
    title: '正在刷新',
    message: '正在获取最新医院数据...',
    duration: 1500
  })
}

const handleView = (hospital) => {
  announceToScreenReader(`查看医院 ${hospital.title} 的详细信息`)
  ElMessage.info(`查看医院: ${hospital.title}`)
  // 这里可以跳转到医院详情页面
}

const handleRowClick = (row) => {
  // 可以在这里添加点击行的处理逻辑
  console.log('点击行:', row)
}

const tableRowClassName = ({ rowIndex }) => {
  return rowIndex % 2 === 0 ? 'even-row' : 'odd-row'
}

const getLevelClass = (level) => {
  const levelMap = {
    '三级甲等': 'level-top',
    '三级乙等': 'level-high',
    '二级甲等': 'level-medium',
    '二级乙等': 'level-low',
    '一级甲等': 'level-basic',
    '一级乙等': 'level-basic',
    '综合医院': 'level-general',
    '影像中心': 'level-center'
  }
  return levelMap[level] || 'level-default'
}

const getStatusClass = (hospital) => {
  // 这里可以根据医院的状态返回不同的class
  return hospital.status === 'active' ? 'status-active' : 'status-inactive'
}

const handleSizeChange = (size) => {
  pageSize.value = size
  fetchHospitals()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  fetchHospitals()
}

// 键盘快捷键支持
const setupKeyboardShortcuts = () => {
  const handleKeyDown = (event) => {
    // Ctrl/Cmd + F 聚焦搜索框
    if ((event.ctrlKey || event.metaKey) && event.key === 'f') {
      event.preventDefault()
      const searchInput = document.querySelector('.filter-input input')
      if (searchInput) {
        searchInput.focus()
        announceToScreenReader('已聚焦到搜索框')
      }
    }
    
    // Ctrl/Cmd + N 新增医院
    if ((event.ctrlKey || event.metaKey) && event.key === 'n') {
      event.preventDefault()
      handleAdd()
    }
    
    // F5 刷新数据
    if (event.key === 'F5') {
      event.preventDefault()
      refreshData()
    }
  }
  
  document.addEventListener('keydown', handleKeyDown)
  return () => document.removeEventListener('keydown', handleKeyDown)
}

onMounted(() => {
  fetchProvinces()
  fetchHospitals()
  fetchCooperationCount()
  
  const cleanup = setupKeyboardShortcuts()
  return () => cleanup()
})
</script>

<style scoped>
.hospital-management {
  padding: 20px;
  max-width: 1600px;
  margin: 0 auto;
}

/* 页面标题和操作 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #E2E8F0;
}

.page-header-left {
  flex: 1;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 28px;
  font-weight: 700;
  color: #164E63;
  margin: 0 0 8px 0;
  font-family: 'Fira Code', monospace;
}

.page-title svg {
  width: 32px;
  height: 32px;
  stroke: #0891B2;
}

.page-subtitle {
  font-size: 14px;
  color: #64748B;
  margin: 0;
}

.page-header-right {
  display: flex;
  gap: 12px;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  padding: 10px 20px;
  border-radius: 10px;
  height: 44px;
  transition: all 0.3s ease;
}

.action-button svg {
  width: 18px;
  height: 18px;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #E2E8F0;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 56px;
  height: 56px;
  min-width: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(8, 145, 178, 0.1);
}

.stat-primary .stat-icon {
  background: rgba(8, 145, 178, 0.1);
}

.stat-success .stat-icon {
  background: rgba(5, 150, 105, 0.1);
}

.stat-warning .stat-icon {
  background: rgba(245, 158, 11, 0.1);
}

.stat-info .stat-icon {
  background: rgba(6, 182, 212, 0.1);
}

.stat-icon svg {
  width: 28px;
  height: 28px;
  stroke: #0891B2;
}

.stat-primary .stat-icon svg { stroke: #0891B2; }
.stat-success .stat-icon svg { stroke: #059669; }
.stat-warning .stat-icon svg { stroke: #F59E0B; }
.stat-info .stat-icon svg { stroke: #06B6D4; }

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: #164E63;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #64748B;
  font-weight: 500;
}

/* 筛选卡片 */
.filter-card {
  margin-bottom: 30px;
  border-radius: 12px;
  border: 1px solid #E2E8F0;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #F1F5F9;
}

.filter-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #164E63;
  margin: 0;
}

.filter-actions {
  display: flex;
  gap: 12px;
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-label {
  font-size: 13px;
  font-weight: 600;
  color: #475569;
}

.filter-input {
  width: 100%;
}

.geo-filters {
  display: flex;
  gap: 12px;
}

.geo-select {
  flex: 1;
}

.price-range {
  display: flex;
  align-items: center;
  gap: 8px;
}

.price-input {
  flex: 1;
}

.price-separator {
  color: #94A3B8;
  font-size: 14px;
  min-width: 20px;
  text-align: center;
}

/* 高级筛选 */
.advanced-filters {
  padding: 20px;
  background: #F8FAFC;
  border-radius: 8px;
  margin-top: 20px;
  border: 1px solid #E2E8F0;
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  max-height: 500px;
  overflow: hidden;
}

.slide-down-enter-from,
.slide-down-leave-to {
  max-height: 0;
  opacity: 0;
  padding-top: 0;
  padding-bottom: 0;
  margin-top: 0;
}

.filter-footer {
  padding-top: 20px;
  border-top: 1px solid #F1F5F9;
  display: flex;
  justify-content: flex-end;
}

.search-button {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  padding: 10px 24px;
  height: 44px;
}

.search-button svg {
  width: 18px;
  height: 18px;
}

/* 表格卡片 */
.table-card {
  border-radius: 12px;
  border: 1px solid #E2E8F0;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #F1F5F9;
}

.table-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #164E63;
  margin: 0;
}

.table-actions {
  display: flex;
  gap: 12px;
}

/* 表格样式 */
.table-container {
  min-height: 400px;
  position: relative;
}

.table-wrapper {
  overflow-x: auto;
}

:deep(.el-table) {
  --el-table-border-color: #E2E8F0;
  --el-table-header-bg-color: #F8FAFC;
  --el-table-row-hover-bg-color: #F1F5F9;
}

:deep(.el-table th) {
  font-weight: 600;
  color: #475569;
  background-color: #F8FAFC;
  border-bottom: 2px solid #E2E8F0;
}

:deep(.el-table .even-row) {
  background-color: #F8FAFC;
}

:deep(.el-table .odd-row) {
  background-color: #FFFFFF;
}

:deep(.el-table tr:hover > td) {
  background-color: #F1F5F9 !important;
}

/* 医院信息单元格 */
.hospital-info {
  padding: 4px 0;
}

.hospital-name {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.hospital-title {
  font-weight: 600;
  color: #164E63;
  font-size: 14px;
}

.hospital-level-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 3px 6px;
  border-radius: 3px;
  color: white;
}

/* 医院图片图标 */
.hospital-cover-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 4px;
  background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
  cursor: pointer;
  transition: all 0.3s ease;
}

.hospital-cover-icon:hover {
  background: linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 100%);
  transform: scale(1.1);
}

.hospital-cover-icon svg {
  width: 14px;
  height: 14px;
  stroke: #0891B2;
}

/* 医院图片预览 */
.hospital-cover-preview {
  max-width: 400px;
  max-height: 300px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.hospital-cover-preview img {
  max-width: 100%;
  max-height: 300px;
  object-fit: cover;
  display: block;
}

.hospital-cover-tooltip {
  display: inline-block;
}

.level-top {
  background: linear-gradient(135deg, #059669 0%, #10B981 100%);
}

.level-high {
  background: linear-gradient(135deg, #0891B2 0%, #0EA5E9 100%);
}

.level-medium {
  background: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);
}

.level-low {
  background: linear-gradient(135deg, #EF4444 0%, #F87171 100%);
}

.level-basic {
  background: linear-gradient(135deg, #6B7280 0%, #9CA3AF 100%);
}

.level-general {
  background: linear-gradient(135deg, #8B5CF6 0%, #A78BFA 100%);
}

.level-center {
  background: linear-gradient(135deg, #EC4899 0%, #F472B6 100%);
}

.level-default {
  background: linear-gradient(135deg, #94A3B8 0%, #CBD5E1 100%);
}

.hospital-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #64748B;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.meta-item svg {
  width: 12px;
  height: 12px;
  stroke: #94A3B8;
}

.meta-divider {
  color: #CBD5E1;
}

/* 设备信息单元格 */
.device-info {
  padding: 4px 0;
}

.device-type {
  color: #164E63;
  font-size: 14px;
}

.device-advantage {
  font-size: 12px;
  color: #64748B;
  line-height: 1.4;
}

/* 价格与状态单元格 */
.price-status {
  padding: 4px 0;
}

.price-tag {
  display: inline-flex;
  align-items: baseline;
  background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
  padding: 6px 12px;
  border-radius: 8px;
  margin-bottom: 8px;
}

.price-currency {
  font-size: 14px;
  font-weight: 600;
  color: #0891B2;
  margin-right: 2px;
}

.price-value {
  font-size: 18px;
  font-weight: 700;
  color: #164E63;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-active {
  background: #10B981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
}

.status-inactive {
  background: #EF4444;
  box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.2);
}

.status-text {
  font-size: 12px;
  color: #64748B;
}

/* 操作按钮 */
.table-actions-buttons {
  display: flex;
  gap: 6px;
}

.action-btn {
  font-weight: 600;
  font-size: 12px;
  padding: 6px 12px;
  min-width: 60px;
}

.view-btn {
  background: linear-gradient(135deg, #0891B2 0%, #0E7490 100%);
  border: none;
}

.edit-btn {
  background: linear-gradient(135deg, #059669 0%, #10B981 100%);
  border: none;
}

.delete-btn {
  background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
  border: none;
}

/* 卡片视图 */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.hospital-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #E2E8F0;
  overflow: hidden;
  transition: all 0.3s ease;
}

.hospital-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  border-color: #0891B2;
}

.card-header {
  padding: 16px;
  border-bottom: 1px solid #F1F5F9;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.hospital-basic {
  flex: 1;
}

.hospital-title {
  font-size: 14px;
  font-weight: 600;
  color: #164E63;
  line-height: 1.3;
}

.hospital-level {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 4px;
  color: white;
}

.card-body {
  padding: 16px;
}

.hospital-location,
.hospital-price,
.hospital-device,
.hospital-address {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #475569;
  margin-bottom: 12px;
}

.hospital-location svg {
  width: 14px;
  height: 14px;
  stroke: #94A3B8;
  flex-shrink: 0;
}

.price-label,
.device-label,
.address-label {
  color: #64748B;
  min-width: 50px;
}

.price-value {
  font-weight: 600;
  color: #0891B2;
}

.device-value {
  font-weight: 500;
  color: #164E63;
}

.address-value {
  color: #475569;
  line-height: 1.4;
}

.card-footer {
  padding: 16px;
  border-top: 1px solid #F1F5F9;
  display: flex;
  gap: 8px;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 80px 40px;
  color: #64748B;
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  background: #F1F5F9;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-icon svg {
  width: 40px;
  height: 40px;
  stroke: #94A3B8;
}

.empty-state h3 {
  font-size: 20px;
  font-weight: 600;
  color: #475569;
  margin: 0 0 8px 0;
}

.empty-state p {
  margin: 0 0 24px 0;
  font-size: 14px;
}

/* 表格页脚 */
.table-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20px;
  border-top: 1px solid #F1F5F9;
}

.table-summary {
  font-size: 13px;
  color: #64748B;
}

.pagination {
  margin: 0;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 可访问性样式 */
:focus-visible {
  outline: 2px solid #0891B2;
  outline-offset: 2px;
}

/* 减少动画支持 */
@media (prefers-reduced-motion: reduce) {
  .stat-card,
  .hospital-card,
  .action-button,
  .search-button,
  .action-btn {
    transition: none !important;
  }
  
  .slide-down-enter-active,
  .slide-down-leave-active,
  .fade-enter-active,
  .fade-leave-active {
    transition: none !important;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
  }
  
  .page-header-right {
    width: 100%;
    justify-content: flex-start;
  }
  
  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }
  
  .filter-grid {
    grid-template-columns: 1fr;
  }
  
  .geo-filters {
    flex-direction: column;
  }
  
  .cards-grid {
    grid-template-columns: 1fr;
  }
  
  .table-footer {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .table-summary {
    text-align: center;
  }
  
  .pagination {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .table-actions-buttons {
    flex-direction: column;
    gap: 8px;
  }
  
  .action-btn {
    width: 100%;
  }
}

/* 高对比度模式 */
@media (prefers-contrast: high) {
  .stat-card,
  .filter-card,
  .table-card,
  .hospital-card {
    border: 2px solid #000;
  }
  
  :focus-visible {
    outline: 3px solid #000;
  }
  
  .hospital-level-badge,
  .hospital-level {
    border: 1px solid #000;
  }
}

/* 触摸设备优化 */
@media (hover: none) and (pointer: coarse) {
  .action-button,
  .search-button,
  .action-btn,
  .el-button {
    min-height: 44px;
    min-width: 44px;
  }
  
  .hospital-card {
    min-height: 200px;
  }
  
  :deep(.el-table tr) {
    min-height: 60px;
  }
}
</style>