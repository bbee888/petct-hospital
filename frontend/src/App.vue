<template>
  <router-view v-slot="{ Component }">
    <transition name="fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<style>
/* 导入Google字体 - 根据设计系统推荐 */
@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Figtree', 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  background-color: #f5f7fa;
  color: #1e293b;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* 基础可访问性样式 */
:focus-visible {
  outline: 2px solid #0891b2;
  outline-offset: 2px;
}

/* 减少动画支持 */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* 高对比度模式支持 */
@media (prefers-contrast: high) {
  body {
    background-color: #ffffff;
  }
  
  :focus-visible {
    outline: 3px solid #000000;
  }
}

/* 触摸设备优化 */
@media (hover: none) and (pointer: coarse) {
  input,
  button,
  select,
  textarea {
    font-size: 16px; /* 防止iOS缩放 */
  }
  
  button,
  .clickable {
    min-height: 44px;
    min-width: 44px;
  }
}
</style>