<template>
  <el-dialog
    v-model="dialogVisible"
    :title="dialogTitle"
    width="600px"
  >
    <el-form :model="form" label-width="120px">
      <el-form-item label="域名" required>
        <el-input v-model="form.domain" placeholder="请输入域名,如：www.ipetct.com" />
      </el-form-item>
      <el-form-item label="站点名称" required>
        <el-input v-model="form.name" placeholder="请输入站点名称" />
      </el-form-item>
      <el-form-item label="SEO标题">
        <el-input v-model="form.seo_title" placeholder="请输入SEO标题" />
      </el-form-item>
      <el-form-item label="SEO关键词">
        <el-input v-model="form.seo_keywords" placeholder="请输入SEO关键词，多个关键词用逗号分隔" />
      </el-form-item>
      <el-form-item label="SEO描述">
        <el-input v-model="form.seo_description" type="textarea" :rows="3" placeholder="请输入SEO描述" />
      </el-form-item>
      <el-form-item label="状态">
        <el-switch v-model="form.status" />
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
    default: '新增站点'
  },
  formData: {
    type: Object,
    default: () => ({
      id: '',
      domain: '',
      name: '',
      seo_title: '',
      seo_keywords: '',
      seo_description: '',
      status: true
    })
  }
})

const emit = defineEmits(['update:visible', 'save'])

const dialogVisible = ref(props.visible)
const dialogTitle = ref(props.title)
const form = ref({ ...props.formData })

watch(() => props.visible, (newVal) => {
  dialogVisible.value = newVal
  if (newVal) {
    // 打开对话框时，重新复制formData
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

const handleSave = () => {
  emit('save', { ...form.value })
  dialogVisible.value = false
  emit('update:visible', false)
}
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>
