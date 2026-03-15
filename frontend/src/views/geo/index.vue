<template>
  <div class="geo-list">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>省份城市管理</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleAddDistrict" style="margin-left: 10px;">新增区县</el-button>
            <el-button type="primary" @click="handleAddCity" style="margin-left: 10px;">新增城市</el-button>
            <el-button type="primary" @click="handleAddProvince" style="margin-left: 10px;">新增省份</el-button>
          </div>
        </div>
      </template>
      
      <el-tree
        ref="treeRef"
        :data="treeData"
        :props="treeProps"
        node-key="id"
        default-expand-all
        highlight-current
      >
        <template #default="{ node, data }">
          <div class="custom-tree-node">
            <span class="node-label">
              <el-icon v-if="data.type === 'province'" class="province-icon">
                <Location />
              </el-icon>
              <el-icon v-else-if="data.type === 'city'" class="city-icon">
                <Position />
              </el-icon>
              <el-icon v-else class="district-icon">
                <OfficeBuilding />
              </el-icon>
              {{ node.label }}
            </span>
            <span class="node-actions">
              <el-button type="primary" link size="small" @click="handleEdit(node, data)">
                编辑
              </el-button>
              <el-button type="danger" link size="small" @click="handleDelete(node, data)">
                删除
              </el-button>
            </span>
          </div>
        </template>
      </el-tree>
    </el-card>

    <!-- 省份编辑对话框 -->
    <ProvinceForm
      v-model:visible="provinceDialogVisible"
      :title="provinceDialogTitle"
      :form-data="provinceForm"
      @save="handleSaveProvince"
    />

    <!-- 城市编辑对话框 -->
    <CityForm
      v-model:visible="cityDialogVisible"
      :title="cityDialogTitle"
      :form-data="cityForm"
      :provinces="provinces"
      @save="handleSaveCity"
    />

    <!-- 区县编辑对话框 -->
    <DistrictForm
      v-model:visible="districtDialogVisible"
      :title="districtDialogTitle"
      :form-data="districtForm"
      :cities="cities"
      @save="handleSaveDistrict"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { geoApi } from '../../api/geo'
import ProvinceForm from './components/ProvinceForm.vue'
import CityForm from './components/CityForm.vue'
import DistrictForm from './components/DistrictForm.vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Location, Position, OfficeBuilding } from '@element-plus/icons-vue'

const treeRef = ref(null)
const treeData = ref([])
const provinces = ref([])
const cities = ref([])

const treeProps = {
  children: 'children',
  label: 'name'
}

const provinceDialogVisible = ref(false)
const provinceDialogTitle = ref('新增省份')
const provinceForm = ref({ id: null, name: '', sort: 0 })

const cityDialogVisible = ref(false)
const cityDialogTitle = ref('新增城市')
const cityForm = ref({ id: null, province_id: null, name: '' })

const districtDialogVisible = ref(false)
const districtDialogTitle = ref('新增区县')
const districtForm = ref({ id: null, city_id: null, name: '' })

const fetchTreeData = async () => {
  try {
    const response = await geoApi.getGeoTree()
    treeData.value = response.data || []
  } catch (error) {
    console.error('获取树形数据失败:', error)
    ElMessage.error('获取数据失败，请稍后重试')
  }
}

const fetchProvinces = async () => {
  try {
    const response = await geoApi.getProvinces()
    provinces.value = response.data || []
  } catch (error) {
    console.error('获取省份列表失败:', error)
  }
}

const fetchCities = async () => {
  try {
    const response = await geoApi.getCities()
    cities.value = response.data || []
  } catch (error) {
    console.error('获取城市列表失败:', error)
  }
}

const handleAddProvince = () => {
  provinceDialogTitle.value = '新增省份'
  provinceForm.value = { id: null, name: '', sort: 0 }
  provinceDialogVisible.value = true
}

const handleAddCity = () => {
  cityDialogTitle.value = '新增城市'
  cityForm.value = { id: null, province_id: null, name: '' }
  cityDialogVisible.value = true
}

const handleAddDistrict = () => {
  districtDialogTitle.value = '新增区县'
  districtForm.value = { id: null, city_id: null, name: '' }
  districtDialogVisible.value = true
}

const handleEdit = (node, data) => {
  console.log('编辑数据:', data)
  if (data.type === 'province') {
    provinceDialogTitle.value = '编辑省份'
    provinceForm.value = { id: data.id, name: data.name, sort: data.sort || 0 }
    provinceDialogVisible.value = true
  } else if (data.type === 'city') {
    cityDialogTitle.value = '编辑城市'
    const parentNode = findParentNode(treeData.value, data.id)
    console.log('父节点:', parentNode)
    const province_id = parentNode ? Number(parentNode.id) : ''
    console.log('设置province_id:', province_id)
    cityForm.value = { id: data.id, province_id: province_id, name: data.name }
    console.log('cityForm:', cityForm.value)
    cityDialogVisible.value = true
  } else {
    districtDialogTitle.value = '编辑区县'
    const parentCity = findParentCityNode(treeData.value, data.id)
    const city_id = parentCity ? Number(parentCity.id) : ''
    districtForm.value = { id: data.id, city_id: city_id, name: data.name }
    districtDialogVisible.value = true
  }
}

const findParentNode = (nodes, childId) => {
  for (const node of nodes) {
    if (node.children && node.children.some(child => child.id === childId)) {
      return node
    }
    if (node.children) {
      const found = findParentNode(node.children, childId)
      if (found) return found
    }
  }
  return null
}

const findParentCityNode = (nodes, districtId) => {
  for (const province of nodes) {
    if (province.children) {
      for (const city of province.children) {
        if (city.children && city.children.some(district => district.id === districtId)) {
          return city
        }
      }
    }
  }
  return null
}

const handleDelete = async (node, data) => {
  const typeMap = {
    'province': '省份',
    'city': '城市',
    'district': '区县'
  }
  const typeName = typeMap[data.type]
  try {
    await ElMessageBox.confirm(`确定要删除该${typeName}吗？删除后无法恢复。`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    if (data.type === 'province') {
      await geoApi.deleteProvince(data.id)
    } else if (data.type === 'city') {
      await geoApi.deleteCity(data.id)
    } else {
      await geoApi.deleteDistrict(data.id)
    }
    
    ElMessage.success(`${typeName}删除成功`)
    fetchTreeData()
    fetchProvinces()
    fetchCities()
  } catch (error) {
    if (error !== 'cancel') {
      console.error(`删除${typeName}失败:`, error)
      ElMessage.error(error.response?.data?.detail || `删除${typeName}失败，请稍后重试`)
    }
  }
}

const handleSaveProvince = async (formData) => {
  try {
    if (formData.id) {
      await geoApi.updateProvince(formData.id, formData)
      ElMessage.success('省份更新成功')
    } else {
      await geoApi.createProvince(formData)
      ElMessage.success('省份创建成功')
    }
    provinceDialogVisible.value = false
    fetchTreeData()
    fetchProvinces()
  } catch (error) {
    console.error('保存省份失败:', error)
    ElMessage.error(error.response?.data?.detail || '保存省份失败，请稍后重试')
  }
}

const handleSaveCity = async (formData) => {
  try {
    if (formData.id) {
      await geoApi.updateCity(formData.id, formData)
      ElMessage.success('城市更新成功')
    } else {
      await geoApi.createCity(formData)
      ElMessage.success('城市创建成功')
    }
    cityDialogVisible.value = false
    fetchTreeData()
    fetchCities()
  } catch (error) {
    console.error('保存城市失败:', error)
    ElMessage.error(error.response?.data?.detail || '保存城市失败，请稍后重试')
  }
}

const handleSaveDistrict = async (formData) => {
  try {
    if (formData.id) {
      await geoApi.updateDistrict(formData.id, formData)
      ElMessage.success('区县更新成功')
    } else {
      await geoApi.createDistrict(formData)
      ElMessage.success('区县创建成功')
    }
    districtDialogVisible.value = false
    fetchTreeData()
  } catch (error) {
    console.error('保存区县失败:', error)
    ElMessage.error(error.response?.data?.detail || '保存区县失败，请稍后重试')
  }
}

onMounted(() => {
  fetchTreeData()
  fetchProvinces()
  fetchCities()
})
</script>

<style scoped>
.geo-list {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
}

.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}

.node-label {
  display: flex;
  align-items: center;
  gap: 6px;
}

.province-icon {
  color: #409eff;
  font-size: 16px;
}

.city-icon {
  color: #67c23a;
  font-size: 14px;
}

.district-icon {
  color: #e6a23c;
  font-size: 12px;
}

.node-actions {
  display: flex;
  gap: 8px;
}
</style>
