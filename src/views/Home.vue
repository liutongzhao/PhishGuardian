<template>
  <div class="home">
    <!-- 英雄区域 -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="title-highlight">云雾 API</span>
        </h1>
        <h2 class="hero-subtitle">统一的大模型接口网关</h2>
        <p class="hero-description">
          提供稳定可靠的API中转服务，支持ChatGPT、Claude等多种AI模型，国内直连无需<br />
          代理，低延迟高并发，按量计费更经济。
        </p>

        <div class="hero-divider">
          <span class="divider-text">向世界揭牌更强大、更具影响力的人工智能</span>
        </div>

        <div class="action-buttons">
          <button class="primary-btn">▶ 前往控制台</button>
          <button class="secondary-btn">📄 文档</button>
        </div>
      </div>
    </section>

    <!-- 合作伙伴区域 -->
    <section class="partners-section">
      <h3 class="partners-title">支持众多的大模型供应商</h3>
      <div class="partners-grid">
        <!-- 第一行 -->
        <div class="partner-row">
          <div class="partner-logo">🟫</div>
          <div class="partner-logo">🌀</div>
          <div class="partner-logo">🔷</div>
          <div class="partner-logo">❄️</div>
          <div class="partner-logo">🔺</div>
          <div class="partner-logo">💬</div>
          <div class="partner-logo">✦</div>
          <div class="partner-logo">🔷</div>
          <div class="partner-logo">🎵</div>
          <div class="partner-logo">🔷</div>
          <div class="partner-logo">🔷</div>
        </div>
        <!-- 第二行 -->
        <div class="partner-row">
          <div class="partner-logo">🔵</div>
          <div class="partner-logo">⭕</div>
          <div class="partner-logo">🔄</div>
          <div class="partner-logo">⚡</div>
          <div class="partner-logo">⛵</div>
          <div class="partner-logo">🟢</div>
          <div class="partner-logo">🔷</div>
          <div class="partner-logo">🌐</div>
          <div class="partner-logo">🔷</div>
          <div class="partner-more">30+</div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
// 首页逻辑
</script>

<style scoped>
/* 英雄区域 */
.hero-section {
  text-align: center;
  padding: 80px 20px 60px;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 64px;
  font-weight: 700;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #1890ff, #40a9ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 36px;
  font-weight: 600;
  color: #333;
  margin-bottom: 30px;
}

.hero-description {
  font-size: 16px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 40px;
}

.hero-divider {
  margin: 50px 0;
  position: relative;
}

.hero-divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, #ddd, transparent);
}

.divider-text {
  display: inline-block;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 0 20px;
  color: #666;
  font-size: 14px;
}

.action-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-bottom: 80px;
}

.primary-btn,
.secondary-btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.primary-btn {
  background: #1890ff;
  color: white;
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.3);
}

.primary-btn:hover {
  background: #40a9ff;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(24, 144, 255, 0.4);
}

.secondary-btn {
  background: white;
  color: #1890ff;
  border: 1px solid #1890ff;
}

.secondary-btn:hover {
  background: #1890ff;
  color: white;
  transform: translateY(-2px);
}

/* 合作伙伴区域 */
.partners-section {
  text-align: center;
  padding: 60px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.partners-title {
  font-size: 24px;
  font-weight: 500;
  color: #666;
  margin-bottom: 40px;
}

.partners-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.partner-row {
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
}

.partner-logo {
  width: 50px;
  height: 50px;
  background: white;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.partner-logo:hover {
  transform: translateY(-2px);
}

.partner-more {
  width: 50px;
  height: 50px;
  background: #f0f0f0;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  color: #666;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-title {
    font-size: 40px;
  }

  .hero-subtitle {
    font-size: 24px;
  }

  .action-buttons {
    flex-direction: column;
    align-items: center;
  }

  .partner-row {
    gap: 15px;
  }

  .partner-logo {
    width: 40px;
    height: 40px;
    font-size: 16px;
  }
}
</style>
