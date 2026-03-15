<template>
  <el-dialog
    v-model="dialogVisible"
    :title="dialogTitle"
    width="500px"
  >
    <el-form :model="form" label-width="80px" :rules="rules" ref="formRef">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="form.username" placeholder="请输入用户名" />
      </el-form-item>
      <el-form-item label="姓名" prop="realname">
        <el-input v-model="form.realname" placeholder="请输入真实姓名" />
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="form.email" placeholder="请输入邮箱" />
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        <span v-if="form.id" class="password-hint">留空则不修改密码</span>
      </el-form-item>
      <el-form-item label="状态">
        <el-switch v-model="form.is_active" />
        <span class="status-text">{{ form.is_active ? '启用' : '禁用' }}</span>
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
    default: '新增用户'
  },
  formData: {
    type: Object,
    default: () => ({
      id: '',
      username: '',
      email: '',
      realname: '',
      password: '',
      is_active: true
    })
  }
})

const emit = defineEmits(['update:visible', 'save'])

const formRef = ref(null)
const dialogVisible = ref(props.visible)
const dialogTitle = ref(props.title)
const form = ref({ ...props.formData })

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { 
      required: !props.formData?.id, 
      message: '请输入密码', 
      trigger: 'blur' 
    },
    { 
      min: 6, 
      message: '密码长度不能少于 6 个字符', 
      trigger: 'blur',
      validator: (rule, value, callback) => {
        if (!form.value.id && !value) {
          callback(new Error('新增用户必须设置密码'))
        } else if (value && value.length < 6) {
          callback(new Error('密码长度不能少于 6 个字符'))
        } else {
          callback()
        }
      }
    }
  ]
}

watch(() => props.visible, (newVal) => {
  dialogVisible.value = newVal
  if (newVal) {
    form.value = { ...props.formData }
    // 更新密码验证规则
    rules.password[0].required = !props.formData?.id
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

.password-hint {
  color: #909399;
  font-size: 12px;
  margin-left: 10px;
}

.status-text {
  margin-left: 10px;
  color: #606266;
}
</style>
