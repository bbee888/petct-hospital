<template>
  <div class="min-h-screen bg-white pb-20">
    <!-- 加载状态 -->
    <div v-if="loading" class="flex items-center justify-center h-screen">
      <div class="inline-block w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
    </div>

    <template v-else-if="article">
      <!-- 顶部导航栏 -->
      <header class="fixed top-0 left-1/2 -translate-x-1/2 w-full max-w-[640px] z-40 px-4 pt-2">
        <div class="flex items-center justify-between">
          <button @click="router.back()" class="w-8 h-8 bg-black/30 rounded-full flex items-center justify-center">
            <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
            </svg>
          </button>
          <div class="flex items-center gap-3">
            <button class="w-8 h-8 bg-black/30 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="currentColor">
                <path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92-1.31-2.92-2.92-2.92z"/>
              </svg>
            </button>
            <button class="w-8 h-8 bg-black/30 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="currentColor">
                <path d="M17 3H7c-1.1 0-2 .9-2 2v16l7-3 7 3V5c0-1.1-.9-2-2-2z"/>
              </svg>
            </button>
          </div>
        </div>
      </header>

      <!-- 文章内容区域 -->
      <div class="px-4 pt-16">
        <!-- 文章头部 -->
        <div class="mb-4">
          <h1 class="text-xl font-bold text-gray-800 leading-tight">{{ article.title }}</h1>
          
          <!-- 作者信息 -->
          <div class="flex items-center justify-between mt-4">
            <div class="flex items-center gap-3">
              <img 
                :src="article.author_avatar || 'https://prototype-prod-1254106194.cos.ap-beijing.myqcloud.com/prototype/default.jpg'" 
                alt="作者头像" 
                class="w-8 h-8 rounded-full object-cover" 
              />
              <div>
                <p class="text-sm font-medium text-gray-800">{{ article.author || '编辑' }}</p>
                <p class="text-xs text-gray-500">{{ article.author_title || '' }}</p>
              </div>
            </div>
          </div>

          <!-- 文章meta -->
          <div class="flex items-center gap-3 mt-3 text-xs text-gray-400">
            <span>{{ formatDate(article.created_at) }}</span>
            <div class="flex items-center gap-1">
              <svg class="w-3 h-3" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
              </svg>
              <span>{{ article.view_count || 0 }} 阅读</span>
            </div>
            <span v-if="article.category_name" class="px-2 py-0.5 bg-blue-50 text-primary rounded-full">{{ article.category_name }}</span>
          </div>
        </div>

        <!-- 文章封面图 -->
        <img 
          v-if="article.cover"
          :src="article.cover" 
          alt="文章封面" 
          class="w-full h-48 object-cover rounded-xl" 
        />

        <!-- 摘要 -->
        <div v-if="article.description" class="mt-4 p-3 bg-gray-50 border-l-4 border-primary rounded-lg">
          <p class="text-sm font-medium text-gray-800 mb-1">摘要</p>
          <p class="text-xs text-gray-600 leading-relaxed">{{ article.description }}</p>
        </div>

        <!-- 文章正文 -->
        <div class="mt-6">
          <div class="text-sm text-gray-700 leading-relaxed whitespace-pre-line">
            {{ article.content || article.body || '暂无正文内容' }}
          </div>

          <!-- 温馨提示框 -->
          <div class="mt-6 p-4 bg-blue-50 border-l-4 border-primary rounded-lg">
            <div class="flex gap-2">
              <svg class="w-5 h-5 text-primary flex-shrink-0 mt-0.5" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
              </svg>
              <div>
                <p class="text-sm font-semibold text-primary mb-2">温馨提示</p>
                <p class="text-sm text-blue-600 leading-relaxed">PET-CT检查虽然是一项非常先进的检查技术，但并非所有人都需要做，也不是万能的。是否需要做PET-CT检查，应该由专业医生根据您的具体情况来判断。</p>
                <p class="text-sm text-blue-600 leading-relaxed mt-2">如果您有PET-CT检查的需求，可以通过我们的平台预约全国正规三甲医院的检查，享受快捷的预约服务和专业的咨询指导。</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 底部操作栏 -->
      <footer class="fixed bottom-0 left-1/2 -translate-x-1/2 w-full max-w-[640px] bg-white border-t border-gray-200 px-3 py-3 flex items-center justify-between z-40 safe-area-bottom">
        <div class="flex items-center gap-6">
          <div class="flex flex-col items-center gap-1">
            <svg class="w-5 h-5 text-gray-500" viewBox="0 0 24 24" fill="currentColor">
              <path d="M1 21h4V9H1v12zm22-11c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 1 7.59 7.59C7.22 7.95 7 8.45 7 9v10c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-2z"/>
            </svg>
            <span class="text-xs text-gray-500">点赞</span>
          </div>
          <div class="flex flex-col items-center gap-1">
            <svg class="w-5 h-5 text-gray-500" viewBox="0 0 24 24" fill="currentColor">
              <path d="M17 3H7c-1.1 0-2 .9-2 2v16l7-3 7 3V5c0-1.1-.9-2-2-2z"/>
            </svg>
            <span class="text-xs text-gray-500">收藏</span>
          </div>
          <div class="flex flex-col items-center gap-1">
            <svg class="w-5 h-5 text-gray-500" viewBox="0 0 24 24" fill="currentColor">
              <path d="M21.99 4c0-1.1-.89-2-1.99-2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4-.01-18zM18 14H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"/>
            </svg>
            <span class="text-xs text-gray-500">评论</span>
          </div>
        </div>
        <NuxtLink to="/booking" class="w-36 py-2.5 bg-primary text-white rounded-lg text-sm font-semibold text-center">
          预约PET-CT检查
        </NuxtLink>
      </footer>
    </template>

    <!-- 加载失败 -->
    <div v-else class="flex flex-col items-center justify-center h-screen text-gray-400">
      <svg class="w-16 h-16 mb-4" viewBox="0 0 24 24" fill="currentColor">
        <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
      </svg>
      <p>加载失败，请返回重试</p>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'article'
})

const router = useRouter()
const route = useRoute()
const { articleApi } = await import('~/composables/useApi')

const loading = ref(true)
const article = ref<any>(null)

// 获取文章ID
const articleId = Number(route.params.id)

// 格式化日期
function formatDate(dateStr: string) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

// 加载文章详情
async function loadArticle() {
  try {
    loading.value = true
    article.value = await articleApi.getDetail(articleId)
  } catch (error) {
    console.error('加载文章详情失败:', error)
    article.value = null
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadArticle()
})
</script>
