<template>
  <div class="register-page">
    <!-- 注册主容器 -->
    <div class="register-container">
      <!-- 品牌Logo - 在卡片上方 -->
      <div class="brand-section">
        <div class="brand-logo">
          <img src="https://ai.wlai.vip/logo123.png" alt="PhishGuard Logo" class="logo-image" />
          <span class="brand-text">PhishGuard</span>
        </div>
      </div>

      <!-- 注册卡片 -->
      <div class="register-card">
        <!-- 注册标题 -->
        <h1 class="register-title">注册</h1>

        <!-- 注册表单 -->
        <form class="register-form" @submit.prevent="handleRegister">
          <!-- 用户名输入 -->
          <div class="form-field">
            <label class="field-label">用户名</label>
            <div class="input-container">
              <svg class="input-icon" viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
                />
              </svg>
              <input
                type="text"
                v-model="registerForm.username"
                placeholder="请输入用户名"
                class="form-input"
                required
              />
            </div>
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
                v-model="registerForm.password"
                placeholder="输入密码，最短 8 位，最长 20 位"
                class="form-input"
                required
                minlength="8"
                maxlength="20"
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
          </div>

          <!-- 确认密码输入 -->
          <div class="form-field">
            <label class="field-label">确认密码</label>
            <div class="input-container">
              <svg class="input-icon" viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zM12 17c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zM15.1 8H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"
                />
              </svg>
              <input
                :type="showConfirmPassword ? 'text' : 'password'"
                v-model="registerForm.confirmPassword"
                placeholder="确认密码"
                class="form-input"
                required
              />
              <button
                type="button"
                @click="toggleConfirmPassword"
                class="password-toggle"
                aria-label="切换确认密码显示"
              >
                <svg v-if="showConfirmPassword" viewBox="0 0 24 24" fill="currentColor">
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
          </div>

          <!-- 邮箱输入 -->
          <div class="form-field">
            <label class="field-label">邮箱</label>
            <div class="input-container">
              <svg class="input-icon" viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.89 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"
                />
              </svg>
              <input
                type="email"
                v-model="registerForm.email"
                placeholder="输入邮箱地址"
                class="form-input"
                required
              />
              <button
                type="button"
                @click="sendVerificationCode"
                class="verification-btn"
                :disabled="!registerForm.email || isCodeSending"
              >
                {{ isCodeSending ? '发送中...' : '获取验证码' }}
              </button>
            </div>
          </div>

          <!-- 验证码输入 -->
          <div class="form-field">
            <label class="field-label">验证码</label>
            <div class="input-container">
              <svg class="input-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z" />
              </svg>
              <input
                type="text"
                v-model="registerForm.verificationCode"
                placeholder="输入验证码"
                class="form-input"
                required
                maxlength="6"
              />
            </div>
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

          <!-- 注册按钮 -->
          <button type="submit" class="register-button" :disabled="isLoading || !agreeTerms">
            <span v-if="!isLoading">注册</span>
            <span v-else>注册中...</span>
          </button>

          <!-- 分隔线 -->
          <div class="divider">
            <span class="divider-text">或</span>
          </div>

          <!-- 其他注册方式 -->
          <div class="other-register-section">
            <button type="button" class="other-register-button">其他注册选项</button>
          </div>

          <!-- 登录提示 -->
          <div class="login-section">
            <span class="login-text">已有账户？</span>
            <router-link to="/login" class="login-link">登录</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

defineOptions({
  name: 'RegisterPage',
})

const router = useRouter()

// 表单数据
const registerForm = ref({
  username: '',
  password: '',
  confirmPassword: '',
  email: '',
  verificationCode: '',
})

// 表单状态
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const agreeTerms = ref(false)
const isLoading = ref(false)
const isCodeSending = ref(false)

// 切换密码显示
const togglePassword = () => {
  showPassword.value = !showPassword.value
}

// 切换确认密码显示
const toggleConfirmPassword = () => {
  showConfirmPassword.value = !showConfirmPassword.value
}

// 发送验证码
const sendVerificationCode = async () => {
  if (!registerForm.value.email) {
    alert('请先输入邮箱地址')
    return
  }

  isCodeSending.value = true

  try {
    // 这里添加发送验证码的逻辑
    console.log('发送验证码到:', registerForm.value.email)

    // 模拟发送验证码请求
    await new Promise((resolve) => setTimeout(resolve, 1000))

    alert('验证码已发送到您的邮箱')
  } catch (error) {
    console.error('发送验证码失败:', error)
    alert('发送验证码失败，请重试')
  } finally {
    isCodeSending.value = false
  }
}

// 处理注册
const handleRegister = async () => {
  // 表单验证
  if (
    !registerForm.value.username ||
    !registerForm.value.password ||
    !registerForm.value.confirmPassword ||
    !registerForm.value.email ||
    !registerForm.value.verificationCode
  ) {
    alert('请填写完整的注册信息')
    return
  }

  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    alert('两次输入的密码不一致')
    return
  }

  if (registerForm.value.password.length < 8 || registerForm.value.password.length > 20) {
    alert('密码长度应在8-20位之间')
    return
  }

  if (!agreeTerms.value) {
    alert('请先同意用户协议')
    return
  }

  isLoading.value = true

  try {
    console.log('注册信息:', registerForm.value)

    // 模拟注册请求
    await new Promise((resolve) => setTimeout(resolve, 1500))

    alert('注册成功！')
    // 注册成功后跳转到登录页面
    router.push('/login')
  } catch (error) {
    console.error('注册失败:', error)
    alert('注册失败，请重试')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* 页面整体布局 - 白色背景，完全无滚动 */
.register-page {
  width: 100vw;
  height: 100vh;
  background: #ffffff;
  font-family:
    -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
}

/* 注册主容器 */
.register-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px 20px 20px; /* 为导航栏留出空间 */
  margin-top: -40px; /* 向上偏移 */
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

/* 注册卡片 - 白色背景带阴影，更窄的设计 */
.register-card {
  background: white;
  border-radius: 16px;
  padding: 32px 28px;
  width: 100%;
  max-width: 360px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  position: relative;
}

/* 注册标题 */
.register-title {
  font-size: 22px;
  font-weight: 600;
  color: #1c1f23;
  text-align: center;
  margin: 0 0 28px 0;
}

/* 表单样式 */
.register-form {
  width: 100%;
}

.form-field {
  margin-bottom: 18px;
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

/* 验证码按钮 */
.verification-btn {
  position: absolute;
  right: 8px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 6px 12px;
  font-size: 12px;
  cursor: pointer;
  transition: background 0.2s ease;
  z-index: 2;
}

.verification-btn:hover:not(:disabled) {
  background: #2563eb;
}

.verification-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

/* 用户协议 */
.form-options {
  margin-bottom: 20px;
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

/* 注册按钮 */
.register-button {
  width: 100%;
  padding: 11px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease;
  margin-bottom: 14px;
}

.register-button:hover:not(:disabled) {
  background: #2563eb;
}

.register-button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

/* 分隔线 */
.divider {
  position: relative;
  text-align: center;
  margin: 20px 0;
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

/* 其他注册方式 */
.other-register-section {
  margin-bottom: 20px;
}

.other-register-button {
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

.other-register-button:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

/* 登录提示 */
.login-section {
  text-align: center;
  font-size: 14px;
}

.login-text {
  color: #6b7280;
  margin-right: 8px;
}

.login-link {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
}

.login-link:hover {
  text-decoration: underline;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .register-card {
    padding: 28px 20px;
    margin: 0 16px;
    max-width: none;
  }

  .brand-text {
    font-size: 20px;
  }

  .register-title {
    font-size: 20px;
  }

  .logo-image {
    width: 32px;
    height: 32px;
  }

  .register-container {
    margin-top: -20px;
  }
}

@media (max-width: 320px) {
  .register-card {
    padding: 24px 16px;
  }
}

/* 确保在所有情况下都无滚动 */
@media (max-height: 600px) {
  .register-container {
    padding: 20px;
    margin-top: -20px;
  }

  .register-card {
    padding: 20px;
  }

  .brand-section {
    margin-bottom: 16px;
  }

  .register-title {
    margin-bottom: 20px;
  }
}
</style>
