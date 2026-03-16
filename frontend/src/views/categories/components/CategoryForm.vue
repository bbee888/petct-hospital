<template>
  <el-dialog
    v-model="dialogVisible"
    :title="dialogTitle"
    width="500px"
  >
    <el-form :model="form" label-width="80px" :rules="rules" ref="formRef">
      <el-form-item label="栏目名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入栏目名称" />
      </el-form-item>
      <el-form-item label="栏目别名" prop="slug">
        <el-input v-model="form.slug" placeholder="请输入栏目别名（用于URL）" />
      </el-form-item>
      <el-form-item label="所属站点" prop="site_domain">
        <el-select v-model="form.site_domain" placeholder="请选择所属网站" style="width: 100%">
          <el-option
            v-for="site in sites"
            :key="site.id"
            :label="site.name"
            :value="site.domain"
          />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import request from '../../../utils/request'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: '新增栏目'
  },
  formData: {
    type: Object,
    default: () => ({
      id: '',
      name: '',
      slug: '',
      site_domain: ''
    })
  }
})

const emit = defineEmits(['update:visible', 'save'])

const formRef = ref(null)
const dialogVisible = ref(props.visible)
const dialogTitle = ref(props.title)
const form = ref({ ...props.formData })
const sites = ref([])

const rules = {
  name: [
    { required: true, message: '请输入栏目名称', trigger: 'blur' },
    { min: 2, max: 50, message: '栏目名称长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  slug: [
    { required: true, message: '请输入栏目别名', trigger: 'blur' },
    { min: 2, max: 50, message: '栏目别名长度在 2 到 50 个字符', trigger: 'blur' },
    { pattern: /^[a-z0-9-]+$/, message: '栏目别名只能包含小写字母、数字和连字符', trigger: 'blur' }
  ],
  site_domain: [
    { required: true, message: '请选择所属网站', trigger: 'change' }
  ]
}

// 获取站点列表
const fetchSites = async () => {
  try {
    const response = await request.get('/v1/sites/')
    sites.value = response.data || []
  } catch (error) {
    console.error('获取站点列表失败:', error)
  }
}

// 组件挂载时获取站点列表
onMounted(() => {
  fetchSites()
})

watch(() => props.visible, (newVal) => {
  dialogVisible.value = newVal
  if (newVal) {
    form.value = { ...props.formData }
  }
})

watch(() => props.title, (newVal) => {
  dialogTitle.value = newVal
})

watch(() => props.formData, (newVal) => {
  form.value = { ...newVal }
}, { deep: true })

watch(() => dialogVisible.value, (newVal) => {
  emit('update:visible', newVal)
})

const handleCancel = () => {
  dialogVisible.value = false
  emit('update:visible', false)
}

const handleSave = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    console.log('准备保存的表单数据:', form.value)
    console.log('site_domain 值:', form.value.site_domain)
    emit('save', { ...form.value })
    dialogVisible.value = false
    emit('update:visible', false)
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>
