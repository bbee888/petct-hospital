<template>
  <div class="hospital-edit">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>{{ isEdit ? '编辑医院' : '新增医院' }}</span>
        </div>
      </template>
      <el-form :model="form" label-width="100px">
        <el-form-item label="医院名称">
          <el-input v-model="form.name" placeholder="请输入医院名称" />
        </el-form-item>
        <el-form-item label="医院等级">
          <el-select v-model="form.level" placeholder="请选择医院等级">
            <el-option label="三级甲等" value="三级甲等" />
            <el-option label="三级乙等" value="三级乙等" />
            <el-option label="二级甲等" value="二级甲等" />
            <el-option label="二级乙等" value="二级乙等" />
            <el-option label="一级甲等" value="一级甲等" />
            <el-option label="一级乙等" value="一级乙等" />
          </el-select>
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="form.address" placeholder="请输入医院地址" />
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="form.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="标签">
          <TagInput v-model="form.tags" />
        </el-form-item>
      </el-form>
      <div class="form-actions">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import request from '../../utils/request'
import TagInput from '../../components/TagInput.vue'

const route = useRoute()
const router = useRouter()
const id = route.params.id
const isEdit = computed(() => !!id)

const form = ref({
  id: '',
  name: '',
  level: '',
  address: '',
  phone: '',
  tags: ''
})

const fetchHospital = async () => {
  try {
    // 这里应该调用实际的API获取医院详情
    // 暂时使用模拟数据
    form.value = {
      id: id,
      name: '北京协和医院',
      level: '三级甲等',
      address: '北京市东城区帅府园1号',
      phone: '010-69156114',
      tags: '三甲,综合,北京'
    }
  } catch (error) {
    console.error('获取医院详情失败:', error)
  }
}

const handleSave = async () => {
  try {
    // 这里应该调用实际的API保存医院
    console.log('保存医院:', form.value)
    router.push('/admin/hospitals')
  } catch (error) {
    console.error('保存医院失败:', error)
  }
}

const handleCancel = () => {
  router.push('/admin/hospitals')
}

onMounted(() => {
  if (isEdit.value) {
    fetchHospital()
  }
})
</script>

<style scoped>
.hospital-edit {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>