<template>
  <div class="hospital-list">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>医院管理</span>
          <el-button type="primary" @click="handleAdd">新增医院</el-button>
        </div>
      </template>
      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索医院名称"
          prefix-icon="el-icon-search"
          style="width: 300px"
          @keyup.enter="fetchHospitals"
        />
        <el-button type="primary" @click="fetchHospitals">搜索</el-button>
      </div>
      <el-table :data="hospitals" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="医院名称" />
        <el-table-column prop="level" label="医院等级" width="100" />
        <el-table-column prop="address" label="地址" />
        <el-table-column prop="phone" label="电话" width="150" />
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
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../../utils/request'
import HospitalForm from './components/HospitalForm.vue'

const hospitals = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchQuery = ref('')
const dialogVisible = ref(false)
const dialogTitle = ref('新增医院')
const form = ref({
  id: '',
  name: '',
  level: '',
  city_id: '',
  address: '',
  phone: '',
  tags: ''
})

const fetchHospitals = async () => {
  try {
    const response = await request.get('/v1/hospitals/')
    hospitals.value = response.data || []
    total.value = hospitals.value.length
  } catch (error) {
    console.error('获取医院列表失败:', error)
  }
}

const handleAdd = () => {
  dialogTitle.value = '新增医院'
  form.value = {
    id: '',
    name: '',
    level: '',
    city_id: '',
    address: '',
    phone: '',
    tags: ''
  }
  dialogVisible.value = true
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

const handleSizeChange = (size) => {
  pageSize.value = size
  fetchHospitals()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  fetchHospitals()
}

onMounted(() => {
  fetchHospitals()
})
</script>

<style scoped>
.hospital-list {
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