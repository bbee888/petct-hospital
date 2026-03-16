<template>
  <div class="dashboard">
    <!-- 仪表盘标题 -->
    <div class="dashboard-header">
      <h1 class="dashboard-title">仪表盘</h1>
      <p class="dashboard-subtitle">欢迎回来,查看系统统计和预约信息</p>
    </div>

    <!-- 统计信息模块 -->
    <div class="section">
      <div class="section-header">
        <h2 class="section-title">
          <svg class="section-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5M9 11.25v1.5M12 9v3.75m3-6v6" />
          </svg>
          统计信息
        </h2>
      </div>

      <div class="stats-grid">
        <div class="stat-card" @click="navigateTo('sites')">
          <div class="stat-icon stat-icon-sites">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ sitesCount }}</div>
            <div class="stat-label">站点数量</div>
            <div class="stat-trend" :class="sitesTrend > 0 ? 'trend-up' : 'trend-down'">
              <svg v-if="sitesTrend > 0" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6L9 12.75l4.286-4.286a11.948 11.948 0 015.818-5.518l2.74-1.22m0 0l-5.94-2.281m5.94 2.281l-2.28 5.941" />
              </svg>
              <span>{{ Math.abs(sitesTrend) }}%</span>
            </div>
          </div>
        </div>

        <div class="stat-card" @click="navigateTo('hospitals')">
          <div class="stat-icon stat-icon-hospitals">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ hospitalsCount }}</div>
            <div class="stat-label">医院数量</div>
            <div class="stat-trend" :class="hospitalsTrend > 0 ? 'trend-up' : 'trend-down'">
              <svg v-if="hospitalsTrend > 0" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6L9 12.75l4.286-4.286a11.948 11.948 0 015.818-5.518l2.74-1.22m0 0l-5.94-2.281m5.94 2.281l-2.28 5.941" />
              </svg>
              <span>{{ Math.abs(hospitalsTrend) }}%</span>
            </div>
          </div>
        </div>

        <div class="stat-card" @click="navigateTo('articles')">
          <div class="stat-icon stat-icon-articles">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ articlesCount }}</div>
            <div class="stat-label">文章数量</div>
            <div class="stat-trend" :class="articlesTrend > 0 ? 'trend-up' : 'trend-down'">
              <svg v-if="articlesTrend > 0" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6L9 12.75l4.286-4.286a11.948 11.948 0 015.818-5.518l2.74-1.22m0 0l-5.94-2.281m5.94 2.281l-2.28 5.941" />
              </svg>
              <span>{{ Math.abs(articlesTrend) }}%</span>
            </div>
          </div>
        </div>

        <div class="stat-card" @click="navigateTo('appointments')">
          <div class="stat-icon stat-icon-appointments">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5m-9-6h.008v.008H12v-.008zM12 15h.008v.008H12V15zm0 2.25h.008v.008H12v-.008zM9.75 15h.008v.008H9.75V15zm0 2.25h.008v.008H9.75v-.008zM7.5 15h.008v.008H7.5V15zm0 2.25h.008v.008H7.5v-.008zm6.75-4.5h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008V15zm0 2.25h.008v.008h-.008v-.008zm2.25-4.5h.008v.008H16.5v-.008zm0 2.25h.008v.008H16.5V15z" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ appointmentsCount }}</div>
            <div class="stat-label">预约数量</div>
            <div class="stat-trend" :class="appointmentsTrend > 0 ? 'trend-up' : 'trend-down'">
              <svg v-if="appointmentsTrend > 0" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6L9 12.75l4.286-4.286a11.948 11.948 0 015.818-5.518l2.74-1.22m0 0l-5.94-2.281m5.94 2.281l-2.28 5.941" />
              </svg>
              <span>{{ Math.abs(appointmentsTrend) }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 预约信息模块 -->
    <div class="section">
      <div class="section-header">
        <h2 class="section-title">
          <svg class="section-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5m-9-6h.008v.008H12v-.008zM12 15h.008v.008H12V15zm0 2.25h.008v.008H12v-.008zM9.75 15h.008v.008H9.75V15zm0 2.25h.008v.008H9.75v-.008zM7.5 15h.008v.008H7.5V15zm0 2.25h.008v.008H7.5v-.008zm6.75-4.5h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008V15zm0 2.25h.008v.008h-.008v-.008zm2.25-4.5h.008v.008H16.5v-.008zm0 2.25h.008v.008H16.5V15z" />
          </svg>
          预约信息
        </h2>
        <el-button type="primary" size="small" @click="navigateTo('appointments')">查看全部</el-button>
      </div>

      <div class="appointments-container">


        <!-- 最近预约列表 -->
        <div class="recent-appointments">
          <h3 class="recent-title">最近预约</h3>
          <div class="appointments-list">
            <div v-if="recentAppointments.length === 0" class="empty-state">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
              </svg>
              <p>暂无预约记录</p>
            </div>
            <div v-for="appointment in recentAppointments" :key="appointment.id" class="appointment-card">
              <div class="appointment-info">
                <div class="appointment-header">
                  <span class="appointment-name">{{ appointment.username }}</span>
                  <el-tag :type="getStatusType(appointment.status)" size="small">
                    {{ getStatusText(appointment.status) }}
                  </el-tag>
                </div>
                <div class="appointment-details">
                  <span class="detail-item">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z" />
                    </svg>
                    {{ appointment.phone }}
                  </span>
                  <span class="detail-item">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {{ appointment.appoint_date }}
                  </span>
                  <span class="detail-item">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
                    </svg>
                    {{ appointment.hospital_name }}
                  </span>
                </div>
              </div>
              <div class="appointment-actions">
                <el-button size="small" @click="handleViewAppointment(appointment)">查看</el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '../../utils/request'

const router = useRouter()

// 统计数据
const sitesCount = ref(0)
const hospitalsCount = ref(0)
const articlesCount = ref(0)
const appointmentsCount = ref(0)
const sitesTrend = ref(0)
const hospitalsTrend = ref(0)
const articlesTrend = ref(0)
const appointmentsTrend = ref(0)

// 预约数据
const pendingCount = ref(0)
const confirmedCount = ref(0)
const completedCount = ref(0)
const cancelledCount = ref(0)
const recentAppointments = ref([])

// 加载状态
const loading = ref(false)

// 导航到指定页面
const navigateTo = (path) => {
  router.push(`/${path}`)
}

// 获取状态类型
const getStatusType = (status) => {
  const typeMap = {
    pending: 'warning',
    confirmed: 'success',
    completed: 'info',
    cancelled: 'danger'
  }
  return typeMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const textMap = {
    pending: '待确认',
    confirmed: '已确认',
    completed: '已完成',
    cancelled: '已取消'
  }
  return textMap[status] || status
}

// 查看预约详情
const handleViewAppointment = (appointment) => {
  router.push(`/appointments`)
}

// 获取统计数据
const fetchStats = async () => {
  try {
    loading.value = true

    // 调用后端API获取统计概览
    const overviewResponse = await request.get('/v1/stats/overview')
    if (overviewResponse.data) {
      sitesCount.value = overviewResponse.data.sites_count || 0
      hospitalsCount.value = overviewResponse.data.hospitals_count || 0
      articlesCount.value = overviewResponse.data.articles_count || 0
      appointmentsCount.value = overviewResponse.data.appointments_count || 0

      sitesTrend.value = overviewResponse.data.sites_trend || 0
      hospitalsTrend.value = overviewResponse.data.hospitals_trend || 0
      articlesTrend.value = overviewResponse.data.articles_trend || 0
      appointmentsTrend.value = overviewResponse.data.appointments_trend || 0
    }

    // 调用后端API获取预约状态统计
    const statusResponse = await request.get('/v1/stats/appointments/status')
    if (statusResponse.data) {
      pendingCount.value = statusResponse.data.pending_count || 0
      confirmedCount.value = statusResponse.data.confirmed_count || 0
      completedCount.value = statusResponse.data.completed_count || 0
      cancelledCount.value = statusResponse.data.cancelled_count || 0
    }

    // 调用后端API获取最近预约
    const recentResponse = await request.get('/v1/stats/appointments/recent?limit=5')
    if (recentResponse.data && recentResponse.data.appointments) {
      // 隐藏手机号中间4位
      recentAppointments.value = recentResponse.data.appointments.map(apt => ({
        ...apt,
        phone: apt.phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
      }))
    }

  } catch (error) {
    console.error('获取统计数据失败:', error)
    ElMessage.error('获取统计数据失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.dashboard {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

/* 仪表盘标题 */
.dashboard-header {
  margin-bottom: 32px;
}

.dashboard-title {
  font-size: 32px;
  font-weight: 700;
  color: #164E63;
  margin: 0 0 8px 0;
  line-height: 1.2;
}

.dashboard-subtitle {
  font-size: 14px;
  color: #64748B;
  margin: 0;
}

/* 模块通用样式 */
.section {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05),
              0 2px 4px -1px rgba(0, 0, 0, 0.03);
  transition: all 0.3s ease;
}

.section:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08),
              0 4px 6px -2px rgba(0, 0, 0, 0.04);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 600;
  color: #164E63;
  margin: 0;
}

.section-icon {
  width: 24px;
  height: 24px;
  color: #0891B2;
}

/* 统计卡片网格 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}

.stat-card {
  background: linear-gradient(135deg, #ECFEFF 0%, #FFFFFF 100%);
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #E5E7EB;
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #0891B2, #22D3EE);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px -8px rgba(8, 145, 178, 0.2);
  border-color: #0891B2;
}

.stat-card:hover::before {
  opacity: 1;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon svg {
  width: 28px;
  height: 28px;
  color: white;
}

.stat-icon-sites {
  background: linear-gradient(135deg, #0891B2, #22D3EE);
}

.stat-icon-hospitals {
  background: linear-gradient(135deg, #059669, #10B981);
}

.stat-icon-articles {
  background: linear-gradient(135deg, #7C3AED, #8B5CF6);
}

.stat-icon-appointments {
  background: linear-gradient(135deg, #EA580C, #F97316);
}

.stat-content {
  flex: 1;
  min-width: 0;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: #164E63;
  line-height: 1.2;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #64748B;
  margin-bottom: 8px;
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  font-weight: 500;
}

.stat-trend svg {
  width: 16px;
  height: 16px;
}

.trend-up {
  color: #059669;
}

.trend-down {
  color: #DC2626;
}

/* 预约容器 */
.appointments-container {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 24px;
}

@media (max-width: 1024px) {
  .appointments-container {
    grid-template-columns: 1fr;
  }
}


.status-item {
  background: #F8FAFC;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  transition: all 0.3s ease;
}

.status-item:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.status-count {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
  line-height: 1.2;
}

.status-label {
  font-size: 13px;
  color: #64748B;
  font-weight: 500;
}

.status-pending .status-count {
  color: #F59E0B;
}

.status-confirmed .status-count {
  color: #10B981;
}

.status-completed .status-count {
  color: #0891B2;
}

.status-cancelled .status-count {
  color: #DC2626;
}

/* 最近预约列表 */
.recent-appointments {
  flex: 1;
}

.recent-title {
  font-size: 16px;
  font-weight: 600;
  color: #164E63;
  margin: 0 0 16px 0;
}

.appointments-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.empty-state {
  text-align: center;
  padding: 48px 24px;
  color: #94A3B8;
}

.empty-state svg {
  width: 48px;
  height: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state p {
  margin: 0;
  font-size: 14px;
}

.appointment-card {
  background: #F8FAFC;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.appointment-card:hover {
  background: #F1F5F9;
  border-color: #E2E8F0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.appointment-info {
  flex: 1;
  min-width: 0;
}

.appointment-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.appointment-name {
  font-size: 15px;
  font-weight: 600;
  color: #164E63;
}

.appointment-details {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #64748B;
}

.detail-item svg {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}

.appointment-actions {
  flex-shrink: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .dashboard {
    padding: 16px;
  }

  .dashboard-title {
    font-size: 24px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .section {
    padding: 20px;
  }

  .appointment-details {
    flex-direction: column;
    gap: 8px;
  }

  .appointment-card {
    flex-direction: column;
    align-items: flex-start;
  }

  .appointment-actions {
    width: 100%;
  }

  .appointment-actions .el-button {
    width: 100%;
  }
}
</style>