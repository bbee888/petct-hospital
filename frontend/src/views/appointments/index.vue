<template>
  <div class="appointment-list">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>预约管理</span>
        </div>
      </template>
      <el-table :data="appointments" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="患者姓名" width="100" />
        <el-table-column prop="phone" label="联系电话" width="130" />
        <el-table-column prop="idcard" label="身份证" width="180" />
        <el-table-column prop="sex" label="性别" width="80" />
        <el-table-column prop="hospital_name" label="预约医院" width="150" />
        <el-table-column prop="appoint_date" label="预约日期" width="120" />
        <el-table-column prop="intro" label="病情介绍" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="scope">
            <el-select v-model="scope.row.status" @change="handleStatusChange(scope.row)" size="small">
              <el-option label="待确认" value="pending" />
              <el-option label="已确认" value="confirmed" />
              <el-option label="已完成" value="completed" />
              <el-option label="已取消" value="cancelled" />
            </el-select>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleView(scope.row)">查看</el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 预约详情对话框组件 -->
    <AppointmentView
      v-model:visible="dialogVisible"
      :appointment="currentAppointment"
      @status-change="handleStatusChange"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { appointmentsApi } from '../../api/appointments'
import AppointmentView from './components/AppointmentView.vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const appointments = ref([])
const dialogVisible = ref(false)
const currentAppointment = ref({})

const fetchAppointments = async () => {
  try {
    const response = await appointmentsApi.getAppointments()
    appointments.value = response.data || []
  } catch (error) {
    console.error('获取预约列表失败:', error)
    ElMessage.error('获取预约列表失败，请稍后重试')
  }
}

const handleView = (row) => {
  currentAppointment.value = { ...row }
  dialogVisible.value = true
}

const handleStatusChange = async (row) => {
  try {
    await appointmentsApi.updateAppointment(row.id, { status: row.status })
    ElMessage.success('状态更新成功')
  } catch (error) {
    console.error('更新预约状态失败:', error)
    ElMessage.error('更新预约状态失败，请稍后重试')
    fetchAppointments()
  }
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该预约吗？删除后无法恢复。', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await appointmentsApi.deleteAppointment(id)
    ElMessage.success('预约删除成功')
    fetchAppointments()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除预约失败:', error)
      ElMessage.error('删除预约失败，请稍后重试')
    }
  }
}

onMounted(() => {
  fetchAppointments()
})
</script>

<style scoped>
.appointment-list {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
