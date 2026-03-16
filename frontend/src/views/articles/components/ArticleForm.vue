<template>
  <el-dialog
    v-model="dialogVisible"
    :title="dialogTitle"
    :close-on-click-modal="false"
    top="20px"
    width="60%"
  >
    <el-form :model="form" label-width="100px">
      <el-form-item label="标题" :required="true">
        <el-input v-model="form.title" placeholder="请输入文章标题" />
      </el-form-item>

      
      <el-form-item label="站点">
        <el-select v-model="selectedSiteDomain" placeholder="请选择所属站点" @change="handleSiteChange" clearable>
          <el-option
            v-for="site in sites"
            :key="site.id"
            :label="site.name"
            :value="site.domain"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="栏目" :required="true">
        <el-select v-model="form.category_id" placeholder="请选择所属栏目" :disabled="!selectedSiteDomain">
          <el-option
            v-for="category in filteredCategories"
            :key="category.id"
            :label="category.name"
            :value="category.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="缩略图">
        <el-upload
          class="upload-demo"
          :action="uploadAction"
          :on-success="handleThumbnailUpload"
          :on-error="handleImageError"
          :file-list="thumbnailFileList"
          :limit="1"
          :auto-upload="true"
          list-type="picture-card"
          :on-preview="handlePicturePreview"
          :on-remove="handleThumbnailRemove"
        >
          <el-icon><Plus /></el-icon>
          <template #tip>
            <div class="el-upload__tip">
              只能上传jpg/png文件，且不超过2MB
            </div>
          </template>
        </el-upload>
      </el-form-item>

      
      
      <el-form-item label="关键词">
        <el-input-tag
    v-model="form.tags"
    placeholder="请输入关键词"
    delimiter=","
  />
      </el-form-item>
      <el-form-item label="文章简介">
        <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入文章简介" />
      </el-form-item>
      <el-form-item label="内容" :required="true">
        <div style="border: 1px solid #dcdfe6; border-radius: 4px;">
          <Toolbar
            :editor="editorInstance"
            :defaultConfig="editorConfig"
            mode="default"
            style="border-bottom: 1px solid #ccc;"
          />
          <Editor
            v-model="form.content"
            :defaultConfig="editorConfig"
            :style="editorStyle"
            @onCreated="handleEditorCreated"
          />
        </div>
      </el-form-item>
      <el-form-item label="状态">
        <el-switch v-model="form.is_published" />
      </el-form-item>
      
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </span>
    </template>
  </el-dialog>

  <!-- 图片预览对话框 -->
  <el-dialog v-model="dialogVisibleImg" title="图片预览" width="600px">
    <img :src="dialogImageUrl" alt="预览图片" style="width: 100%; height: auto;" />
  </el-dialog>
</template>

<script setup>
import { ref, shallowRef, watch, onMounted, onUnmounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
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
      is_published: true,
      cover: '',
      tags: '',
      description: '',
    })
  }
})

const emit = defineEmits(['update:visible', 'save'])

const dialogVisible = ref(props.visible)
const dialogTitle = ref(props.title)
const form = ref({ ...props.formData })
const categories = ref([])
const sites = ref([])
const filteredCategories = ref([])
const selectedSiteDomain = ref('')
const thumbnailFileList = ref([])
const dialogVisibleImg = ref(false)
const dialogImageUrl = ref('')

// API 配置
const apiUrl = import.meta.env.VITE_API_BASE_URL
const uploadAction = `${apiUrl}/api/v1/upload/image`

// 编辑器配置
const editorConfig = {
  placeholder: '请输入文章内容',
  scroll: true,
  MENU_CONF: {
    uploadImage: {
      // 自定义上传回调
      customUpload: async (file, insertFn) => {
        const apiUrl = import.meta.env.VITE_API_BASE_URL
        const formData = new FormData()
        formData.append('file', file)

        try {
          const response = await fetch(`${apiUrl}/api/v1/upload/image`, {
            method: 'POST',
            body: formData
          })
          const result = await response.json()

          console.log('编辑器图片上传结果:', result)

          if (result.code === 200 && result.data) {
            const fullUrl = result.data.url.startsWith('http') ? result.data.url : `${apiUrl}${result.data.url}`
            console.log('插入图片URL:', fullUrl)
            insertFn(fullUrl, 'image', fullUrl)
          } else {
            console.error('上传失败:', result)
            alert('图片上传失败，请重试')
          }
        } catch (error) {
          console.error('图片上传错误:', error)
          alert('图片上传失败，请检查网络连接')
        }
      }
    }
  }
}

// 编辑器样式
const editorStyle = {
  height: '350px',
  overflowY: 'hidden'
}

// 编辑器实例 ref
const editorInstance = shallowRef(null)

// 获取栏目列表
const fetchCategories = async () => {
  try {
    const response = await request.get('/v1/articles/categories')
    categories.value = response.data || []
    console.log('获取到的所有栏目:', categories.value)
    // 根据当前选中的站点过滤栏目
    filterCategories()
  } catch (error) {
    console.error('获取栏目列表失败:', error)
  }
}

// 获取站点列表
const fetchSites = async () => {
  try {
    const response = await request.get('/v1/sites/')
    sites.value = response.data || []
    console.log('获取到的所有站点:', sites.value)
  } catch (error) {
    console.error('获取站点列表失败:', error)
  }
}

// 先获取站点，再获取栏目
const fetchData = async () => {
  await fetchSites()
  await fetchCategories()
}

// 站点变化处理
const handleSiteChange = () => {
  console.log('站点发生变化，新站点:', selectedSiteDomain.value)
  // 清空栏目选择
  form.value.category_id = ''
  // 根据新站点过滤栏目
  filterCategories()
}

// 根据站点过滤栏目
const filterCategories = () => {
  console.log('开始过滤栏目，当前站点域名:', selectedSiteDomain.value)
  console.log('所有栏目数据:', categories.value)

  if (selectedSiteDomain.value) {
    filteredCategories.value = categories.value.filter(
      category => {
        console.log(`检查栏目: ${category.name}, site_domain: ${category.site_domain}, 是否匹配: ${category.site_domain === selectedSiteDomain.value}`)
        return category.site_domain === selectedSiteDomain.value
      }
    )
    console.log(`站点 ${selectedSiteDomain.value} 下的栏目:`, filteredCategories.value)
  } else {
    filteredCategories.value = []
    console.log('未选择站点，清空过滤后的栏目')
  }
}

// 编辑器创建成功回调
const handleEditorCreated = (editor) => {
  editorInstance.value = editor
  console.log('编辑器创建成功:', editor)
}

// 缩略图上传成功处理
const handleThumbnailUpload = (response, uploadFile) => {
  if (response.code === 200 && response.data) {
    const fullUrl = response.data.url.startsWith('http') ? response.data.url : `${apiUrl}${response.data.url}`
    form.value.cover = fullUrl
    thumbnailFileList.value = [{ url: fullUrl, name: uploadFile.name }]
  }
}

// 图片上传失败处理
const handleImageError = (error) => {
  console.error('图片上传失败:', error)
}

// 图片预览处理
const handlePicturePreview = (file) => {
  dialogImageUrl.value = file.url
  dialogVisibleImg.value = true
}

// 缩略图删除处理
const handleThumbnailRemove = () => {
  form.value.cover = ''
  thumbnailFileList.value = []
}

// 组件挂载时获取站点和栏目列表
onMounted(() => {
  fetchData()
  // 如果有缩略图，初始化显示
  if (form.value.cover) {
    const fullUrl = form.value.cover.startsWith('http') ? form.value.cover : `${apiUrl}${form.value.cover}`
    thumbnailFileList.value = [{ url: fullUrl, name: '缩略图' }]
  }
})

// 组件卸载时销毁编辑器
onUnmounted(() => {
  if (editorInstance.value) {
    editorInstance.value.destroy()
  }
})

watch(() => props.visible, (newVal) => {
  dialogVisible.value = newVal
  if (newVal) {
    fetchData()
  }
})

watch(() => props.title, (newVal) => {
  dialogTitle.value = newVal
})

watch(() => props.formData, (newVal) => {
  form.value = { ...newVal }
  console.log('formData 变化:', newVal)
  // 如果有缩略图，更新文件列表
  if (newVal.cover) {
    const fullUrl = newVal.cover.startsWith('http') ? newVal.cover : `${apiUrl}${newVal.cover}`
    thumbnailFileList.value = [{ url: fullUrl, name: '缩略图' }]
  } else {
    thumbnailFileList.value = []
  }
  // 如果编辑已有文章，根据文章所属栏目的 site_domain 自动选择站点
  if (newVal.category_id && categories.value.length > 0) {
    const category = categories.value.find(cat => cat.id === newVal.category_id)
    if (category) {
      selectedSiteDomain.value = category.site_domain
      setTimeout(() => filterCategories(), 100)
    }
  }
}, { deep: true })

// 监听站点变化，自动过滤栏目
watch(() => selectedSiteDomain.value, (newSiteDomain) => {
  console.log('站点变化 watch:', newSiteDomain)
  if (newSiteDomain) {
    setTimeout(() => filterCategories(), 100)
  }
})

const handleSave = () => {
  emit('save', form.value)
}

const handleCancel = () => {
  emit('update:visible', false)
}
</script>

<style scoped>
@import '@wangeditor/editor/dist/css/style.css';

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}

.upload-demo {
  margin-top: 10px;
}
</style>