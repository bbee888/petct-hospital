<template>
  <div class="article-edit">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>{{ isEdit ? '编辑文章' : '新增文章' }}</span>
        </div>
      </template>
      <el-form :model="form" label-width="100px">
        <el-form-item label="标题">
          <el-input v-model="form.title" placeholder="请输入文章标题" />
        </el-form-item>
        <el-form-item label="内容">
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="10"
            placeholder="请输入文章内容"
          />
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
      <div class="form-actions">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import request from '../../utils/request'
import TagInput from '../../components/TagInput.vue'

const route = useRoute()
const router = useRouter()
const id = route.params.id
const isEdit = computed(() => !!id)

const form = ref({
  id: '',
  title: '',
  content: '',
  site_domain: '',
  status: true,
  tags: ''
})

const fetchArticle = async () => {
  try {
    // 这里应该调用实际的API获取文章详情
    // 暂时使用模拟数据
    form.value = {
      id: id,
      title: '心脏病预防指南',
      content: '心脏病是一种常见的心血管疾病，预防心脏病需要注意以下几点：\n1. 保持健康的生活方式\n2. 合理饮食\n3. 适量运动\n4. 定期体检\n5. 控制血压和血糖',
      site_domain: 'localhost:8080',
      status: true,
      tags: '心脏病,预防,健康'
    }
  } catch (error) {
    console.error('获取文章详情失败:', error)
  }
}

const handleSave = async () => {
  try {
    // 这里应该调用实际的API保存文章
    console.log('保存文章:', form.value)
    router.push('/admin/articles')
  } catch (error) {
    console.error('保存文章失败:', error)
  }
}

const handleCancel = () => {
  router.push('/admin/articles')
}

onMounted(() => {
  if (isEdit.value) {
    fetchArticle()
  }
})
</script>

<style scoped>
.article-edit {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>