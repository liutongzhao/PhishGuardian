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
      <div class="stage stage-start" :class="{ active: currentStage >= 1 }">
        <div class="stage-header">
          <div class="stage-number">01</div>
          <h3 class="stage-title">开始检测</h3>
        </div>
        
        <div class="stage-content">
          <!-- 当前检测邮件 -->
          <div class="current-email" v-if="currentEmail">
            <div class="email-info">
              <div class="email-from">
                <span class="label">发件人:</span>
                <span class="value">{{ currentEmail.from }}</span>
              </div>
              <div class="email-subject">
                <span class="label">主题:</span>
                <span class="value">{{ currentEmail.subject }}</span>
              </div>
            </div>
            <div class="email-status">
              <div class="status-indicator" :class="getStatusClass()"></div>
              <span class="status-text">{{ getStatusText() }}</span>
            </div>
          </div>

          <!-- 待检测队列 -->
          <div class="pending-queue">
            <h4 class="queue-title">待检测队列 ({{ pendingEmails.length }})</h4>
            <div class="queue-list">
              <div 
                v-for="email in pendingEmails.slice(0, 3)" 
                :key="email.id" 
                class="queue-item"
              >
                <div class="queue-dot"></div>
                <span class="queue-subject">{{ email.subject }}</span>
              </div>
              <div v-if="pendingEmails.length > 3" class="queue-more">
                +{{ pendingEmails.length - 3 }} 更多
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 连接线 -->
      <div class="connection-hub">
        <div class="line line-1" :class="{ active: currentStage >= 2 }"></div>
        <div class="line line-2" :class="{ active: currentStage >= 2 }"></div>
        <div class="line line-3" :class="{ active: currentStage >= 2 }"></div>
      </div>

      <!-- 第二阶段：并行检测 -->
      <div class="stage stage-parallel" :class="{ active: currentStage >= 2 }">
        <div class="stage-header">
          <div class="stage-number">02</div>
          <h3 class="stage-title">并行检测</h3>
        </div>

        <div class="stage-content">
          <div class="parallel-detections">
            <!-- 邮件正文检测 -->
            <div class="detection-module" :class="{ active: contentDetection.active, completed: contentDetection.completed }">
              <div class="module-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14,2 14,8 20,8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                  <polyline points="10,9 9,9 8,9"/>
                </svg>
              </div>
              <h4 class="module-title">正文检测</h4>
              <div class="module-progress">
                <div class="progress-bar" :style="{ width: contentDetection.progress + '%' }"></div>
              </div>
              <p class="module-status">{{ contentDetection.status }}</p>
            </div>

            <!-- URL检测 -->
            <div class="detection-module" :class="{ active: urlDetection.active, completed: urlDetection.completed }">
              <div class="module-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
                  <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
                </svg>
              </div>
              <h4 class="module-title">URL检测</h4>
              <div class="module-progress">
                <div class="progress-bar" :style="{ width: urlDetection.progress + '%' }"></div>
              </div>
              <p class="module-status">{{ urlDetection.status }}</p>
            </div>

            <!-- 元数据检测 -->
            <div class="detection-module" :class="{ active: metadataDetection.active, completed: metadataDetection.completed }">
              <div class="module-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
                </svg>
              </div>
              <h4 class="module-title">元数据检测</h4>
              <div class="module-progress">
                <div class="progress-bar" :style="{ width: metadataDetection.progress + '%' }"></div>
              </div>
              <p class="module-status">{{ metadataDetection.status }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 汇聚线 -->
      <div class="convergence-hub">
        <div class="conv-line conv-line-1" :class="{ active: currentStage >= 3 }"></div>
        <div class="conv-line conv-line-2" :class="{ active: currentStage >= 3 }"></div>
        <div class="conv-line conv-line-3" :class="{ active: currentStage >= 3 }"></div>
      </div>

      <!-- 第三阶段：AI判断 -->
      <div class="stage stage-ai" :class="{ active: currentStage >= 3 }">
        <div class="stage-header">
          <div class="stage-number">03</div>
          <h3 class="stage-title">AI综合判断</h3>
        </div>

        <div class="stage-content">
          <div class="ai-analysis">
            <div class="ai-brain">
              <div class="brain-core" :class="{ thinking: aiAnalysis.thinking }">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/>
                  <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"/>
                </svg>
              </div>
            </div>
            <div class="analysis-result" v-if="aiAnalysis.completed">
              <div class="result-status" :class="aiAnalysis.result.type">
                <div class="status-icon">
                  <svg v-if="aiAnalysis.result.type === 'safe'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                    <path d="M9 12l2 2 4-4"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                    <path d="M12 8v4"/>
                    <path d="M12 16h.01"/>
                  </svg>
                </div>
                <span class="status-label">{{ aiAnalysis.result.label }}</span>
              </div>
              <p class="result-reason">{{ aiAnalysis.result.reason }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 最终连接线 -->
      <div class="final-line" :class="{ active: currentStage >= 4 }"></div>

      <!-- 第四阶段：信息提取 -->
      <div class="stage stage-extract" :class="{ active: currentStage >= 4 }">
        <div class="stage-header">
          <div class="stage-number">04</div>
          <h3 class="stage-title">信息提取</h3>
        </div>

        <div class="stage-content">
          <div class="extraction-process">
            <div class="extract-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14,2 14,8 20,8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
              </svg>
            </div>
            <div class="extract-status">
              <p class="extract-text">{{ extractionStatus }}</p>
              <div class="extract-progress" v-if="extractionProgress < 100">
                <div class="progress-bar" :style="{ width: extractionProgress + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>


  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

defineOptions({
  name: 'EmailDetection'
})

// 响应式数据
const currentStage = ref(0)
const isDetecting = ref(false)

// 当前检测邮件
const currentEmail = ref({
  id: 1,
  from: 'suspicious@example.com',
  subject: '紧急：您的账户需要验证',
  content: '点击链接验证您的账户...'
})

// 待检测邮件队列
const pendingEmails = ref([
  { id: 2, subject: '银行安全提醒', from: 'bank@security.com' },
  { id: 3, subject: '中奖通知', from: 'lottery@winner.com' },
  { id: 4, subject: '系统升级通知', from: 'system@update.com' },
  { id: 5, subject: '账单提醒', from: 'billing@service.com' },
  { id: 6, subject: '会议邀请', from: 'meeting@company.com' }
])

// 检测模块状态
const contentDetection = reactive({
  active: false,
  completed: false,
  progress: 0,
  status: '等待开始'
})

const urlDetection = reactive({
  active: false,
  completed: false,
  progress: 0,
  status: '等待开始'
})

const metadataDetection = reactive({
  active: false,
  completed: false,
  progress: 0,
  status: '等待开始'
})

// AI分析状态
const aiAnalysis = reactive({
  thinking: false,
  completed: false,
  result: {
    type: 'danger', // 'safe' or 'danger'
    label: '钓鱼邮件',
    reason: '检测到可疑链接和诱导性内容，存在钓鱼风险'
  }
})

// 信息提取状态
const extractionStatus = ref('等待开始')
const extractionProgress = ref(0)

// 方法
function getStatusClass() {
  if (currentStage.value === 0) return 'pending'
  if (currentStage.value < 4) return 'processing'
  return aiAnalysis.result.type === 'safe' ? 'safe' : 'danger'
}

function getStatusText() {
  if (currentStage.value === 0) return '等待检测'
  if (currentStage.value < 4) return '检测中'
  return aiAnalysis.result.type === 'safe' ? '安全邮件' : '钓鱼邮件'
}

async function startDetection() {
  if (isDetecting.value) return
  
  isDetecting.value = true
  currentStage.value = 1
  
  // 延迟进入第二阶段
  await new Promise(resolve => setTimeout(resolve, 1000))
  currentStage.value = 2
  
  // 开始并行检测
  await Promise.all([
    runContentDetection(),
    runUrlDetection(),
    runMetadataDetection()
  ])
  
  // 进入AI分析阶段
  currentStage.value = 3
  await runAiAnalysis()
  
  // 进入信息提取阶段
  currentStage.value = 4
  await runExtraction()
  
  isDetecting.value = false
}

async function runContentDetection() {
  contentDetection.active = true
  contentDetection.status = '分析邮件正文...'
  
  for (let i = 0; i <= 100; i += 10) {
    contentDetection.progress = i
    await new Promise(resolve => setTimeout(resolve, 200))
  }
  
  contentDetection.completed = true
  contentDetection.status = '正文分析完成'
}

async function runUrlDetection() {
  await new Promise(resolve => setTimeout(resolve, 300))
  urlDetection.active = true
  urlDetection.status = '检测URL链接...'
  
  for (let i = 0; i <= 100; i += 15) {
    urlDetection.progress = i
    await new Promise(resolve => setTimeout(resolve, 150))
  }
  
  urlDetection.completed = true
  urlDetection.status = 'URL检测完成'
}

async function runMetadataDetection() {
  await new Promise(resolve => setTimeout(resolve, 500))
  metadataDetection.active = true
  metadataDetection.status = '分析元数据...'
  
  for (let i = 0; i <= 100; i += 20) {
    metadataDetection.progress = i
    await new Promise(resolve => setTimeout(resolve, 100))
  }
  
  metadataDetection.completed = true
  metadataDetection.status = '元数据分析完成'
}

async function runAiAnalysis() {
  aiAnalysis.thinking = true
  await new Promise(resolve => setTimeout(resolve, 2000))
  aiAnalysis.thinking = false
  aiAnalysis.completed = true
}

async function runExtraction() {
  extractionStatus.value = '提取邮件摘要...'
  
  for (let i = 0; i <= 100; i += 25) {
    extractionProgress.value = i
    await new Promise(resolve => setTimeout(resolve, 200))
  }
  
  extractionStatus.value = '信息提取完成'
}

function resetDetection() {
  if (isDetecting.value) return
  
  currentStage.value = 0
  
  // 重置检测模块
  Object.assign(contentDetection, {
    active: false,
    completed: false,
    progress: 0,
    status: '等待开始'
  })
  
  Object.assign(urlDetection, {
    active: false,
    completed: false,
    progress: 0,
    status: '等待开始'
  })
  
  Object.assign(metadataDetection, {
    active: false,
    completed: false,
    progress: 0,
    status: '等待开始'
  })
  
  // 重置AI分析
  aiAnalysis.thinking = false
  aiAnalysis.completed = false
  
  // 重置信息提取
  extractionStatus.value = '等待开始'
  extractionProgress.value = 0
}

onMounted(() => {
  // 自动开始检测流程
  startContinuousDetection()
})

// 持续检测函数
async function startContinuousDetection() {
  while (pendingEmails.value.length > 0) {
    await startDetection()
    // 检测完成后等待一段时间再检测下一封
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // 模拟处理完当前邮件，移除第一封邮件
    if (pendingEmails.value.length > 0) {
      // 更新当前检测邮件为下一封
      const nextEmail = pendingEmails.value.shift()
      if (nextEmail) {
        currentEmail.value = nextEmail
      }
    }
  }
  
  // 如果没有待检测邮件，显示等待状态
  if (pendingEmails.value.length === 0) {
    currentStage.value = 0
    resetDetection()
  }
}
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
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 2rem;
  width: 320px;
  min-height: 450px;
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  transform: translateZ(0) rotateY(5deg);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stage.active {
  transform: translateZ(20px) rotateY(0deg);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  background: rgba(255, 255, 255, 0.15);
}

.stage-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.stage-number {
  width: 40px;
  height: 40px;
  background: linear-gradient(45deg, #ff6b6b, #ee5a24);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
}

.stage-title {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
}

.stage-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
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
  width: 12px;
  height: 12px;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.status-indicator.pending {
  background: #ffd93d;
  animation: pulse 2s infinite;
}

.status-indicator.processing {
  background: #74b9ff;
  animation: pulse 1s infinite;
}

.status-indicator.safe {
  background: #00b894;
}

.status-indicator.danger {
  background: #e17055;
}

.pending-queue {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 1rem;
}

.queue-title {
  font-size: 0.9rem;
  margin-bottom: 1rem;
  opacity: 0.8;
}

.queue-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.queue-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
}

.queue-dot {
  width: 6px;
  height: 6px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 50%;
}

.queue-subject {
  opacity: 0.8;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.queue-more {
  font-size: 0.7rem;
  opacity: 0.6;
  text-align: center;
  margin-top: 0.5rem;
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
  background: linear-gradient(90deg, 
    rgba(255, 255, 255, 0.1) 0%, 
    rgba(255, 255, 255, 0.3) 25%, 
    rgba(255, 255, 255, 0.1) 50%, 
    rgba(255, 255, 255, 0.3) 75%, 
    rgba(255, 255, 255, 0.1) 100%);
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
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(0, 210, 255, 0.6) 20%, 
    rgba(116, 185, 255, 0.8) 50%, 
    rgba(58, 123, 213, 0.6) 80%, 
    transparent 100%);
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
  background: linear-gradient(90deg, 
    rgba(0, 210, 255, 0.2) 0%, 
    rgba(116, 185, 255, 0.8) 25%, 
    rgba(0, 210, 255, 0.4) 50%, 
    rgba(116, 185, 255, 0.8) 75%, 
    rgba(0, 210, 255, 0.2) 100%);
  background-size: 200% 100%;
  box-shadow: 
    0 0 20px rgba(116, 185, 255, 0.6),
    0 0 40px rgba(0, 210, 255, 0.3),
    inset 0 0 20px rgba(255, 255, 255, 0.1);
  animation: energy-flow 2s linear infinite, glow-pulse 3s ease-in-out infinite;
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
  background: linear-gradient(90deg, 
    rgba(255, 255, 255, 0.1) 0%, 
    rgba(255, 255, 255, 0.3) 25%, 
    rgba(255, 255, 255, 0.1) 50%, 
    rgba(255, 255, 255, 0.3) 75%, 
    rgba(255, 255, 255, 0.1) 100%);
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
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(116, 185, 255, 0.6) 20%, 
    rgba(0, 210, 255, 0.8) 50%, 
    rgba(58, 123, 213, 0.6) 80%, 
    transparent 100%);
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
  background: linear-gradient(90deg, 
    rgba(116, 185, 255, 0.2) 0%, 
    rgba(0, 210, 255, 0.8) 25%, 
    rgba(116, 185, 255, 0.4) 50%, 
    rgba(0, 210, 255, 0.8) 75%, 
    rgba(116, 185, 255, 0.2) 100%);
  background-size: 200% 100%;
  box-shadow: 
    0 0 20px rgba(0, 210, 255, 0.6),
    0 0 40px rgba(116, 185, 255, 0.3),
    inset 0 0 20px rgba(255, 255, 255, 0.1);
  animation: energy-flow-reverse 2s linear infinite, glow-pulse 3s ease-in-out infinite;
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
  background: linear-gradient(90deg, 
    rgba(255, 255, 255, 0.1) 0%, 
    rgba(255, 255, 255, 0.3) 25%, 
    rgba(255, 255, 255, 0.1) 50%, 
    rgba(255, 255, 255, 0.3) 75%, 
    rgba(255, 255, 255, 0.1) 100%);
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
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(0, 210, 255, 0.6) 20%, 
    rgba(116, 185, 255, 0.8) 50%, 
    rgba(58, 123, 213, 0.6) 80%, 
    transparent 100%);
  border-radius: 20px;
  opacity: 0;
  transition: opacity 0.8s ease;
}

.final-line.active {
  background: linear-gradient(90deg, 
    rgba(0, 210, 255, 0.2) 0%, 
    rgba(116, 185, 255, 0.8) 25%, 
    rgba(0, 210, 255, 0.4) 50%, 
    rgba(116, 185, 255, 0.8) 75%, 
    rgba(0, 210, 255, 0.2) 100%);
  background-size: 200% 100%;
  box-shadow: 
    0 0 20px rgba(116, 185, 255, 0.6),
    0 0 40px rgba(0, 210, 255, 0.3),
    inset 0 0 20px rgba(255, 255, 255, 0.1);
  animation: energy-flow 2s linear infinite, glow-pulse 3s ease-in-out infinite;
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
  gap: 1rem;
  margin-top: 1rem;
}

.detection-module {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 1rem;
  transition: all 0.4s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.detection-module.active {
  background: rgba(116, 185, 255, 0.2);
  border-color: rgba(116, 185, 255, 0.4);
  transform: scale(1.05);
}

.detection-module.completed {
  background: rgba(0, 184, 148, 0.2);
  border-color: rgba(0, 184, 148, 0.4);
}

.module-icon {
  width: 32px;
  height: 32px;
  margin-bottom: 0.8rem;
}

.module-icon svg {
  width: 100%;
  height: 100%;
  stroke: currentColor;
}

.module-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.8rem;
}

.module-progress {
  width: 100%;
  height: 3px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  margin-bottom: 0.8rem;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #74b9ff, #0984e3);
  border-radius: 2px;
  transition: width 0.3s ease;
}

.module-status {
  font-size: 0.8rem;
  opacity: 0.8;
  margin: 0;
  flex: 1;
  display: flex;
  align-items: center;
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
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

@keyframes thinking {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 0 20px rgba(116, 185, 255, 0.6), 0 0 40px rgba(0, 210, 255, 0.3);
  }
  50% {
    box-shadow: 0 0 30px rgba(116, 185, 255, 0.8), 0 0 60px rgba(0, 210, 255, 0.5);
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
  0%, 100% {
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
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.8;
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