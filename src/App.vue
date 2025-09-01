<script setup></script>

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
            <h4 class="brand-title">鱼卫 PhishGuard</h4>
          </div>
        </router-link>

        <!-- 导航菜单 -->
        <nav class="primary-nav">
          <router-link to="/" class="nav-link active-link">
            <span>首页</span>
          </router-link>
          <a href="#" class="nav-link">
            <span>控制台</span>
          </a>
          <a href="#" class="nav-link">
            <span>定价</span>
          </a>
          <a href="#" class="nav-link">
            <span>代理加盟</span>
          </a>
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
          <!-- 未登录状态 -->
          <div class="auth-buttons">
            <router-link to="/login" class="login-btn">
              登录
            </router-link>
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

.nav-link.active-link,
.nav-link.router-link-active {
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
  gap: 8px;
}

.login-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  background: #1890ff;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  border: 1px solid #1890ff;
}

.login-btn:hover {
  background: #40a9ff;
  border-color: #40a9ff;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.3);
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
}
</style>
