<template>
  <div class="login-page">
    <!-- 登录主容器 -->
    <div class="login-container">
      <!-- 品牌Logo - 在卡片上方 -->
      <div class="brand-section">
        <div class="brand-logo">
          <img src="https://ai.wlai.vip/logo123.png" alt="PhishGuard Logo" class="logo-image" />
          <span class="brand-text">PhishGuard</span>
        </div>
      </div>

      <!-- 登录卡片 -->
      <div class="login-card">
        <!-- 登录标题 -->
        <h1 class="login-title">登录</h1>

        <!-- 登录表单 -->
        <form class="login-form" @submit.prevent="handleLogin">
          <!-- 用户名或邮箱输入 -->
          <div class="form-field">
            <label class="field-label">用户名或邮箱</label>
            <div class="input-container">
              <svg class="input-icon" viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
                />
              </svg>
              <input
                type="text"
                v-model="loginForm.username"
                placeholder="请输入您的用户名或邮箱地址"
                class="form-input"
                :class="{ 'error': usernameError }"
                @blur="handleUsernameChange"
                @input="usernameError = ''"
                required
              />
            </div>
            <div v-if="usernameError" class="error-message">{{ usernameError }}</div>
          </div>

          <!-- 密码输入 -->
          <div class="form-field">
            <label class="field-label">密码</label>
            <div class="input-container">
              <svg class="input-icon" viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zM12 17c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zM15.1 8H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"
                />
              </svg>
              <input
                :type="showPassword ? 'text' : 'password'"
                v-model="loginForm.password"
                placeholder="请输入您的密码"
                class="form-input"
                :class="{ 'error': passwordError }"
                @blur="handlePasswordChange"
                @input="passwordError = ''"
                required
              />
              <button
                type="button"
                @click="togglePassword"
                class="password-toggle"
                aria-label="切换密码显示"
              >
                <svg v-if="showPassword" viewBox="0 0 24 24" fill="currentColor">
                  <path
                    d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"
                  />
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="currentColor">
                  <path
                    d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z"
                  />
                </svg>
              </button>
            </div>
            <div v-if="passwordError" class="error-message">{{ passwordError }}</div>
          </div>

          <!-- 用户协议 -->
          <div class="form-options">
            <label class="checkbox-wrapper">
              <input type="checkbox" v-model="agreeTerms" class="checkbox-input" />
              <span class="checkbox-mark"></span>
              <span class="checkbox-text">我已阅读并同意</span>
              <a href="#" class="terms-link">《用户协议》</a>
            </label>
          </div>

          <!-- 登录按钮 -->
          <button type="submit" class="login-button" :disabled="isLoading || !agreeTerms">
            <span v-if="!isLoading">登录</span>
            <span v-else>登录中...</span>
          </button>

          <!-- 忘记密码 -->
          <div class="forgot-section">
            <a href="#" class="forgot-link">忘记密码？</a>
          </div>

          <!-- 分隔线 -->
          <div class="divider">
            <span class="divider-text">或</span>
          </div>

          <!-- 其他登录方式 -->
          <div class="other-login-section">
            <button type="button" class="other-login-button">其他登录方式</button>
          </div>

          <!-- 注册提示 -->
          <div class="register-section">
            <span class="register-text">没有账户？</span>
            <router-link to="/register" class="register-link">注册</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { showToast } from '@/utils/toast'

defineOptions({
  name: 'LoginPage',
})

const router = useRouter()
const authStore = useAuthStore()

// 表单数据
const loginForm = ref({
  username: '',
  password: '',
})

// 表单状态
const showPassword = ref(false)
const agreeTerms = ref(false)

// 计算属性
const isLoading = computed(() => authStore.isLoading)

// 表单验证状态
const usernameError = ref('')
const passwordError = ref('')

// 切换密码显示
const togglePassword = () => {
  showPassword.value = !showPassword.value
}

// 验证用户名/邮箱格式
const validateUsername = (value) => {
  if (!value) {
    return '用户名或邮箱不能为空'
  }
  
  // 如果包含@符号，验证邮箱格式
  if (value.includes('@')) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(value)) {
      return '邮箱格式不正确'
    }
  } else {
    // 验证用户名格式（3-20位，字母数字下划线）
    const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/
    if (!usernameRegex.test(value)) {
      return '用户名格式不正确（3-20位字母数字下划线）'
    }
  }
  
  return ''
}

// 验证密码格式
const validatePassword = (value) => {
  if (!value) {
    return '密码不能为空'
  }
  
  if (value.length < 6 || value.length > 20) {
    return '密码长度应为6-20位'
  }
  
  // 必须包含字母和数字
  const hasLetter = /[a-zA-Z]/.test(value)
  const hasDigit = /\d/.test(value)
  
  if (!hasLetter || !hasDigit) {
    return '密码必须包含字母和数字'
  }
  
  return ''
}

// 实时验证用户名
const handleUsernameChange = () => {
  usernameError.value = validateUsername(loginForm.value.username)
}

// 实时验证密码
const handlePasswordChange = () => {
  passwordError.value = validatePassword(loginForm.value.password)
}

// 处理登录
const handleLogin = async () => {
  // 表单验证
  const usernameValidation = validateUsername(loginForm.value.username)
  const passwordValidation = validatePassword(loginForm.value.password)
  
  usernameError.value = usernameValidation
  passwordError.value = passwordValidation
  
  if (usernameValidation || passwordValidation) {
    showToast({ message: '请检查输入信息', type: 'error' })
    return
  }

  if (!agreeTerms.value) {
    showToast({ message: '请先同意用户协议', type: 'warning' })
    return
  }

  try {
    const result = await authStore.login({
      username: loginForm.value.username,
      password: loginForm.value.password
    })

    if (result.success) {
      // 登录成功，跳转到原始请求的页面或控制台页面
      const redirect = router.currentRoute.value.query.redirect || '/console'
      router.push(redirect)
    }
  } catch (error) {
    console.error('登录失败:', error)
  }
}
</script>

<style scoped>
/* 页面整体布局 - 白色背景，支持滚动 */
.login-page {
  min-width: 100vw;
  min-height: 100vh;
  background: #ffffff;
  font-family:
    -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  overflow-y: auto;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
}

/* 登录主容器 */
.login-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 20px 40px 20px; /* 为导航栏留出更多空间，底部增加更多空间 */
  margin-top: 0; /* 移除向上偏移 */
  min-height: calc(100vh - 60px); /* 确保最小高度 */
}

/* 品牌区域 - 在卡片上方 */
.brand-section {
  margin-bottom: 20px;
}

.brand-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.logo-image {
  width: 40px;
  height: 40px;
  border-radius: 8px;
}

.brand-text {
  font-size: 24px;
  font-weight: 600;
  background: linear-gradient(135deg, #1890ff 0%, #40a9ff 50%, #69c0ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.02em;
}

/* 登录卡片 - 白色背景带阴影，更窄的设计 */
.login-card {
  background: white;
  border-radius: 16px;
  padding: 32px 28px; /* 减少内边距 */
  width: 100%;
  max-width: 360px; /* 从400px减少到360px，让卡片更窄 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  position: relative;
}

/* 登录标题 */
.login-title {
  font-size: 22px; /* 稍微减小字体 */
  font-weight: 600;
  color: #1c1f23;
  text-align: center;
  margin: 0 0 28px 0; /* 减少下边距 */
}

/* 表单样式 */
.login-form {
  width: 100%;
}

.form-field {
  margin-bottom: 18px; /* 减少字段间距 */
}

.field-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}

.input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 12px;
  width: 16px;
  height: 16px;
  color: #9ca3af;
  z-index: 2;
}

.form-input {
  width: 100%;
  padding: 12px 12px 12px 40px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  background: #f9fafb;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input.error {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.error-message {
  color: #ef4444;
  font-size: 14px;
  margin-top: 8px;
  margin-left: 4px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.form-input::placeholder {
  color: #9ca3af;
}

/* 密码切换按钮 */
.password-toggle {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: 4px;
  z-index: 2;
}

.password-toggle svg {
  width: 16px;
  height: 16px;
}

.password-toggle:hover {
  color: #6b7280;
}

/* 用户协议 */
.form-options {
  margin-bottom: 20px; /* 减少间距 */
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 14px;
  color: #6b7280;
}

.checkbox-input {
  display: none;
}

.checkbox-mark {
  width: 16px;
  height: 16px;
  border: 1px solid #d1d5db;
  border-radius: 3px;
  margin-right: 8px;
  position: relative;
  background: white;
  flex-shrink: 0;
}

.checkbox-input:checked + .checkbox-mark {
  background: #3b82f6;
  border-color: #3b82f6;
}

.checkbox-input:checked + .checkbox-mark::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 10px;
  font-weight: bold;
}

.checkbox-text {
  margin-right: 4px;
}

.terms-link {
  color: #3b82f6;
  text-decoration: none;
}

.terms-link:hover {
  text-decoration: underline;
}

/* 登录按钮 */
.login-button {
  width: 100%;
  padding: 11px; /* 稍微减少内边距 */
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease;
  margin-bottom: 14px; /* 减少下边距 */
}

.login-button:hover:not(:disabled) {
  background: #2563eb;
}

.login-button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

/* 忘记密码 */
.forgot-section {
  text-align: center;
  margin-bottom: 20px; /* 减少间距 */
}

.forgot-link {
  color: #3b82f6;
  text-decoration: none;
  font-size: 14px;
}

.forgot-link:hover {
  text-decoration: underline;
}

/* 分隔线 */
.divider {
  position: relative;
  text-align: center;
  margin: 20px 0; /* 减少间距 */
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #e5e7eb;
}

.divider-text {
  background: white;
  padding: 0 16px;
  color: #9ca3af;
  font-size: 14px;
}

/* 其他登录方式 */
.other-login-section {
  margin-bottom: 20px; /* 减少间距 */
}

.other-login-button {
  width: 100%;
  padding: 12px;
  background: white;
  color: #374151;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.other-login-button:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

/* 注册提示 */
.register-section {
  text-align: center;
  font-size: 14px;
}

.register-text {
  color: #6b7280;
  margin-right: 8px;
}

.register-link {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
}

.register-link:hover {
  text-decoration: underline;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-container {
    padding: 80px 16px 30px 16px;
    margin-top: 0;
    min-height: calc(100vh - 60px);
  }

  .login-card {
    padding: 28px 20px;
    margin: 0;
    max-width: none;
    width: 100%;
  }

  .brand-text {
    font-size: 20px;
  }

  .login-title {
    font-size: 20px;
  }

  .logo-image {
    width: 32px;
    height: 32px;
  }
}

@media (max-width: 320px) {
  .login-card {
    padding: 24px 16px;
  }

  .login-container {
    padding: 70px 12px 20px 12px;
  }
}

/* 低高度设备优化 - 支持滚动 */
@media (max-height: 700px) {
  .login-container {
    justify-content: flex-start;
    padding-top: 60px;
    margin-top: 0;
  }

  .brand-section {
    margin-bottom: 16px;
  }
}

@media (max-height: 600px) {
  .login-container {
    padding: 20px;
    margin-top: 0;
  }

  .login-card {
    padding: 20px;
  }

  .brand-section {
    margin-bottom: 12px;
  }

  .login-title {
    margin-bottom: 16px;
    font-size: 18px;
  }

  .form-field {
    margin-bottom: 14px;
  }
}

@media (max-height: 500px) {
  .login-container {
    padding: 10px;
  }

  .login-card {
    padding: 16px;
  }

  .brand-section {
    margin-bottom: 8px;
  }

  .login-title {
    margin-bottom: 12px;
    font-size: 16px;
  }

  .form-field {
    margin-bottom: 10px;
  }

  .field-label {
    font-size: 13px;
    margin-bottom: 6px;
  }

  .form-input {
    padding: 10px 10px 10px 36px;
    font-size: 13px;
  }
}
</style>
