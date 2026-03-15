<template>
  <el-dialog
    v-model="dialogVisible"
    :title="dialogTitle"
    width="800px"
  >
    <el-form :model="form" label-width="100px">
      <el-tabs v-model="activeTab">
        <!-- 基本信息 -->
        <el-tab-pane label="基本信息" name="basic">
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
          <el-form-item label="所属省份">
            <el-select v-model="form.province_id" placeholder="请选择省份" @change="handleProvinceChange">
              <el-option
                v-for="province in provinces"
                :key="province.id"
                :label="province.name"
                :value="province.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="所属城市">
            <el-select v-model="form.city_id" placeholder="请选择城市">
              <el-option
                v-for="city in cities"
                :key="city.id"
                :label="city.name"
                :value="city.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="医院地址">
            <el-input v-model="form.address" placeholder="请输入医院地址" />
          </el-form-item>
          <el-form-item label="联系电话">
            <el-input v-model="form.phone" placeholder="请输入联系电话" />
          </el-form-item>
          <el-form-item label="医院图片">
            <el-upload
              class="upload-demo"
              action="/api/v1/upload/image"
              :on-success="handleImageUpload"
              :on-error="handleImageError"
              :file-list="fileList"
              :limit="1"
              :auto-upload="true"
            >
              <el-button type="primary">上传图片</el-button>
              <template #tip>
                <div class="el-upload__tip">
                  只能上传jpg/png文件，且不超过2MB
                </div>
              </template>
            </el-upload>
          </el-form-item>
          <el-form-item label="设备型号">
            <el-input v-model="form.device" placeholder="请输入设备型号" />
          </el-form-item>
          <el-form-item label="petct价格">
            <el-input v-model="form.price" type="number" placeholder="请输入价格" />
          </el-form-item>
          <el-form-item label="医院优势">
            <el-input v-model="form.advantage" type="textarea" rows="3" placeholder="请输入医院优势" />
          </el-form-item>
        </el-tab-pane>
        
        <!-- 科室介绍 -->
        <el-tab-pane label="科室介绍" name="department">
          <el-form-item label="科室介绍">
            <div style="border: 1px solid #dcdfe6; border-radius: 4px;">
              <Editor
                v-model="form.ks_intro"
                :config="editorConfig"
                style="height: 300px; overflow-y: auto;"
              />
            </div>
          </el-form-item>
        </el-tab-pane>
        
        <!-- 医院介绍 -->
        <el-tab-pane label="医院介绍" name="hospital">
          <el-form-item label="医院介绍">
            <div style="border: 1px solid #dcdfe6; border-radius: 4px;">
              <Editor
                v-model="form.content"
                :config="editorConfig"
                style="height: 300px; overflow-y: auto;"
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
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import TagInput from '../../../components/TagInput.vue'
import request from '../../../utils/request'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import '@wangeditor/editor/dist/css/style.css'

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
      name: '',
      level: '',
      province_id: '',
      city_id: '',
      address: '',
      phone: '',
      cover: '',
      device: '',
      price: '',
      advantage: '',
      ks_intro: '',
      content: '',
      seo_title: '',
      seo_keywords: '',
      seo_description: '',
      tags: ''
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

// 编辑器配置
const editorConfig = {
  placeholder: '请输入内容...',
  MENU_CONF: {
    uploadImage: {
      server: '/api/v1/upload/image',
      fieldName: 'file',
      maxFileSize: 2 * 1024 * 1024, // 2MB
      accept: ['jpg', 'jpeg', 'png']
    }
  }
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
  if (provinceId) {
    fetchCities(provinceId)
  } else {
    cities.value = []
  }
}

// 图片上传成功处理
const handleImageUpload = (response, uploadFile) => {
  if (response.code === 200 && response.data) {
    form.value.cover = response.data.url
    fileList.value = [{ url: response.data.url }]
  }
}

// 图片上传失败处理
const handleImageError = (error) => {
  console.error('图片上传失败:', error)
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
    fileList.value = [{ url: newVal.cover }]
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
  // 只传递city_id，不传递province_id
  const formData = { ...form.value }
  delete formData.province_id
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
    fileList.value = [{ url: form.value.cover }]
  }
})
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
}

.upload-demo {
  margin-top: 10px;
}
</style>