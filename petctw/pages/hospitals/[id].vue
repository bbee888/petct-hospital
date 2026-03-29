<template>
  <div class="min-h-screen bg-gray-50 pb-20">
    <!-- 加载状态 -->
    <div v-if="loading" class="flex items-center justify-center h-screen">
      <div class="inline-block w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
    </div>

    <template v-else-if="hospital">
      <!-- 顶部导航栏 -->
      <header class="fixed top-0 left-1/2 -translate-x-1/2 w-full max-w-[640px] z-40 px-4 pt-2">
        <div class="flex items-center justify-between">
          <button @click="router.back()" class="w-8 h-8 bg-black/30 rounded-full flex items-center justify-center">
            <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
            </svg>
          </button>
          <button class="w-8 h-8 bg-black/30 rounded-full flex items-center justify-center">
            <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92-1.31-2.92-2.92-2.92z"/>
            </svg>
          </button>
        </div>
      </header>

      <!-- 医院轮播图 -->
      <div class="h-56 bg-gray-200 relative">
        <img 
          :src="hospital.cover || 'https://prototype-prod-1254106194.cos.ap-beijing.myqcloud.com/prototype/default.jpg'" 
          alt="医院图片" 
          class="w-full h-full object-cover" 
        />
      </div>

      <!-- 基础信息区域 -->
      <div class="bg-white mx-4 -mt-8 rounded-xl p-4 card-shadow relative z-10">
        <div class="flex justify-between items-start mb-3">
          <div>
            <h1 class="text-xl font-bold text-gray-800 mb-2">{{ hospital.title }}</h1>
            <div class="flex gap-2">
              <span v-if="hospital.level" class="px-2 py-0.5 bg-blue-50 text-primary text-xs rounded">{{ hospital.level }}</span>
              <span v-if="hospital.is_insurance" class="px-2 py-0.5 bg-green-50 text-green-600 text-xs rounded">医保定点</span>
            </div>
          </div>
          <div class="text-right">
            <div class="flex items-center gap-1 justify-end">
              <svg class="w-4 h-4 text-yellow-500" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
              </svg>
              <span class="text-lg font-bold text-yellow-500">{{ hospital.rating || '5.0' }}</span>
            </div>
            <p class="text-xs text-gray-500">{{ hospital.reviews || 0 }}人评价</p>
          </div>
        </div>

        <div class="flex items-center gap-2 text-sm text-gray-600 mb-2">
          <svg class="w-4 h-4 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
          </svg>
          <span>{{ hospital.province_name || '' }} - {{ hospital.city_name || '' }} - {{ hospital.address || '' }}</span>
        </div>

        <div class="flex items-center gap-2 text-sm text-gray-600 mb-4">
          <svg class="w-4 h-4 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
            <path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z"/>
          </svg>
          <span>{{ hospital.device || 'GE Discovery' }}</span>
        </div>

        <!-- 价格区域 -->
        <div class="bg-blue-50 rounded-lg p-3 flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600">PET-CT检查费用</p>
            <div class="flex items-center gap-1">
              <span class="text-2xl font-bold text-red-500">¥{{ hospital.price || '待定' }}</span>
              <span class="text-xs text-gray-500">/次</span>
            </div>
          </div>
          <a :href="`tel:${hospital.phone || '400-887-9166'}`" class="px-4 py-2 bg-white border border-blue-200 text-primary rounded-lg text-sm font-medium flex items-center gap-1">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
            </svg>
            咨询底价
          </a>
        </div>
      </div>

      <!-- 医院优势 -->
      <div class="bg-white mx-4 mt-4 rounded-xl p-4 card-shadow">
        <div class="flex items-center gap-2 mb-3">
          <svg class="w-5 h-5 text-primary" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
          </svg>
          <h3 class="font-semibold text-gray-800">医院优势</h3>
        </div>
        <div class="text-sm text-gray-600">
          <div v-if="hospital.advantage" class="flex items-center gap-2">
            <span class="w-1.5 h-1.5 bg-green-500 rounded-full"></span>
            <span>{{ hospital.advantage }}</span>
          </div>
        </div>
      </div>

      <!-- Tab栏 -->
      <div class="bg-white mx-4 mt-4 rounded-xl overflow-hidden card-shadow">
        <div class="flex border-b">
          <button 
            v-for="tab in tabs" 
            :key="tab"
            class="flex-1 py-3 text-sm font-medium"
            :class="activeTab === tab ? 'text-primary border-b-2 border-primary' : 'text-gray-500'"
            @click="activeTab = tab"
          >
            {{ tab }}
          </button>
        </div>

        <!-- 医院介绍内容 -->
        <div v-if="activeTab === '医院介绍'" class="p-4">
          <div class="text-sm text-gray-600 leading-relaxed" v-html="hospital.content || '暂无医院介绍'"></div>
        </div>

        <!-- 科室介绍内容 -->
        <div v-if="activeTab === '科室介绍'" class="p-4">
          <div class="text-sm text-gray-600 leading-relaxed" v-html="hospital.ks_intro || '暂无科室介绍'"></div>
        </div>

        <!-- 预约须知内容 -->
        <div v-if="activeTab === '预约须知'" class="p-4">
          <div class="space-y-3 text-sm text-gray-600 whitespace-pre-line">
            <p>{{ hospital.title }}医生会详细交代检查相关注意事项，在检查当天请主动向{{ hospital.title }}医生询问。特需患者，{{ hospital.title }}医生会在患者检查前一两天，再次发送短信、或打电话告知检查注意事项。</p>
                            <p>⑴ 检查前需禁食4～6小时，可饮白开水，检查前晚清淡饮食，禁用高糖类、葡萄糖类药物(如：止咳糖浆等)。</p>
                            <p>⑵ 检查前请注意休息，避免剧烈运动。检查前一周内不宜行食道吞钡、胃肠道钡剂或钡剂灌肠造影检查。</p>
                            <p>⑶ 部分患者尤其是糖尿病患者需要做血糖浓度测定，血糖控制在11以下。有些糖尿病患者需要使用胰岛素，在预约时请事先说明，{{ hospital.title }}(影像科/放射科)医生将指导患者调整好血糖，避免影响检查。</p>
                            <p>⑷ 请携带齐病情相关资料备查(包括病志病史记录、治疗相关情况、影像学检查资料如CT、MRI、ECT等 、血清学检查、内窥镜检查等临床资料）。</p>
                            <p>⑸ 请勿穿戴有金属拉链、纽扣的衣裤前来检查。</p>
                            <p>⑹ 年老体弱者及幼儿必须由家属陪同，危重病人须由医务人员陪护。 女性受检者如正在妊娠或哺乳期，请提前告知医生。怀孕妇女、情绪不稳定者或急性持续痉挛者禁止做PET检查。</p>
                            <p>⑺ 检查过程中，切勿移动身体，以免影响检查效果。</p>
                            <p>⑻ 请提前1-2天预约检查，因故需改变检查时间，请至少提前一天通知。</p>
          </div>
        </div>
      </div>

      <!-- 底部预约栏 -->
      <div class="fixed bottom-0 left-1/2 -translate-x-1/2 w-full max-w-[640px] bg-white border-t border-gray-200 p-3 flex items-center gap-3 z-30">
        <a :href="`tel:${hospital.phone || '400-887-9166'}`" class="w-12 h-12 border border-blue-200 bg-blue-50 rounded-lg flex items-center justify-center">
          <svg class="w-5 h-5 text-primary" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
          </svg>
        </a>
        <NuxtLink :to="`/booking?hospital_id=${hospital.id}`" class="flex-1 bg-primary text-white py-3 rounded-lg text-base font-semibold text-center">
          立即预约检查
        </NuxtLink>
      </div>
    </template>

    <!-- 加载失败 -->
    <div v-else class="flex flex-col items-center justify-center h-screen text-gray-400">
      <svg class="w-16 h-16 mb-4" viewBox="0 0 24 24" fill="currentColor">
        <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.93 0 3.5 1.57 3.5 3.5S13.93 13 12 13s-3.5-1.57-3.5-3.5S10.07 6 12 6zm7 13H5v-.23c0-.62.28-1.2.76-1.58C7.47 15.82 9.64 15 12 15s4.53.82 6.24 2.19c.48.38.76.97.76 1.58V19z"/>
      </svg>
      <p>加载失败，请返回重试</p>
    </div>

    <!-- 同省合作医院推荐 -->
    <div v-if="provinceHospitals.length > 0" class="mx-4 mt-4 mb-20">
      <h3 class="text-base font-bold text-gray-800 mb-3">合作医院推荐</h3>
      <div class="bg-white rounded-xl overflow-hidden card-shadow">
        <NuxtLink 
          v-for="h in provinceHospitals" 
          :key="h.id"
          :to="`/hospitals/${h.id}`"
          class="flex items-center p-3 border-b last:border-b-0"
        >
          <img 
            :src="h.cover || 'https://prototype-prod-1254106194.cos.ap-beijing.myqcloud.com/prototype/default.jpg'" 
            class="w-16 h-16 rounded-lg object-cover"
          />
          <div class="ml-3 flex-1">
            <h4 class="text-sm font-medium text-gray-800">{{ h.title }}</h4>
            <p class="text-xs text-gray-500 mt-1">{{ h.province_name }} - {{ h.city_name }}</p>
            <div class="flex items-center gap-2 mt-1">
              <span v-if="h.level" class="px-2 py-0.5 bg-blue-50 text-primary text-xs rounded">{{ h.level }}</span>
            </div>
          </div>
          <svg class="w-5 h-5 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
          </svg>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const router = useRouter()
const route = useRoute()
const { hospitalApi } = await import('~/composables/useApi')

const loading = ref(true)
const hospital = ref<any>(null)
const provinceHospitals = ref<any[]>([])
const activeTab = ref('医院介绍')
const tabs = ['医院介绍', '科室介绍', '预约须知']

// 获取医院ID
const hospitalId = Number(route.params.id)

// 加载医院详情
async function loadHospital() {
  try {
    loading.value = true
    hospital.value = await hospitalApi.getDetail(hospitalId)
    
    // 加载同省合作医院
    if (hospital.value?.province_id) {
      const res = await hospitalApi.getProvinceHospitals(hospitalId)
      provinceHospitals.value = res.items || []
    }
  } catch (error) {
    console.error('加载医院详情失败:', error)
    hospital.value = null
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadHospital()
})
</script>
