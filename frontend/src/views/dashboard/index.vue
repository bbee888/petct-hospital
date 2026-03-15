<template>
  <div class="dashboard">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>仪表盘</span>
        </div>
      </template>
      <div class="dashboard-stats">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-number">{{ sitesCount }}</div>
                <div class="stat-label">站点数量</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-number">{{ hospitalsCount }}</div>
                <div class="stat-label">医院数量</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-number">{{ articlesCount }}</div>
                <div class="stat-label">文章数量</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-number">{{ appointmentsCount }}</div>
                <div class="stat-label">预约数量</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
      <div class="recent-activity">
        <h3>最近活动</h3>
        <el-table :data="recentActivities" style="width: 100%">
          <el-table-column prop="type" label="类型" width="100" />
          <el-table-column prop="content" label="内容" />
          <el-table-column prop="time" label="时间" width="180" />
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '../../utils/request'

const sitesCount = ref(0)
const hospitalsCount = ref(0)
const articlesCount = ref(0)
const appointmentsCount = ref(0)
const recentActivities = ref([])

const fetchStats = async () => {
  try {
    // 这里应该调用实际的API获取统计数据
    // 暂时使用模拟数据
    sitesCount.value = 2
    hospitalsCount.value = 15
    articlesCount.value = 42
    appointmentsCount.value = 89
    
    recentActivities.value = [
      { type: '文章', content: '新增文章：心脏病预防指南', time: '2024-01-15 14:30' },
      { type: '医院', content: '新增医院：北京协和医院', time: '2024-01-14 10:15' },
      { type: '预约', content: '新增预约：张医生 - 2024-01-20', time: '2024-01-13 09:45' },
      { type: '站点', content: '新增站点：上海分站', time: '2024-01-12 16:20' }
    ]
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dashboard-stats {
  margin-bottom: 30px;
}

.stat-card {
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-content {
  text-align: center;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

.recent-activity {
  margin-top: 30px;
}

.recent-activity h3 {
  margin-bottom: 15px;
  font-size: 16px;
  color: #303133;
}
</style>