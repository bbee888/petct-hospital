<template>
  <div class="admin-layout">
    <!-- 侧边栏 -->
    <aside class="sidebar" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <div class="sidebar-header">
        <div class="logo-container" @click="sidebarCollapsed = !sidebarCollapsed">
          <div class="logo-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>
              <path d="M15 8a3 3 0 1 0-6 0"/>
            </svg>
          </div>
          <h1 v-show="!sidebarCollapsed" class="logo-title">后台管理系统</h1>
        </div>
        <button 
          class="sidebar-toggle" 
          @click="sidebarCollapsed = !sidebarCollapsed"
          :aria-label="sidebarCollapsed ? '展开侧边栏' : '收起侧边栏'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="m15 18-6-6 6-6"/>
          </svg>
        </button>
      </div>
      
      <nav class="sidebar-nav" role="navigation" aria-label="主菜单">
        <ul class="nav-menu">
          <li 
            v-for="item in menuItems" 
            :key="item.path"
            :class="['nav-item', { 'active': activeMenu === item.path }]"
          >
            <router-link 
              :to="item.path" 
              class="nav-link"
              :aria-current="activeMenu === item.path ? 'page' : null"
            >
              <span class="nav-icon" :aria-label="item.label">
                <component :is="item.icon" />
              </span>
              <transition name="fade-slide">
                <span v-show="!sidebarCollapsed" class="nav-label">{{ item.label }}</span>
              </transition>
              <span v-if="item.badge" class="nav-badge">{{ item.badge }}</span>
            </router-link>
          </li>
        </ul>
      </nav>
      
      <div class="sidebar-footer" v-show="!sidebarCollapsed">
        <div class="system-info">
          <p class="system-status">
            <span class="status-dot status-active"></span>
            系统正常
          </p>
          <p class="system-version">v2.0.1</p>
        </div>
      </div>
    </aside>
    
    <!-- 主要内容区域 -->
    <main class="main-content">
      <!-- 顶部导航栏 -->
      <header class="topbar">
        <div class="topbar-left">
          <button 
            class="menu-toggle" 
            @click="sidebarCollapsed = !sidebarCollapsed"
            aria-label="切换侧边栏"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="3" y1="12" x2="21" y2="12"/>
              <line x1="3" y1="6" x2="21" y2="6"/>
              <line x1="3" y1="18" x2="21" y2="18"/>
            </svg>
          </button>
          <div class="breadcrumb" aria-label="导航路径">
            <span class="breadcrumb-item">{{ currentPageTitle }}</span>
          </div>
        </div>
        
        <div class="topbar-right">
          <div class="user-actions">
            <!-- <button 
              class="notification-btn" 
              aria-label="通知"
              @click="showNotifications"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
              </svg>
              <span v-if="notificationCount > 0" class="notification-badge">
                {{ notificationCount > 9 ? '9+' : notificationCount }}
              </span>
            </button> -->
            
            <div class="user-profile">
              <div class="user-avatar">
                {{ userInitials }}
              </div>
              <div class="user-details">
                <span class="user-name">{{ userStore.user?.username }}</span>
                <span class="user-role">管理员</span>
              </div>
              <el-dropdown trigger="click" @command="handleUserCommand">
                <button class="user-menu-btn" aria-label="用户菜单">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="1"/>
                    <circle cx="12" cy="5" r="1"/>
                    <circle cx="12" cy="19" r="1"/>
                  </svg>
                </button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="profile">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                        <circle cx="12" cy="7" r="4"/>
                      </svg>
                      个人资料
                    </el-dropdown-item>
                    <el-dropdown-item command="settings">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
                        <circle cx="12" cy="12" r="3"/>
                      </svg>
                      系统设置
                    </el-dropdown-item>
                    <el-dropdown-item divided command="logout">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                        <polyline points="16 17 21 12 16 7"/>
                        <line x1="21" y1="12" x2="9" y2="12"/>
                      </svg>
                      退出登录
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
        </div>
      </header>
      
      <!-- 页面内容 -->
      <div class="page-container">
        <router-view v-slot="{ Component }">
          <transition name="page-transition" mode="out-in">
            <component :is="Component" :key="$route.path" />
          </transition>
        </router-view>
      </div>
      
      <!-- 页脚 -->
      <footer class="page-footer">
        <div class="footer-content">
          <p class="copyright">
            © 2025 PET-CT医院管理系统 v2.0
          </p>
          <div class="footer-links">
            <a href="#" @click.prevent="showHelp">帮助中心</a>
            <a href="#" @click.prevent="showPrivacy">隐私政策</a>
            <a href="#" @click.prevent="showTerms">服务条款</a>
          </div>
        </div>
      </footer>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, markRaw } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ElMessage, ElNotification } from 'element-plus'
import request from '../utils/request'
import {
  House,
  OfficeBuilding,
  FirstAidKit,
  Document,
  Folder,
  Calendar,
  User,
  Location,
  Setting,
  Bell,
  Help
} from '@element-plus/icons-vue'
import { announceToScreenReader } from '../utils/accessibility'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 响应式状态
const sidebarCollapsed = ref(false)

// 菜单配置 (初始badge为null,将从API获取)
const menuItems = ref([
  { path: '/admin/dashboard', label: '仪表盘', icon: markRaw(House), badge: null },
  { path: '/admin/sites', label: '站点管理', icon: markRaw(OfficeBuilding), badge: null },
  { path: '/admin/hospitals', label: '医院管理', icon: markRaw(FirstAidKit), badge: null },
  { path: '/admin/articles', label: '文章管理', icon: markRaw(Document), badge: null },
  { path: '/admin/categories', label: '栏目管理', icon: markRaw(Folder), badge: null },
  { path: '/admin/appointments', label: '预约管理', icon: markRaw(Calendar), badge: null },
  { path: '/admin/users', label: '用户管理', icon: markRaw(User), badge: null },
  { path: '/admin/geo', label: '省份城市', icon: markRaw(Location), badge: null }
])

// 获取菜单badge数据
const fetchMenuBadges = async () => {
  try {
    const response = await request.get('/v1/stats/menu-badges')

    // 更新badge数据
    menuItems.value = menuItems.value.map(item => {
      let badge = null

      switch (item.path) {
        case '/admin/sites':
          badge = response.data.sites
          break
        case '/admin/hospitals':
          badge = response.data.hospitals
          break
        case '/admin/articles':
          badge = response.data.articles
          break
        case '/admin/appointments':
          badge = response.data.appointments
          break
        case '/admin/users':
          badge = response.data.users
          break
        default:
          badge = null
      }

      return { ...item, badge }
    })
  } catch (error) {
    console.error('获取菜单badge失败:', error)
    // 保持原有的null值
  }
}

// 计算属性
const activeMenu = computed(() => route.path)
const userInitials = computed(() => {
  const username = userStore.user?.username || ''
  return username.slice(0, 2).toUpperCase()
})

const currentPageTitle = computed(() => {
  const routeName = route.name
  const item = menuItems.value.find(item => item.path === route.path)
  return item?.label || routeName || '仪表盘'
})

// 用户命令处理
const handleUserCommand = (command) => {
  switch (command) {
    case 'profile':
      showUserProfile()
      break
    case 'settings':
      showSettings()
      break
    case 'logout':
      handleLogout()
      break
  }
}

// 用户操作函数
const showUserProfile = () => {
  ElMessage.info('个人资料功能开发中')
  announceToScreenReader('打开个人资料设置')
}

const showSettings = () => {
  ElMessage.info('系统设置功能开发中')
  announceToScreenReader('打开系统设置')
}

const handleLogout = () => {
  userStore.logout()
  ElNotification.success({
    title: '退出登录成功',
    message: '您已安全退出系统',
    duration: 2000
  })
  announceToScreenReader('退出登录成功，正在跳转到登录页面')
  setTimeout(() => {
    router.push('/login')
  }, 1500)
}

const showNotifications = () => {
  ElMessage.info(`您有 ${notificationCount.value} 条未读通知`)
  announceToScreenReader(`显示通知，共有 ${notificationCount.value} 条未读`)
}

const showHelp = () => {
  ElMessage.info('帮助中心页面开发中')
  announceToScreenReader('打开帮助中心')
}

const showPrivacy = () => {
  ElMessage.info('隐私政策页面开发中')
  announceToScreenReader('查看隐私政策')
}

const showTerms = () => {
  ElMessage.info('服务条款页面开发中')
  announceToScreenReader('查看服务条款')
}

// 键盘快捷键支持
const setupKeyboardShortcuts = () => {
  const handleKeyDown = (event) => {
    // Ctrl/Cmd + B 切换侧边栏
    if ((event.ctrlKey || event.metaKey) && event.key === 'b') {
      event.preventDefault()
      sidebarCollapsed.value = !sidebarCollapsed.value
      announceToScreenReader(
        sidebarCollapsed.value ? '侧边栏已收起' : '侧边栏已展开'
      )
    }
    
    // F1 显示帮助
    if (event.key === 'F1') {
      event.preventDefault()
      showHelp()
    }
    
    // Escape 关闭下拉菜单等
    if (event.key === 'Escape') {
      // 可以在这里添加关闭弹出窗口的逻辑
    }
  }
  
  document.addEventListener('keydown', handleKeyDown)
  return () => document.removeEventListener('keydown', handleKeyDown)
}

// 生命周期
onMounted(() => {
  const cleanup = setupKeyboardShortcuts()
  
  // 获取菜单badge数据
  fetchMenuBadges()
  
  // 组件卸载时清理
  return () => {
    cleanup()
  }
})
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #ECFEFF 0%, #F8FAFC 100%);
  position: relative;
}

/* 侧边栏样式 */
.sidebar {
  width: 240px;
  background: linear-gradient(135deg, #0E7490 0%, #0891B2 100%);
  color: white;
  display: flex;
  flex-direction: column;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.08);
  z-index: 100;
  position: relative;
  overflow: hidden;
}

.sidebar.sidebar-collapsed {
  width: 72px;
}

.sidebar-header {
  padding: 24px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 10px;
  padding: 8px;
  background: rgba(255, 255, 255, 0.05);
}

.logo-container:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.logo-icon {
  width: 40px;
  height: 40px;
  min-width: 40px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.logo-icon svg {
  width: 24px;
  height: 24px;
  stroke: white;
}

.logo-title {
  font-size: 16px;
  font-weight: 700;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: white;
  font-family: 'Fira Code', monospace;
}

.sidebar-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
}

.sidebar-toggle:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-50%) scale(1.1);
}

.sidebar-toggle svg {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
}

.sidebar-collapsed .sidebar-toggle svg {
  transform: rotate(180deg);
}

/* 导航菜单 */
.sidebar-nav {
  flex: 1;
  padding: 20px 16px;
  overflow-y: auto;
}

.nav-menu {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  position: relative;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  border-radius: 10px;
  transition: all 0.3s ease;
  position: relative;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  transform: translateX(4px);
}

.nav-item.active .nav-link {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  font-weight: 600;
}

.nav-item.active .nav-link::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 24px;
  background: #22D3EE;
  border-radius: 0 4px 4px 0;
}

.nav-icon {
  width: 24px;
  height: 24px;
  min-width: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-icon svg {
  width: 18px;
  height: 18px;
  stroke: currentColor;
}

.nav-label {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.nav-badge {
  background: #059669;
  color: white;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 20px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 侧边栏页脚 */
.sidebar-footer {
  padding: 20px 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.system-info {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.system-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  margin: 0 0 4px 0;
  color: rgba(255, 255, 255, 0.9);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-active {
  background: #10B981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4);
  }
  70% {
    box-shadow: 0 0 0 6px rgba(16, 185, 129, 0);
  }
}

.system-version {
  font-size: 11px;
  margin: 0;
  color: rgba(255, 255, 255, 0.6);
}

/* 主要内容区域 */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow: hidden;
}

/* 顶部导航栏 */
.topbar {
  background: white;
  border-bottom: 1px solid #E2E8F0;
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  position: sticky;
  top: 0;
  z-index: 90;
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.menu-toggle {
  background: none;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #64748B;
}

.menu-toggle:hover {
  background: #F1F5F9;
  color: #0891B2;
}

.menu-toggle svg {
  width: 20px;
  height: 20px;
}

.breadcrumb {
  font-size: 14px;
  color: #64748B;
}

.breadcrumb-item {
  font-weight: 600;
  color: #164E63;
  position: relative;
  padding-left: 24px;
}

.breadcrumb-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%230891B2' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z'/%3E%3Cpolyline points='9 22 9 12 15 12 15 22'/%3E%3C/svg%3E") no-repeat center;
}

/* 用户操作区域 */
.topbar-right {
  display: flex;
  align-items: center;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.notification-btn {
  position: relative;
  background: none;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #64748B;
}

.notification-btn:hover {
  background: #F1F5F9;
  color: #0891B2;
}

.notification-btn svg {
  width: 20px;
  height: 20px;
}

.notification-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  background: #EF4444;
  color: white;
  font-size: 10px;
  font-weight: 600;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid white;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 4px 12px;
  border-radius: 12px;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  transition: all 0.3s ease;
}

.user-profile:hover {
  background: #F1F5F9;
  border-color: #0891B2;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, #0891B2 0%, #0E7490 100%);
  color: white;
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #164E63;
}

.user-role {
  font-size: 12px;
  color: #64748B;
  font-weight: 500;
}

.user-menu-btn {
  background: none;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #64748B;
}

.user-menu-btn:hover {
  background: #E2E8F0;
  color: #0891B2;
}

.user-menu-btn svg {
  width: 16px;
  height: 16px;
}

/* 页面容器 */
.page-container {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  position: relative;
}

/* 页面过渡动画 */
.page-transition-enter-active,
.page-transition-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-transition-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.page-transition-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.page-transition-leave-active {
  position: absolute;
  width: 100%;
}

/* 页脚 */
.page-footer {
  background: white;
  border-top: 1px solid #E2E8F0;
  padding: 16px 24px;
  margin-top: auto;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.copyright {
  font-size: 12px;
  color: #64748B;
  margin: 0;
}

.divider {
  margin: 0 8px;
  color: #CBD5E1;
}

.footer-links {
  display: flex;
  gap: 16px;
}

.footer-links a {
  font-size: 12px;
  color: #64748B;
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer-links a:hover {
  color: #0891B2;
}

/* 导航标签过渡动画 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}

/* 可访问性样式 */
:focus-visible {
  outline: 2px solid #0891B2;
  outline-offset: 2px;
}

/* 减少动画支持 */
@media (prefers-reduced-motion: reduce) {
  .sidebar,
  .logo-container,
  .nav-link,
  .menu-toggle,
  .notification-btn,
  .user-profile,
  .user-menu-btn {
    transition: none !important;
  }
  
  .status-dot {
    animation: none !important;
  }
  
  .page-transition-enter-active,
  .page-transition-leave-active {
    transition: none !important;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    z-index: 1000;
    transform: translateX(-100%);
    width: 280px !important;
  }
  
  .sidebar.sidebar-collapsed {
    transform: translateX(-100%);
  }
  
  .sidebar:not(.sidebar-collapsed) {
    transform: translateX(0);
  }
  
  .menu-toggle {
    display: flex;
  }
  
  .sidebar-toggle {
    display: none;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }
  
  .footer-links {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .topbar {
    padding: 0 16px;
  }
  
  .page-container {
    padding: 16px;
  }
  
  .user-details {
    display: none;
  }
}

/* 高对比度模式 */
@media (prefers-contrast: high) {
  .sidebar {
    background: #0E7490;
    border-right: 2px solid #000;
  }
  
  .topbar {
    border-bottom: 2px solid #000;
  }
  
  :focus-visible {
    outline: 3px solid #000;
  }
}

/* 触摸设备优化 */
@media (hover: none) and (pointer: coarse) {
  .nav-link,
  .menu-toggle,
  .notification-btn,
  .user-menu-btn {
    min-height: 44px;
    min-width: 44px;
  }
  
  .user-profile {
    min-height: 60px;
  }
}
</style>
