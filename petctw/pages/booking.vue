<template>
  <div class="min-h-screen bg-gray-50 pb-20">
    <!-- 顶部导航栏 -->
    <header class="bg-white px-4 py-3 sticky top-0 z-30">
      <div class="flex items-center gap-3">
        <NuxtLink to="/" class="w-8 h-8 flex items-center justify-center">
          <svg class="w-5 h-5 text-gray-600" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
          </svg>
        </NuxtLink>
        <h1 class="text-lg font-semibold text-gray-800">PET-CT预约</h1>
      </div>
    </header>

    <!-- 预约提示栏 -->
    <div class="px-4 mt-4">
      <div class="bg-blue-50 border-l-4 border-primary rounded-r-lg p-3">
        <div class="flex items-start gap-2">
          <svg class="w-5 h-5 text-primary flex-shrink-0 mt-0.5" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
          </svg>
          <div>
            <p class="text-sm font-medium text-primary">预约须知</p>
            <p class="text-xs text-gray-600 mt-1">提交预约后，工作人员将在30分钟内与您联系确认具体检查时间和注意事项</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 已选医院信息 -->
    <div class="px-4 mt-4">
      <div class="bg-white rounded-xl shadow-sm p-4">
        <div class="flex items-center justify-between mb-3">
          <span class="text-sm font-semibold text-gray-800">已选医院</span>
          <NuxtLink to="/hospitals" class="text-sm text-primary">更换</NuxtLink>
        </div>
        
        <!-- 加载医院信息 -->
        <div v-if="selectedHospital" class="flex gap-3">
          <img 
            :src="selectedHospital.image || 'https://prototype-prod-1254106194.cos.ap-beijing.myqcloud.com/prototype/default.jpg'" 
            alt="医院图片" 
            class="w-16 h-15 object-cover rounded-lg flex-shrink-0" 
          />
          <div class="flex-1 min-w-0">
            <h3 class="text-base font-semibold text-gray-800">{{ selectedHospital.title }}</h3>
            <div class="flex items-center gap-1 text-gray-400 text-xs mt-1">
              <svg class="w-3 h-3" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
              </svg>
              <span>{{ selectedHospital.province_name || '' }} {{ selectedHospital.city_name || '' }} {{ selectedHospital.address || '' }}</span>
            </div>
            <div class="flex items-center gap-1 mt-1">
              <span class="text-xs text-gray-500">检查费用：</span>
              <span class="text-lg font-bold text-red-500">¥{{ selectedHospital.price || '待定' }}</span>
            </div>
          </div>
        </div>
        
        <!-- 未选择医院 -->
        <div v-else class="text-center py-4">
          <NuxtLink to="/hospitals" class="text-primary text-sm">请先选择医院</NuxtLink>
        </div>
      </div>
    </div>

    <!-- 表单区域 -->
    <div class="px-4 mt-4">
      <div class="bg-white rounded-xl shadow-sm p-4">
        <h3 class="text-sm font-semibold text-gray-800 mb-4">填写预约信息</h3>

        <!-- 体检人姓名 -->
        <div class="mb-4">
          <label class="text-sm font-medium text-gray-800">
            <span class="text-red-500">*</span> 体检人姓名
          </label>
          <input 
            v-model="form.username"
            type="text" 
            placeholder="请输入体检人姓名" 
            class="w-full mt-2 px-3 py-2.5 border border-gray-200 rounded-lg bg-gray-50 text-sm focus:outline-none focus:border-primary" 
          />
        </div>

        <!-- 联系电话 -->
        <div class="mb-4">
          <label class="text-sm font-medium text-gray-800">
            <span class="text-red-500">*</span> 联系电话
          </label>
          <input 
            v-model="form.phone"
            type="tel" 
            placeholder="请输入联系电话" 
            class="w-full mt-2 px-3 py-2.5 border border-gray-200 rounded-lg bg-gray-50 text-sm focus:outline-none focus:border-primary" 
          />
        </div>

        <!-- 身份证号 -->
        <div class="mb-4">
          <label class="text-sm font-medium text-gray-800">
            <span class="text-red-500">*</span> 身份证号
          </label>
          <input 
            v-model="form.idcard"
            type="text" 
            placeholder="请输入身份证号码" 
            class="w-full mt-2 px-3 py-2.5 border border-gray-200 rounded-lg bg-gray-50 text-sm focus:outline-none focus:border-primary" 
          />
          <p class="text-xs text-gray-400 mt-1">身份证号用于医院登记和医保结算，我们将严格保护您的信息安全</p>
        </div>

        <!-- 性别 -->
        <div class="mb-4">
          <label class="text-sm font-medium text-gray-800">
            <span class="text-red-500">*</span> 性别
          </label>
          <div class="flex gap-3 mt-2">
            <button 
              @click="form.sex = '男'"
              class="flex-1 flex items-center justify-center gap-2 py-2.5 border rounded-lg cursor-pointer"
              :class="form.sex === '男' ? 'border-primary bg-blue-50' : 'border-gray-200'"
            >
              <span 
                class="w-5 h-5 border-2 rounded-full flex items-center justify-center"
                :class="form.sex === '男' ? 'border-primary' : 'border-gray-300'"
              >
                <span v-if="form.sex === '男'" class="w-2.5 h-2.5 bg-primary rounded-full"></span>
              </span>
              <span 
                class="text-sm font-medium"
                :class="form.sex === '男' ? 'text-primary' : 'text-gray-600'"
              >男</span>
            </button>
            <button 
              @click="form.sex = '女'"
              class="flex-1 flex items-center justify-center gap-2 py-2.5 border rounded-lg cursor-pointer"
              :class="form.sex === '女' ? 'border-primary bg-blue-50' : 'border-gray-200'"
            >
              <span 
                class="w-5 h-5 border-2 rounded-full flex items-center justify-center"
                :class="form.sex === '女' ? 'border-primary' : 'border-gray-300'"
              >
                <span v-if="form.sex === '女'" class="w-2.5 h-2.5 bg-primary rounded-full"></span>
              </span>
              <span 
                class="text-sm font-medium"
                :class="form.sex === '女' ? 'text-primary' : 'text-gray-600'"
              >女</span>
            </button>
          </div>
        </div>

        <!-- 期望检查日期 -->
        <div class="mb-4">
          <label class="text-sm font-medium text-gray-800">
            <span class="text-red-500">*</span> 期望检查日期
          </label>
          <input 
            v-model="form.appoint_date"
            type="date" 
            class="w-full mt-2 px-3 py-2.5 border border-gray-200 rounded-lg bg-gray-50 text-sm focus:outline-none focus:border-primary"
          />
          <p class="text-xs text-gray-400 mt-1">我们将尽量为您安排所选日期，具体时间以医院确认为准</p>
        </div>

        <!-- 病情描述 -->
        <div class="mb-4">
          <label class="text-sm font-medium text-gray-800">病情描述（选填）</label>
          <textarea 
            v-model="form.intro"
            placeholder="请简要描述病情、检查目的等信息，有助于医生提前了解情况" 
            rows="4" 
            class="w-full mt-2 px-3 py-2.5 border border-gray-200 rounded-lg bg-gray-50 text-sm focus:outline-none focus:border-primary resize-none"
          ></textarea>
          <p class="text-xs text-gray-400 mt-1">您提供的信息仅用于医院安排检查，严格保密</p>
        </div>

        <!-- 用户协议 -->
        <div class="flex items-start gap-2 mb-6">
          <button 
            @click="agreed = !agreed"
            class="w-4 h-4 border border-gray-300 rounded mt-0.5 flex-shrink-0 flex items-center justify-center"
            :class="agreed ? 'bg-primary border-primary' : ''"
          >
            <svg v-if="agreed" class="w-3 h-3 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
            </svg>
          </button>
          <p class="text-xs text-gray-500">
            我已阅读并同意
            <span class="text-primary">《用户服务协议》</span>
            和
            <span class="text-primary">《隐私政策》</span>
            ，授权平台收集我的信息用于预约服务
          </p>
        </div>

        <!-- 提交按钮 -->
        <button 
          @click="submitAppointment"
          :disabled="submitting"
          class="w-full py-3 bg-primary text-white rounded-lg text-base font-semibold disabled:opacity-50"
        >
          {{ submitting ? '提交中...' : '提交预约申请' }}
        </button>
      </div>
    </div>

    <!-- 联系咨询区域 -->
    <div class="px-4 mt-4 pb-6">
      <div class="bg-white rounded-xl shadow-sm p-4">
        <div class="flex items-center justify-between mb-3">
          <span class="text-sm font-semibold text-gray-800">预约咨询电话</span>
          <a href="tel:400-887-9166" class="flex items-center gap-1 text-sm text-primary">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56-.35-.12-.74-.03-1.01.24l-1.57 1.97c-2.83-1.35-5.48-3.9-6.89-6.83l1.95-1.66c.27-.28.35-.67.24-1.02-.37-1.11-.56-2.3-.56-3.53 0-.54-.45-.99-.99-.99H4.19C3.65 3 3 3.24 3 3.99 3 13.28 10.73 21 20.01 21c.71 0 .99-.63.99-1.18v-3.45c0-.54-.45-.99-.99-.99z"/>
            </svg>
            <span>立即拨打</span>
          </a>
        </div>
        <p class="text-2xl font-bold text-primary mb-2">400-887-9166</p>
        <p class="text-xs text-gray-500">服务时间：周一至周日 8:00-22:00</p>
      </div>
    </div>

    <!-- 成功提示 -->
    <Teleport to="body">
      <div v-if="showSuccess" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center">
        <div class="bg-white w-full max-w-sm mx-4 rounded-xl p-6 text-center">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-green-500" viewBox="0 0 24 24" fill="currentColor">
              <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-800 mb-2">预约提交成功</h3>
          <p class="text-sm text-gray-500 mb-4">工作人员将在1个工作日内与您联系</p>
          <NuxtLink to="/" class="block w-full py-3 bg-primary text-white rounded-lg text-base font-semibold">
            返回首页
          </NuxtLink>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const { hospitalApi, appointmentApi } = await import('~/composables/useApi')

// 表单数据
const form = reactive({
  username: '',
  phone: '',
  idcard: '',
  sex: '男',
  appoint_date: '',
  intro: ''
})

const agreed = ref(false)
const submitting = ref(false)
const showSuccess = ref(false)
const selectedHospital = ref<any>(null)

// 获取URL中的医院ID
const hospitalId = route.query.hospital_id ? Number(route.query.hospital_id) : null

// 加载医院信息
async function loadHospital() {
  if (!hospitalId) return
  
  try {
    selectedHospital.value = await hospitalApi.getDetail(hospitalId)
  } catch (error) {
    console.error('加载医院失败:', error)
  }
}

// 提交预约
async function submitAppointment() {
  // 表单验证
  if (!form.username.trim()) {
    alert('请输入体检人姓名')
    return
  }
  if (!form.phone.trim()) {
    alert('请输入联系电话')
    return
  }
  if (!form.idcard.trim()) {
    alert('请输入身份证号')
    return
  }
  if (!form.appoint_date) {
    alert('请选择期望检查日期')
    return
  }
  if (!agreed.value) {
    alert('请阅读并同意用户服务协议')
    return
  }
  if (!hospitalId) {
    alert('请先选择医院')
    return
  }
  
  try {
    submitting.value = true
    
    await appointmentApi.create({
      hospital_id: hospitalId,
      username: form.username,
      phone: form.phone,
      idcard: form.idcard,
      sex: form.sex,
      appoint_date: form.appoint_date,
      intro: form.intro
    })
    
    showSuccess.value = true
  } catch (error: any) {
    alert(error.message || '提交失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadHospital()
})
</script>
