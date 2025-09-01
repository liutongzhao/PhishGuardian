<template>
  <div class="home">
    <!-- 英雄区域 -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="shine-text-blue">PhishGuard</span>
        </h1>
        <h2 class="hero-subtitle">统一的邮件安全网关助手</h2>
        <p class="hero-description">
          提供稳定可靠的邮件安全服务，自动识别钓鱼邮件，总结邮件内容、生成邮件摘要、判断邮件紧急及重要程度，实时向用户推送相关信息。
        </p>

        <div class="hero-divider">
          <div
            class="relative w-full max-w-[700px] min-h-[60px] flex items-center justify-center mx-auto"
          >
            <div class="flex items-center whitespace-nowrap">
              <span class="font-mono font-black text-sm md:text-base tracking-normal text-gray-400"
                >——————</span
              >
              <span
                class="divider-text typewriter-text font-mono font-black text-sm md:text-base tracking-wider leading-relaxed text-left whitespace-nowrap ml-2"
                ref="typewriterElement"
                >{{ displayedText }}</span
              >
            </div>
          </div>
        </div>

        <div class="action-buttons">
          <button class="primary-btn">▶ 前往控制台</button>
          <button class="secondary-btn">📄 文档</button>
        </div>
      </div>
    </section>

    <!-- 合作伙伴区域 -->
    <section class="partners-section">
      <h3 class="partners-title">支持众多的邮件供应商</h3>
      <div class="partners-grid">
        <div class="partner-logo">
          <svg class="partner-icon" fill="currentColor" viewBox="0 0 24 24" width="24" height="24">
            <title>Gmail</title>
            <path
              d="M592.299 661.76c60.458-47.573 67.072-49.92 84.992-27.392 15.573 19.243 12.245 22.741-91.734 113.365-34.688 30.592-63.744 62.294-63.744 71.382 0 7.936-8.96 14.762-19.029 14.762-10.027 0-46.933 19.286-81.493 44.288-68.267 48.726-193.451 103.168-237.099 103.168-71.467 0-67.072-71.381 5.632-91.733 124.117-34.09 251.605-106.581 402.432-227.84zM545.45 461.141c14.506-5.717 39.125-7.978 54.826-5.589 15.574 1.11 51.371 5.675 80.427 9.045 128.512 14.806 224.64 132.694 214.613 259.627-5.546 70.23-24.576 106.539-81.578 158.635-89.515 81.536-214.699 121.216-257.11 82.688-27.989-26.112-50.304-81.707-41.344-103.211 5.547-15.915 10.07-15.915 41.344 1.152 70.4 36.267 171.008-2.261 229.12-87.296 58.155-86.187 33.494-180.267-46.933-180.267-29.056 0-40.235-6.741-51.37-31.701-21.334-44.16-63.745-46.379-111.83-4.48-223.53 196.053-431.488 302.592-478.421 245.93-30.166-36.223-6.742-54.357 117.333-90.666 42.539-12.544 112.939-49.835 191.147-103.168 111.786-74.752 124.074-86.059 119.68-112.17-4.523-21.505 0-30.593 20.096-38.529zM354.304 50.86c60.33-12.459 257.024-10.24 307.37 3.328 95.062 25.002 110.635 41.941 138.667 160 16.726 70.272 15.616 101.973-4.522 150.698-22.315 55.595-64.854 69.12-201.216 68.011-109.611-1.11-111.787 0-130.816 29.44-23.51 38.443-118.571 114.432-160.982 130.347C174.293 639.06 102.7 643.627 91.52 607.36c-11.136-35.2 13.397-56.704 66.005-56.704 65.835 0 174.336-44.245 205.611-82.773 12.245-13.568 4.437-17.067-48.085-21.547-70.4-5.59-95.019-28.33-108.374-99.712-12.373-61.184-10.069-168.832 2.219-193.835 13.483-23.722 50.347-29.44 62.635-9.045 4.522 7.936 7.85 49.835 8.96 95.232 2.218 124.672 8.96 130.39 172.16 124.672 72.704-2.347 152.021-4.565 178.858-5.717 71.51 0 96.128-30.592 87.211-109.91-7.85-71.338-23.552-100.821-62.677-115.626-34.56-14.763-231.382-19.243-309.59-6.827-58.112 7.979-59.221 7.979-59.221-20.395 0-33.92 12.245-43.008 67.072-54.314z m-2.347 167.68c7.851-9.046 50.39-13.526 133.035-12.502 158.72 1.195 150.827-1.152 146.432 35.158l-3.328 30.592-139.776 1.109c-125.184 0-139.776-2.219-143.104-20.395-2.176-11.306 1.11-25.984 6.741-33.92z"
            />
          </svg>
        </div>
        <div class="partner-logo">
          <svg class="partner-icon" fill="currentColor" viewBox="0 0 24 24" width="24" height="24">
            <title>Outlook</title>
            <path
              d="M7.88 12.04q0 .45-.11.87-.1.41-.33.74-.22.33-.58.52-.35.2-.87.2t-.87-.2q-.35-.19-.58-.52-.22-.33-.33-.74-.1-.42-.1-.87 0-.44.1-.86.11-.41.33-.74.23-.33.58-.52.35-.2.87-.2t.87.2q.35.19.58.52.22.33.33.74.11.42.11.86zM12 0C5.383 0 0 5.383 0 12s5.383 12 12 12 12-5.383 12-12S18.617 0 12 0z"
            />
          </svg>
        </div>
        <div class="partner-logo">
          <svg class="partner-icon" fill="currentColor" viewBox="0 0 24 24" width="24" height="24">
            <title>Yahoo Mail</title>
            <path
              d="M12 0C5.372 0 0 5.372 0 12s5.372 12 12 12 12-5.372 12-12S18.628 0 12 0zm5.568 7.568l-4.139 6.925v3.33h-2.858v-3.33L6.432 7.568V6.107h3.568l2.285 4.04 2.286-4.04h3.568v1.461z"
            />
          </svg>
        </div>
        <div class="partner-logo">
          <svg class="partner-icon" fill="currentColor" viewBox="0 0 24 24" width="24" height="24">
            <title>Protonmail</title>
            <path
              d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm7.5 9.75v7.5c0 .414-.336.75-.75.75h-2.25v-6h-9v6H4.25c-.414 0-.75-.336-.75-.75v-7.5c0-2.07 1.68-3.75 3.75-3.75h9c2.07 0 3.75 1.68 3.75 3.75z"
            />
          </svg>
        </div>
        <div class="partner-logo">
          <svg class="partner-icon" fill="currentColor" viewBox="0 0 24 24" width="24" height="24">
            <title>Apple Mail</title>
            <path
              d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 6.62 5.367 11.987 11.988 11.987s11.987-5.367 11.987-11.987C24.004 5.367 18.637.001 12.017.001zM8.818 8.05c0-.414.336-.75.75-.75h4.864c.414 0 .75.336.75.75s-.336.75-.75.75H9.568c-.414 0-.75-.336-.75-.75zm0 3c0-.414.336-.75.75-.75h4.864c.414 0 .75.336.75.75s-.336.75-.75.75H9.568c-.414 0-.75-.336-.75-.75zm0 3c0-.414.336-.75.75-.75h2.432c.414 0 .75.336.75.75s-.336.75-.75.75H9.568c-.414 0-.75-.336-.75-.75z"
            />
          </svg>
        </div>
        <div class="partner-logo">
          <svg class="partner-icon" fill="currentColor" viewBox="0 0 24 24" width="24" height="24">
            <title>Thunderbird</title>
            <path
              d="M23.98 12.01c0 6.627-5.373 12-12 12s-12-5.373-12-12 5.373-12 12-12 12 5.373 12 12zm-12-8c-4.418 0-8 3.582-8 8s3.582 8 8 8 8-3.582 8-8-3.582-8-8-8zm0 2c3.314 0 6 2.686 6 6s-2.686 6-6 6-6-2.686-6-6 2.686-6 6-6z"
            />
          </svg>
        </div>
        <div class="partner-logo">
          <svg class="partner-icon" fill="currentColor" viewBox="0 0 24 24" width="24" height="24">
            <title>Others</title>
            <path
              d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"
            />
            <text x="12" y="16" text-anchor="middle" font-size="8" fill="currentColor">+</text>
          </svg>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// HomePage 组件逻辑
defineOptions({
  name: 'HomePage',
})

// 打字机效果
const fullText = '向世界展示更强大、更具影响力的邮件安全助手！'
const displayedText = ref('')
const typewriterElement = ref(null)

// 打字机动画函数
const typeWriter = () => {
  displayedText.value = ''
  let i = 0

  const typing = () => {
    if (i < fullText.length) {
      displayedText.value += fullText.charAt(i)
      i++
      setTimeout(typing, 80) // 每个字符间隔80ms
    } else {
      // 动画完成后等待2秒，然后重新开始
      setTimeout(() => {
        typeWriter()
      }, 2000)
    }
  }

  typing()
}

onMounted(() => {
  // 页面加载后延迟1秒开始打字机效果
  setTimeout(() => {
    typeWriter()
  }, 1000)
})
</script>

<style scoped>
/* 隐藏滚动条但保持滚动功能 */
:global(html) {
  overflow: -moz-scrollbars-none; /* Firefox */
  -ms-overflow-style: none; /* IE 10+ */
  scrollbar-width: none; /* Firefox */
}

:global(html::-webkit-scrollbar) {
  display: none; /* Chrome, Safari, Opera */
}

:global(body) {
  overflow: -moz-scrollbars-none; /* Firefox */
  -ms-overflow-style: none; /* IE 10+ */
  scrollbar-width: none; /* Firefox */
}

:global(body::-webkit-scrollbar) {
  display: none; /* Chrome, Safari, Opera */
}

/* 英雄区域 */
.hero-section {
  text-align: center;
  padding: 100px 20px 60px; /* 增加顶部padding为导航栏留出空间 */
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 10;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
  position: relative;
}

/* 在英雄区域添加不规则渐变背景 */
.hero-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 150%;
  height: 100%;
  background: radial-gradient(
    ellipse 60% 70% at 30% 40%,
    rgba(234, 245, 255, 0.4) 0%,
    rgba(233, 247, 253, 0.3) 35%,
    rgba(248, 250, 252, 0.2) 60%,
    transparent 80%
  );
  z-index: -1;
  border-radius: 60% 40% 50% 70% / 70% 50% 60% 40%;
  filter: blur(1px);
}

.hero-content::after {
  content: '';
  position: absolute;
  top: 20%;
  right: 10%;
  width: 80%;
  height: 60%;
  background: radial-gradient(
    ellipse 70% 60% at 60% 50%,
    rgba(239, 246, 255, 0.3) 0%,
    rgba(245, 250, 255, 0.2) 40%,
    transparent 70%
  );
  z-index: -1;
  border-radius: 70% 30% 40% 60% / 50% 70% 30% 50%;
  filter: blur(0.5px);
}

.hero-title {
  font-size: 84px; /* 增大字体 */
  font-weight: 700;
  margin-bottom: 0;
  margin-top: 0; /* 确保没有顶部边距 */
  color: #1c1f23;
  line-height: 0.9; /* 减少行高让文字更紧凑 */
  height: auto; /* 改为自适应高度 */
  font-family: Lato, 'Helvetica Neue', Arial, Helvetica, sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 发光文字动画样式 */
.shine-text-blue {
  -webkit-text-fill-color: transparent;
  font-weight: 700;
  background: linear-gradient(
      90deg,
      rgb(30, 64, 175),
      rgb(59, 130, 246),
      rgb(96, 165, 250) 40%,
      rgba(255, 255, 255, 0.95),
      rgb(96, 165, 250) 60%,
      rgb(59, 130, 246),
      rgb(30, 64, 175)
    )
    0% 0% / 200% 100% text;
  animation: 4s linear 0s infinite normal none running sweep-shine;
  display: inline-block;
}

/* 动画关键帧 */
@keyframes sweep-shine {
  0% {
    background-position: 200% 0;
  }
  50% {
    background-position: -50% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.hero-subtitle {
  font-size: 52px; /* 增大字体 */
  font-weight: 800; /* 增加字体粗细 */
  color: #1c1f23;
  margin-top: 32px; /* 进一步增加与主标题的间距 */
  margin-bottom: 0;
  line-height: 1;
  opacity: 0.8;
  font-family: Lato, 'Helvetica Neue', Arial, Helvetica, sans-serif;
}

.hero-tagline {
  display: block;
  font-size: 0.6em;
  opacity: 0.8;
  color: #666;
  font-weight: 400;
  margin-bottom: 25px;
  letter-spacing: 0.5px;
  position: relative;
  top: -8px;
}

.hero-description {
  font-size: 18px;
  color: rgba(var(--semi-grey-9), 0.8);
  line-height: 1.75;
  margin-top: 16px;
  margin-bottom: 40px;
  font-family:
    Inter,
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    'PingFang SC',
    'Hiragino Sans GB',
    'Microsoft YaHei',
    'Helvetica Neue',
    Helvetica,
    Arial,
    sans-serif;
}

/* 响应式设计 */
@media (min-width: 768px) {
  .hero-description {
    font-size: 20px;
    margin-top: 24px;
  }
}

@media (min-width: 1024px) {
  .hero-description {
    font-size: 24px;
    line-height: 2;
  }
}

.hero-divider {
  margin: 50px 0;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 分隔线文字样式 */
.divider-text {
  display: inline-block;
  background: #ffffff;
  padding: 0 20px;
  color: #666;
  font-size: 14px;
}

/* 打字机效果样式 */
.typewriter-text {
  position: relative;
  min-height: 1.25rem; /* 防止高度变化 */
  color: #666;
  /* 确保使用与参考样式相同的字体 */
  font-family:
    ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New',
    monospace !important;
  font-weight: 900 !important;
  letter-spacing: 0.05em !important;
  line-height: 1.625 !important;
  white-space: nowrap !important; /* 强制单行显示 */
  overflow: visible !important;
}

/* 响应式字体大小匹配参考样式 */
@media (max-width: 767px) {
  .typewriter-text {
    font-size: 0.875rem !important; /* 14px */
    line-height: 1.25rem !important;
  }
}

@media (min-width: 768px) {
  .typewriter-text {
    font-size: 1rem !important; /* 16px */
    line-height: 1.5rem !important;
  }
}

/* 光标效果 */
.typewriter-text::after {
  content: '|';
  animation: blink 1s infinite;
  color: #666;
  margin-left: 2px;
}

/* 光标闪烁动画 */
@keyframes blink {
  0%,
  50% {
    opacity: 1;
  }
  51%,
  100% {
    opacity: 0;
  }
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
  padding: 20px 20px;
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
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 12px;
  max-width: 80rem;
  margin: 0 auto;
  padding: 0 16px;
}

/* 响应式间距 */
@media (min-width: 640px) {
  .partners-grid {
    gap: 16px;
  }
}

@media (min-width: 768px) {
  .partners-grid {
    gap: 24px;
  }
}

@media (min-width: 1024px) {
  .partners-grid {
    gap: 32px;
  }
}

.partner-row {
  display: contents;
}

.partner-logo {
  width: 32px;
  height: 32px;
  background: white;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  color: #666;
}

/* 响应式图标尺寸 */
@media (min-width: 640px) {
  .partner-logo {
    width: 40px;
    height: 40px;
  }
}

@media (min-width: 768px) {
  .partner-logo {
    width: 48px;
    height: 48px;
  }
}

.partner-logo:hover {
  transform: translateY(-2px);
}

.partner-icon {
  width: 20px;
  height: 20px;
}

@media (min-width: 640px) {
  .partner-icon {
    width: 24px;
    height: 24px;
  }
}

@media (min-width: 768px) {
  .partner-icon {
    width: 28px;
    height: 28px;
  }
}

/* 响应式设计 - 增强自适应功能 */
@media (max-width: 480px) {
  .hero-section {
    padding: 80px 15px 40px; /* 小屏幕也要为导航栏留出空间 */
  }

  .hero-title {
    font-size: 38px; /* 增大小屏幕字体 */
    line-height: 0.8;
  }

  .hero-subtitle {
    font-size: 22px; /* 增大小屏幕副标题字体 */
    font-weight: 800; /* 增加字体粗细 */
    margin-top: 18px; /* 小屏幕进一步增加间距 */
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

@media (min-width: 481px) and (max-width: 768px) {
  .hero-section {
    padding: 90px 20px 50px; /* 中小屏幕为导航栏留出空间 */
  }

  .hero-title {
    font-size: 56px; /* 增大中小屏幕字体 */
    line-height: 0.85;
  }

  .hero-subtitle {
    font-size: 28px; /* 增大中小屏幕副标题字体 */
    font-weight: 800; /* 增加字体粗细 */
    margin-top: 22px; /* 中小屏幕进一步增加间距 */
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

@media (min-width: 769px) and (max-width: 1024px) {
  .hero-section {
    padding: 95px 20px 55px; /* 中等屏幕为导航栏留出空间 */
  }

  .hero-title {
    font-size: 70px; /* 增大中等屏幕字体 */
    line-height: 0.9;
  }

  .hero-subtitle {
    font-size: 44px; /* 增大中等屏幕副标题字体 */
    font-weight: 800; /* 增加字体粗细 */
    margin-top: 28px; /* 中等屏幕进一步增加间距 */
  }
}

@media (min-width: 1025px) {
  .hero-section {
    padding: 100px 20px 60px; /* 大屏幕为导航栏留出空间 */
  }

  .hero-title {
    font-size: 84px; /* 增大大屏幕字体 */
    line-height: 0.9;
  }

  .hero-subtitle {
    font-size: 52px; /* 增大大屏幕副标题字体 */
    font-weight: 800; /* 增加字体粗细 */
    margin-top: 32px; /* 大屏幕进一步增加间距 */
  }
}
</style>
