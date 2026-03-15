<template>
  <el-dialog
    v-model="dialogVisible"
    :title="dialogTitle"
    width="800px"
  >
    <el-form :model="form" label-width="100px">
      <el-form-item label="标题">
        <el-input v-model="form.title" placeholder="请输入文章标题" />
      </el-form-item>
      <el-form-item label="内容">
        <div style="border: 1px solid #dcdfe6; border-radius: 4px; overflow: hidden;">
          <Toolbar
            :editor="editorInstance"
            :config="editorConfig"
          />
          <Editor
            :default-content="form.content"
            :config="editorConfig"
            @onCreated="handleEditorCreated"
            @onChange="handleEditorChange"
          />
        </div>
      </el-form-item>
      <el-form-item label="栏目">
        <el-select v-model="form.category_id" placeholder="请选择所属栏目">
          <el-option
            v-for="category in categories"
            :key="category.id"
            :label="category.name"
            :value="category.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="站点">
        <el-select v-model="form.site_domain" placeholder="请选择所属站点">
          <el-option label="本地测试站点" value="localhost:8080" />
          <el-option label="示例站点" value="example.com" />
        </el-select>
      </el-form-item>
      <el-form-item label="状态">
        <el-switch v-model="form.status" />
      </el-form-item>
      <el-form-item label="标签">
        <TagInput v-model="form.tags" />
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
import { ref, watch, onMounted, onUnmounted } from 'vue'
import TagInput from '../../../components/TagInput.vue'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import '@wangeditor/editor/dist/css/style.css'
import request from '../../../utils/request'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: '新增文章'
  },
  formData: {
    type: Object,
    default: () => ({
      id: '',
      title: '',
      content: '',
      category_id: '',
      site_domain: '',
      status: true,
      tags: ''
    })
  }
})

const emit = defineEmits(['update:visible', 'save'])

const dialogVisible = ref(props.visible)
const dialogTitle = ref(props.title)
const form = ref({ ...props.formData })
const categories = ref([])

// 编辑器配置
const editorConfig = {
  placeholder: '请输入文章内容',
  MENU_CONF: {
    uploadImage: {
      server: '/v1/upload',
      fieldName: 'file',
      maxFileSize: 10 * 1024 * 1024, // 10MB
      accept: 'image/*'
    }
  }
}

// 编辑器实例
let editorInstance = null

// 获取栏目列表
const fetchCategories = async () => {
  try {
    const response = await request.get('/v1/articles/categories')
    categories.value = response.data || []
  } catch (error) {
    console.error('获取栏目列表失败:', error)
  }
}

// 编辑器创建成功回调
const handleEditorCreated = (editor) => {
  editorInstance = editor
  console.log('编辑器创建成功:', editor)
}

// 编辑器内容变化回调
const handleEditorChange = (editor) => {
  form.value.content = editor.getHtml()
  console.log('编辑器内容变化:', editor.getHtml())
}

// 组件挂载时获取栏目列表
onMounted(() => {
  fetchCategories()
})

// 组件卸载时销毁编辑器
onUnmounted(() => {
  if (editorInstance) {
    editorInstance.destroy()
  }
})

watch(() => props.visible, (newVal) => {
  dialogVisible.value = newVal
})

watch(() => props.title, (newVal) => {
  dialogTitle.value = newVal
})

watch(() => props.formData, (newVal) => {
  form.value = { ...newVal }
}, { deep: true })

const handleSave = () => {
  emit('save', form.value)
}

const handleCancel = () => {
  emit('update:visible', false)
}
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>