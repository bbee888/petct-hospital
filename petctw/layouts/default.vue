<template>
  <div class="min-h-screen bg-gray-50 pb-16">
    <slot />
    <!-- 底部导航栏 -->
    <nav class="fixed bottom-0 left-1/2 -translate-x-1/2 w-full max-w-[640px] bg-white border-t border-gray-200 safe-area-bottom z-50">
      <div class="flex justify-between items-center px-6 py-2">
        <NuxtLink 
          v-for="item in navItems" 
          :key="item.path"
          :to="item.path"
          class="flex flex-col items-center py-1"
          :class="isActive(item.path) ? 'text-primary' : 'text-gray-400'"
        >
          <component :is="item.icon" class="w-5 h-5" />
          <span class="text-[11px] mt-0.5" :class="isActive(item.path) ? 'text-primary font-medium' : ''">{{ item.label }}</span>
        </NuxtLink>
      </div>
    </nav>
  </div>
</template>

<script setup lang="ts">
import IconHome from '~/components/IconHome.vue'
import IconHospital from '~/components/IconHospital.vue'
import IconCalendar from '~/components/IconCalendar.vue'
import IconArticle from '~/components/IconArticle.vue'
import IconUser from '~/components/IconUser.vue'

const route = useRoute()

const navItems = [
  { path: '/', label: '首页', icon: IconHome },
  { path: '/hospitals', label: '医院', icon: IconHospital },
  { path: '/booking', label: '预约', icon: IconCalendar },
  { path: '/articles', label: '资讯', icon: IconArticle },
  { path: '/profile', label: '我的', icon: IconUser }
]

const isActive = (path: string) => {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}
</script>
