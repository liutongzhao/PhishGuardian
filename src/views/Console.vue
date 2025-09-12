<template>
  <div class="console-page">
    <!-- 控制台主容器 -->
    <div class="console-container">
      <!-- 左侧导航栏 -->
      <aside class="console-sidebar" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
        <!-- 控制台标题 -->
        <div class="sidebar-header">
          <h2 class="sidebar-title">控制台</h2>
          <button class="toggle-sidebar" @click="toggleSidebar">
            <svg
              v-if="!isSidebarCollapsed"
              class="toggle-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <polyline points="15 18 9 12 15 6" />
            </svg>
            <svg
              v-else
              class="toggle-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <polyline points="9 18 15 12 9 6" />
            </svg>
          </button>
        </div>

        <!-- 导航菜单 -->
        <nav class="sidebar-nav">
          <router-link
            to="/console/dashboard"
            class="nav-item"
            :class="{ active: $route.path.includes('dashboard') }"
          >
            <svg
              class="nav-icon"
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
            <span class="nav-text">数据看板</span>
          </router-link>

          <router-link
            to="/console/email-bind"
            class="nav-item"
            :class="{ active: $route.path.includes('email-bind') }"
          >
            <svg
              class="nav-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"
              />
              <polyline points="22,6 12,13 2,6" />
            </svg>
            <span class="nav-text">邮箱绑定</span>
          </router-link>

          <router-link
            to="/console/email-view"
            class="nav-item"
            :class="{ active: $route.path.includes('email-view') }"
          >
            <svg
              class="nav-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
              <circle cx="12" cy="12" r="3" />
            </svg>
            <span class="nav-text">邮件查看</span>
          </router-link>

          <router-link
            to="/console/email-assistant"
            class="nav-item"
            :class="{ active: $route.path.includes('email-assistant') }"
          >
            <svg
              class="nav-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
              <circle cx="9" cy="10" r="1" />
              <circle cx="15" cy="10" r="1" />
              <path d="M9.5 13a3.5 3.5 0 0 0 5 0" />
            </svg>
            <span class="nav-text">邮件助手</span>
          </router-link>

          <router-link
            to="/console/email-detection"
            class="nav-item"
            :class="{ active: $route.path.includes('email-detection') }"
          >
            <svg
              class="nav-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M12 2L2 7l10 5 10-5-10-5z" />
              <path d="M2 17l10 5 10-5" />
              <path d="M2 12l10 5 10-5" />
            </svg>
            <span class="nav-text">邮件检测</span>
          </router-link>
        </nav>
      </aside>

      <!-- 右侧主内容区 -->
      <main class="console-main">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineOptions({
  name: 'ConsolePage',
})

const isSidebarCollapsed = ref(false)

function toggleSidebar() {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}
</script>

<style scoped>
/* 控制台页面整体布局 */
.console-page {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: #ffffff;
  font-family:
    -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  padding-top: 64px;
  overflow: hidden;
}

/* 控制台主容器 */
.console-container {
  display: flex;
  width: 100%;
  height: calc(100vh - 64px);
  overflow: hidden;
}

/* 左侧导航栏 */
.console-sidebar {
  width: 220px;
  min-width: 220px;
  background: white;
  display: flex;
  flex-direction: column;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.05);
  position: relative;
  z-index: 10;
  overflow: hidden;
  transition: all 0.3s ease;
}

/* 收起的侧边栏 */
.sidebar-collapsed {
  width: 60px;
  min-width: 60px;
}

/* 切换按钮 */
.toggle-sidebar {
  position: absolute;
  top: 24px;
  right: 12px;
  width: 24px;
  height: 24px;
  border: none;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  border-radius: 4px;
  padding: 0;
}

.toggle-sidebar:hover {
  background: #f3f4f6;
  color: #374151;
}

.toggle-icon {
  width: 16px;
  height: 16px;
}

/* 侧边栏标题 */
.sidebar-header {
  padding: 24px 20px 20px 20px;
  position: relative;
  display: flex;
  align-items: center;
}

.sidebar-title {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
  margin: 0;
  letter-spacing: -0.025em;
  transition: opacity 0.3s ease;
}

.sidebar-collapsed .sidebar-title {
  opacity: 0;
  width: 0;
  overflow: hidden;
}

/* 侧边栏导航 */
.sidebar-nav {
  flex: 1;
  padding: 8px 12px 20px 12px;
  overflow: hidden;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  color: #6b7280;
  text-decoration: none;
  border-radius: 8px;
  margin-bottom: 2px;
  transition: all 0.15s ease;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
}

.sidebar-collapsed .nav-item {
  justify-content: center;
  padding: 10px 0;
}

.sidebar-collapsed .nav-text {
  display: none;
}

.nav-item:hover {
  background: #f3f4f6;
  color: #374151;
}

.nav-item.active {
  background: #eaf5ff;
  font-weight: 600;
}

/* 每个导航项的不同颜色 */
.nav-item.active[href*='dashboard'] {
  color: #f59e0b;
}

.nav-item.active[href*='email-bind'] {
  color: #ec4899;
}

.nav-item.active[href*='email-view'] {
  color: #3b82f6;
}

.nav-item.active[href*='email-assistant'] {
  color: #d12323;
}

.nav-icon {
  width: 18px;
  height: 18px;
  margin-right: 12px;
  flex-shrink: 0;
}

.nav-text {
  font-size: 14px;
  line-height: 1.25;
}

/* 右侧主内容区 */
.console-main {
  flex: 1;
  background: #ffffff;
  overflow-y: auto;
  overflow-x: hidden;
  height: 100%;
  min-width: 0;
}

/* 隐藏滚动条但保持滚动功能 */
.console-sidebar::-webkit-scrollbar {
  display: none;
}

.console-main::-webkit-scrollbar {
  display: none;
}

.console-sidebar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.console-main {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
/* 响应式设计 */
@media (max-width: 768px) {
  .console-sidebar {
    width: 180px;
    min-width: 180px;
  }

  .sidebar-collapsed {
    width: 50px;
    min-width: 50px;
  }

  .sidebar-header {
    padding: 20px 12px 16px 12px;
  }

  .sidebar-title {
    font-size: 15px;
  }

  .sidebar-nav {
    padding: 8px 8px 16px 8px;
  }

  .nav-item {
    padding: 8px 8px;
    margin-bottom: 1px;
  }

  .nav-text {
    font-size: 13px;
  }

  .nav-icon {
    width: 16px;
    height: 16px;
    margin-right: 8px;
  }
}

@media (max-width: 480px) {
  .console-sidebar {
    width: 160px;
    min-width: 160px;
  }

  .sidebar-collapsed {
    width: 45px;
    min-width: 45px;
  }

  .sidebar-header {
    padding: 16px 8px 12px 8px;
  }

  .sidebar-title {
    font-size: 14px;
  }

  .sidebar-nav {
    padding: 6px 6px 12px 6px;
  }

  .nav-item {
    padding: 6px 6px;
    margin-bottom: 1px;
  }

  .nav-text {
    font-size: 12px;
  }

  .nav-icon {
    width: 14px;
    height: 14px;
    margin-right: 6px;
  }
}
</style>
