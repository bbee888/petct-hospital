<template>
  <div class="login-page">
    <!-- 背景装饰 -->
    <div class="background-design">
      <div class="bg-gradient"></div>
      <div class="bg-pattern"></div>
    </div>
    
    <!-- 主登录容器 -->
    <div class="login-container">
      <div class="login-wrapper">
        <!-- 左侧品牌和信息区域 -->
        <div class="brand-section">
          <div class="logo-container">
            <div class="logo-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>
                <path d="M15 8a3 3 0 1 0-6 0"/>
              </svg>
            </div>
            <h1 class="brand-name">PET-CT 医院管理系统</h1>
            <p class="brand-subtitle">专业、安全、高效</p>
          </div>
          
          <div class="info-section">
            <div class="info-item">
              <div class="info-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="m8 3 4 8 5-5 5 15H2L8 3z"/>
                </svg>
              </div>
              <div class="info-content">
                <h3>患者数据管理</h3>
                <p>全面追踪患者检查记录和影像数据</p>
              </div>
            </div>
            
            <div class="info-item">
              <div class="info-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="m9 12 2 2 4-4"/>
                </svg>
              </div>
              <div class="info-content">
                <h3>质量控制</h3>
                <p>确保医疗设备安全和检查质量</p>
              </div>
            </div>
            
            <div class="info-item">
              <div class="info-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/>
                </svg>
              </div>
              <div class="info-content">
                <h3>安全访问</h3>
                <p>符合医疗行业安全和隐私标准</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 右侧登录表单区域 -->
        <div class="form-section">
          <div class="form-wrapper">
            <div class="form-header">
              <h2 id="form-title">登录账户</h2>
              <p>请输入您的凭证以访问系统</p>
            </div>
            
            <el-form 
              :model="form" 
              :rules="rules" 
              ref="loginForm" 
              label-position="top" 
              size="large"
              class="login-form"
              @submit.prevent="handleLogin"
              role="form"
              aria-labelledby="form-title"
            >
              <el-form-item 
                label="用户名 / 邮箱" 
                prop="username"
                class="form-item-enhanced"
              >
                <el-input 
                  v-model="form.username" 
                  placeholder="请输入用户名或邮箱地址"
                  size="large"
                  :validate-event="true"
                  autocomplete="username"
                  aria-required="true"
                  aria-describedby="username-hint"
                >
                  <template #prefix>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                      <circle cx="12" cy="7" r="4"/>
                    </svg>
                  </template>
                </el-input>
                <div v-if="form.username && usernameError" class="error-hint" id="username-hint" role="alert" aria-live="polite">
                  {{ usernameError }}
                </div>
              </el-form-item>
              
              <el-form-item 
                label="密码" 
                prop="password"
                class="form-item-enhanced"
              >
                <el-input 
                  v-model="form.password" 
                  type="password" 
                  placeholder="请输入密码"
                  size="large"
                  :show-password="true"
                  autocomplete="current-password"
                  aria-required="true"
                  aria-describedby="password-hint"
                >
                  <template #prefix>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                    </svg>
                  </template>
                </el-input>
                <div class="password-hint" id="password-hint">
                  密码区分大小写，请确保Caps Lock已关闭
                </div>
              </el-form-item>
              
              <div class="form-options">
                <el-checkbox v-model="rememberMe" label="记住我" size="large" />
                <a href="#" class="forgot-password" @click.prevent="showForgotPassword">忘记密码？</a>
              </div>
              
              <el-button 
                type="primary" 
                @click="handleLogin" 
                :loading="loading" 
                size="large"
                class="login-button"
                :disabled="!form.username || !form.password"
                aria-label="登录系统"
                :aria-busy="loading"
              >
                <span v-if="!loading">登录系统</span>
                <span v-else>登录中...</span>
              </el-button>
              
              <div class="form-divider">
                <span>或</span>
              </div>
              
              <div class="alternative-actions">
                <p class="register-hint">
                  还没有账户？<a href="#" class="register-link" @click.prevent="showRegister">申请访问权限</a>
                </p>
                <p class="help-hint">
                  需要帮助？<a href="#" class="help-link" @click.prevent="showHelp">查看登录指南</a>
                </p>
              </div>
            </el-form>
            
            <div class="form-footer">
              <p class="security-note">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/>
                </svg>
                您的信息安全受保护，我们严格遵守HIPAA和医疗隐私标准
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 页脚 -->
    <footer class="login-footer">
      <div class="footer-content">
        <p>© 2025 PET-CT医院管理系统 | 版本 2.0</p>
        <div class="footer-links">
          <a href="#">隐私政策</a>
          <a href="#">服务条款</a>
          <a href="#">帮助中心</a>
          <a href="#">联系我们</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { authApi } from '../api/auth'
import { ElMessage, ElNotification } from 'element-plus'
import { setupFormShortcuts, announceToScreenReader, checkColorContrast } from '../utils/accessibility'

const router = useRouter()
const userStore = useUserStore()
const loginForm = ref(null)
const loading = ref(false)
const rememberMe = ref(false)
const usernameError = ref('')

const form = reactive({
  username: '',
  password: ''
})

// 计算属性用于实时验证
const isValidEmail = computed(() => {
  if (!form.username) return false
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(form.username)
})

const rules = {
  username: [
    { required: true, message: '请输入用户名或邮箱地址', trigger: 'blur' },
    { 
      validator: (rule, value, callback) => {
        if (value && value.includes('@') && !isValidEmail.value) {
          callback(new Error('请输入有效的邮箱地址'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginForm.value) return
  
  try {
    // 验证表单
    await loginForm.value.validate()
    loading.value = true
    
    // 显示加载状态
    ElNotification({
      title: '正在登录',
      message: '正在验证您的身份信息...',
      type: 'info',
      duration: 2000
    })
    
    // 调用登录API
    const response = await authApi.login(form.username, form.password)
    
    // 保存用户信息
    userStore.setToken(response.access_token)
    userStore.setUser({ username: form.username })
    
    // 如果选择了记住我，保存到本地存储
    if (rememberMe.value) {
      localStorage.setItem('rememberedUsername', form.username)
    } else {
      localStorage.removeItem('rememberedUsername')
    }
    
    // 成功提示
    ElNotification.success({
      title: '登录成功',
      message: '欢迎回来！正在跳转到控制台...',
      duration: 1500
    })
    
    // 延迟跳转让用户看到成功消息
    setTimeout(() => {
      router.push('/admin/dashboard')
    }, 1500)
    
  } catch (error) {
    // 根据错误类型显示不同的消息
    if (error.response) {
      switch (error.response.status) {
        case 401:
          ElNotification.error({
            title: '登录失败',
            message: '用户名或密码错误，请重试',
            duration: 3000
          })
          break
        case 403:
          ElNotification.error({
            title: '访问被拒绝',
            message: '您的账户没有访问权限',
            duration: 3000
          })
          break
        case 429:
          ElNotification.warning({
            title: '登录尝试过多',
            message: '请稍后再试，或联系管理员',
            duration: 4000
          })
          break
        case 500:
          ElNotification.error({
            title: '服务器错误',
            message: '系统暂时不可用，请稍后重试',
            duration: 3000
          })
          break
        default:
          ElNotification.error({
            title: '登录失败',
            message: '请检查网络连接后重试',
            duration: 3000
          })
      }
    } else if (error.request) {
      ElNotification.error({
        title: '网络错误',
        message: '无法连接到服务器，请检查网络',
        duration: 3000
      })
    } else {
      ElNotification.error({
        title: '登录失败',
        message: error.message || '未知错误，请重试',
        duration: 3000
      })
    }
  } finally {
    loading.value = false
  }
}

const showForgotPassword = () => {
  announceToScreenReader('请联系系统管理员重置密码');
  ElMessage.info('请联系系统管理员重置密码')
}

const showRegister = () => {
  announceToScreenReader('请联系医院管理员申请访问权限');
  ElMessage.info('请联系医院管理员申请访问权限')
}

const showHelp = () => {
  announceToScreenReader('查看用户手册或联系技术支持');
  ElMessage.info('查看用户手册或联系技术支持')
}

const showKeyboardShortcuts = () => {
  const shortcuts = [
    'Ctrl/Cmd + Enter: 提交表单',
    'Ctrl/Cmd + H: 显示帮助',
    'F1: 显示帮助',
    'Escape: 取消操作'
  ];
  
  const message = `可用键盘快捷键:\n${shortcuts.join('\n')}`;
  announceToScreenReader('显示键盘快捷键帮助');
  ElMessage.info(message)
}

// 组件挂载时检查是否有记住的用户名
onMounted(() => {
  const rememberedUsername = localStorage.getItem('rememberedUsername')
  if (rememberedUsername) {
    form.username = rememberedUsername
    rememberMe.value = true
  }
  
  // 设置键盘快捷键
  const formElement = document.querySelector('.login-form')
  if (formElement) {
    const cleanupShortcuts = setupFormShortcuts(formElement, {
      onSubmit: handleLogin,
      onHelp: showKeyboardShortcuts
    })
    
    // 清理函数
    onUnmounted(cleanupShortcuts)
  }
  
  // 检查颜色对比度（开发期间）
  if (process.env.NODE_ENV === 'development') {
    const contrastResult = checkColorContrast('#0891B2', '#FFFFFF')
    console.log('按钮颜色对比度:', contrastResult)
    
    const textContrastResult = checkColorContrast('#164E63', '#FFFFFF')
    console.log('文字颜色对比度:', textContrastResult)
  }
  
  // 页面加载完成提示
  announceToScreenReader('PET-CT医院管理系统登录页面已加载完成。请填写用户名和密码进行登录。')
})
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #ECFEFF 0%, #F0F9FF 100%);
  position: relative;
  overflow: hidden;
}

/* 背景装饰 */
.background-design {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
  pointer-events: none;
}

.bg-gradient {
  position: absolute;
  top: -50%;
  left: -50%;
  right: -50%;
  bottom: -50%;
  background: radial-gradient(circle at 20% 80%, rgba(8, 145, 178, 0.08) 0%, transparent 50%),
              radial-gradient(circle at 80% 20%, rgba(5, 150, 105, 0.05) 0%, transparent 50%);
  animation: gradientFloat 20s ease-in-out infinite alternate;
}

.bg-pattern {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 1px 1px, rgba(8, 145, 178, 0.05) 1px, transparent 0);
  background-size: 40px 40px;
  opacity: 0.5;
}

@keyframes gradientFloat {
  0% {
    transform: translate(0, 0) scale(1);
  }
  100% {
    transform: translate(-2%, 2%) scale(1.02);
  }
}

/* 主登录容器 */
.login-container {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-wrapper {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  max-width: 1200px;
  width: 100%;
  background: white;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.08),
    0 8px 30px rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

/* 左侧品牌区域 */
.brand-section {
  background: linear-gradient(135deg, #0891B2 0%, #0E7490 100%);
  color: white;
  padding: 60px 40px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.logo-container {
  text-align: center;
  margin-bottom: 40px;
}

.logo-icon {
  width: 72px;
  height: 72px;
  margin: 0 auto 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.logo-icon svg {
  width: 36px;
  height: 36px;
  stroke: white;
}

.brand-name {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 8px;
  color: white;
  font-family: 'Helvetica Neue', 'Segoe UI', sans-serif;
}

.brand-subtitle {
  font-size: 14px;
  opacity: 0.9;
  margin: 0;
  font-weight: 400;
}

.info-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.info-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  cursor: default;
}

.info-item:hover {
  background: rgba(255, 255, 255, 0.12);
  transform: translateY(-2px);
}

.info-icon {
  width: 40px;
  height: 40px;
  min-width: 40px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.info-icon svg {
  width: 20px;
  height: 20px;
  stroke: white;
}

.info-content h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 4px 0;
  color: white;
}

.info-content p {
  font-size: 13px;
  opacity: 0.8;
  margin: 0;
  line-height: 1.4;
}

/* 右侧表单区域 */
.form-section {
  padding: 60px 50px;
  background: white;
}

.form-wrapper {
  max-width: 380px;
  margin: 0 auto;
}

.form-header {
  text-align: center;
  margin-bottom: 40px;
}

.form-header h2 {
  font-size: 28px;
  font-weight: 700;
  color: #164E63;
  margin: 0 0 8px 0;
  font-family: 'Helvetica Neue', 'Segoe UI', sans-serif;
}

.form-header p {
  color: #64748B;
  font-size: 14px;
  margin: 0;
}

/* 表单样式 */
.login-form {
  margin-bottom: 30px;
}

.form-item-enhanced {
  margin-bottom: 24px;
}

.form-item-enhanced :deep(.el-form-item__label) {
  font-weight: 600;
  color: #475569;
  margin-bottom: 6px;
  font-size: 14px;
}

.form-item-enhanced :deep(.el-input__wrapper) {
  border-radius: 10px;
  border: 1px solid #E2E8F0;
  background: #F8FAFC;
  transition: all 0.3s ease;
  box-shadow: none;
  padding: 0 16px;
  height: 48px;
}

.form-item-enhanced :deep(.el-input__wrapper:hover) {
  border-color: #0891B2;
  background: white;
}

.form-item-enhanced :deep(.el-input__wrapper.is-focus) {
  border-color: #0891B2;
  box-shadow: 0 0 0 2px rgba(8, 145, 178, 0.1);
  background: white;
}

.form-item-enhanced :deep(.el-input__prefix) {
  margin-right: 8px;
  display: flex;
  align-items: center;
}

.form-item-enhanced :deep(.el-input__prefix svg) {
  width: 18px;
  height: 18px;
  stroke: #94A3B8;
}

.form-item-enhanced :deep(.el-input__inner) {
  color: #1E293B;
  font-size: 14px;
}

.form-item-enhanced :deep(.el-input__inner::placeholder) {
  color: #94A3B8;
}

.error-hint {
  font-size: 12px;
  color: #EF4444;
  margin-top: 4px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.password-hint {
  font-size: 12px;
  color: #64748B;
  margin-top: 4px;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* 表单选项 */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.form-options :deep(.el-checkbox__label) {
  font-size: 14px;
  color: #475569;
}

.forgot-password {
  font-size: 14px;
  color: #0891B2;
  text-decoration: none;
  transition: color 0.3s ease;
  font-weight: 500;
}

.forgot-password:hover {
  color: #0E7490;
  text-decoration: underline;
}

/* 登录按钮 */
.login-button {
  width: 100%;
  height: 48px;
  background: linear-gradient(135deg, #0891B2 0%, #0E7490 100%);
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 15px;
  margin-bottom: 20px;
  transition: all 0.3s ease;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(8, 145, 178, 0.3);
}

.login-button:active {
  transform: translateY(0);
}

.login-button:disabled {
  background: #CBD5E1;
  transform: none;
  box-shadow: none;
  cursor: not-allowed;
}

/* 分割线 */
.form-divider {
  display: flex;
  align-items: center;
  margin: 24px 0;
}

.form-divider::before,
.form-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #E2E8F0;
}

.form-divider span {
  padding: 0 16px;
  color: #64748B;
  font-size: 12px;
  text-transform: uppercase;
}

/* 备用操作 */
.alternative-actions {
  text-align: center;
}

.register-hint,
.help-hint {
  font-size: 14px;
  color: #64748B;
  margin: 8px 0;
}

.register-link,
.help-link {
  color: #0891B2;
  text-decoration: none;
  font-weight: 500;
  margin-left: 4px;
  transition: color 0.3s ease;
}

.register-link:hover,
.help-link:hover {
  color: #0E7490;
  text-decoration: underline;
}

/* 表单页脚 */
.form-footer {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #E2E8F0;
}

.security-note {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #64748B;
  margin: 0;
}

.security-note svg {
  width: 14px;
  height: 14px;
  stroke: #059669;
  flex-shrink: 0;
}

/* 页脚 */
.login-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-content p {
  font-size: 12px;
  color: #64748B;
  margin: 0;
}

.footer-links {
  display: flex;
  gap: 20px;
}

.footer-links a {
  font-size: 12px;
  color: #475569;
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer-links a:hover {
  color: #0891B2;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-wrapper {
    grid-template-columns: 1fr;
    max-width: 400px;
  }
  
  .brand-section {
    display: none;
  }
  
  .form-section {
    padding: 40px 30px;
  }
  
  .form-wrapper {
    max-width: 100%;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }
  
  .footer-links {
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .login-container {
    padding: 10px;
  }
  
  .form-section {
    padding: 30px 20px;
  }
  
  .form-header h2 {
    font-size: 24px;
  }
  
  .login-wrapper {
    border-radius: 16px;
  }
}

/* 焦点状态增强 */
.login-form :deep(*) {
  outline-offset: 2px;
}

.login-form :deep(*:focus-visible) {
  outline: 2px solid #0891B2;
  outline-offset: 2px;
}

/* 触摸设备优化 */
@media (hover: none) {
  .info-item:hover {
    transform: none;
  }
  
  .login-button:hover {
    transform: none;
    box-shadow: none;
  }
  
  .form-item-enhanced :deep(.el-input__wrapper:hover) {
    border-color: #E2E8F0;
  }
}

/* 减少动画设置 */
@media (prefers-reduced-motion: reduce) {
  .bg-gradient,
  .info-item,
  .login-button,
  .form-item-enhanced :deep(.el-input__wrapper) {
    transition: none !important;
    animation: none !important;
  }
  
  .info-item:hover {
    transform: none !important;
  }
}
</style>