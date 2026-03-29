<template>
  <div class="min-h-screen bg-gray-50 pb-16">
    <!-- 顶部导航栏 -->
    <header class="bg-white px-4 py-3 sticky top-0 z-30">
      <div class="flex items-center justify-between">
        <h1 class="text-lg font-semibold text-gray-800">个人中心</h1>
      </div>
    </header>

    <!-- 用户信息卡片 -->
    <div class="px-4 mt-4">
      <div class="bg-gradient-to-r from-primary to-blue-600 rounded-xl p-6">
        <div class="flex items-center gap-4">
          <div class="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center">
            <svg class="w-10 h-10 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
            </svg>
          </div>
          <div>
            <p class="text-white font-semibold text-lg">用户</p>
            <p class="text-white/80 text-sm">点击登录 / 注册</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 功能菜单 -->
    <div class="px-4 mt-4">
      <div class="bg-white rounded-xl shadow-sm overflow-hidden">
        <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-primary" viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
            </svg>
            <span class="text-sm text-gray-800">我的预约</span>
          </div>
          <svg class="w-5 h-5 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
            <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
          </svg>
        </div>
        <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-primary" viewBox="0 0 24 24" fill="currentColor">
              <path d="M17 3H7c-1.1 0-2 .9-2 2v16l7-3 7 3V5c0-1.1-.9-2-2-2z"/>
            </svg>
            <span class="text-sm text-gray-800">我的收藏</span>
          </div>
          <svg class="w-5 h-5 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
            <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
          </svg>
        </div>
        <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-primary" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
            </svg>
            <span class="text-sm text-gray-800">检查记录</span>
          </div>
          <svg class="w-5 h-5 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
            <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
          </svg>
        </div>
        <div class="flex items-center justify-between px-4 py-3">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-primary" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
            </svg>
            <span class="text-sm text-gray-800">消息通知</span>
          </div>
          <svg class="w-5 h-5 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
            <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- 更多设置 -->
    <div class="px-4 mt-4">
      <div class="bg-white rounded-xl shadow-sm overflow-hidden">
        <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-gray-500" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
            <span class="text-sm text-gray-800">设置</span>
          </div>
          <svg class="w-5 h-5 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
            <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
          </svg>
        </div>
        <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-gray-500" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm2.07-7.75l-.9.92C13.45 12.9 13 13.5 13 15h-2v-.5c0-1.1.45-2.1 1.17-2.83l1.24-1.26c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2s-2 .9-2 2H8c0-2.21 1.79-4 4-4s4 1.79 4 4c0 .88-.36 1.68-.93 2.25z"/>
            </svg>
            <span class="text-sm text-gray-800">帮助与反馈</span>
          </div>
          <svg class="w-5 h-5 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
            <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
          </svg>
        </div>
        <div class="flex items-center justify-between px-4 py-3">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-gray-500" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 7V3H2v18h20V7H12zM6 19H4v-2h2v2zm0-4H4v-2h2v2zm0-4H4V9h2v2zm0-4H4V5h2v2zm4 12H8v-2h2v2zm0-4H8v-2h2v2zm0-4H8V9h2v2zm0-4H8V5h2v2zm10 12h-8v-2h2v-2h-2v-2h2v-2h-2V9h8v10zm-2-8h-2v2h2v-2zm0 4h-2v2h2v-2z"/>
            </svg>
            <span class="text-sm text-gray-800">关于我们</span>
          </div>
          <svg class="w-5 h-5 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
            <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- 客服热线 -->
    <div class="px-4 mt-6 pb-6">
      <div class="bg-white rounded-xl shadow-sm p-4 text-center">
        <p class="text-sm text-gray-500 mb-2">客服热线</p>
        <p class="text-xl font-bold text-primary">400-888-9999</p>
        <p class="text-xs text-gray-400 mt-1">周一至周日 8:00-22:00</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>
