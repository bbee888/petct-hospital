<template>
  <el-dialog
    v-model="dialogVisible"
    title="预约详情"
    width="600px"
  >
    <el-form :model="appointmentData" label-width="100px">
      <el-form-item label="患者姓名">
        {{ appointmentData.username }}
      </el-form-item>
      <el-form-item label="联系电话">
        {{ appointmentData.phone }}
      </el-form-item>
      <el-form-item label="身份证号">
        {{ appointmentData.idcard }}
      </el-form-item>
      <el-form-item label="性别">
        {{ appointmentData.sex }}
      </el-form-item>
      <el-form-item label="预约医院">
        {{ appointmentData.hospital_name }}
      </el-form-item>
      <el-form-item label="预约日期">
        {{ appointmentData.appoint_date }}
      </el-form-item>
      <el-form-item label="病情介绍">
        {{ appointmentData.intro || '无' }}
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="appointmentData.status" @change="handleStatusChange">
          <el-option label="待确认" value="pending" />
          <el-option label="已确认" value="confirmed" />
          <el-option label="已完成" value="completed" />
          <el-option label="已取消" value="cancelled" />
        </el-select>
      </el-form-item>
      <el-form-item label="创建时间">
        {{ appointmentData.created_at }}
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">关闭</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  appointment: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:visible', 'status-change'])

const dialogVisible = ref(props.visible)
const appointmentData = ref({ ...props.appointment })

watch(() => props.visible, (newVal) => {
  dialogVisible.value = newVal
})

watch(() => props.appointment, (newVal) => {
  appointmentData.value = { ...newVal }
}, { deep: true })

watch(() => dialogVisible.value, (newVal) => {
  emit('update:visible', newVal)
})

const handleStatusChange = () => {
  emit('status-change', appointmentData.value)
}
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>
