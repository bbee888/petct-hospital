<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航栏 -->
    <header class="bg-primary px-4 py-3">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center">
            <svg class="w-4 h-4 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.93 0 3.5 1.57 3.5 3.5S13.93 13 12 13s-3.5-1.57-3.5-3.5S10.07 6 12 6zm7 13H5v-.23c0-.62.28-1.2.76-1.58C7.47 15.82 9.64 15 12 15s4.53.82 6.24 2.19c.48.38.76.97.76 1.58V19z"/>
            </svg>
          </div>
          <span class="text-white font-bold text-lg">全国PET-CT预约平台</span>
        </div>
        <div class="flex items-center gap-1">
          <button class="w-7 h-7 flex items-center justify-center">
            <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
            </svg>
          </button>
        </div>
      </div>
    </header>

    <!-- 轮播Banner -->
    <div class="bg-gradient-to-r from-primary to-blue-700 px-6 py-8">
      <h1 class="text-white text-2xl font-bold mb-2">专业PET-CT检查预约</h1>
      <p class="text-white/80 text-sm mb-4">覆盖全国300+三甲医院 · 官方授权 · 快速安排</p>
      <NuxtLink to="/booking" class="inline-block bg-white text-primary px-6 py-2 rounded-lg text-sm font-semibold">
        立即预约
      </NuxtLink>
    </div>

    <!-- 快速入口区域 -->
    <div class="px-4 -mt-4">
      <div class="bg-white rounded-xl p-4 card-shadow">
        <div class="grid grid-cols-4 gap-2">
          <NuxtLink to="/hospitals" class="flex flex-col items-center gap-2">
            <div class="w-14 h-14 bg-blue-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-primary" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.93 0 3.5 1.57 3.5 3.5S13.93 13 12 13s-3.5-1.57-3.5-3.5S10.07 6 12 6zm7 13H5v-.23c0-.62.28-1.2.76-1.58C7.47 15.82 9.64 15 12 15s4.53.82 6.24 2.19c.48.38.76.97.76 1.58V19z"/>
              </svg>
            </div>
            <span class="text-xs text-gray-700">按医院预约</span>
          </NuxtLink>
          <NuxtLink to="/hospitals" class="flex flex-col items-center gap-2">
            <div class="w-14 h-14 bg-green-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-green-600" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
              </svg>
            </div>
            <span class="text-xs text-gray-700">按地区预约</span>
          </NuxtLink>
          <NuxtLink to="/hospitals" class="flex flex-col items-center gap-2">
            <div class="w-14 h-14 bg-orange-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-orange-500" viewBox="0 0 24 24" fill="currentColor">
                <path d="M11.8 10.9c-2.27-.59-3-1.2-3-2.15 0-1.09 1.01-1.85 2.7-1.85 1.78 0 2.44.85 2.5 2.1h2.21c-.07-1.72-1.12-3.3-3.21-3.81V3h-3v2.16c-1.94.42-3.5 1.68-3.5 3.61 0 2.31 1.91 3.46 4.7 4.13 2.5.6 3 1.48 3 2.41 0 .69-.49 1.79-2.7 1.79-2.06 0-2.87-.92-2.98-2.1h-2.2c.12 2.19 1.76 3.42 3.68 3.83V21h3v-2.15c1.95-.37 3.5-1.5 3.5-3.55 0-2.84-2.43-3.81-4.7-4.4z"/>
              </svg>
            </div>
            <span class="text-xs text-gray-700">价格查询</span>
          </NuxtLink>
          <NuxtLink to="/articles" class="flex flex-col items-center gap-2">
            <div class="w-14 h-14 bg-purple-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-purple-600" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
              </svg>
            </div>
            <span class="text-xs text-gray-700">科普知识</span>
          </NuxtLink>
        </div>
      </div>
    </div>

    <!-- 联系咨询栏 -->
    <div class="px-4 mt-4">
      <div class="bg-blue-50 rounded-lg p-3 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <svg class="w-5 h-5 text-primary" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
          </svg>
          <span class="text-sm text-gray-700">有疑问？免费咨询专业顾问</span>
        </div>
        <a href="tel:400-887-9166" class="bg-primary text-white px-4 py-1.5 rounded-lg text-sm font-medium">
          立即拨打
        </a>
      </div>
    </div>

    <!-- 热门医院推荐区域 -->
    <div class="px-4 mt-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-bold text-gray-800">热门医院推荐</h2>
        <NuxtLink to="/hospitals" class="text-sm text-gray-500 flex items-center gap-1">
          查看全部
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
          </svg>
        </NuxtLink>
      </div>

      <!-- 加载状态 -->
      <div v-if="loadingHospitals" class="text-center py-8">
        <div class="inline-block w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
        <p class="text-gray-400 text-sm mt-2">加载中...</p>
      </div>

      <!-- 医院列表 -->
      <div v-else-if="hospitals.length > 0">
        <NuxtLink 
          v-for="hospital in hospitals" 
          :key="hospital.id" 
          :to="`/hospitals/${hospital.id}`"
          class="block bg-white rounded-xl overflow-hidden card-shadow mb-4"
        >
          <div class="h-40 bg-gray-200 relative">
            <img 
              :src="hospital.cover || 'https://prototype-prod-1254106194.cos.ap-beijing.myqcloud.com/calicat/file/ai/canvas/image/2035272075264860160.jpg'" 
              :alt="hospital.title" 
              class="w-full h-full object-cover"
            />
            <span v-if="hospital.is_cooperation" class="absolute top-2 right-2 bg-red-500 text-white text-xs px-2 py-0.5 rounded">合作</span>
          </div>
          <div class="p-4">
            <div class="flex justify-between items-start mb-2">
              <div>
                <h3 class="text-base font-bold text-gray-800">{{ hospital.title }}</h3>
                <div class="flex gap-2 mt-1">
                  <span v-if="hospital.level" class="px-2 py-0.5 bg-blue-50 text-primary text-xs rounded">{{ hospital.level }}</span>
                  <span v-if="hospital.equipment" class="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">{{ hospital.equipment }}</span>
                </div>
              </div>
              <div class="text-right">
                <p class="text-xs text-gray-500">检查费用</p>
                <p class="text-xl font-bold text-red-500">¥{{ hospital.price || '待定' }}</p>
              </div>
            </div>
            <div class="flex items-center gap-1 text-gray-400 text-sm mb-3">
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
              </svg>
              <span class="text-xs">{{ hospital.province_name || '' }} {{ hospital.city_name || '' }} {{ hospital.address || '' }}</span>
            </div>
            <div class="flex gap-2 mb-3">
              <span v-if="hospital.advantage1" class="px-3 py-1 bg-green-50 text-green-600 text-xs rounded-full">{{ hospital.advantage1 }}</span>
              <span v-if="hospital.advantage2" class="px-3 py-1 bg-green-50 text-green-600 text-xs rounded-full">{{ hospital.advantage2 }}</span>
              <span v-if="hospital.advantage3" class="px-3 py-1 bg-green-50 text-green-600 text-xs rounded-full">{{ hospital.advantage3 }}</span>
            </div>
            <div class="flex gap-2">
              <NuxtLink :to="`/hospitals/${hospital.id}`" class="flex-1 py-2 border border-gray-200 rounded-lg text-sm text-gray-600 text-center">查看详情</NuxtLink>
              <NuxtLink :to="`/booking?hospital_id=${hospital.id}`" class="flex-1 py-2 bg-primary text-white rounded-lg text-sm font-medium text-center">立即预约</NuxtLink>
            </div>
          </div>
        </NuxtLink>
      </div>

      <!-- 无数据 -->
      <div v-else class="text-center py-8 text-gray-400">
        <p>暂无热门医院数据</p>
      </div>
    </div>

    <!-- 科普文章区域 -->
    <div class="px-4 mt-6 pb-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-bold text-gray-800">PET-CT科普</h2>
        <NuxtLink to="/articles" class="text-sm text-gray-500 flex items-center gap-1">
          更多文章
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
          </svg>
        </NuxtLink>
      </div>

      <!-- 加载状态 -->
      <div v-if="loadingArticles" class="text-center py-8">
        <div class="inline-block w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
        <p class="text-gray-400 text-sm mt-2">加载中...</p>
      </div>

      <!-- 文章列表 -->
      <div v-else-if="articles.length > 0">
        <NuxtLink 
          v-for="article in articles" 
          :key="article.id" 
          :to="`/articles/${article.id}`"
          class="block bg-white rounded-xl p-3 card-shadow flex gap-3 mb-3"
        >
          <img 
            :src="article.cover || 'https://prototype-prod-1254106194.cos.ap-beijing.myqcloud.com/prototype/default.jpg'" 
            alt="文章缩略图" 
            class="w-24 h-16 object-cover rounded-lg flex-shrink-0" 
          />
          <div class="flex-1 min-w-0">
            <h3 class="text-sm font-semibold text-gray-800 line-clamp-2 mb-1">{{ article.title }}</h3>
            <div class="flex items-center justify-between text-xs text-gray-400">
              <span class="flex items-center gap-1">
                <svg class="w-3 h-3" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
                </svg>
                {{ article.view_count }} 阅读
              </span>
              <span>{{ formatDate(article.created_at) }}</span>
            </div>
          </div>
        </NuxtLink>
      </div>

      <!-- 无数据 -->
      <div v-else class="text-center py-8 text-gray-400">
        <p>暂无文章数据</p>
      </div>
    </div>

    <!-- 固定咨询按钮 -->
    <a href="tel:400-887-9166" class="fixed bottom-20 right-4 w-14 h-14 bg-primary rounded-full flex items-center justify-center shadow-lg z-40">
      <svg class="w-6 h-6 text-white" viewBox="0 0 24 24" fill="currentColor">
        <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
      </svg>
    </a>
  </div>
</template>

<script setup lang="ts">
const { hospitalApi, articleApi } = await import('~/composables/useApi')

// 医院数据
const hospitals = ref<any[]>([])
const loadingHospitals = ref(true)

// 文章数据
const articles = ref<any[]>([])
const loadingArticles = ref(true)

// 加载热门医院
async function loadHospitals() {
  try {
    loadingHospitals.value = true
    const res = await hospitalApi.getHotList(6)
    hospitals.value = res.items || []
  } catch (error) {
    console.error('加载医院失败:', error)
    hospitals.value = []
  } finally {
    loadingHospitals.value = false
  }
}

// 加载文章列表
async function loadArticles() {
  try {
    loadingArticles.value = true
    const res = await articleApi.getLatestList(5)
    articles.value = res || []
  } catch (error) {
    console.error('加载文章失败:', error)
    articles.value = []
  } finally {
    loadingArticles.value = false
  }
}

// 格式化日期
function formatDate(dateStr: string) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

// 页面加载时获取数据
onMounted(() => {
  loadHospitals()
  loadArticles()
})
</script>
