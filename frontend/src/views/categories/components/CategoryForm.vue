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
import { ref, watch } from 'vue'

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
      slug: ''
    })
  }
})

const emit = defineEmits(['update:visible', 'save'])

const formRef = ref(null)
const dialogVisible = ref(props.visible)
const dialogTitle = ref(props.title)
const form = ref({ ...props.formData })

const rules = {
  name: [
    { required: true, message: '请输入栏目名称', trigger: 'blur' },
    { min: 2, max: 50, message: '栏目名称长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  slug: [
    { required: true, message: '请输入栏目别名', trigger: 'blur' },
    { min: 2, max: 50, message: '栏目别名长度在 2 到 50 个字符', trigger: 'blur' },
    { pattern: /^[a-z0-9-]+$/, message: '栏目别名只能包含小写字母、数字和连字符', trigger: 'blur' }
  ]
}

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
