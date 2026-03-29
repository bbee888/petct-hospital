<template>
  <el-dialog
    v-model="dialogVisible"
    :title="dialogTitle"
    :close-on-click-modal="false"
    width="60%"
  >
    <el-form :model="form" label-width="120px">
      <el-tabs v-model="activeTab">
        <!-- 基本信息 -->
        <el-tab-pane label="基本信息" name="basic">
          <el-form-item label="医院名称" :required="true">
            <el-input v-model="form.title" placeholder="请输入医院名称" />
          </el-form-item>
          <el-form-item label="petct价格" :required="true">
            <el-input v-model="form.price" type="number" placeholder="请输入价格" />
          </el-form-item>
          <el-form-item label="医院等级" :required="true">
            <el-select v-model="form.level" placeholder="请选择医院等级">
              <el-option label="综合医院" value="综合医院" />
              <el-option label="影像中心" value="影像中心" />
              <el-option label="三级甲等" value="三级甲等" />
              <el-option label="三级乙等" value="三级乙等" />
              <el-option label="二级甲等" value="二级甲等" />
              <el-option label="二级乙等" value="二级乙等" />
              <el-option label="一级甲等" value="一级甲等" />
              <el-option label="一级乙等" value="一级乙等" />
            </el-select>
          </el-form-item>
          <el-form-item label="所属地区" :required="true">
            <el-select v-model="form.province_id" placeholder="请选择省份" @change="handleProvinceChange" style="width: 200px;margin-right: 20px;">
              <el-option
                v-for="province in provinces"
                :key="province.id"
                :label="province.name"
                :value="province.id"
              />
            </el-select>
            <el-select v-model="form.city_id" placeholder="请选择城市" style="width: 200px;">
              <el-option
                v-for="city in cities"
                :key="city.id"
                :label="city.name"
                :value="city.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="医院地址" :required="true">
            <el-input v-model="form.address" placeholder="请输入医院地址" />
          </el-form-item>
          <el-form-item label="医院图片">
            <el-upload
              class="upload-demo"
              :action="uploadAction"
              :on-success="handleImageUpload"
              :on-error="handleImageError"
              :file-list="fileList"
              :limit="1"
              :auto-upload="true"
              list-type="picture-card"
              :on-preview="handlePicturePreview"
              :on-remove="handleRemove"
            >
              <el-icon><Plus /></el-icon>
              <template #tip>
                <div class="el-upload__tip">
                  只能上传jpg/png文件，且不超过2MB,图片大小:400*280
                </div>
              </template>
            </el-upload>
          </el-form-item>
          <el-form-item label="设备型号">
            <el-input v-model="form.device" placeholder="请输入设备型号" />
          </el-form-item>
          
          <el-form-item label="医院优势">
            <el-input v-model="form.advantage" type="textarea" :rows="3" placeholder="请输入医院优势" />
          </el-form-item>
          <el-form-item label="是否合作" :required="true">
            <el-switch v-model="form.is_cooperation" active-value="1" inactive-value="0" />
          </el-form-item>
        </el-tab-pane>
        
        <!-- 科室介绍 -->
        <el-tab-pane label="科室介绍" name="department">
          <el-form-item label="科室介绍">
            <div style="border: 1px solid #dcdfe6; border-radius: 4px;">
              <Toolbar
                :editor="ksIntroEditorRef"
                :defaultConfig="editorConfig"
                mode="default"
                style="border-bottom: 1px solid #ccc;"
              />
              <Editor
                v-model="form.ks_intro"
                :defaultConfig="editorConfig"
                :style="editorStyle"
                @onCreated="handleKsIntroCreated"
              />
            </div>
          </el-form-item>
        </el-tab-pane>

        <!-- 医院介绍 -->
        <el-tab-pane label="医院介绍" name="hospital">
          <el-form-item label="医院介绍">
            <div style="border: 1px solid #dcdfe6; border-radius: 4px;">
              <Toolbar
                :editor="contentEditorRef"
                :defaultConfig="editorConfig"
                mode="default"
                style="border-bottom: 1px solid #ccc;"
              />
              <Editor
                v-model="form.content"
                :defaultConfig="editorConfig"
                :style="editorStyle"
                @onCreated="handleContentCreated"
              />
            </div>
          </el-form-item>
        </el-tab-pane>
        
        <!-- SEO信息 -->
        <el-tab-pane label="SEO信息" name="seo">
          <el-form-item label="SEO标题">
            <el-input v-model="form.seo_title" placeholder="请输入SEO标题" />
          </el-form-item>
          <el-form-item label="SEO关键字">
            <el-input v-model="form.seo_keywords" placeholder="请输入SEO关键字，多个用逗号分隔" />
          </el-form-item>
          <el-form-item label="SEO描述">
            <el-input v-model="form.seo_description" type="textarea" rows="3" placeholder="请输入SEO描述" />
          </el-form-item>
        </el-tab-pane>
      </el-tabs>
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
import { ref, shallowRef, watch, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import TagInput from '../../../components/TagInput.vue'
import request from '../../../utils/request'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: '新增医院'
  },
  formData: {
    type: Object,
    default: () => ({
      id: '',
      title: '',
      level: '',
      province_id: '',
      city_id: '',
      address: '',
      cover: '',
      device: '',
      price: '',
      advantage: '',
      ks_intro: '',
      content: '',
      seo_title: '',
      tags: '',
      seo_description: '',
    })
  }
})

const emit = defineEmits(['update:visible', 'save'])

const dialogVisible = ref(props.visible)
const dialogTitle = ref(props.title)
const form = ref({ ...props.formData })
const activeTab = ref('basic')
const provinces = ref([])
const cities = ref([])
const fileList = ref([])

// API 配置
const apiUrl = import.meta.env.VITE_API_BASE_URL
const uploadAction = `${apiUrl}/api/v1/upload/image`

// 图片预览对话框
const dialogImageUrl = ref('')
const dialogVisibleImg = ref(false)

// 编辑器实例 ref
const ksIntroEditorRef = shallowRef(null)
const contentEditorRef = shallowRef(null)

// 编辑器配置
const editorConfig = {
  placeholder: '请输入内容...',
  scroll: true,
  MENU_CONF: {
    uploadImage: {
      // 自定义上传回调
      customUpload: async (file, insertFn) => {
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
            // console.log('插入图片URL:', fullUrl)
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
  height: '500px',
  overflowY: 'hidden'
}

// 编辑器创建时的回调
const handleKsIntroCreated = (editor) => {
  ksIntroEditorRef.value = editor
  console.log('ks_intro editor created', editor)
}

const handleContentCreated = (editor) => {
  contentEditorRef.value = editor
  console.log('content editor created', editor)
}

// 获取省份列表
const fetchProvinces = async () => {
  try {
    const response = await request.get('/v1/geo/provinces')
    provinces.value = response.data || []
  } catch (error) {
    console.error('获取省份列表失败:', error)
  }
}

// 获取城市列表
const fetchCities = async (provinceId) => {
  try {
    const response = await request.get(`/v1/geo/cities?province_id=${provinceId}`)
    cities.value = response.data || []
  } catch (error) {
    console.error('获取城市列表失败:', error)
  }
}

// 省份变化处理
const handleProvinceChange = (provinceId) => {
  form.value.city_id = ''
  form.value.province_id = provinceId
  if (provinceId) {
    fetchCities(provinceId)
  } else {
    cities.value = []
  }
}

// 图片上传成功处理
const handleImageUpload = (response, uploadFile) => {
  if (response.code === 200 && response.data) {
    const fullUrl = response.data.url.startsWith('http') ? response.data.url : `${apiUrl}${response.data.url}`
    form.value.cover = fullUrl
    fileList.value = [{ url: fullUrl, name: uploadFile.name }]
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

// 图片删除处理
const handleRemove = () => {
  form.value.cover = ''
  fileList.value = []
}

// 根据城市ID获取省份ID
const fetchProvinceByCityId = async (cityId) => {
  try {
    const response = await request.get(`/v1/geo/cities/${cityId}`)
    if (response.data && response.data.province_id) {
      form.value.province_id = response.data.province_id
      fetchCities(response.data.province_id)
    }
  } catch (error) {
    console.error('获取城市信息失败:', error)
  }
}

watch(() => props.visible, (newVal) => {
  dialogVisible.value = newVal
  if (newVal) {
    fetchProvinces()
    if (form.value.province_id) {
      fetchCities(form.value.province_id)
    }
  }
})

watch(() => props.title, (newVal) => {
  dialogTitle.value = newVal
})

watch(() => props.formData, (newVal) => {
  form.value = { ...newVal }
  if (newVal.cover) {
    const fullUrl = newVal.cover.startsWith('http') ? newVal.cover : `${apiUrl}${newVal.cover}`
    fileList.value = [{ url: fullUrl, name: '医院封面' }]
  } else {
    fileList.value = []
  }
  if (newVal.province_id) {
    fetchCities(newVal.province_id)
  } else if (newVal.city_id) {
    // 如果没有province_id但有city_id，根据city_id获取province_id
    fetchProvinceByCityId(newVal.city_id)
  }
}, { deep: true })

const handleSave = () => {
  const formData = { ...form.value }
  emit('save', formData)
  emit('update:visible', false)
}

const handleCancel = () => {
  emit('update:visible', false)
}

// 组件挂载时获取省份列表
onMounted(() => {
  fetchProvinces()
  if (form.value.province_id) {
    fetchCities(form.value.province_id)
  }
  if (form.value.cover) {
    const fullUrl = form.value.cover.startsWith('http') ? form.value.cover : `${apiUrl}${form.value.cover}`
    fileList.value = [{ url: fullUrl, name: '医院封面' }]
  }
})
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