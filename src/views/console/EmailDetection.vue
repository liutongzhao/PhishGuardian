<template>
  <div class="email-detection">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">邮件检测</h1>
      <p class="page-subtitle">实时监控邮件安全检测流程</p>
    </div>

    <!-- 3D检测流程容器 -->
    <div class="detection-container">
      <!-- 第一阶段：开始检测 -->
      <div
        class="stage stage-start"
        :class="{ active: detectingDetail && detectingDetail.detection_stage === 1 }"
      >
        <div class="stage-header">
          <div class="stage-number">01</div>
          <h3 class="stage-title">开始检测</h3>
        </div>

        <div class="stage-content">
          <!-- 正在检测的邮件 -->
          <div v-if="detectingEmail" class="current-email">
            <div class="email-info">
              <div class="email-from">
                <span class="label">发件人:</span>
                <span class="value">{{ detectingEmail.sender }}</span>
              </div>
              <div class="email-subject">
                <span class="label">主题:</span>
                <span class="value">{{ detectingEmail.subject }}</span>
              </div>
            </div>
            <div class="email-status">
              <div class="status-indicator processing"></div>
              <span>正在检测中...</span>
            </div>
          </div>

          <!-- 无邮件状态 -->
          <div v-if="!detectingEmail && pendingEmails.length === 0" class="no-email-state">
            <div class="no-email-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path
                  d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"
                />
                <polyline points="22,6 12,13 2,6" />
              </svg>
            </div>
            <p>暂无待检测邮件</p>
            <p class="sub-text">系统将自动检测新收到的邮件</p>
          </div>

          <!-- 待检测队列 -->
          <div v-if="pendingEmails.length > 0" class="pending-queue">
            <h4 class="queue-title">待检测队列 ({{ pendingEmails.length }})</h4>
            <div class="queue-list">
              <div v-for="email in pendingEmails.slice(0, 3)" :key="email.id" class="queue-item">
                <div class="queue-dot"></div>
                <span class="queue-subject">{{ email.subject }}</span>
              </div>
              <div v-if="pendingEmails.length > 3" class="queue-more">
                还有 {{ pendingEmails.length - 3 }} 封邮件等待检测
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 连接线 -->
      <div class="connection-hub">
        <div class="line line-1"></div>
        <div class="line line-2"></div>
        <div class="line line-3"></div>
      </div>

      <!-- 第二阶段：并行检测 -->
      <div
        class="stage stage-parallel"
        :class="{ active: detectingDetail && detectingDetail.detection_stage === 2 }"
      >
        <div class="stage-header">
          <div class="stage-number">02</div>
          <h3 class="stage-title">并行检测</h3>
        </div>

        <div class="stage-content">
          <div class="parallel-detections">
            <!-- 邮件正文检测 -->
            <div class="detection-circle" :class="getModuleStatusClass('content')">
              <div class="circle-container">
                <div class="circle-progress" :style="getCircleProgressStyle('content')">
                  <div class="circle-inner">
                    <div class="module-icon">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                        <polyline points="14,2 14,8 20,8" />
                        <line x1="16" y1="13" x2="8" y2="13" />
                        <line x1="16" y1="17" x2="8" y2="17" />
                        <polyline points="10,9 9,9 8,9" />
                      </svg>
                    </div>
                    <div class="module-info">
                      <h4 class="module-title">正文检测</h4>
                      <div class="module-details">
                        <div v-if="getModuleWeight('content')" class="weight-info">
                          权重: {{ getModuleWeight('content') }}%
                        </div>
                        <div v-if="getModuleProbability('content')" class="probability-info">
                          概率: {{ getModuleProbability('content') }}%
                        </div>
                        <div v-if="getModuleReason('content')" class="reason-info">
                          {{ getModuleReason('content') }}
                        </div>
                      </div>
                      <p class="module-status">{{ getModuleStatusText('content') }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- URL检测 -->
            <div class="detection-circle" :class="getModuleStatusClass('url')">
              <div class="circle-container">
                <div class="circle-progress" :style="getCircleProgressStyle('url')">
                  <div class="circle-inner">
                    <div class="module-icon">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
                        <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
                      </svg>
                    </div>
                    <div class="module-info">
                      <h4 class="module-title">URL检测</h4>
                      <div class="module-details">
                        <div v-if="getModuleWeight('url')" class="weight-info">
                          权重: {{ getModuleWeight('url') }}%
                        </div>
                        <div v-if="getModuleProbability('url')" class="probability-info">
                          概率: {{ getModuleProbability('url') }}%
                        </div>
                        <div v-if="getModuleReason('url')" class="reason-info">
                          {{ getModuleReason('url') }}
                        </div>
                      </div>
                      <p class="module-status">{{ getModuleStatusText('url') }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 元数据检测 -->
            <div class="detection-circle" :class="getModuleStatusClass('metadata')">
              <div class="circle-container">
                <div class="circle-progress" :style="getCircleProgressStyle('metadata')">
                  <div class="circle-inner">
                    <div class="module-icon">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
                      </svg>
                    </div>
                    <div class="module-info">
                      <h4 class="module-title">元数据检测</h4>
                      <div class="module-details">
                        <div v-if="getModuleWeight('metadata')" class="weight-info">
                          权重: {{ getModuleWeight('metadata') }}%
                        </div>
                        <div v-if="getModuleProbability('metadata')" class="probability-info">
                          概率: {{ getModuleProbability('metadata') }}%
                        </div>
                        <div v-if="getModuleReason('metadata')" class="reason-info">
                          {{ getModuleReason('metadata') }}
                        </div>
                      </div>
                      <p class="module-status">{{ getModuleStatusText('metadata') }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 汇聚线 -->
      <div class="convergence-hub">
        <div class="conv-line conv-line-1"></div>
        <div class="conv-line conv-line-2"></div>
        <div class="conv-line conv-line-3"></div>
      </div>

      <!-- 第三阶段：AI判断 -->
      <div
        class="stage stage-ai"
        :class="{ active: detectingDetail && detectingDetail.detection_stage === 3 }"
      >
        <div class="stage-header">
          <div class="stage-number">03</div>
          <h3 class="stage-title">AI综合判断</h3>
        </div>

        <div class="stage-content">
          <div class="ai-analysis">
            <div class="ai-brain">
              <div class="brain-core">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path
                    d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"
                  />
                  <path
                    d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"
                  />
                </svg>
              </div>
            </div>
            <div class="analysis-result">
              <p class="waiting-text">等待检测完成后进行AI分析</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 最终连接线 -->
      <div class="final-line"></div>

      <!-- 第四阶段：信息提取 -->
      <div
        class="stage stage-extract"
        :class="{ active: detectingDetail && detectingDetail.detection_stage === 4 }"
      >
        <div class="stage-header">
          <div class="stage-number">04</div>
          <h3 class="stage-title">信息提取</h3>
        </div>

        <div class="stage-content">
          <div class="extraction-process">
            <div class="extract-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <polyline points="14,2 14,8 20,8" />
                <line x1="16" y1="13" x2="8" y2="13" />
                <line x1="16" y1="17" x2="8" y2="17" />
              </svg>
            </div>
            <div class="extract-status">
              <p class="extract-text">等待开始</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { getDetectionOverview, startEmailDetection } from '@/api/email'
import wsManager from '@/utils/websocket'

// 响应式变量
const detectingEmail = ref(null)
const detectingDetail = ref(null)
const pendingEmails = ref([])
const loading = ref(false)

// 获取检测概览数据
const loadDetectionOverview = async () => {
  try {
    loading.value = true
    const response = await getDetectionOverview()

    if (response.success) {
      detectingEmail.value = response.data.detecting_email
      detectingDetail.value = response.data.detecting_detail
      pendingEmails.value = response.data.pending_emails
    } else {
      console.error('获取检测概览失败:', response.message)
      // 出错时重置状态
      detectingEmail.value = null
      detectingDetail.value = null
      pendingEmails.value = []
    }
  } catch (error) {
    console.error('请求检测概览接口出错:', error)
    // 出错时重置状态
    detectingEmail.value = null
    detectingDetail.value = null
    pendingEmails.value = []
  } finally {
    loading.value = false
  }
}

// 开始检测邮件的函数
const startDetection = async (emailId) => {
  try {
    const response = await startEmailDetection(emailId)
    console.log('开始检测API返回数据:', response)
  } catch (error) {
    console.error('调用开始检测API出错:', error)
  }
}

// 自动检测逻辑（封装的通用方法）
const autoDetectionLogic = async () => {
  console.log('🔍 [DEBUG] autoDetectionLogic 开始执行')
  // 显示加载状态
  loading.value = true

  try {
    // 1. 先调用loadDetectionOverview加载数据
    console.log('🔍 [DEBUG] autoDetectionLogic 调用 loadDetectionOverview')
    await loadDetectionOverview()

    // 2. 判断是否有正在检测的邮件
    console.log(
      '🔍 [DEBUG] autoDetectionLogic 检查状态 - detectingEmail:',
      !!detectingEmail.value,
      'pendingEmails.length:',
      pendingEmails.value.length,
    )
    if (!detectingEmail.value && pendingEmails.value.length > 0) {
      // 没有正在检测的邮件，选择第一封待检测邮件
      const firstPendingEmail = pendingEmails.value[0]
      console.log(
        '🔍 [DEBUG] autoDetectionLogic 自动开始检测第一封待检测邮件:',
        firstPendingEmail.id,
      )

      // 3. 调用startDetection函数去检测
      await startDetection(firstPendingEmail.id)

      // 4. 等到返回结果时再次调用loadDetectionOverview函数渲染页面
      await loadDetectionOverview()
    } else {
      console.log('🔍 [DEBUG] autoDetectionLogic 无需自动检测 - 已有检测中邮件或无待检测邮件')
    }
  } catch (error) {
    console.error('自动检测逻辑执行出错:', error)
  } finally {
    loading.value = false
    console.log('🔍 [DEBUG] autoDetectionLogic 执行完成')
  }
}

// 处理新邮件推送
const handleNewEmails = async (data) => {
  const timestamp = new Date().toLocaleTimeString()
  console.log(`[${timestamp}] 🔍 [DEBUG] 收到新邮件推送，触发 autoDetectionLogic:`, data)
  console.log(`[${timestamp}] 🔍 [DEBUG] WebSocket连接状态:`, wsManager.isConnected)
  console.log(
    `[${timestamp}] 🔍 [DEBUG] 当前注册的事件处理器数量:`,
    wsManager.eventHandlers['new_email_notification']?.length || 0,
  )

  // 更新邮件数量
  if (data.email_count) {
    console.log(`[${timestamp}] 🔍 [DEBUG] 开始重新加载检测概览数据`)
    await autoDetectionLogic()
  }
  console.log(`[${timestamp}] 🔍 [DEBUG] handleNewEmails执行完毕`)
}

// 处理检测完成推送
const handleDetectionCompleted = (data) => {
  console.log('🎉 检测完成推送:', data)
  console.log('邮件ID:', data.email_id)
  console.log('检测详情:', data.detection_detail)
  console.log('消息:', data.message)
}

// 获取检测模块状态类
const getModuleStatusClass = (moduleType) => {
  if (!detectingDetail.value) return ''

  const statusMap = {
    content: detectingDetail.value.content_detection_status,
    url: detectingDetail.value.url_detection_status,
    metadata: detectingDetail.value.metadata_detection_status,
  }

  const status = statusMap[moduleType]
  if (status === 1) return 'detecting' // 检测中
  if (status === 2) return 'completed' // 检测完成
  if (status === 3) return 'no-need' // 无需检测
  return 'waiting' // 等待开始
}

// 获取模块状态文本
const getModuleStatusText = (moduleType) => {
  if (!detectingDetail.value) return '等待开始'

  const statusMap = {
    content: detectingDetail.value.content_detection_status,
    url: detectingDetail.value.url_detection_status,
    metadata: detectingDetail.value.metadata_detection_status,
  }

  const status = statusMap[moduleType]
  switch (status) {
    case 1:
      return '检测中...'
    case 2:
      return '检测完成'
    case 3:
      return '无需检测'
    default:
      return '等待开始'
  }
}

// 获取模块权重
const getModuleWeight = (moduleType) => {
  if (!detectingDetail.value) return null

  const weightMap = {
    content: detectingDetail.value.content_detection_weight,
    url: detectingDetail.value.url_detection_weight,
    metadata: detectingDetail.value.metadata_detection_weight,
  }

  const weight = weightMap[moduleType]
  return weight ? Math.round(weight * 100) : null
}

// 获取模块钓鱼概率
const getModuleProbability = (moduleType) => {
  if (!detectingDetail.value) return null

  const probabilityMap = {
    content: detectingDetail.value.content_detection_probability,
    url: detectingDetail.value.url_detection_probability,
    metadata: detectingDetail.value.metadata_detection_probability,
  }

  const probability = probabilityMap[moduleType]
  return probability !== null && probability !== undefined ? Math.round(probability * 100) : null
}

// 获取模块检测原因
const getModuleReason = (moduleType) => {
  if (!detectingDetail.value) return null

  const reasonMap = {
    content: detectingDetail.value.content_detection_reason,
    url: detectingDetail.value.url_detection_reason,
    metadata: detectingDetail.value.metadata_detection_reason,
  }

  return reasonMap[moduleType] || null
}

// 获取圆形进度条样式
const getCircleProgressStyle = (moduleType) => {
  if (!detectingDetail.value) return {}

  const statusMap = {
    content: detectingDetail.value.content_detection_status,
    url: detectingDetail.value.url_detection_status,
    metadata: detectingDetail.value.metadata_detection_status,
  }

  const status = statusMap[moduleType]
  const probability = getModuleProbability(moduleType)

  let progressColor = '#74b9ff'
  let progressPercent = 0

  switch (status) {
    case 1: // 检测中
      progressColor = '#fdcb6e'
      progressPercent = 50
      break
    case 2: // 检测完成
      if (probability !== null) {
        progressColor = probability > 50 ? '#e17055' : '#00b894'
        progressPercent = 100
      } else {
        progressColor = '#74b9ff'
        progressPercent = 100
      }
      break
    case 3: // 无需检测
      progressColor = '#636e72'
      progressPercent = 100
      break
    default: // 等待开始
      progressColor = '#ddd'
      progressPercent = 0
  }

  return {
    '--progress-color': progressColor,
    '--progress-percent': progressPercent + '%',
  }
}

// 页面挂载时加载数据
onMounted(() => {
  loadDetectionOverview()
  // startDetection(1)

  autoDetectionLogic()

  // 初始化WebSocket连接（只在未连接时连接）
  if (!wsManager.isConnected) {
    wsManager.connect()
  }

  // 注册事件监听器（每次都需要注册，因为组件可能重新挂载）
  wsManager.on('new_email_notification', handleNewEmails)
  wsManager.on('detection_completed', handleDetectionCompleted)
})

// 页面卸载时清理事件监听
onUnmounted(() => {
  wsManager.off('new_email_notification', handleNewEmails)
  wsManager.off('detection_completed', handleDetectionCompleted)
})
</script>

<style scoped>
.email-detection {
  padding: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  color: white;
  overflow-x: auto;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.page-subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin: 0;
}

.detection-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  min-width: 1200px;
  padding: 2rem 0;
  perspective: 1000px;
}

.stage {
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.12) 0%,
    rgba(255, 255, 255, 0.06) 50%,
    rgba(255, 255, 255, 0.12) 100%
  );
  backdrop-filter: blur(15px);
  border-radius: 25px;
  padding: 2.5rem;
  width: 340px;
  min-height: 480px;
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  transform: translateZ(0) rotateY(5deg);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.25);
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.stage::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(116, 185, 255, 0.8),
    rgba(255, 107, 107, 0.8),
    transparent
  );
  animation: stage-scan 4s linear infinite;
}

@keyframes stage-scan {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.stage.active {
  transform: translateZ(25px) rotateY(0deg) scale(1.05);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
  background: linear-gradient(
    135deg,
    rgba(116, 185, 255, 0.2) 0%,
    rgba(255, 255, 255, 0.15) 50%,
    rgba(116, 185, 255, 0.2) 100%
  );
  border: 2px solid rgba(116, 185, 255, 0.5);
  animation: active-pulse 2s ease-in-out infinite;
}

.stage.active::before {
  background: linear-gradient(
    90deg,
    transparent,
    rgba(116, 185, 255, 1),
    rgba(255, 217, 61, 1),
    transparent
  );
  animation: active-scan 2s linear infinite;
}

@keyframes active-pulse {
  0%,
  100% {
    box-shadow:
      0 25px 50px rgba(0, 0, 0, 0.4),
      0 0 30px rgba(116, 185, 255, 0.3);
  }
  50% {
    box-shadow:
      0 30px 60px rgba(0, 0, 0, 0.5),
      0 0 50px rgba(116, 185, 255, 0.6);
  }
}

@keyframes active-scan {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.stage.active .stage-number {
  background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
  box-shadow: 0 10px 30px rgba(116, 185, 255, 0.6);
  animation: active-number-glow 1.5s ease-in-out infinite;
}

@keyframes active-number-glow {
  0%,
  100% {
    transform: scale(1);
    box-shadow: 0 10px 30px rgba(116, 185, 255, 0.6);
  }
  50% {
    transform: scale(1.1);
    box-shadow: 0 15px 40px rgba(116, 185, 255, 0.8);
  }
}

.stage.active .stage-title {
  color: rgba(116, 185, 255, 1);
  text-shadow: 0 0 10px rgba(116, 185, 255, 0.5);
}

.stage-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
  position: relative;
  z-index: 2;
}

.stage-number {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 1.2rem;
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
  position: relative;
  transition: all 0.3s ease;
}

.stage-number::before {
  content: '';
  position: absolute;
  top: -3px;
  left: -3px;
  right: -3px;
  bottom: -3px;
  background: linear-gradient(135deg, #ff6b6b, #ee5a24);
  border-radius: 50%;
  z-index: -1;
  opacity: 0;
  animation: number-pulse 2s ease-in-out infinite;
}

@keyframes number-pulse {
  0%,
  100% {
    opacity: 0;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(1.1);
  }
}

.stage-title {
  margin: 0;
  font-size: 1.4rem;
  font-weight: 800;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  letter-spacing: 0.5px;
}

.stage-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  position: relative;
  z-index: 2;
}

.current-email {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.email-info {
  margin-bottom: 1rem;
}

.email-from,
.email-subject {
  display: flex;
  margin-bottom: 0.5rem;
}

.label {
  font-weight: 600;
  min-width: 60px;
  opacity: 0.8;
}

.value {
  flex: 1;
  word-break: break-all;
}

.email-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-indicator {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  position: relative;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.status-indicator::before {
  content: '';
  position: absolute;
  top: -4px;
  left: -4px;
  right: -4px;
  bottom: -4px;
  border-radius: 50%;
  opacity: 0.3;
  transition: all 0.4s ease;
}

.status-indicator.pending {
  background: linear-gradient(45deg, #ffd93d, #f39c12);
  box-shadow: 0 0 20px rgba(255, 217, 61, 0.5);
  animation: pulse-glow 2s infinite;
}

.status-indicator.pending::before {
  background: linear-gradient(45deg, #ffd93d, #f39c12);
  animation: ripple 2s infinite;
}

.status-indicator.processing {
  background: linear-gradient(45deg, #74b9ff, #0984e3);
  box-shadow: 0 0 25px rgba(116, 185, 255, 0.6);
  animation: processing-spin 1.5s linear infinite;
}

.status-indicator.processing::before {
  background: linear-gradient(45deg, #74b9ff, #0984e3);
  animation: processing-ripple 1s infinite;
}

.status-indicator.safe {
  background: linear-gradient(45deg, #00b894, #00a085);
  box-shadow: 0 0 20px rgba(0, 184, 148, 0.5);
}

.status-indicator.danger {
  background: linear-gradient(45deg, #e17055, #d63031);
  box-shadow: 0 0 20px rgba(225, 112, 85, 0.5);
}

@keyframes pulse-glow {
  0%,
  100% {
    transform: scale(1);
    box-shadow: 0 0 20px rgba(255, 217, 61, 0.5);
  }
  50% {
    transform: scale(1.1);
    box-shadow: 0 0 30px rgba(255, 217, 61, 0.8);
  }
}

@keyframes processing-spin {
  0% {
    transform: rotate(0deg) scale(1);
    box-shadow: 0 0 25px rgba(116, 185, 255, 0.6);
  }
  50% {
    transform: rotate(180deg) scale(1.05);
    box-shadow: 0 0 35px rgba(116, 185, 255, 0.9);
  }
  100% {
    transform: rotate(360deg) scale(1);
    box-shadow: 0 0 25px rgba(116, 185, 255, 0.6);
  }
}

@keyframes ripple {
  0% {
    transform: scale(0.8);
    opacity: 0.8;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}

@keyframes processing-ripple {
  0% {
    transform: scale(0.8);
    opacity: 0.9;
  }
  100% {
    transform: scale(2.5);
    opacity: 0;
  }
}

/* 正在检测的邮件样式 - 炫酷版本 */
.current-email {
  background: linear-gradient(
    135deg,
    rgba(116, 185, 255, 0.15) 0%,
    rgba(58, 123, 213, 0.1) 50%,
    rgba(0, 210, 255, 0.15) 100%
  );
  border: 2px solid transparent;
  background-clip: padding-box;
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 1.5rem;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(20px);
  box-shadow:
    0 8px 32px rgba(116, 185, 255, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.2),
    inset 0 -1px 0 rgba(0, 0, 0, 0.1);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  transform: translateY(0);
}

.current-email::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  animation: shimmer 3s infinite;
}

.current-email:hover {
  transform: translateY(-5px);
  box-shadow:
    0 16px 48px rgba(116, 185, 255, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

@keyframes shimmer {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

.email-info {
  margin-bottom: 1.5rem;
  position: relative;
  z-index: 2;
}

.email-from,
.email-subject {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  font-size: 0.95rem;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.email-from .label,
.email-subject .label {
  font-weight: 700;
  min-width: 80px;
  color: rgba(255, 255, 255, 0.9);
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 1px;
  position: relative;
}

.email-from .label::after,
.email-subject .label::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 20px;
  height: 2px;
  background: linear-gradient(90deg, #74b9ff, #00d2ff);
  border-radius: 1px;
}

.email-from .value,
.email-subject .value {
  margin-left: 1rem;
  color: rgba(255, 255, 255, 0.95);
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 180px;
  background: linear-gradient(90deg, #ffffff, #e3f2fd);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.email-status {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.95);
  position: relative;
  z-index: 2;
}

.pending-queue {
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.08) 0%,
    rgba(255, 255, 255, 0.03) 50%,
    rgba(255, 255, 255, 0.08) 100%
  );
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.pending-queue::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(116, 185, 255, 0.6), transparent);
  animation: queue-scan 3s linear infinite;
}

@keyframes queue-scan {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.queue-title {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 1.2rem;
  color: rgba(255, 255, 255, 0.95);
  text-transform: uppercase;
  letter-spacing: 1px;
  position: relative;
  padding-left: 1rem;
}

.queue-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 16px;
  background: linear-gradient(180deg, #74b9ff, #0984e3);
  border-radius: 2px;
}

.queue-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.queue-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.85rem;
  padding: 0.8rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.queue-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(180deg, #ffd93d, #f39c12);
  transform: scaleY(0);
  transition: transform 0.3s ease;
}

.queue-item:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(116, 185, 255, 0.3);
  transform: translateX(5px);
}

.queue-item:hover::before {
  transform: scaleY(1);
}

.queue-dot {
  width: 8px;
  height: 8px;
  background: linear-gradient(45deg, #ffd93d, #f39c12);
  border-radius: 50%;
  box-shadow: 0 0 10px rgba(255, 217, 61, 0.5);
  animation: queue-dot-pulse 2s infinite;
  flex-shrink: 0;
}

@keyframes queue-dot-pulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.8;
  }
}

.queue-subject {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.queue-more {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
  text-align: center;
  margin-top: 1rem;
  padding: 0.8rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  border: 1px dashed rgba(255, 255, 255, 0.2);
  font-weight: 500;
  letter-spacing: 0.5px;
}

/* 加载状态样式 - 炫酷版本 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  text-align: center;
  position: relative;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.08) 0%,
    rgba(255, 255, 255, 0.03) 50%,
    rgba(255, 255, 255, 0.08) 100%
  );
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.loading-state::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: conic-gradient(from 0deg, transparent, rgba(116, 185, 255, 0.1), transparent);
  border-radius: 20px;
  animation: loading-rotate 3s linear infinite;
  pointer-events: none;
}

@keyframes loading-rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading-state p {
  margin: 0.8rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  position: relative;
  z-index: 2;
  letter-spacing: 0.5px;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.9),
    rgba(116, 185, 255, 0.9),
    rgba(255, 255, 255, 0.9)
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: loading-text-flow 2s ease-in-out infinite;
}

@keyframes loading-text-flow {
  0%,
  100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.loading-spinner {
  width: 60px;
  height: 60px;
  position: relative;
  margin-bottom: 2rem;
}

.loading-spinner::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border: 4px solid transparent;
  border-top: 4px solid #74b9ff;
  border-right: 4px solid #0984e3;
  border-radius: 50%;
  animation: spin-fast 1s linear infinite;
}

.loading-spinner::after {
  content: '';
  position: absolute;
  top: 8px;
  left: 8px;
  right: 8px;
  bottom: 8px;
  border: 3px solid transparent;
  border-bottom: 3px solid #74b9ff;
  border-left: 3px solid #0984e3;
  border-radius: 50%;
  animation: spin-slow 2s linear infinite reverse;
}

@keyframes spin-fast {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes spin-slow {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* 无邮件状态样式 - 炫酷版本 */
.no-email-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  text-align: center;
  position: relative;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.05) 0%,
    rgba(255, 255, 255, 0.02) 50%,
    rgba(255, 255, 255, 0.05) 100%
  );
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  transition: all 0.4s ease;
}

.no-email-state::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at center, rgba(116, 185, 255, 0.1) 0%, transparent 70%);
  border-radius: 20px;
  opacity: 0;
  animation: ambient-glow 4s ease-in-out infinite;
}

@keyframes ambient-glow {
  0%,
  100% {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
}

.no-email-icon {
  width: 80px;
  height: 80px;
  margin-bottom: 2rem;
  position: relative;
  z-index: 2;
  transition: all 0.4s ease;
}

.no-email-icon svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 0 20px rgba(116, 185, 255, 0.3));
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.no-email-state p {
  margin: 0.8rem 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  position: relative;
  z-index: 2;
  letter-spacing: 0.5px;
}

.no-email-state .sub-text {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 400;
  letter-spacing: 0.3px;
  position: relative;
  z-index: 2;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.7),
    rgba(116, 185, 255, 0.8),
    rgba(255, 255, 255, 0.7)
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: text-shimmer 3s ease-in-out infinite;
}

@keyframes text-shimmer {
  0%,
  100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.connection-hub {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  gap: 0;
  position: relative;
  width: 120px;
  height: 200px;
}

.line {
  width: 80px;
  height: 4px;
  position: absolute;
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  transform-origin: left center;
  border-radius: 20px;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.1) 0%,
    rgba(255, 255, 255, 0.3) 25%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0.3) 75%,
    rgba(255, 255, 255, 0.1) 100%
  );
  background-size: 200% 100%;
  overflow: hidden;
  clip-path: polygon(0% 0%, 85% 0%, 100% 50%, 85% 100%, 0% 100%);
}

.line::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(0, 210, 255, 0.6) 20%,
    rgba(116, 185, 255, 0.8) 50%,
    rgba(58, 123, 213, 0.6) 80%,
    transparent 100%
  );
  border-radius: 20px;
  opacity: 0;
  transition: opacity 0.8s ease;
}

.line-1 {
  transform: rotate(-20deg);
  top: 20%;
  left: 0px;
}

.line-2 {
  transform: rotate(0deg);
  top: 50%;
  left: 0px;
}

.line-3 {
  transform: rotate(20deg);
  top: 80%;
  left: 0px;
}

.line.active {
  background: linear-gradient(
    90deg,
    rgba(0, 210, 255, 0.2) 0%,
    rgba(116, 185, 255, 0.8) 25%,
    rgba(0, 210, 255, 0.4) 50%,
    rgba(116, 185, 255, 0.8) 75%,
    rgba(0, 210, 255, 0.2) 100%
  );
  background-size: 200% 100%;
  box-shadow:
    0 0 20px rgba(116, 185, 255, 0.6),
    0 0 40px rgba(0, 210, 255, 0.3),
    inset 0 0 20px rgba(255, 255, 255, 0.1);
  animation:
    energy-flow 2s linear infinite,
    glow-pulse 3s ease-in-out infinite;
}

.line.active::before {
  opacity: 1;
  animation: particle-flow 1.5s linear infinite;
}

.convergence-hub {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-end;
  gap: 0;
  position: relative;
  width: 120px;
  height: 200px;
}

.conv-line {
  width: 80px;
  height: 4px;
  position: absolute;
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  transform-origin: right center;
  border-radius: 20px;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.1) 0%,
    rgba(255, 255, 255, 0.3) 25%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0.3) 75%,
    rgba(255, 255, 255, 0.1) 100%
  );
  background-size: 200% 100%;
  overflow: hidden;
  clip-path: polygon(0% 0%, 85% 0%, 100% 50%, 85% 100%, 0% 100%);
}

.conv-line::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(116, 185, 255, 0.6) 20%,
    rgba(0, 210, 255, 0.8) 50%,
    rgba(58, 123, 213, 0.6) 80%,
    transparent 100%
  );
  border-radius: 20px;
  opacity: 0;
  transition: opacity 0.8s ease;
}

.conv-line-1 {
  transform: rotate(20deg);
  top: 20%;
  right: 0px;
}

.conv-line-2 {
  transform: rotate(0deg);
  top: 50%;
  right: 0px;
  clip-path: polygon(0% 0%, 85% 0%, 100% 50%, 85% 100%, 0% 100%);
}

.conv-line-3 {
  transform: rotate(-20deg);
  top: 80%;
  right: 0px;
}

.conv-line.active {
  background: linear-gradient(
    90deg,
    rgba(116, 185, 255, 0.2) 0%,
    rgba(0, 210, 255, 0.8) 25%,
    rgba(116, 185, 255, 0.4) 50%,
    rgba(0, 210, 255, 0.8) 75%,
    rgba(116, 185, 255, 0.2) 100%
  );
  background-size: 200% 100%;
  box-shadow:
    0 0 20px rgba(0, 210, 255, 0.6),
    0 0 40px rgba(116, 185, 255, 0.3),
    inset 0 0 20px rgba(255, 255, 255, 0.1);
  animation:
    energy-flow-reverse 2s linear infinite,
    glow-pulse 3s ease-in-out infinite;
}

.conv-line.active::before {
  opacity: 1;
  animation: particle-flow-reverse 1.5s linear infinite;
}

.final-line {
  width: 80px;
  height: 4px;
  border-radius: 20px;
  position: relative;
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.1) 0%,
    rgba(255, 255, 255, 0.3) 25%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0.3) 75%,
    rgba(255, 255, 255, 0.1) 100%
  );
  background-size: 200% 100%;
  clip-path: polygon(0% 0%, 85% 0%, 100% 50%, 85% 100%, 0% 100%);
  overflow: hidden;
}

.final-line::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(0, 210, 255, 0.6) 20%,
    rgba(116, 185, 255, 0.8) 50%,
    rgba(58, 123, 213, 0.6) 80%,
    transparent 100%
  );
  border-radius: 20px;
  opacity: 0;
  transition: opacity 0.8s ease;
}

.final-line.active {
  background: linear-gradient(
    90deg,
    rgba(0, 210, 255, 0.2) 0%,
    rgba(116, 185, 255, 0.8) 25%,
    rgba(0, 210, 255, 0.4) 50%,
    rgba(116, 185, 255, 0.8) 75%,
    rgba(0, 210, 255, 0.2) 100%
  );
  background-size: 200% 100%;
  box-shadow:
    0 0 20px rgba(116, 185, 255, 0.6),
    0 0 40px rgba(0, 210, 255, 0.3),
    inset 0 0 20px rgba(255, 255, 255, 0.1);
  animation:
    energy-flow 2s linear infinite,
    glow-pulse 3s ease-in-out infinite;
}

.final-line.active::before {
  opacity: 1;
  animation: particle-flow 1.5s linear infinite;
}

.parallel-detections {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  flex: 1;
  gap: 2rem;
  margin-top: 1rem;
}

.detection-circle {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  position: relative;
  flex: 1;
}

.circle-container {
  position: relative;
  width: 120px;
  height: 120px;
  margin-bottom: 1rem;
}

.circle-progress {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  position: relative;
  background: conic-gradient(
    var(--progress-color, #74b9ff) var(--progress-percent, 0%),
    rgba(255, 255, 255, 0.1) var(--progress-percent, 0%)
  );
  padding: 4px;
  transition: all 0.4s ease;
}

.circle-inner {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.15) 0%,
    rgba(255, 255, 255, 0.05) 50%,
    rgba(255, 255, 255, 0.15) 100%
  );
  backdrop-filter: blur(10px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.detection-circle.detecting .circle-progress {
  animation: circle-pulse 2s ease-in-out infinite;
}

.detection-circle.detecting .circle-inner {
  animation: inner-glow 2s ease-in-out infinite;
}

.detection-circle.completed .circle-progress {
  box-shadow: 0 0 30px var(--progress-color, #74b9ff);
}

.detection-circle.no-need .circle-progress {
  opacity: 0.6;
}

.detection-circle.waiting .circle-progress {
  opacity: 0.4;
}

@keyframes circle-pulse {
  0%,
  100% {
    transform: scale(1);
    filter: brightness(1);
  }
  50% {
    transform: scale(1.05);
    filter: brightness(1.2);
  }
}

@keyframes inner-glow {
  0%,
  100% {
    box-shadow: inset 0 0 20px rgba(255, 255, 255, 0.1);
  }
  50% {
    box-shadow: inset 0 0 30px rgba(255, 255, 255, 0.2);
  }
}

.module-icon {
  width: 28px;
  height: 28px;
  margin-bottom: 0.5rem;
  transition: all 0.3s ease;
  color: rgba(255, 255, 255, 0.9);
}

.module-icon svg {
  width: 100%;
  height: 100%;
  stroke: currentColor;
  transition: all 0.3s ease;
}

.detection-circle.detecting .module-icon {
  animation: icon-pulse 2s ease-in-out infinite;
}

.detection-circle.detecting .module-icon svg {
  animation: icon-rotate 2s linear infinite;
}

.detection-circle.completed .module-icon {
  color: rgba(255, 255, 255, 1);
}

.detection-circle.no-need .module-icon {
  color: rgba(149, 165, 166, 0.8);
}

@keyframes icon-pulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 0.8;
  }
  50% {
    transform: scale(1.1);
    opacity: 1;
  }
}

@keyframes icon-rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.module-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  width: 100%;
}

.module-title {
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: rgba(255, 255, 255, 0.95);
}

.module-details {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  margin-bottom: 0.5rem;
  font-size: 0.75rem;
  width: 100%;
}

.weight-info {
  color: rgba(116, 185, 255, 0.9);
  font-weight: 600;
}

.probability-info {
  color: rgba(255, 217, 61, 0.9);
  font-weight: 600;
}

.reason-info {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.7rem;
  line-height: 1.2;
  max-width: 100px;
  word-wrap: break-word;
  text-overflow: ellipsis;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.module-status {
  font-size: 0.75rem;
  opacity: 0.9;
  margin: 0;
  transition: all 0.3s ease;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.8);
}

.detection-circle.detecting .module-status {
  color: rgba(255, 217, 61, 1);
  opacity: 1;
  animation: text-glow 2s ease-in-out infinite;
}

.detection-circle.completed .module-status {
  color: rgba(255, 255, 255, 1);
  opacity: 1;
  font-weight: 600;
}

.detection-circle.no-need .module-status {
  color: rgba(149, 165, 166, 0.8);
  opacity: 0.7;
}

@keyframes text-glow {
  0%,
  100% {
    text-shadow: 0 0 5px rgba(255, 217, 61, 0.3);
  }
  50% {
    text-shadow: 0 0 10px rgba(255, 217, 61, 0.6);
  }
}

.ai-analysis {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.ai-brain {
  position: relative;
}

.brain-core {
  width: 80px;
  height: 80px;
  background: linear-gradient(45deg, #a29bfe, #6c5ce7);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.4s ease;
  box-shadow: 0 10px 30px rgba(108, 92, 231, 0.3);
}

.brain-core.thinking {
  animation: thinking 2s infinite;
  box-shadow: 0 10px 30px rgba(108, 92, 231, 0.6);
}

.brain-core svg {
  width: 40px;
  height: 40px;
  stroke: white;
}

.analysis-result {
  text-align: center;
}

.result-status {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.result-status.safe {
  color: #00b894;
}

.result-status.danger {
  color: #e17055;
}

.status-icon {
  width: 24px;
  height: 24px;
}

.status-icon svg {
  width: 100%;
  height: 100%;
  stroke: currentColor;
}

.status-label {
  font-weight: 600;
  font-size: 1.1rem;
}

.result-reason {
  font-size: 0.9rem;
  opacity: 0.8;
  margin: 0;
  line-height: 1.5;
}

.extraction-process {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.extract-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(45deg, #fd79a8, #e84393);
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 25px rgba(232, 67, 147, 0.3);
}

.extract-icon svg {
  width: 30px;
  height: 30px;
  stroke: white;
}

.extract-status {
  text-align: center;
  width: 100%;
}

.extract-text {
  font-size: 0.9rem;
  margin-bottom: 1rem;
  opacity: 0.9;
}

.extract-progress {
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  overflow: hidden;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

@keyframes thinking {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

@keyframes pulse-glow {
  0%,
  100% {
    box-shadow:
      0 0 20px rgba(116, 185, 255, 0.6),
      0 0 40px rgba(0, 210, 255, 0.3);
  }
  50% {
    box-shadow:
      0 0 30px rgba(116, 185, 255, 0.8),
      0 0 60px rgba(0, 210, 255, 0.5);
  }
}

@keyframes energy-flow {
  0% {
    background-position: -300% 0;
    transform: scaleX(0.8);
  }
  50% {
    transform: scaleX(1.1);
  }
  100% {
    background-position: 300% 0;
    transform: scaleX(0.8);
  }
}

@keyframes energy-flow-reverse {
  0% {
    background-position: 300% 0;
    transform: scaleX(0.8);
  }
  50% {
    transform: scaleX(1.1);
  }
  100% {
    background-position: -300% 0;
    transform: scaleX(0.8);
  }
}

@keyframes particle-flow {
  0% {
    transform: translateX(-120%) scaleX(0.5);
    opacity: 0;
  }
  15% {
    opacity: 1;
    transform: translateX(-80%) scaleX(1);
  }
  85% {
    opacity: 1;
    transform: translateX(80%) scaleX(1);
  }
  100% {
    transform: translateX(120%) scaleX(0.5);
    opacity: 0;
  }
}

@keyframes particle-flow-reverse {
  0% {
    transform: translateX(120%) scaleX(0.5);
    opacity: 0;
  }
  15% {
    opacity: 1;
    transform: translateX(80%) scaleX(1);
  }
  85% {
    opacity: 1;
    transform: translateX(-80%) scaleX(1);
  }
  100% {
    transform: translateX(-120%) scaleX(0.5);
    opacity: 0;
  }
}

@keyframes glow-pulse {
  0%,
  100% {
    box-shadow:
      0 0 20px rgba(116, 185, 255, 0.6),
      0 0 40px rgba(0, 210, 255, 0.3),
      inset 0 0 20px rgba(255, 255, 255, 0.1);
  }
  50% {
    box-shadow:
      0 0 30px rgba(116, 185, 255, 0.8),
      0 0 60px rgba(0, 210, 255, 0.5),
      inset 0 0 30px rgba(255, 255, 255, 0.2);
  }
}

@keyframes arrow-pulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.8;
  }
}

/* 加载转圈样式 */
.loading-spinner {
  width: 24px;
  height: 24px;
  border: 3px solid rgba(116, 185, 255, 0.3);
  border-top: 3px solid #74b9ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* 响应式设计 */
@media (max-width: 1400px) {
  .detection-container {
    min-width: 1000px;
  }

  .stage {
    padding: 1.5rem;
  }
}

@media (max-width: 1200px) {
  .detection-container {
    flex-direction: column;
    align-items: center;
    min-width: auto;
  }

  .connection-lines,
  .convergence-lines,
  .final-line {
    transform: rotate(90deg);
    margin: 1rem 0;
  }

  .stage {
    width: 100%;
    max-width: 500px;
  }
}
</style>
