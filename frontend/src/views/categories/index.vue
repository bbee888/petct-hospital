<template>
  <div class="category-list">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>栏目管理</span>
          <el-button type="primary" @click="handleAdd">新增栏目</el-button>
        </div>
      </template>
      <el-table :data="categories" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="栏目名称" />
        <el-table-column prop="slug" label="栏目别名" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 栏目编辑对话框组件 -->
    <CategoryForm
      v-model:visible="dialogVisible"
      :title="dialogTitle"
      :form-data="form"
      @save="handleSave"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { categoriesApi } from '../../api/categories'
import CategoryForm from './components/CategoryForm.vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const categories = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('新增栏目')
const form = ref({
  id: '',
  name: '',
  slug: ''
})

const fetchCategories = async () => {
  try {
    const categoriesList = await categoriesApi.getCategories()
    categories.value = categoriesList || []
  } catch (error) {
    console.error('获取栏目列表失败:', error)
    ElMessage.error('获取栏目列表失败，请稍后重试')
  }
}

const handleAdd = () => {
  dialogTitle.value = '新增栏目'
  form.value = {
    id: '',
    name: '',
    slug: ''
  }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑栏目'
  form.value = { ...row }
  dialogVisible.value = true
}

const handleSave = async (formData) => {
  try {
    if (formData.id) {
      await categoriesApi.updateCategory(formData.id, formData)
      ElMessage.success('栏目更新成功')
    } else {
      await categoriesApi.createCategory(formData)
      ElMessage.success('栏目创建成功')
    }
    dialogVisible.value = false
    fetchCategories()
  } catch (error) {
    console.error('保存栏目失败:', error)
    ElMessage.error(error.response?.data?.detail || '保存栏目失败，请稍后重试')
  }
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该栏目吗？删除后无法恢复。', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await categoriesApi.deleteCategory(id)
    ElMessage.success('栏目删除成功')
    fetchCategories()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除栏目失败:', error)
      ElMessage.error(error.response?.data?.detail || '删除栏目失败，请稍后重试')
    }
  }
}

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.category-list {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
