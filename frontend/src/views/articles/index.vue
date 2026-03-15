<template>
  <div class="article-list">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>文章管理</span>
          <el-button type="primary" @click="handleAdd">新增文章</el-button>
        </div>
      </template>
      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索文章标题"
          prefix-icon="el-icon-search"
          style="width: 300px"
          @keyup.enter="fetchArticles"
        />
        <el-button type="primary" @click="fetchArticles">搜索</el-button>
      </div>
      <el-table :data="articles" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="site_domain" label="所属站点" width="150" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-switch v-model="scope.row.status" @change="handleStatusChange(scope.row)" />
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 文章编辑对话框组件 -->
    <ArticleForm
      v-model:visible="dialogVisible"
      :title="dialogTitle"
      :form-data="form"
      @save="handleSave"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../../utils/request'
import ArticleForm from './components/ArticleForm.vue'

const articles = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchQuery = ref('')
const dialogVisible = ref(false)
const dialogTitle = ref('新增文章')
const form = ref({
  id: '',
  title: '',
  content: '',
  category_id: '',
  site_domain: '',
  status: true,
  tags: ''
})

const fetchArticles = async () => {
  try {
    const response = await request.get('/v1/articles/')
    articles.value = response.data || []
    total.value = articles.value.length
  } catch (error) {
    console.error('获取文章列表失败:', error)
    ElMessage.error('获取文章列表失败，请稍后重试')
  }
}

const handleAdd = () => {
  dialogTitle.value = '新增文章'
  form.value = {
    id: '',
    title: '',
    content: '',
    category_id: '',
    site_domain: '',
    status: true,
    tags: ''
  }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑文章'
  form.value = { ...row }
  dialogVisible.value = true
}

const handleSave = async (formData) => {
  try {
    if (formData.id) {
      await request.put(`/v1/articles/${formData.id}`, formData)
      ElMessage.success('文章更新成功')
    } else {
      await request.post('/v1/articles/', formData)
      ElMessage.success('文章创建成功')
    }
    dialogVisible.value = false
    fetchArticles()
  } catch (error) {
    console.error('保存文章失败:', error)
    ElMessage.error(error.response?.data?.detail || '保存文章失败，请稍后重试')
  }
}

const handleStatusChange = async (row) => {
  try {
    await request.put(`/v1/articles/${row.id}`, { status: row.status })
    ElMessage.success('文章状态更新成功')
  } catch (error) {
    console.error('更新文章状态失败:', error)
    ElMessage.error('更新文章状态失败，请稍后重试')
    fetchArticles() // 失败后重新获取数据
  }
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该文章吗？删除后无法恢复。', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await request.delete(`/v1/articles/${id}`)
    ElMessage.success('文章删除成功')
    fetchArticles()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除文章失败:', error)
      ElMessage.error(error.response?.data?.detail || '删除文章失败，请稍后重试')
    }
  }
}

const handleSizeChange = (size) => {
  pageSize.value = size
  fetchArticles()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  fetchArticles()
}

onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.article-list {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-bar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>