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
        <h1 class="text-lg font-semibold text-gray-800">PET-CT科普资讯</h1>
      </div>
    </header>

    <!-- 搜索栏 -->
    <div class="bg-white px-4 py-3">
      <div class="flex items-center gap-2 px-3 py-2 bg-gray-50 rounded-lg">
        <svg class="w-5 h-5 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
          <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
        </svg>
        <input 
          v-model="searchKeyword"
          @keyup.enter="handleSearch"
          type="text" 
          placeholder="搜索文章内容" 
          class="flex-1 bg-transparent text-sm outline-none"
        />
      </div>
    </div>

    <!-- 栏目分类 -->
    <div class="bg-white px-4 pb-3 overflow-x-auto">
      <div class="flex gap-3 min-w-max">
        <button 
          v-for="category in categories" 
          :key="category.id"
          @click="selectCategory(category.id)"
          class="px-4 py-1.5 rounded-full text-sm"
          :class="selectedCategoryId === category.id ? 'bg-primary text-white font-medium' : 'bg-gray-100 text-gray-600'"
        >
          {{ category.name }}
        </button>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="px-4 mt-4">
      <div class="text-center py-8">
        <div class="inline-block w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
        <p class="text-gray-400 text-sm mt-2">加载中...</p>
      </div>
    </div>

    <!-- 文章列表 -->
    <div v-else-if="articles.length > 0" class="px-4 mt-4 pb-6">
      <!-- 置顶文章 -->
      <div v-if="topArticle" class="bg-white rounded-xl overflow-hidden shadow-sm mb-4">
        <div class="bg-orange-50 px-3 py-2 flex items-center gap-1">
          <svg class="w-4 h-4 text-orange-500" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
          </svg>
          <span class="text-xs font-medium text-orange-500">置顶</span>
        </div>
        <NuxtLink :to="`/articles/${topArticle.id}`" class="p-4 block">
          <h3 class="text-base font-bold text-gray-800 leading-snug">{{ topArticle.title }}</h3>
          <p class="text-xs text-gray-500 mt-2 line-clamp-2">{{ topArticle.description || topArticle.excerpt || '' }}</p>
          <div class="flex items-center justify-between mt-3 text-xs text-gray-400">
            <div class="flex items-center gap-1">
              <svg class="w-3 h-3" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
              </svg>
              <span>{{ topArticle.views || 0 }} 阅读</span>
            </div>
            <span>{{ formatDate(topArticle.created_at) }}</span>
          </div>
        </NuxtLink>
      </div>

      <!-- 普通文章列表 -->
      <NuxtLink 
        v-for="article in normalArticles" 
        :key="article.id" 
        :to="`/articles/${article.id}`"
        class="block bg-white rounded-xl p-4 shadow-sm mb-4"
      >
        <div class="flex gap-3">
          <img 
            :src="article.cover || 'https://prototype-prod-1254106194.cos.ap-beijing.myqcloud.com/prototype/default.jpg'" 
            alt="文章缩略图" 
            class="w-24 h-17 object-cover rounded-lg flex-shrink-0" 
          />
          <div class="flex-1 min-w-0">
            <h3 class="text-sm font-semibold text-gray-800 line-clamp-2">{{ article.title }}</h3>
            <p class="text-xs text-gray-500 mt-1 line-clamp-2">{{ article.description || article.excerpt || '' }}</p>
            <div class="flex items-center justify-between mt-2 text-xs text-gray-400">
              <div class="flex items-center gap-2">
                <span class="px-2 py-0.5 bg-blue-50 text-primary rounded-full">{{ article.category_name || '科普' }}</span>
                <div class="flex items-center gap-1">
                  <svg class="w-3 h-3" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
                  </svg>
                  <span>{{ article.views || 0 }} 阅读</span>
                </div>
              </div>
              <span>{{ formatDate(article.created_at) }}</span>
            </div>
          </div>
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
    <div v-else class="px-4 mt-4">
      <div class="text-center py-12 text-gray-400">
        <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" viewBox="0 0 24 24" fill="currentColor">
          <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
        </svg>
        <p>暂无文章数据</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { articleApi } = await import('~/composables/useApi')

// 状态变量
const loading = ref(true)
const loadingMore = ref(false)
const articles = ref<any[]>([])
const categories = ref<any[]>([
  { id: null, name: '全部' },
  { id: 1, name: '检查须知' },
  { id: 2, name: '适应症' },
  { id: 3, name: '价格医保' },
  { id: 4, name: '案例分享' }
])
const selectedCategoryId = ref<number | null>(null)
const searchKeyword = ref('')
const page = ref(1)
const size = ref(10)
const hasMore = ref(true)

// 计算属性
const topArticle = computed(() => {
  if (!articles.value.length) return null
  return articles.value.find(a => a.is_top) || null
})

const normalArticles = computed(() => {
  if (!articles.value.length) return []
  return topArticle.value 
    ? articles.value.filter(a => a.id !== topArticle.value.id)
    : articles.value
})

// 格式化日期
function formatDate(dateStr: string) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

// 选择分类
function selectCategory(categoryId: number | null) {
  selectedCategoryId.value = categoryId
  loadArticles(true)
}

// 搜索
function handleSearch() {
  loadArticles(true)
}

// 加载文章列表
async function loadArticles(reset = false) {
  if (reset) {
    page.value = 1
    articles.value = []
    hasMore.value = true
  }
  
  try {
    loading.value = true
    const params: any = {}
    
    if (searchKeyword.value) {
      params.title = searchKeyword.value
    }
    if (selectedCategoryId.value) {
      params.category_id = selectedCategoryId.value
    }
    
    const res = await articleApi.getList(params)
    articles.value = res || []
    hasMore.value = false // 文章列表暂时不支持分页
  } catch (error) {
    console.error('加载文章失败:', error)
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
  loadArticles()
}

onMounted(() => {
  loadArticles()
})
</script>
