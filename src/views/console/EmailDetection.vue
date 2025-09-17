<template>
  <div class="email-detection">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">邮件检测</h1>
          <p class="page-subtitle">实时监控邮件安全检测流程</p>
        </div>
        <div class="action-section">
          <button class="fetch-email-btn" @click="handleFetchEmails" :disabled="isFetching">
            <svg
              v-if="!isFetching"
              class="btn-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="7,10 12,15 17,10" />
              <line x1="12" y1="15" x2="12" y2="3" />
            </svg>
            <div v-else class="loading-spinner"></div>
            {{ isFetching ? '获取中...' : '获取邮件' }}
          </button>
        </div>
      </div>
      <!-- 新邮件提示 -->
      <div v-if="newEmailsMessage" class="new-emails-notification">
        {{ newEmailsMessage }}
      </div>
    </div>

    <!-- 3D检测流程容器 -->
    <div class="detection-container">
      <!-- 第一阶段：开始检测 -->
      <div class="stage stage-start" :class="getStageClass(1)">
        <div class="stage-header">
          <div class="stage-number">01</div>
          <h3 class="stage-title">开始检测</h3>
        </div>

        <div class="stage-content">
          <!-- 正在检测邮件 -->
          <div v-if="detectingEmail" class="detecting-email">
            <div class="email-card current-detecting">
              <div class="email-header">
                <div class="email-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path
                      d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"
                    />
                    <polyline points="22,6 12,13 2,6" />
                  </svg>
                </div>
                <div class="detecting-badge">
                  <div class="pulse-dot"></div>
                  正在检测
                </div>
              </div>
              <div class="email-info">
                <h4 class="email-subject">{{ detectingEmail.subject || '无主题' }}</h4>
                <p class="email-sender">发送人: {{ detectingEmail.sender || '未知' }}</p>
              </div>
            </div>
          </div>

          <!-- 待检测邮件列表 -->
          <div v-if="pendingEmails.length > 0" class="pending-emails">
            <h4 class="pending-title">待检测邮件 ({{ pendingEmails.length }})</h4>
            <div class="pending-list">
              <div v-for="email in pendingEmails" :key="email.id" class="email-card pending">
                <div class="email-info">
                  <h5 class="email-subject">{{ email.subject || '无主题' }}</h5>
                  <p class="email-sender">{{ email.sender || '未知' }}</p>
                </div>
                <div class="pending-status">
                  <div class="status-dot"></div>
                  等待中
                </div>
              </div>
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
        </div>
      </div>

      <!-- 连接线 -->
      <div class="connection-hub">
        <div class="line line-1"></div>
        <div class="line line-2"></div>
        <div class="line line-3"></div>
      </div>

      <!-- 第二阶段：并行检测 -->
      <div class="stage stage-parallel" :class="getStageClass(2)">
        <div class="stage-header">
          <div class="stage-number">02</div>
          <h3 class="stage-title">并行检测</h3>
        </div>

        <div class="stage-content">
          <div class="parallel-detections">
            <!-- 邮件正文检测 -->
            <div
              class="detection-circle"
              :class="getDetectionClass('content')"
              v-if="
                detectingDetail &&
                (detectingDetail.content_detection_status === 1 ||
                  (detectingDetail.content_detection_status === 2 &&
                    detectingDetail.content_reason))
              "
              :title="
                detectingDetail.content_detection_status === 1
                  ? '正在检测邮件内容...'
                  : detectingDetail.content_reason
              "
            >
              <div class="circle-container">
                <div class="circle-progress" :style="getProgressStyle('content')">
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
                      <div class="module-details">{{ getDetectionDetails('content') }}</div>
                      <p class="module-status" :class="getDetectionStatusClass('content')">
                        {{ getDetectionStatus('content') }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- 邮件正文检测（无提示时） -->
            <div v-else class="detection-circle" :class="getDetectionClass('content')">
              <div class="circle-container">
                <div class="circle-progress" :style="getProgressStyle('content')">
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
                      <div class="module-details">{{ getDetectionDetails('content') }}</div>
                      <p class="module-status" :class="getDetectionStatusClass('content')">
                        {{ getDetectionStatus('content') }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- URL检测 -->
            <div
              class="detection-circle"
              :class="getDetectionClass('url')"
              v-if="
                detectingDetail &&
                (detectingDetail.url_detection_status === 1 ||
                  (detectingDetail.url_detection_status === 2 && detectingDetail.url_reason))
              "
              :title="
                detectingDetail.url_detection_status === 1
                  ? '正在检测URL链接...'
                  : detectingDetail.url_reason
              "
            >
              <div class="circle-container">
                <div class="circle-progress" :style="getProgressStyle('url')">
                  <div class="circle-inner">
                    <div class="module-icon">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
                        <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
                      </svg>
                    </div>
                    <div class="module-info">
                      <h4 class="module-title">URL检测</h4>
                      <div class="module-details">{{ getDetectionDetails('url') }}</div>
                      <p class="module-status" :class="getDetectionStatusClass('url')">
                        {{ getDetectionStatus('url') }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- URL检测（无提示时） -->
            <div v-else class="detection-circle" :class="getDetectionClass('url')">
              <div class="circle-container">
                <div class="circle-progress" :style="getProgressStyle('url')">
                  <div class="circle-inner">
                    <div class="module-icon">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
                        <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
                      </svg>
                    </div>
                    <div class="module-info">
                      <h4 class="module-title">URL检测</h4>
                      <div class="module-details">{{ getDetectionDetails('url') }}</div>
                      <p class="module-status" :class="getDetectionStatusClass('url')">
                        {{ getDetectionStatus('url') }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 元数据检测 -->
            <div
              class="detection-circle"
              :class="getDetectionClass('metadata')"
              v-if="
                detectingDetail &&
                (detectingDetail.metadata_detection_status === 1 ||
                  (detectingDetail.metadata_detection_status === 2 &&
                    detectingDetail.metadata_reason))
              "
              :title="
                detectingDetail.metadata_detection_status === 1
                  ? '正在检测邮件元数据...'
                  : detectingDetail.metadata_reason
              "
            >
              <div class="circle-container">
                <div class="circle-progress" :style="getProgressStyle('metadata')">
                  <div class="circle-inner">
                    <div class="module-icon">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
                      </svg>
                    </div>
                    <div class="module-info">
                      <h4 class="module-title">元数据检测</h4>
                      <div class="module-details">{{ getDetectionDetails('metadata') }}</div>
                      <p class="module-status" :class="getDetectionStatusClass('metadata')">
                        {{ getDetectionStatus('metadata') }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- 元数据检测（无提示时） -->
            <div v-else class="detection-circle" :class="getDetectionClass('metadata')">
              <div class="circle-container">
                <div class="circle-progress" :style="getProgressStyle('metadata')">
                  <div class="circle-inner">
                    <div class="module-icon">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
                      </svg>
                    </div>
                    <div class="module-info">
                      <h4 class="module-title">元数据检测</h4>
                      <div class="module-details">{{ getDetectionDetails('metadata') }}</div>
                      <p class="module-status" :class="getDetectionStatusClass('metadata')">
                        {{ getDetectionStatus('metadata') }}
                      </p>
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
      <div class="stage stage-ai" :class="getStageClass(3)">
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
              <!-- 如果有检测结果，显示AI分析结果 -->
              <div
                v-if="detectingDetail && detectingDetail.final_fusion_score !== undefined"
                class="ai-result-details"
              >
                <div class="result-item">
                  <label class="result-label">融合评分:</label>
                  <span
                    class="result-value score"
                    :class="getScoreClass(detectingDetail.final_fusion_score)"
                    >{{ detectingDetail.final_fusion_score }}</span
                  >
                </div>
                <div class="result-item">
                  <label class="result-label">是否钓鱼:</label>
                  <span
                    class="result-value phishing"
                    :class="detectingDetail.final_is_phishing ? 'is-phishing' : 'not-phishing'"
                  >
                    {{ detectingDetail.final_is_phishing ? '是' : '否' }}
                  </span>
                </div>
                <div class="result-item reason-item">
                  <label class="result-label">分析原因:</label>
                  <div
                    class="result-value reason"
                    :title="detectingDetail.final_reason || '暂无分析原因'"
                  >
                    {{ truncateText(detectingDetail.final_reason || '暂无分析原因', 100) }}
                  </div>
                </div>
              </div>
              <!-- 等待状态 -->
              <div v-else class="waiting-analysis">
                <p class="waiting-text">等待检测完成后进行AI分析</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 最终连接线 -->
      <div class="final-line"></div>

      <!-- 第四阶段：信息提取 -->
      <div class="stage stage-extract" :class="getStageClass(4)">
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

            <!-- 钓鱼邮件情况 -->
            <div
              v-if="detectingDetail && detectingDetail.final_is_phishing"
              class="phishing-warning"
            >
              <div class="warning-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path
                    d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"
                  />
                  <path d="M12 9v4" />
                  <path d="m12 17 .01 0" />
                </svg>
              </div>
              <p class="warning-text">钓鱼邮件无需分析</p>
            </div>

            <!-- 非钓鱼邮件且detection_stage为4的情况 -->
            <div
              v-else-if="
                detectingDetail &&
                !detectingDetail.final_is_phishing &&
                detectingDetail.detection_stage === 4
              "
            >
              <!-- reserved_field2为'2'时显示完整分析结果 -->
              <div v-if="detectingDetail.reserved_field2 === '2'" class="extraction-details">
                <div class="detail-item" v-if="detectingDetail.urgency_level">
                  <label class="detail-label">紧急程度:</label>
                  <span
                    class="detail-value urgency"
                    :class="getUrgencyClass(detectingDetail.urgency_level)"
                    >{{ detectingDetail.urgency_level }}</span
                  >
                </div>
                <div class="detail-item" v-if="detectingDetail.email_summary">
                  <label class="detail-label">邮件总结:</label>
                  <div class="detail-value summary" :title="detectingDetail.email_summary">
                    {{ truncateText(detectingDetail.email_summary, 120) }}
                  </div>
                </div>
                <div class="detail-item" v-if="detectingDetail.email_type">
                  <label class="detail-label">邮件类型:</label>
                  <span class="detail-value type">{{ detectingDetail.email_type }}</span>
                </div>
              </div>

              <!-- reserved_field2为'0'时显示检测中状态 -->
              <div v-else-if="detectingDetail.reserved_field2 === '0'" class="analyzing-status">
                <div class="analyzing-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="3" />
                    <path d="M12 1v6m0 6v6" />
                    <path d="m15.5 3.5-1.5 1.5m0 6-1.5 1.5" />
                    <path d="m8.5 3.5 1.5 1.5m0 6 1.5 1.5" />
                    <path d="M1 12h6m6 0h6" />
                    <path d="m3.5 8.5 1.5 1.5m6 0 1.5 1.5" />
                    <path d="m3.5 15.5 1.5-1.5m6 0 1.5-1.5" />
                  </svg>
                </div>
                <p class="analyzing-text">正在进行真伪性分析...</p>
              </div>

              <!-- reserved_field2为null或其他值时显示默认状态 -->
              <div v-else class="extract-status">
                <p class="extract-text">等待开始真伪性分析</p>
              </div>
            </div>

            <!-- 默认状态 -->
            <div v-else class="extract-status">
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
import {
  fetchEmails,
  getDetectionOverview,
  startEmailDetection,
  updateDetectionStage,
  startStage3Detection,
  setEmailDetectionStatus,
  startStage4Detection,
} from '@/api/email'
import { showSuccess, showError, showInfo } from '@/utils/toast'

// 响应式数据
const isFetching = ref(false)
const newEmailsMessage = ref('')

// 检测数据响应式变量
const detectingDetail = ref(null)
const detectingEmail = ref(null)
const pendingEmails = ref([])

// 第三阶段轮询相关变量
const isPollingStage3 = ref(false)
const stage3PollingTimer = ref(null)

// 第四阶段轮询相关变量
const isPollingStage4 = ref(false)
const stage4PollingTimer = ref(null)

// 计算阶段样式类
const getStageClass = (stageNumber) => {
  if (!detectingDetail.value || detectingDetail.value.detection_stage === undefined) {
    return 'stage-tilted' // 默认倾斜状态
  }

  const currentStageNumber = detectingDetail.value.detection_stage

  if (stageNumber < currentStageNumber) {
    return 'stage-completed' // 已完成阶段
  } else if (stageNumber === currentStageNumber) {
    return 'stage-active' // 当前激活阶段
  } else {
    return 'stage-tilted' // 未开始阶段
  }
}

// 获取评分样式类
const getScoreClass = (score) => {
  if (score >= 0.8) {
    return 'high-risk'
  } else if (score >= 0.5) {
    return 'medium-risk'
  } else {
    return 'low-risk'
  }
}

// 获取紧急程度样式类
const getUrgencyClass = (urgency) => {
  const urgencyLower = urgency?.toLowerCase()
  if (urgencyLower === 'high' || urgencyLower === '高' || urgencyLower === '紧急') {
    return 'urgency-high'
  } else if (urgencyLower === 'medium' || urgencyLower === '中' || urgencyLower === '中等') {
    return 'urgency-medium'
  } else if (urgencyLower === 'low' || urgencyLower === '低' || urgencyLower === '普通') {
    return 'urgency-low'
  } else {
    return 'urgency-normal'
  }
}

// 文字截断函数
const truncateText = (text, maxLength) => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

// 获取检测模块样式类
const getDetectionClass = (type) => {
  if (!detectingDetail.value) return 'pending'

  const statusField = `${type}_detection_status`
  const status = detectingDetail.value[statusField]

  switch (status) {
    case 0:
      return 'pending' // 未检测
    case 1:
      return 'detecting' // 正在检测
    case 2: {
      // 检测完成，根据结果添加额外样式类
      const isPhishingField = `${type}_is_phishing`
      const isPhishing = detectingDetail.value[isPhishingField]
      return isPhishing ? 'completed phishing' : 'completed safe'
    }
    case 3:
      return 'no-need' // 不需要检测
    default:
      return 'pending'
  }
}

// 获取检测进度样式
const getProgressStyle = (type) => {
  if (!detectingDetail.value) return { '--progress': '0%' }

  const statusField = `${type}_detection_status`
  const status = detectingDetail.value[statusField]

  switch (status) {
    case 0:
      return { '--progress': '0%' } // 未检测
    case 1:
      return { '--progress': '50%' } // 正在检测
    case 2:
      return { '--progress': '100%' } // 检测完成
    case 3:
      return { '--progress': '0%' } // 不需要检测
    default:
      return { '--progress': '0%' }
  }
}

// 获取检测详情信息
const getDetectionDetails = (type) => {
  if (!detectingDetail.value) return ''

  const statusField = `${type}_detection_status`
  const status = detectingDetail.value[statusField]

  switch (status) {
    case 0:
      return '' // 未检测，不显示详情
    case 1: {
      // 正在检测，显示权重
      const weightField = `${type}_weight`
      const weight = detectingDetail.value[weightField]
      return weight ? `权重: ${Number(weight).toFixed(2)}` : ''
    }
    case 2: {
      // 检测完成，显示结果
      const isPhishingField = `${type}_is_phishing`
      const probabilityField = `${type}_phishing_probability`
      const isPhishing = detectingDetail.value[isPhishingField]
      const probability = detectingDetail.value[probabilityField]

      if (isPhishing) {
        return probability ? `概率: ${(Number(probability) * 100).toFixed(0)}%` : ''
      } else {
        return '正常'
      }
    }
    case 3:
      return '无需检测' // 不需要检测
    default:
      return ''
  }
}

// 获取检测状态文本
const getDetectionStatus = (type) => {
  if (!detectingDetail.value) return '等待开始'

  const statusField = `${type}_detection_status`
  const status = detectingDetail.value[statusField]

  switch (status) {
    case 0:
      return '等待开始'
    case 1:
      return '正在检测...'
    case 2: {
      const isPhishingField = `${type}_is_phishing`
      const isPhishing = detectingDetail.value[isPhishingField]
      return isPhishing ? '钓鱼' : '正常'
    }
    case 3:
      return '无需检测'
    default:
      return '等待开始'
  }
}

// 获取检测状态样式类
const getDetectionStatusClass = (type) => {
  if (!detectingDetail.value) return ''

  const statusField = `${type}_detection_status`
  const status = detectingDetail.value[statusField]

  if (status === 2) {
    const isPhishingField = `${type}_is_phishing`
    const isPhishing = detectingDetail.value[isPhishingField]
    return isPhishing ? 'phishing-result' : 'safe-result'
  }

  return ''
}

// 获取检测概览数据
const fetchDetectionOverview = async () => {
  try {
    const overviewResponse = await getDetectionOverview()
    

    if (overviewResponse.success && overviewResponse.data) {
      detectingDetail.value = overviewResponse.data.detecting_detail
      detectingEmail.value = overviewResponse.data.detecting_email
      pendingEmails.value = overviewResponse.data.pending_emails || []

      // 检查是否需要开始或停止轮询
      if (detectingDetail.value) {
        // 如果当前是第二阶段且还没有开始轮询，则开始轮询
        if (detectingDetail.value.detection_stage === 2 && !pollingTimer) {
  
          startPollingDetectionStatus()
        }
        // 如果所有并行检测已完成，停止轮询并更新到第三阶段
        else if (isAllDetectionCompleted(detectingDetail.value) && pollingTimer) {

          stopPollingDetectionStatus()

          // 调用API更新检测阶段到第三阶段
          try {
            const updateResponse = await updateDetectionStage(detectingEmail.value.id)
            if (updateResponse.success) {
      
              // 刷新概览数据以获取最新状态
              await fetchDetectionOverview()
              // 启动第三阶段检测
              await checkAndStartStage3Detection()
            } else {
              console.error('更新检测阶段失败:', updateResponse.message)
            }
          } catch (error) {
            console.error('调用更新检测阶段API失败:', error)
          }
        }
      }
    }
  } catch (overviewError) {
    console.error('获取检测概览失败:', overviewError)
  }
}

// 获取邮件方法
const handleFetchEmails = async () => {
  if (isFetching.value) return

  isFetching.value = true
  newEmailsMessage.value = ''

  try {
    const response = await fetchEmails()

    if (response.success) {
      const newEmailCount = response.data?.new_emails_count || 0

      if (newEmailCount > 0) {
        newEmailsMessage.value = `成功获取到 ${newEmailCount} 封新邮件`
        showSuccess(`成功获取到 ${newEmailCount} 封新邮件`)
      } else {
        newEmailsMessage.value = '暂无新邮件'
        showInfo('暂无新邮件')
      }

      // 获取邮件成功后，调用检测概览函数
      await fetchDetectionOverview()
      await checkAndStartDetection()
      await fetchDetectionOverview()

      // 检查并启动第三阶段检测
      await checkAndStartStage3Detection()
      await fetchDetectionOverview()

      // 检查钓鱼邮件结果并处理第四阶段
      await checkPhishingResultAndHandleStage4()
      await fetchDetectionOverview()

      // 3秒后清除提示信息
      setTimeout(() => {
        newEmailsMessage.value = ''
      }, 3000)
    } else {
      showError(response.message || '获取邮件失败')
    }
  } catch (error) {
    console.error('获取邮件失败:', error)
    showError('获取邮件失败，请检查网络连接')
  } finally {
    isFetching.value = false
  }
}

// 轮询检测状态的定时器
let pollingTimer = null

// 检查三个并行检测是否都已完成
const isAllDetectionCompleted = (detail) => {
  if (!detail) return false

  const statuses = [
    detail.content_detection_status,
    detail.url_detection_status,
    detail.metadata_detection_status,
  ]

  // 检查所有状态是否都是完成(2)或无需检测(3)
  return statuses.every((status) => status === 2 || status === 3)
}

// 开始轮询检测状态
const startPollingDetectionStatus = () => {


  pollingTimer = setInterval(async () => {
    try {
      await fetchDetectionOverview()

      // 检查是否所有检测都已完成
      if (isAllDetectionCompleted(detectingDetail.value)) {

        stopPollingDetectionStatus()
      }
    } catch (error) {
      console.error('轮询检测状态失败:', error)
    }
  }, 1000) // 每隔1秒轮询一次
}

// 停止轮询检测状态
const stopPollingDetectionStatus = () => {
  if (pollingTimer) {
    clearInterval(pollingTimer)
    pollingTimer = null
  
  }
}

// 检查并启动邮件检测
const checkAndStartDetection = async () => {
  try {
    // 如果有正在检测的邮件，直接返回
    if (detectingEmail.value) {
  
      return
    }

    // 如果没有正在检测的邮件，且有待检测邮件，启动第一封邮件的检测
    if (pendingEmails.value && pendingEmails.value.length > 0) {
      const firstPendingEmail = pendingEmails.value[0]


      const response = await startEmailDetection(firstPendingEmail.id)

      if (response.success) {
        showSuccess('已启动邮件检测')
        // 启动检测后，重新获取检测概览
        await fetchDetectionOverview()
      } else {
        showError(response.message || '启动检测失败')
      }
    } else {
  
      showInfo('没有待检测的邮件')
    }
  } catch (error) {
    console.error('检查并启动检测失败:', error)
    showError('检查并启动检测失败')
  }
}

// 第三阶段检测相关函数
const checkAndStartStage3Detection = async () => {
  if (!detectingDetail.value || !detectingEmail.value) {
    return
  }

  // 检查是否在第三阶段且reserved_field1为'0'
  if (
    detectingDetail.value.detection_stage === 3 &&
    detectingDetail.value.reserved_field1 === '0'
  ) {
    try {

      const response = await startStage3Detection(detectingEmail.value.id)
      if (response.success) {
        showSuccess('已启动第三阶段综合分析')
        // 启动轮询检查reserved_field1状态
        startPollingStage3Status()
      } else {
        showError(response.message || '启动第三阶段检测失败')
      }
    } catch (error) {
      console.error('启动第三阶段检测失败:', error)
      showError('启动第三阶段检测失败')
    }
  }
}

// 开始轮询第三阶段状态
const startPollingStage3Status = () => {
  if (isPollingStage3.value) {
    return
  }

  isPollingStage3.value = true

  stage3PollingTimer.value = setInterval(async () => {
    try {
      await fetchDetectionOverview()

      // 检查是否应该停止轮询
      if (detectingDetail.value) {
        const currentStage = detectingDetail.value.detection_stage
        const reserved_field1 = detectingDetail.value.reserved_field1

        // 停止条件：1) reserved_field1变为'1' 2) 不再是第三阶段 3) 检测完成(阶段4或5)
        if (reserved_field1 === '1' || currentStage !== 3 || currentStage >= 4) {
          stopPollingStage3Status()
          if (reserved_field1 === '1') {
            showSuccess('第三阶段综合分析完成')
            // 第三阶段完成后，检查并处理第四阶段
            await checkPhishingResultAndHandleStage4()
          }
        }
      }
    } catch (error) {
      console.error('轮询第三阶段状态失败:', error)
    }
  }, 1000) // 每秒轮询一次
}

// 停止轮询第三阶段状态
const stopPollingStage3Status = () => {
  if (stage3PollingTimer.value) {
    clearInterval(stage3PollingTimer.value)
    stage3PollingTimer.value = null
  }
  isPollingStage3.value = false
}

// 开始轮询第四阶段状态
const startPollingStage4Status = () => {
  if (isPollingStage4.value) {
    return
  }

  isPollingStage4.value = true

  stage4PollingTimer.value = setInterval(async () => {
    try {
      await fetchDetectionOverview()

      // 检查是否应该停止轮询
      if (detectingDetail.value) {
        const reserved_field2 = detectingDetail.value.reserved_field2

        // 停止条件：reserved_field2变为'2'表示第四阶段完成
        if (reserved_field2 === '2') {
          stopPollingStage4Status()
          
          // 显示第四阶段分析结果
          const detail = detectingDetail.value
          const summaryInfo = `邮件摘要: ${detail.summary || '无'}`
          const typeInfo = `邮件类型: ${detail.email_type || '未知'}`
          const urgencyInfo = `紧急程度: ${detail.urgency_level || 1}`
          const importanceInfo = `重要程度: ${detail.importance_level || 1}`
          
          showSuccess(`第四阶段分析完成！\n${summaryInfo}\n${typeInfo}\n${urgencyInfo}\n${importanceInfo}`)
          
          // 等待1秒后设置邮件为已完成
          setTimeout(async () => {
            try {
               await setEmailDetectionStatus(detail.email_id)
               // 刷新概览并启动下一个检测
              await fetchDetectionOverview()
              await checkAndStartDetection()
            } catch (error) {
              console.error('设置邮件完成状态失败:', error)
              showError('设置邮件完成状态失败')
            }
          }, 1000)
        }
      }
    } catch (error) {
      console.error('轮询第四阶段状态失败:', error)
    }
  }, 1000) // 每秒轮询一次
}

// 停止轮询第四阶段状态
const stopPollingStage4Status = () => {
  if (stage4PollingTimer.value) {
    clearInterval(stage4PollingTimer.value)
    stage4PollingTimer.value = null
  }
  isPollingStage4.value = false
}

// 检查钓鱼邮件结果并处理第四阶段
const checkPhishingResultAndHandleStage4 = async () => {
  try {
    if (!detectingDetail.value || !detectingDetail.value.id) {
  
      return
    }

    const emailId = detectingDetail.value.email_id
    const isPhishing = detectingDetail.value.final_is_phishing
    const detectionStage = detectingDetail.value.detection_stage

  

    // 只有在第三阶段完成后才处理
    if (detectionStage < 4) {
  
      return
    }

    if (isPhishing) {
      // 如果是钓鱼邮件，设置检测状态为完成

      const response = await setEmailDetectionStatus(emailId)
      if (response.success) {
        showSuccess('钓鱼邮件已标记完成')
        // 检测完成，刷新概览并启动下一个检测
        await fetchDetectionOverview()
        await checkAndStartDetection()
      } else {
        showError('设置钓鱼邮件状态失败')
      }
    } else {
      // 如果不是钓鱼邮件，启动第四阶段检测

      const response = await startStage4Detection(emailId)
      if (response.success) {
        showSuccess('第四阶段检测已启动')
        // 启动轮询检查第四阶段状态
        startPollingStage4Status()
      } else {
        showError('启动第四阶段检测失败')
      }
    }
  } catch (error) {
    console.error('处理第四阶段失败:', error)
    showError('处理第四阶段失败')
  }
}




onMounted(() => {
  fetchDetectionOverview()
})

onUnmounted(() => {
  // 停止轮询检测状态
  stopPollingDetectionStatus()
  // 停止第三阶段轮询
  stopPollingStage3Status()
  // 停止第四阶段轮询
  stopPollingStage4Status()
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

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.title-section {
  flex: 1;
}

.action-section {
  flex-shrink: 0;
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

.fetch-email-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
}

.fetch-email-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(79, 172, 254, 0.4);
}

.fetch-email-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.btn-icon {
  width: 18px;
  height: 18px;
}

.loading-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.new-emails-notification {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 500;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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
  border: none;
  outline: none;
  box-shadow: none;
  cursor: pointer;
}

.circle-container {
  position: relative;
  width: 120px;
  height: 120px;
  margin-bottom: 1rem;
  border: none;
  outline: none;
  box-shadow: none;
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
    transform: scale(1.03);
    filter: brightness(1.1);
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

.detection-circle.detecting .module-icon svg {
  animation: icon-scale 1.5s ease-in-out infinite;
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

@keyframes icon-scale {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
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

/* 钓鱼结果时的模块信息布局优化 */
.detection-circle.completed.phishing .module-info {
  justify-content: center;
}

.detection-circle.completed.phishing .module-details {
  order: 1;
  margin-bottom: 0.8rem;
}

.detection-circle.completed.phishing .module-status {
  order: 2;
  margin-top: 0.3rem;
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

/* 钓鱼结果时的概率信息突出显示 */
.detection-circle.completed.phishing .probability-info {
  color: rgba(239, 68, 68, 1);
  font-size: 1rem;
  font-weight: 800;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
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

@keyframes detecting-shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

@keyframes dot-glow {
  0%,
  100% {
    box-shadow: 0 0 6px rgba(116, 185, 255, 0.8);
    transform: scale(1);
  }
  50% {
    box-shadow:
      0 0 12px rgba(116, 185, 255, 1),
      0 0 20px rgba(0, 210, 255, 0.6);
    transform: scale(1.1);
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

/* 阶段动态样式 */
.stage-tilted {
  transform: perspective(1000px) rotateX(5deg) rotateY(-3deg);
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.stage-completed {
  transform: perspective(1000px) rotateX(0deg) rotateY(0deg);
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 0.9;
}

.stage-active {
  transform: perspective(1000px) rotateX(0deg) rotateY(0deg) scale(1.02);
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 10px 40px rgba(116, 185, 255, 0.3);
  border: 2px solid rgba(116, 185, 255, 0.5);
}

/* 邮件卡片样式 */
.detecting-email {
  margin-bottom: 20px;
  width: 100%;
  overflow: hidden;
}

.email-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
  min-height: 80px;
  display: flex;
  flex-direction: column;
}

.email-card.current-detecting {
  border: 2px solid rgba(116, 185, 255, 0.8);
  background: linear-gradient(
    135deg,
    rgba(116, 185, 255, 0.15),
    rgba(0, 210, 255, 0.1),
    rgba(255, 255, 255, 0.08)
  );
  box-shadow:
    0 8px 32px rgba(116, 185, 255, 0.3),
    0 4px 16px rgba(0, 210, 255, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  animation: pulse-glow 2s infinite;
  position: relative;
  overflow: hidden;
}

.email-card.current-detecting::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  animation: detecting-shimmer 3s infinite;
  pointer-events: none;
}

.email-card.pending {
  opacity: 0.8;
}

.email-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.email-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
  flex-shrink: 0;
  min-height: 32px;
}

.email-icon {
  width: 24px;
  height: 24px;
  color: rgba(116, 185, 255, 0.8);
}

.detecting-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, rgba(116, 185, 255, 0.3), rgba(0, 210, 255, 0.2));
  color: #ffffff;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  box-shadow:
    0 2px 8px rgba(116, 185, 255, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(116, 185, 255, 0.4);
}

.pulse-dot {
  width: 10px;
  height: 10px;
  background: radial-gradient(circle, #ffffff, #74b9ff);
  border-radius: 50%;
  animation:
    pulse 1.5s infinite,
    dot-glow 2s infinite;
  box-shadow: 0 0 6px rgba(116, 185, 255, 0.8);
}

.email-info {
  flex: 1;
  min-width: 0;
  overflow: hidden;
}

.email-subject {
  color: #ffffff;
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px 0;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100%;
  word-break: break-all;
}

.email-sender {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100%;
  word-break: break-all;
}

.pending-emails {
  margin-top: 20px;
  width: 100%;
  overflow: hidden;
}

.pending-title {
  color: #ffffff;
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 16px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.pending-list {
  max-height: 300px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(116, 185, 255, 0.3) transparent;
  width: 100%;
  box-sizing: border-box;
}

.pending-list::-webkit-scrollbar {
  width: 6px;
}

.pending-list::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.pending-list::-webkit-scrollbar-thumb {
  background: rgba(116, 185, 255, 0.3);
  border-radius: 3px;
}

.pending-list::-webkit-scrollbar-thumb:hover {
  background: rgba(116, 185, 255, 0.5);
}

.pending-status {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 12px;
}

.status-dot {
  width: 6px;
  height: 6px;
  background: rgba(255, 255, 255, 0.4);
  border-radius: 50%;
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

@media (max-width: 1024px) {
  .stage-content {
    padding: 20px;
  }

  .email-card {
    padding: 14px;
  }

  .email-subject {
    font-size: 15px;
  }

  .email-sender {
    font-size: 13px;
  }
}

@media (max-width: 768px) {
  .stage-content {
    padding: 12px;
  }

  .email-card {
    padding: 12px;
    min-height: 70px;
  }

  .email-subject {
    font-size: 14px;
    line-height: 1.3;
    margin-bottom: 6px;
  }

  .email-sender {
    font-size: 12px;
  }

  .pending-title {
    font-size: 16px;
  }

  .detecting-badge {
    padding: 3px 8px;
    font-size: 11px;
  }

  .email-header {
    margin-bottom: 8px;
    flex-wrap: wrap;
    gap: 8px;
  }
}

@media (max-width: 480px) {
  .stage-content {
    padding: 10px;
  }

  .email-card {
    padding: 10px;
    min-height: 60px;
  }

  .email-subject {
    font-size: 13px;
    line-height: 1.2;
  }

  .email-sender {
    font-size: 11px;
  }

  .pending-title {
    font-size: 14px;
  }

  .detecting-badge {
    padding: 2px 6px;
    font-size: 10px;
  }

  .email-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
  }

  .pending-list {
    max-height: 200px;
  }
}

/* 第二阶段检测模块样式 */

.detection-circle.pending {
  opacity: 0.6;
}

.detection-circle.detecting {
  opacity: 1;
  animation: detection-pulse 2s ease-in-out infinite;
}

.detection-circle.detecting .circle-progress {
  background: conic-gradient(
    from 0deg,
    rgba(116, 185, 255, 0.8) 0deg,
    rgba(116, 185, 255, 0.8) calc(var(--progress) * 3.6deg),
    rgba(255, 255, 255, 0.1) calc(var(--progress) * 3.6deg),
    rgba(255, 255, 255, 0.1) 360deg
  );
  animation: circle-pulse 2s ease-in-out infinite;
}

.detection-circle.completed {
  opacity: 1;
}

.detection-circle.completed .circle-progress {
  background: conic-gradient(from 0deg, rgba(0, 184, 148, 0.8) 0deg, rgba(0, 184, 148, 0.8) 360deg);
}

.detection-circle.no-need {
  opacity: 0.4;
  filter: grayscale(0.5);
}

@keyframes detection-pulse {
  0%,
  100% {
    transform: scale(1);
    box-shadow: 0 0 20px rgba(116, 185, 255, 0.3);
  }
  50% {
    transform: scale(1.02);
    box-shadow: 0 0 30px rgba(116, 185, 255, 0.5);
  }
}

@keyframes progress-rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* 检测完成状态的特殊样式 */
.detection-circle.completed.phishing .circle-progress {
  background: conic-gradient(from 0deg, rgba(239, 68, 68, 0.7) 0deg, rgba(239, 68, 68, 0.7) 360deg);
  box-shadow: 0 0 25px rgba(239, 68, 68, 0.4);
  border: 2px solid rgba(239, 68, 68, 0.6);
}

.detection-circle.completed.phishing .circle-inner {
  background: linear-gradient(
    135deg,
    rgba(239, 68, 68, 0.15) 0%,
    rgba(220, 38, 38, 0.1) 50%,
    rgba(239, 68, 68, 0.15) 100%
  );
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.detection-circle.completed.phishing .module-icon {
  color: rgba(239, 68, 68, 0.9);
}

.detection-circle.completed.phishing .module-title {
  font-size: 0.75rem;
  opacity: 0.7;
}

.detection-circle.completed.phishing .module-status {
  color: rgba(239, 68, 68, 1);
}

.detection-circle.completed.safe .circle-progress {
  background: conic-gradient(from 0deg, rgba(5, 150, 105, 0.8) 0deg, rgba(5, 150, 105, 0.8) 360deg);
  box-shadow: 0 0 25px rgba(5, 150, 105, 0.4);
}

.detection-circle.completed.safe .module-status {
  color: rgba(5, 150, 105, 1);
}

/* 钓鱼结果特殊样式 */
.module-status.phishing-result {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.9) 0%, rgba(220, 38, 38, 0.8) 100%);
  color: white;
  font-size: 1.4rem;
  font-weight: 900;
  padding: 0.6rem 1.2rem;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3);
  animation: phishing-alert 2.5s ease-in-out infinite;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin: 0.8rem 0;
  border: 2px solid rgba(255, 255, 255, 0.4);
  position: relative;
  z-index: 5;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

.module-status.safe-result {
  background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
  color: white;
  font-size: 1rem;
  font-weight: 700;
  padding: 0.3rem 0.8rem;
  border-radius: 6px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(39, 174, 96, 0.3);
}

@keyframes phishing-alert {
  0%,
  100% {
    transform: scale(1);
    box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3);
  }
  50% {
    transform: scale(1.03);
    box-shadow: 0 6px 25px rgba(239, 68, 68, 0.5);
  }
}

@media (max-width: 1200px) {
  .module-status.phishing-result {
    font-size: 1rem;
    padding: 0.4rem 0.8rem;
  }
}

/* AI分析结果样式 */
.ai-result-details {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.result-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.result-item.reason-item {
  flex-direction: column;
  align-items: stretch;
  gap: 0.5rem;
}

.result-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  min-width: 80px;
  flex-shrink: 0;
}

.result-value {
  font-size: 1rem;
  font-weight: 500;
  color: white;
}

.result-value.score {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-weight: 700;
  text-align: center;
  min-width: 60px;
}

.result-value.score.high-risk {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 2px 10px rgba(239, 68, 68, 0.3);
}

.result-value.score.medium-risk {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  box-shadow: 0 2px 10px rgba(245, 158, 11, 0.3);
}

.result-value.score.low-risk {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 2px 10px rgba(16, 185, 129, 0.3);
}

.result-value.phishing {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-weight: 700;
  text-align: center;
  min-width: 50px;
}

.result-value.phishing.is-phishing {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 2px 10px rgba(239, 68, 68, 0.3);
}

.result-value.phishing.not-phishing {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 2px 10px rgba(16, 185, 129, 0.3);
}

.result-value.reason {
  background: rgba(255, 255, 255, 0.05);
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
  max-height: 4.5em;
  overflow: hidden;
  word-wrap: break-word;
  word-break: break-all;
  cursor: help;
  transition: all 0.3s ease;
}

.result-value.reason:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.waiting-analysis {
  text-align: center;
  padding: 2rem;
}

.waiting-analysis .waiting-text {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
}

/* 第四阶段样式 */
.phishing-warning {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%);
  border: 2px solid rgba(239, 68, 68, 0.3);
  border-radius: 12px;
}

.warning-icon {
  width: 48px;
  height: 48px;
  color: #ef4444;
  animation: warning-pulse 2s ease-in-out infinite;
}

.warning-text {
  color: #ef4444;
  font-size: 1.1rem;
  font-weight: 600;
  text-align: center;
  margin: 0;
}

@keyframes warning-pulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
}

.extraction-details {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.detail-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.detail-item:last-child {
  flex-direction: column;
  align-items: stretch;
  gap: 0.5rem;
}

.detail-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  min-width: 80px;
  flex-shrink: 0;
}

.detail-value {
  font-size: 1rem;
  font-weight: 500;
  color: white;
}

.detail-value.urgency {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-weight: 700;
  text-align: center;
  min-width: 60px;
}

.detail-value.urgency.urgency-high {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 2px 10px rgba(239, 68, 68, 0.3);
}

.detail-value.urgency.urgency-medium {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  box-shadow: 0 2px 10px rgba(245, 158, 11, 0.3);
}

.detail-value.urgency.urgency-low {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 2px 10px rgba(16, 185, 129, 0.3);
}

.detail-value.urgency.urgency-normal {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  color: white;
  box-shadow: 0 2px 10px rgba(107, 114, 128, 0.3);
}

.detail-value.summary {
  background: rgba(255, 255, 255, 0.05);
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
  max-height: 4.5em;
  overflow: hidden;
  word-wrap: break-word;
  word-break: break-all;
  cursor: help;
  transition: all 0.3s ease;
}

.detail-value.summary:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.detail-value.type {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-weight: 600;
  box-shadow: 0 2px 10px rgba(139, 92, 246, 0.3);
}

.analyzing-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
}

.analyzing-icon {
  width: 40px;
  height: 40px;
  color: rgba(116, 185, 255, 0.8);
  animation: analyzing-spin 2s linear infinite;
}

.analyzing-text {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  text-align: center;
  margin: 0;
}

@keyframes analyzing-spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.extract-status {
  text-align: center;
  padding: 2rem;
}

.extract-text {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
  margin: 0;
}
</style>
