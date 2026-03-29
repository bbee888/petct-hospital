<template>
  <div class="min-h-screen bg-gray-50 pb-16">
    <!-- 顶部导航栏 -->
    <header class="bg-white px-4 py-3 sticky top-0 z-30">
      <div class="flex items-center gap-3">
        <NuxtLink to="/" class="w-8 h-8 flex items-center justify-center">
          <svg class="w-5 h-5 text-gray-600" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
          </svg>
        </NuxtLink>
        <h1 class="text-lg font-semibold text-gray-800">全国医院列表</h1>
      </div>
    </header>

    <!-- 搜索栏 -->
    <div class="bg-white px-4 py-3">
      <div class="flex items-center gap-2 bg-gray-100 rounded-lg px-3 py-2.5">
        <svg class="w-4 h-4 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
          <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
        </svg>
        <input 
          v-model="searchKeyword" 
          @keyup.enter="handleSearch"
          type="text" 
          placeholder="搜索医院名称" 
          class="flex-1 bg-transparent text-sm outline-none" 
        />
      </div>
    </div>

    <!-- 筛选栏 -->
    <div class="bg-white px-4 pb-3 flex items-center gap-4 text-sm">
      <button @click="showRegionPicker = true" class="flex items-center gap-1 text-gray-700">
        <span>{{ selectedProvinceName || '地区' }}</span>
        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
          <path d="M7 10l5 5 5-5z"/>
        </svg>
      </button>
      <button @click="showLevelPicker = true" class="flex items-center gap-1 text-gray-700">
        <span>{{ selectedLevel || '医院等级' }}</span>
        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
          <path d="M7 10l5 5 5-5z"/>
        </svg>
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="px-4 pt-4">
      <div class="text-center py-8">
        <div class="inline-block w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
        <p class="text-gray-400 text-sm mt-2">加载中...</p>
      </div>
    </div>

    <!-- 医院列表 -->
    <div v-else-if="hospitals.length > 0" class="px-4 pt-4">
      <NuxtLink 
        v-for="hospital in hospitals" 
        :key="hospital.id" 
        :to="`/hospitals/${hospital.id}`"
        class="block bg-white rounded-xl p-4 card-shadow mb-4"
      >
        <div class="flex gap-3">
          <img 
            :src="hospital.image || 'https://prototype-prod-1254106194.cos.ap-beijing.myqcloud.com/prototype/default.jpg'" 
            alt="医院图片" 
            class="w-20 h-20 object-cover rounded-lg flex-shrink-0" 
          />
          <div class="flex-1 min-w-0">
            <div class="flex justify-between items-start mb-1">
              <div>
                <h3 class="text-base font-bold text-gray-800">{{ hospital.title }}</h3>
                <div class="flex gap-2 mt-1">
                  <span v-if="hospital.level" class="px-2 py-0.5 bg-blue-50 text-primary text-xs rounded">{{ hospital.level }}</span>
                </div>
              </div>
            </div>
            <p v-if="hospital.equipment" class="text-xs text-gray-500 mb-1">设备型号：{{ hospital.equipment }}</p>
            <div class="flex items-center gap-1 text-gray-400 text-xs mb-1">
              <svg class="w-3 h-3" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
              </svg>
              <span class="truncate">{{ hospital.province_name || '' }} {{ hospital.city_name || '' }} {{ hospital.address || '' }}</span>
            </div>
            <div class="flex items-center gap-1">
              <span class="text-xs text-gray-500">价格：</span>
              <span class="text-lg font-bold text-red-500">¥{{ hospital.price || '待定' }}</span>
            </div>
          </div>
        </div>
        <div class="flex gap-2 mt-3">
          <span v-if="hospital.advantage1" class="px-3 py-1 bg-green-50 text-green-600 text-xs rounded-full">{{ hospital.advantage1 }}</span>
          <span v-if="hospital.advantage2" class="px-3 py-1 bg-green-50 text-green-600 text-xs rounded-full">{{ hospital.advantage2 }}</span>
          <span v-if="hospital.advantage3" class="px-3 py-1 bg-green-50 text-green-600 text-xs rounded-full">{{ hospital.advantage3 }}</span>
        </div>
        <div class="flex gap-2 mt-3">
          <a :href="`tel:${hospital.phone || '400-887-9166'}`" class="flex-1 py-2 bg-blue-50 text-primary rounded-lg text-sm font-medium flex items-center justify-center gap-1">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
            </svg>
            电话咨询
          </a>
          <NuxtLink :to="`/booking?hospital_id=${hospital.id}`" class="flex-1 py-2 bg-primary text-white rounded-lg text-sm font-medium text-center">
            立即预约
          </NuxtLink>
        </div>
      </NuxtLink>

      <!-- 加载更多 -->
      <div v-if="hasMore" class="text-center py-4">
        <button @click="loadMore" class="text-primary text-sm">
          {{ loadingMore ? '加载中...' : '点击加载更多' }}
        </button>
      </div>
    </div>

    <!-- 无数据 -->
    <div v-else class="px-4 pt-4">
      <div class="text-center py-12 text-gray-400">
        <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" viewBox="0 0 24 24" fill="currentColor">
          <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.93 0 3.5 1.57 3.5 3.5S13.93 13 12 13s-3.5-1.57-3.5-3.5S10.07 6 12 6zm7 13H5v-.23c0-.62.28-1.2.76-1.58C7.47 15.82 9.64 15 12 15s4.53.82 6.24 2.19c.48.38.76.97.76 1.58V19z"/>
        </svg>
        <p>暂无医院数据</p>
      </div>
    </div>

    <!-- 地区选择弹窗 -->
    <Teleport to="body">
      <div v-if="showRegionPicker" class="fixed inset-0 bg-black/50 z-50 flex items-end" @click.self="showRegionPicker = false">
        <div class="bg-white w-full max-w-[640px] mx-auto rounded-t-2xl max-h-[80vh] overflow-hidden">
          <div class="flex items-center justify-between p-4 border-b">
            <h3 class="font-semibold text-gray-800">选择地区</h3>
            <button @click="showRegionPicker = false" class="w-8 h-8 flex items-center justify-center">
              <svg class="w-5 h-5 text-gray-500" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
              </svg>
            </button>
          </div>
          <div class="flex h-[400px]">
            <div class="w-1/3 bg-gray-50 overflow-y-auto">
              <button 
                v-for="province in provinces" 
                :key="province.id"
                class="w-full px-4 py-3 text-left text-sm"
                :class="selectedProvinceId === province.id ? 'bg-white text-primary font-medium' : 'text-gray-600'"
                @click="selectProvince(province)"
              >
                {{ province.name }}
              </button>
            </div>
            <div class="flex-1 overflow-y-auto p-2">
              <button 
                v-for="city in filteredCities" 
                :key="city.id"
                class="w-full px-4 py-2 text-left text-sm rounded-lg"
                :class="selectedCityId === city.id ? 'bg-blue-50 text-primary font-medium' : 'text-gray-600 hover:bg-gray-50'"
                @click="selectCity(city)"
              >
                {{ city.name }}
              </button>
            </div>
          </div>
          <div class="flex gap-3 p-4 border-t">
            <button @click="resetRegion" class="flex-1 py-2.5 border border-gray-200 rounded-lg text-gray-600">重置</button>
            <button @click="confirmRegion" class="flex-1 py-2.5 bg-primary text-white rounded-lg font-medium">确定</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- 等级选择弹窗 -->
    <Teleport to="body">
      <div v-if="showLevelPicker" class="fixed inset-0 bg-black/50 z-50 flex items-end" @click.self="showLevelPicker = false">
        <div class="bg-white w-full max-w-[640px] mx-auto rounded-t-2xl">
          <div class="flex items-center justify-between p-4 border-b">
            <h3 class="font-semibold text-gray-800">选择医院等级</h3>
            <button @click="showLevelPicker = false" class="w-8 h-8 flex items-center justify-center">
              <svg class="w-5 h-5 text-gray-500" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
              </svg>
            </button>
          </div>
          <div class="p-4 grid grid-cols-3 gap-3">
            <button 
              v-for="level in levels" 
              :key="level"
              @click="selectedLevel = level; showLevelPicker = false"
              class="py-2 px-4 rounded-lg text-sm border"
              :class="selectedLevel === level ? 'bg-primary text-white border-primary' : 'border-gray-200 text-gray-600'"
            >
              {{ level }}
            </button>
          </div>
          <div class="p-4 border-t">
            <button @click="selectedLevel = ''; showLevelPicker = false" class="w-full py-2.5 text-primary text-sm">清除选择</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
const { hospitalApi, geoApi } = await import('~/composables/useApi')

// 状态变量
const loading = ref(true)
const loadingMore = ref(false)
const hospitals = ref<any[]>([])
const page = ref(1)
const size = ref(10)
const hasMore = ref(true)

// 搜索和筛选
const searchKeyword = ref('')
const showRegionPicker = ref(false)
const showLevelPicker = ref(false)

// 地区数据
const provinces = ref<any[]>([])
const cities = ref<any[]>([])
const selectedProvinceId = ref<number | null>(null)
const selectedCityId = ref<number | null>(null)
const selectedProvinceName = ref('')
const selectedLevel = ref('')

const levels = ['三甲', '三乙', '二甲', '二乙']

// 筛选后的城市
const filteredCities = computed(() => {
  if (!selectedProvinceId.value) return []
  return cities.value.filter(city => city.province_id === selectedProvinceId.value)
})

// 加载医院列表
async function loadHospitals(reset = false) {
  if (reset) {
    page.value = 1
    hospitals.value = []
    hasMore.value = true
  }
  
  try {
    loading.value = true
    const params: any = {
      page: page.value,
      size: size.value
    }
    
    if (searchKeyword.value) {
      params.title = searchKeyword.value
    }
    if (selectedProvinceId.value) {
      params.province_id = selectedProvinceId.value
    }
    if (selectedCityId.value) {
      params.city_id = selectedCityId.value
    }
    if (selectedLevel.value) {
      params.level = selectedLevel.value
    }
    
    const res = await hospitalApi.getList(params)
    
    if (reset) {
      hospitals.value = res.items || []
    } else {
      hospitals.value = [...hospitals.value, ...(res.items || [])]
    }
    
    hasMore.value = hospitals.value.length < res.total
  } catch (error) {
    console.error('加载医院失败:', error)
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

// 加载更多
function loadMore() {
  if (loadingMore.value || !hasMore.value) return
  loadingMore.value = true
  page.value++
  loadHospitals()
}

// 搜索
function handleSearch() {
  loadHospitals(true)
}

// 加载地区数据
async function loadRegions() {
  try {
    const [provinceData, cityData] = await Promise.all([
      geoApi.getProvinces(),
      geoApi.getCities()
    ])
    provinces.value = provinceData || []
    cities.value = cityData || []
  } catch (error) {
    console.error('加载地区失败:', error)
    // 使用备用数据
    provinces.value = [
      { id: 1, name: '北京' },
      { id: 2, name: '上海' },
      { id: 3, name: '广东' }
    ]
  }
}

// 选择省份
function selectProvince(province: any) {
  selectedProvinceId.value = province.id
  selectedProvinceName.value = province.name
  selectedCityId.value = null
}

// 选择城市
function selectCity(city: any) {
  selectedCityId.value = city.id
}

// 确认地区选择
function confirmRegion() {
  showRegionPicker.value = false
  loadHospitals(true)
}

// 重置地区
function resetRegion() {
  selectedProvinceId.value = null
  selectedCityId.value = null
  selectedProvinceName.value = ''
  showRegionPicker.value = false
  loadHospitals(true)
}

// 页面加载
onMounted(async () => {
  await loadRegions()
  await loadHospitals()
})
</script>
