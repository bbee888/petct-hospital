<template>
  <el-dialog
    :title="title"
    :model-value="visible"
    @update:model-value="(val) => emit('update:visible', val)"
    width="500px"
    :close-on-click-modal="false"
    destroy-on-close
  >
    <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
      <el-form-item label="所属城市" prop="city_id">
        <el-select v-model="form.city_id" placeholder="请选择城市" style="width: 100%">
          <el-option
            v-for="city in cities"
            :key="city.id"
            :label="city.name"
            :value="city.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="区县名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入区县名称" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="handleCancel">取消</el-button>
      <el-button type="primary" @click="handleSubmit">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: '新增区县'
  },
  formData: {
    type: Object,
    default: () => ({
      id: null,
      city_id: null,
      name: ''
    })
  },
  cities: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:visible', 'save'])

const formRef = ref(null)
const form = ref({
  id: null,
  city_id: null,
  name: ''
})

const rules = {
  city_id: [
    { required: true, message: '请选择城市', trigger: 'change' }
  ],
  name: [
    { required: true, message: '请输入区县名称', trigger: 'blur' }
  ]
}

watch(() => props.visible, (newVal) => {
  if (newVal) {
    form.value = { ...props.formData }
  }
})

watch(() => props.formData, (newVal) => {
  form.value = { ...newVal }
}, { deep: true })

const handleCancel = () => {
  emit('update:visible', false)
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    emit('save', { ...form.value })
    emit('update:visible', false)
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}
</script>

<style scoped>
</style>
