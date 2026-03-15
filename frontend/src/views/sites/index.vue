<template>
  <div class="site-list">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>站点管理</span>
          <el-button type="primary" @click="handleAdd">新增站点</el-button>
        </div>
      </template>
      <el-table :data="sites" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="域名" width="200">
          <template #default="scope">
            <el-link :href="'http://' + scope.row.domain" target="_blank" type="primary">
              {{ scope.row.domain }}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="站点名称" />
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

    <!-- 站点编辑对话框组件 -->
    <SiteForm
      v-model:visible="dialogVisible"
      :title="dialogTitle"
      :form-data="form"
      @save="handleSave"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { sitesApi } from '../../api/sites'
import SiteForm from './components/SiteForm.vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const sites = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('新增站点')
const form = ref({
  id: '',
  domain: '',
  name: '',
  seo_title: '',
  seo_keywords: '',
  seo_description: '',
  status: true
})

const fetchSites = async () => {
  try {
    const response = await sitesApi.getSites(currentPage.value, pageSize.value)
    sites.value = response.data || []
    total.value = response.total || 0
  } catch (error) {
    console.error('获取站点列表失败:', error)
    ElMessage.error('获取站点列表失败，请稍后重试')
  }
}

const handleAdd = () => {
  dialogTitle.value = '新增站点'
  form.value = {
    id: '',
    domain: '',
    name: '',
    seo_title: '',
    seo_keywords: '',
    seo_description: '',
    status: true
  }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑站点'
  form.value = { ...row }
  dialogVisible.value = true
}

const handleSave = async (formData) => {
  try {
    if (formData.id) {
      // 更新站点
      await sitesApi.updateSite(formData.id, formData)
      ElMessage.success('站点更新成功')
    } else {
      // 创建站点
      await sitesApi.createSite(formData)
      ElMessage.success('站点创建成功')
    }
    dialogVisible.value = false
    fetchSites()
  } catch (error) {
    console.error('保存站点失败:', error)
    ElMessage.error('保存站点失败，请稍后重试')
  }
}

const handleStatusChange = async (row) => {
  try {
    await sitesApi.updateSite(row.id, { status: row.status })
    ElMessage.success('站点状态更新成功')
  } catch (error) {
    console.error('更新站点状态失败:', error)
    ElMessage.error('更新站点状态失败，请稍后重试')
    // 恢复原状态
    row.status = !row.status
  }
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该站点吗？删除后无法恢复。', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await sitesApi.deleteSite(id)
    ElMessage.success('站点删除成功')
    fetchSites()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除站点失败:', error)
      ElMessage.error('删除站点失败，请稍后重试')
    }
  }
}

const handleSizeChange = (size) => {
  pageSize.value = size
  fetchSites()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  fetchSites()
}

onMounted(() => {
  fetchSites()
})
</script>

<style scoped>
.site-list {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>