<template>
  <div class="login">
    <!-- 登录主要内容区域 -->
    <main class="login-content">
      <!-- 背景装饰 -->
      <div class="background-decoration"></div>

      <!-- 登录表单容器 -->
      <section class="login-section">
        <div class="login-container">
          <!-- 品牌logo -->
          <div class="brand-logo-container">
            <img src="https://ai.wlai.vip/logo123.png" alt="PhishGuard Logo" class="brand-logo-img" />
            <h1 class="brand-title">PhishGuard</h1>
          </div>

          <!-- 登录标题 -->
          <h2 class="login-title">登录</h2>

          <!-- 登录表单 -->
          <form class="login-form" @submit.prevent="handleLogin">
            <!-- 用户名或邮箱输入 -->
            <div class="form-group">
              <label class="form-label">用户名或邮箱</label>
              <div class="input-wrapper">
                <svg class="input-icon" fill="currentColor" viewBox="0 0 24 24" width="16" height="16">
                  <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                </svg>
                <input
                  type="email"
                  v-model="loginForm.email"
                  placeholder="请输入您的用户名或邮箱地址"
                  class="form-input"
                  required
                />
              </div>
            </div>

            <!-- 密码输入 -->
            <div class="form-group">
              <label class="form-label">密码</label>
              <div class="input-wrapper">
                <svg class="input-icon" fill="currentColor" viewBox="0 0 24 24" width="16" height="16">
                  <path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zM12 17c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zM15.1 8H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/>
                </svg>
                <input
                  :type="showPassword ? 'text' : 'password'"
                  v-model="loginForm.password"
                  placeholder="请输入您的密码"
                  class="form-input"
                  required
                />
                <button
                  type="button"
                  @click="togglePassword"
                  class="password-toggle"
                  aria-label="切换密码显示"
                >
                  <svg v-if="showPassword" fill="currentColor" viewBox="0 0 24 24" width="16" height="16">
                    <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
                  </svg>
                  <svg v-else fill="currentColor" viewBox="0 0 24 24" width="16" height="16">
                    <path d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- 记住密码和忘记密码 -->
            <div class="form-options">
              <label class="checkbox-container">
                <input type="checkbox" v-model="rememberMe" class="checkbox-input">
                <span class="checkbox-custom"></span>
                <span class="checkbox-label">我已阅读并同意</span>
                <router-link to="/terms" class="terms-link">《用户协议》</router-link>
              </label>
            </div>

            <!-- 登录按钮 -->
            <button type="submit" class="login-button" :disabled="isLoading">
              <span v-if="!isLoading">登录</span>
              <span v-else>登录中...</span>
            </button>

            <!-- 忘记密码 -->
            <div class="forgot-password">
              <router-link to="/forgot-password" class="forgot-link">忘记密码？</router-link>
            </div>

            <!-- 分隔线 -->
            <div class="divider">
              <span class="divider-text">或</span>
            </div>

            <!-- 其他登录方式 -->
            <div class="other-login">
              <button type="button" class="other-login-btn">
                其他登录方式
              </button>
            </div>

            <!-- 注册链接 -->
            <div class="register-link">
              <span class="register-text">没有账户？</span>
              <router-link to="/register" class="register-btn">注册</router-link>
            </div>
          </form>
        </div>
      </section>
    </main>

    <!-- 底部版权信息 -->
    <footer class="login-footer">
      <p class="copyright">Copyright © 2025 重庆云之雾网络科技有限公司 版权所有 友链: 电影小窝</p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// 页面组件逻辑
defineOptions({
  name: 'LoginPage',
})

const router = useRouter()

// 表单数据
const loginForm = ref({
  email: '',
  password: ''
})

// 表单状态
const showPassword = ref(false)
const rememberMe = ref(false)
const isLoading = ref(false)

// 切换密码显示
const togglePassword = () => {
  showPassword.value = !showPassword.value
}

// 处理登录
const handleLogin = async () => {
  if (!loginForm.value.email || !loginForm.value.password) {
    alert('请填写完整的登录信息')
    return
  }

  isLoading.value = true

  try {
    // 这里添加实际的登录逻辑
    console.log('登录信息:', loginForm.value)

    // 模拟登录请求
    await new Promise(resolve => setTimeout(resolve, 1000))

    // 登录成功后跳转
    router.push('/')
  } catch (error) {
    console.error('登录失败:', error)
    alert('登录失败，请重试')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* 页面整体布局 */
.login {
  min-height: 100vh;
  background: #ffffff;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  display: flex;
  flex-direction: column;
}

/* 主要内容区域 */
.login-content {
  flex: 1;
  position: relative;
  padding-top: 64px; /* 为固定导航栏留出空间 */
  min-height: calc(100vh - 64px);
}

/* 背景装饰 */
.background-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(
    ellipse 60% 70% at 30% 40%,
    rgba(234, 245, 255, 0.3) 0%,
    rgba(233, 247, 253, 0.2) 35%,
    rgba(248, 250, 252, 0.1) 60%,
    transparent 80%
  );
  z-index: 1;
}

/* 登录区域 */
.login-section {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 128px);
  padding: 40px 20px;
}

/* 登录容器 */
.login-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
  padding: 48px;
  width: 100%;
  max-width: 400px;
  text-align: center;
}

/* 品牌logo区域 */
.brand-logo-container {
  margin-bottom: 32px;
}

.brand-logo-img {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  margin-bottom: 12px;
}

.brand-title {
  font-size: 24px;
  font-weight: 600;
  color: #1c1f23;
  margin: 0;
}

/* 登录标题 */
.login-title {
  font-size: 28px;
  font-weight: 600;
  color: #1c1f23;
  margin: 0 0 32px 0;
}

/* 表单样式 */
.login-form {
  text-align: left;
}

.form-group {
  margin-bottom: 24px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 12px;
  color: #9CA3AF;
  z-index: 2;
}

.form-input {
  width: 100%;
  padding: 12px 12px 12px 40px;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  font-size: 14px;
  background: #F9FAFB;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #3B82F6;
  background: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input::placeholder {
  color: #9CA3AF;
}

/* 密码切换按钮 */
.password-toggle {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  color: #9CA3AF;
  cursor: pointer;
  padding: 4px;
  z-index: 2;
}

.password-toggle:hover {
  color: #6B7280;
}

/* 表单选项 */
.form-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.checkbox-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 14px;
  color: #6B7280;
}

.checkbox-input {
  display: none;
}

.checkbox-custom {
  width: 16px;
  height: 16px;
  border: 1px solid #D1D5DB;
  border-radius: 3px;
  margin-right: 8px;
  position: relative;
  background: white;
}

.checkbox-input:checked + .checkbox-custom {
  background: #3B82F6;
  border-color: #3B82F6;
}

.checkbox-input:checked + .checkbox-custom::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 10px;
  font-weight: bold;
}

.checkbox-label {
  margin-right: 4px;
}

.terms-link {
  color: #3B82F6;
  text-decoration: none;
}

.terms-link:hover {
  text-decoration: underline;
}

/* 登录按钮 */
.login-button {
  width: 100%;
  padding: 12px;
  background: #3B82F6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease;
  margin-bottom: 16px;
}

.login-button:hover:not(:disabled) {
  background: #2563EB;
}

.login-button:disabled {
  background: #9CA3AF;
  cursor: not-allowed;
}

/* 忘记密码 */
.forgot-password {
  text-align: center;
  margin-bottom: 24px;
}

.forgot-link {
  color: #3B82F6;
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
  margin: 24px 0;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #E5E7EB;
}

.divider-text {
  background: white;
  padding: 0 16px;
  color: #9CA3AF;
  font-size: 14px;
}

/* 其他登录方式 */
.other-login {
  margin-bottom: 24px;
}

.other-login-btn {
  width: 100%;
  padding: 12px;
  background: white;
  color: #374151;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.other-login-btn:hover {
  background: #F9FAFB;
  border-color: #D1D5DB;
}

/* 注册链接 */
.register-link {
  text-align: center;
  font-size: 14px;
}

.register-text {
  color: #6B7280;
  margin-right: 8px;
}

.register-btn {
  color: #3B82F6;
  text-decoration: none;
  font-weight: 500;
}

.register-btn:hover {
  text-decoration: underline;
}

/* 底部版权 */
.login-footer {
  background: #F9FAFB;
  padding: 16px 20px;
  text-align: center;
  border-top: 1px solid #E5E7EB;
}

.copyright {
  color: #6B7280;
  font-size: 12px;
  margin: 0;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-container {
    padding: 32px 24px;
    margin: 0 16px;
    max-width: none;
  }

  .brand-logo-img {
    width: 40px;
    height: 40px;
  }

  .brand-title {
    font-size: 20px;
  }

  .login-title {
    font-size: 24px;
  }
}

@media (max-width: 320px) {
  .login-container {
    padding: 24px 16px;
  }
}
</style>
