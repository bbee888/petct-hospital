export default defineNuxtConfig({
  devtools: { enabled: true },
  app: {
    head: {
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no' },
        { name: 'apple-mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-status-bar-style', content: 'black' }
      ],
      title: '全国PET-CT预约平台',
      link: [
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&display=swap' }
      ]
    }
  },
  modules: ['@nuxtjs/tailwindcss'],
  css: ['~/assets/css/main.css'],
  tailwindcss: {
    cssPath: '~/assets/css/main.css',
    configPath: 'tailwind.config.js'
  },
  // 后端API代理配置
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE || '/api/v1'
    }
  },
  nitro: {
    routeRules: {
      '/api/**': {
        proxy: 'http://localhost:8001/api/**'
      }
    }
  },
  compatibilityDate: '2024-04-03'
})
