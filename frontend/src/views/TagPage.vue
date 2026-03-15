<template>
  <div class="tag-page">
    <el-container>
      <el-header>
        <h1>{{ tag?.name }} - 相关内容</h1>
      </el-header>
      <el-main>
        <div v-if="loading" class="loading">
          <el-skeleton :rows="10" animated />
        </div>
        <div v-else-if="error" class="error">
          <el-alert
            title="加载失败"
            type="error"
            :closable="false"
          />
          <el-button type="primary" @click="loadData">重新加载</el-button>
        </div>
        <div v-else>
          <!-- 相关文章 -->
          <div class="section" v-if="articles.length > 0">
            <h2>相关文章</h2>
            <el-card v-for="article in articles" :key="article.id" class="article-card">
              <template #header>
                <div class="article-header">
                  <h3>{{ article.title }}</h3>
                  <span class="article-date">{{ formatDate(article.published_at) }}</span>
                </div>
              </template>
              <div class="article-content">{{ truncateText(article.content, 100) }}</div>
            </el-card>
          </div>
          
          <!-- 相关医院 -->
          <div class="section" v-if="hospitals.length > 0">
            <h2>相关医院</h2>
            <el-card v-for="hospital in hospitals" :key="hospital.id" class="hospital-card">
              <template #header>
                <div class="hospital-header">
                  <h3>{{ hospital.title }}</h3>
                  <span class="hospital-price" v-if="hospital.price">¥{{ hospital.price }}</span>
                </div>
              </template>
              <div class="hospital-content">
                <div class="hospital-address" v-if="hospital.address">{{ hospital.address }}</div>
                <div class="hospital-advantage" v-if="hospital.advantage">{{ truncateText(hospital.advantage, 100) }}</div>
              </div>
            </el-card>
          </div>
          
          <div v-if="articles.length === 0 && hospitals.length === 0" class="empty">
            <el-empty description="暂无相关内容" />
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import request from '../utils/request'

const route = useRoute()
const slug = computed(() => route.params.slug)

const loading = ref(true)
const error = ref(false)
const tag = ref(null)
const articles = ref([])
const hospitals = ref([])

const loadData = async () => {
  loading.value = true
  error.value = false
  
  try {
    const response = await request.get(`/v1/tags/${slug.value}`)
    tag.value = response.tag
    articles.value = response.articles
    hospitals.value = response.hospitals
    
    // 更新页面标题
    document.title = `${tag.value.name} - 相关内容`
  } catch (err) {
    console.error('加载标签数据失败:', err)
    error.value = true
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

const truncateText = (text, length) => {
  if (!text) return ''
  const plainText = text.replace(/<[^>]*>/g, '')
  return plainText.length > length ? plainText.substring(0, length) + '...' : plainText
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.tag-page {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.el-header {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.el-main {
  padding: 20px;
}

.section {
  margin-bottom: 30px;
}

.section h2 {
  font-size: 18px;
  margin-bottom: 16px;
  color: #303133;
}

.article-card,
.hospital-card {
  margin-bottom: 16px;
}

.article-header,
.hospital-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.article-date {
  font-size: 12px;
  color: #909399;
}

.hospital-price {
  font-size: 14px;
  color: #f56c6c;
  font-weight: bold;
}

.article-content,
.hospital-content {
  margin-top: 12px;
  font-size: 14px;
  line-height: 1.5;
  color: #606266;
}

.hospital-address {
  margin-bottom: 8px;
  color: #909399;
}

.loading,
.error,
.empty {
  margin: 20px 0;
}

.error {
  text-align: center;
  padding: 40px 0;
}
</style>
