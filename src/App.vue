<script setup></script>

<template>
  <div class="app">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="nav-container">
        <div class="nav-left">
          <div class="logo">
            <span class="logo-icon">☁️</span>
            <span class="logo-text">云雾 API</span>
          </div>
          <nav class="nav-menu">
            <router-link to="/" class="nav-item">首页</router-link>
            <a href="#" class="nav-item">控制台</a>
            <a href="#" class="nav-item">定价</a>
            <a href="#" class="nav-item">使用指南</a>
            <a href="#" class="nav-item">联系我们</a>
            <a href="#" class="nav-item">文档</a>
          </nav>
        </div>
        <div class="nav-right">
          <button class="icon-btn">🔔</button>
          <button class="icon-btn">🌙</button>
          <button class="icon-btn">🌐</button>
          <span class="user-info">登录</span>
          <button class="register-btn">注册</button>
        </div>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <!-- 背景装饰 -->
      <div class="background-decoration">
        <div class="decoration-circle decoration-1"></div>
        <div class="decoration-circle decoration-2"></div>
        <div class="decoration-circle decoration-3"></div>
      </div>

      <!-- 路由内容 -->
      <router-view />
    </main>
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
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  font-family:
    -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

/* 顶部导航栏 */
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 40px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.logo-icon {
  font-size: 24px;
}

.nav-menu {
  display: flex;
  gap: 24px;
}

.nav-item {
  color: #666;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s ease;
}

.nav-item:hover {
  color: #1890ff;
}

.nav-item.router-link-active {
  color: #1890ff;
  font-weight: 600;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.icon-btn {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  padding: 8px;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.icon-btn:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.user-info {
  color: #666;
  font-size: 14px;
}

.register-btn {
  background: #1890ff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.register-btn:hover {
  background: #40a9ff;
}

/* 主要内容区域 */
.main-content {
  position: relative;
  padding-top: 80px;
  min-height: 100vh;
  overflow: hidden;
}

/* 背景装饰 */
.background-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.decoration-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
}

.decoration-1 {
  width: 200px;
  height: 200px;
  top: 100px;
  left: -50px;
  background: rgba(24, 144, 255, 0.1);
}

.decoration-2 {
  width: 150px;
  height: 150px;
  top: 200px;
  right: -30px;
  background: rgba(255, 255, 255, 0.2);
}

.decoration-3 {
  width: 300px;
  height: 300px;
  bottom: 100px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(24, 144, 255, 0.05);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .nav-container {
    padding: 0 16px;
  }

  .nav-menu {
    display: none;
  }
}
</style>
