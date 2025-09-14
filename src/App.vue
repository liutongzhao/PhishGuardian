<script setup>
import { computed, ref, watch, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import wsManager from '@/utils/websocket'

const authStore = useAuthStore()
const router = useRouter()
const showUserDropdown = ref(false)

// 计算属性
const isAuthenticated = computed(() => authStore.isAuthenticated)
const currentUser = computed(() => authStore.user)

// 切换用户下拉菜单
const toggleUserDropdown = () => {
  showUserDropdown.value = !showUserDropdown.value
}

// 关闭下拉菜单
const closeUserDropdown = () => {
  showUserDropdown.value = false
}

// 处理退出登录
const handleLogout = async () => {
  closeUserDropdown()
  // 断开WebSocket连接
  wsManager.disconnect()
  await authStore.logout()
  router.push('/')
}

// 全局WebSocket连接管理
const initializeWebSocket = () => {
  if (authStore.isAuthenticated && !wsManager.isConnected) {
    wsManager.connect()
  }
}

const cleanupWebSocket = () => {
  if (wsManager.isConnected) {
    wsManager.disconnect()
  }
}

// 监听认证状态变化
watch(
  () => authStore.isAuthenticated,
  (isAuthenticated) => {
    if (isAuthenticated) {
      // 用户登录时连接WebSocket
      initializeWebSocket()
    } else {
      // 用户退出时断开WebSocket
      cleanupWebSocket()
    }
  },
  { immediate: true }
)

// 组件挂载时初始化WebSocket
onMounted(() => {
  initializeWebSocket()
})

// 组件卸载时清理WebSocket
onUnmounted(() => {
  cleanupWebSocket()
})

// 点击外部关闭下拉菜单
const handleClickOutside = (event) => {
  if (!event.target.closest('.user-dropdown-container')) {
    closeUserDropdown()
  }
}

// 监听全局点击事件
if (typeof window !== 'undefined') {
  document.addEventListener('click', handleClickOutside)
}
</script>

<template>
  <div class="app">
    <!-- 主要内容区域 -->
    <main class="page-content">
      <!-- 路由内容 -->
      <router-view />
    </main>

    <!-- 顶部导航栏 - 固定悬浮层 -->
    <header class="navbar">
      <!-- 左侧区域 -->
      <div class="navbar-left">
        <!-- 移动端菜单按钮 -->
        <div class="mobile-menu-btn">
          <button class="menu-toggle-btn" aria-label="打开菜单">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              width="18"
              height="18"
            >
              <path
                d="M2 19.5c0-.83.67-1.5 1.5-1.5h17a1.5 1.5 0 0 1 0 3h-17A1.5 1.5 0 0 1 2 19.5Z"
                fill="currentColor"
              />
              <path
                d="M2 12c0-.83.67-1.5 1.5-1.5h17a1.5 1.5 0 0 1 0 3h-17A1.5 1.5 0 0 1 2 12Z"
                fill="currentColor"
              />
              <path
                d="M2 4.5C2 3.67 2.67 3 3.5 3h17a1.5 1.5 0 0 1 0 3h-17A1.5 1.5 0 0 1 2 4.5Z"
                fill="currentColor"
              />
            </svg>
          </button>
        </div>

        <!-- Logo区域 -->
        <router-link to="/" class="brand-logo">
          <img src="https://ai.wlai.vip/logo123.png" alt="logo" class="brand-icon" />
          <div class="brand-text-wrapper">
            <h4 class="brand-title">智邮盾 PhishGuard</h4>
          </div>
        </router-link>

        <!-- 导航菜单 -->
        <nav class="primary-nav">
          <router-link to="/" class="nav-link">
            <span>首页</span>
          </router-link>
          <router-link to="/console" class="nav-link">
            <span>控制台</span>
          </router-link>
          <a href="#" class="nav-link">
            <span>联系我们</span>
          </a>
          <a href="#" class="nav-link" target="_blank">
            <span>文档</span>
          </a>
        </nav>
      </div>

      <!-- 中间透明区域 -->
      <div class="navbar-center"></div>

      <!-- 右侧区域 -->
      <div class="navbar-right">
        <!-- 功能按钮组 -->
        <div class="action-buttons">
          <button class="action-btn notification-btn" aria-label="系统公告">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              width="18"
              height="18"
            >
              <path
                d="M18 9a6 6 0 0 0-3-5.2 3 3 0 0 0-6 0A6 6 0 0 0 6 9s0 2-.5 4c-.28 1.13-1.69 2.9-2.86 4.23-.58.67-.12 1.77.77 1.77H20.6c.89 0 1.35-1.1.77-1.77-1.17-1.32-2.58-3.1-2.86-4.23-.5-2-.5-4-.5-4Z"
                fill="currentColor"
              />
              <path d="M15 20a3 3 0 1 1-6 0h6Z" fill="currentColor" />
            </svg>
          </button>

          <button class="action-btn theme-btn" aria-label="切换主题">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              width="18"
              height="18"
            >
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M12 23a11 11 0 1 0 0-22 11 11 0 0 0 0 22Zm5-8c.48 0 .94-.05 1.39-.14a7 7 0 1 1-7.78-9.72A7 7 0 0 0 17 15Z"
                fill="currentColor"
              />
            </svg>
          </button>

          <button class="action-btn language-btn" aria-label="切换语言">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              width="18"
              height="18"
            >
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="m6.62 3.25.44.75H2.6C1.72 4 1 4.67 1 5.5S1.72 7 2.6 7h1.9c0 2.45 1.1 4.71 2.5 6.5-1.1.64-2.63 1-4 1a1.5 1.5 0 1 0 0 3c2.23 0 4.3-.7 6-1.88 1.4.98 3.06 1.62 4.85 1.82l-1.7 3.39a1.5 1.5 0 0 0 2.7 1.34l.58-1.17h4.14l.59 1.17a1.5 1.5 0 0 0 2.68-1.34l-4-8a1.5 1.5 0 0 0-2.68 0l-.85 1.7a1.5 1.5 0 0 0-.31-.03c-1.37 0-2.9-.36-4-1A10.7 10.7 0 0 0 13.5 7h1.9c.88 0 1.6-.67 1.6-1.5S16.28 4 15.4 4h-4.88l-1.3-2.25a1.5 1.5 0 0 0-2.6 1.5ZM7.5 7h3c0 1.69-.56 3.25-1.5 4.5A7.47 7.47 0 0 1 7.5 7Zm10 9.85L18.57 19h-2.14l1.07-2.15Z"
                fill="currentColor"
              />
            </svg>
          </button>
        </div>

        <!-- 用户信息/登录区域 -->
        <div class="user-section">
          <!-- 已登录状态 -->
          <div v-if="isAuthenticated" class="user-dropdown-container">
            <button class="user-info-btn" @click="toggleUserDropdown">
              <div class="user-avatar">
                <span class="avatar-text">{{
                  currentUser?.username?.charAt(0)?.toUpperCase() || 'U'
                }}</span>
              </div>
              <span class="username">{{ currentUser?.username || '用户' }}</span>
              <svg
                class="dropdown-arrow"
                :class="{ 'arrow-up': showUserDropdown }"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <polyline points="6 9 12 15 18 9" />
              </svg>
            </button>

            <!-- 用户下拉菜单 -->
            <div v-if="showUserDropdown" class="user-dropdown-menu">
              <div class="dropdown-header">
                <div class="user-info">
                  <div class="user-avatar large">
                    <span class="avatar-text">{{
                      currentUser?.username?.charAt(0)?.toUpperCase() || 'U'
                    }}</span>
                  </div>
                  <div class="user-details">
                    <div class="user-name">{{ currentUser?.username || '用户' }}</div>
                    <div class="user-email">{{ currentUser?.email || '' }}</div>
                  </div>
                </div>
              </div>

              <div class="dropdown-divider"></div>

              <div class="dropdown-menu-items">
                <router-link to="/console" class="dropdown-item" @click="closeUserDropdown">
                  <svg
                    class="item-icon"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <rect x="3" y="3" width="7" height="9" rx="1" />
                    <rect x="14" y="3" width="7" height="5" rx="1" />
                    <rect x="14" y="12" width="7" height="9" rx="1" />
                    <rect x="3" y="16" width="7" height="5" rx="1" />
                  </svg>
                  <span>控制台</span>
                </router-link>

                <a href="#" class="dropdown-item" @click="closeUserDropdown">
                  <svg
                    class="item-icon"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                    <circle cx="12" cy="7" r="4" />
                  </svg>
                  <span>个人设置</span>
                </a>

                <a href="#" class="dropdown-item" @click="closeUserDropdown">
                  <svg
                    class="item-icon"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <circle cx="12" cy="12" r="3" />
                    <path
                      d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"
                    />
                  </svg>
                  <span>账户设置</span>
                </a>
              </div>

              <div class="dropdown-divider"></div>

              <div class="dropdown-menu-items">
                <button class="dropdown-item logout-item" @click="handleLogout">
                  <svg
                    class="item-icon"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                    <polyline points="16 17 21 12 16 7" />
                    <line x1="21" y1="12" x2="9" y2="12" />
                  </svg>
                  <span>退出登录</span>
                </button>
              </div>
            </div>
          </div>

          <!-- 未登录状态 -->
          <div v-else class="auth-buttons">
            <div class="auth-button-group">
              <router-link to="/login" class="auth-btn login-btn"> 登录 </router-link>
              <router-link to="/register" class="auth-btn register-btn"> 注册 </router-link>
            </div>
          </div>
        </div>
      </div>
    </header>
  </div>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app {
  min-height: 100vh;
  background: #ffffff;
  font-family:
    -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

/* 页面内容区域 */
.page-content {
  min-height: 100vh;
  position: relative;
}

/* 顶部导航栏 - 固定悬浮层 */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  display: flex;
  z-index: 1000;
  pointer-events: auto;
}

/* 左侧区域 - 白色背景 */
.navbar-left {
  background: rgba(255, 255, 255, 1);
  display: flex;
  align-items: center;
  padding: 0 24px;
  gap: 24px;
  min-width: fit-content;
}

/* 中间区域 - 透明毛玻璃 */
.navbar-center {
  flex: 1;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

/* 右侧区域 - 白色背景 */
.navbar-right {
  background: rgba(255, 255, 255, 1);
  display: flex;
  align-items: center;
  padding: 0 24px;
  gap: 12px;
  min-width: fit-content;
}

/* 移动端菜单按钮 */
.mobile-menu-btn {
  display: none;
}

.menu-toggle-btn {
  background: none;
  border: none;
  padding: 8px;
  border-radius: 6px;
  color: #4e5969;
  cursor: pointer;
  transition: all 0.2s ease;
}

.menu-toggle-btn:hover {
  background: rgba(17, 25, 39, 0.04);
  color: #1890ff;
}

/* Logo区域 */
.brand-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  transition: transform 0.3s ease;
}

.brand-logo:hover {
  transform: scale(1.05);
}

.brand-icon {
  height: 28px;
  width: 28px;
  border-radius: 50%;
  transition: transform 0.3s ease;
}

.brand-text-wrapper {
  display: flex;
  align-items: center;
}

.brand-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  background: linear-gradient(135deg, #1890ff 0%, #40a9ff 50%, #69c0ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.02em;
}

/* 导航菜单 */
.primary-nav {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: 24px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  font-size: 14px;
  font-weight: 700;
  color: #4e5969;
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.2s ease;
  position: relative;
}

.nav-link:hover {
  color: #0064fa;
  font-weight: 700;
}

/* 功能按钮组 */
.action-buttons {
  display: flex;
  align-items: center;
  gap: 4px;
}

.action-btn {
  background: rgba(17, 25, 39, 0.04);
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 6px;
  border-radius: 50%;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
}

.action-btn:hover {
  background: rgba(17, 25, 39, 0.08);
  color: #374151;
  transform: translateY(-1px);
}

/* 用户信息/登录区域 */
.user-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: 8px;
}

/* 认证按钮 */
.auth-buttons {
  display: flex;
  align-items: center;
}

.auth-button-group {
  display: flex;
  background: #ffffff;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e1e5e9;
}

.auth-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
  border: none;
  min-width: 60px;
}

.login-btn {
  background: #f5f5f5;
  color: #666666;
  border-radius: 20px 0 0 20px;
}

.login-btn:hover {
  background: #e8e8e8;
  color: #333333;
}

.register-btn {
  background: #1890ff;
  color: white;
  border-radius: 0 20px 20px 0;
}

.register-btn:hover {
  background: #40a9ff;
}

/* 用户下拉菜单样式 */
.user-dropdown-container {
  position: relative;
}

.user-info-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: transparent;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
  color: #374151;
}

.user-info-btn:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

.user-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1890ff 0%, #40a9ff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.user-avatar.large {
  width: 40px;
  height: 40px;
}

.avatar-text {
  color: white;
  font-weight: 600;
  font-size: 12px;
}

.user-avatar.large .avatar-text {
  font-size: 16px;
}

.username {
  font-weight: 500;
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropdown-arrow {
  width: 16px;
  height: 16px;
  transition: transform 0.2s ease;
}

.dropdown-arrow.arrow-up {
  transform: rotate(180deg);
}

.user-dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 280px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  z-index: 1001;
  overflow: hidden;
}

.dropdown-header {
  padding: 16px;
  background: #f9fafb;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-details {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-weight: 600;
  font-size: 16px;
  color: #111827;
  margin-bottom: 2px;
}

.user-email {
  font-size: 14px;
  color: #6b7280;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropdown-divider {
  height: 1px;
  background: #e5e7eb;
  margin: 0;
}

.dropdown-menu-items {
  padding: 8px 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 12px 16px;
  background: none;
  border: none;
  text-decoration: none;
  color: #374151;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.dropdown-item:hover {
  background: #f3f4f6;
}

.dropdown-item.logout-item {
  color: #dc2626;
}

.dropdown-item.logout-item:hover {
  background: #fef2f2;
}

.item-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.dropdown-item.logout-item .item-icon {
  color: #dc2626;
}

/* 原用户样式保留但隐藏 */
.user-profile {
  display: none;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .navbar-left,
  .navbar-right {
    padding: 0 20px;
  }

  .primary-nav {
    gap: 6px;
    margin-left: 16px;
  }

  .nav-link {
    padding: 6px 10px;
    font-size: 13px;
  }
}

@media (max-width: 768px) {
  .mobile-menu-btn {
    display: block;
  }

  .navbar-left {
    padding: 0 16px;
    gap: 16px;
  }

  .navbar-right {
    padding: 0 16px;
    gap: 8px;
  }

  .brand-title {
    font-size: 16px;
  }

  .brand-icon {
    height: 24px;
    width: 24px;
  }

  .primary-nav {
    display: none;
  }

  .action-btn {
    width: 28px;
    height: 28px;
    padding: 4px;
  }

  .user-avatar {
    width: 24px;
    height: 24px;
  }

  .avatar-text {
    font-size: 10px;
  }

  .username {
    font-size: 11px;
  }

  .page-content {
    position: relative;
  }
}

@media (max-width: 480px) {
  .navbar-left,
  .navbar-right {
    padding: 0 12px;
  }

  .brand-title {
    font-size: 15px;
  }

  .brand-text-wrapper {
    display: none;
  }

  .username {
    display: none;
  }

  .action-btn {
    width: 26px;
    height: 26px;
  }

  .user-avatar {
    width: 22px;
    height: 22px;
  }

  .auth-btn {
    padding: 6px 12px;
    font-size: 13px;
    min-width: 50px;
  }
}
</style>
