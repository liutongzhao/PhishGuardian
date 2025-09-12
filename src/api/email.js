/**
 * 邮件相关API服务
 */
import request from '@/utils/api'

/**
 * 获取待检测邮件列表
 * @returns {Promise} API响应
 */
export function getPendingEmails() {
  return request({
    url: '/email/pending',
    method: 'get'
  })
}

/**
 * 获取检测中邮件列表
 * @returns {Promise} API响应
 */
export function getDetectingEmails() {
  return request({
    url: '/email/detecting',
    method: 'get'
  })
}

/**
 * 获取待检测邮件数量
 * @returns {Promise} API响应
 */
export function getPendingEmailCount() {
  return request({
    url: '/email/pending/count',
    method: 'get'
  })
}

/**
 * 更新邮件检测状态
 * @param {number} emailId - 邮件ID
 * @param {string} status - 检测状态 (PENDING, DETECTING, SUCCESS, FAILED)
 * @param {Object} result - 检测结果（可选）
 * @returns {Promise} API响应
 */
export function updateEmailStatus(emailId, status, result = null) {
  return request({
    url: `/email/${emailId}/status`,
    method: 'put',
    data: {
      status,
      result
    }
  })
}

/**
 * 获取邮箱绑定列表
 * @returns {Promise} API响应
 */
export function getEmailBindings() {
  return request({
    url: '/email/bindings',
    method: 'get'
  })
}

/**
 * 添加邮箱绑定
 * @param {Object} data - 邮箱绑定数据
 * @returns {Promise} API响应
 */
export function addEmailBinding(data) {
  return request({
    url: '/email/bindings',
    method: 'post',
    data
  })
}

/**
 * 删除邮箱绑定
 * @param {number} bindingId - 绑定ID
 * @returns {Promise} API响应
 */
export function deleteEmailBinding(bindingId) {
  return request({
    url: `/email/bindings/${bindingId}`,
    method: 'delete'
  })
}

/**
 * 获取邮箱厂商列表
 * @returns {Promise} API响应
 */
export function getEmailProviders() {
  return request({
    url: '/email/providers',
    method: 'get'
  })
}

/**
 * 手动获取邮件
 * @returns {Promise} API响应
 */
export function fetchEmails() {
  return request({
    url: '/email/fetch',
    method: 'post'
  })
}

/**
 * 获取邮件详情
 * @param {number} emailId - 邮件ID
 * @returns {Promise} API响应
 */
export function getEmailDetail(emailId) {
  return request({
    url: `/email/${emailId}`,
    method: 'get'
  })
}

/**
 * 批量更新邮件状态
 * @param {Array} emailIds - 邮件ID数组
 * @param {string} status - 检测状态
 * @returns {Promise} API响应
 */
export function batchUpdateEmailStatus(emailIds, status) {
  return request({
    url: '/email/batch/status',
    method: 'put',
    data: {
      email_ids: emailIds,
      status
    }
  })
}

/**
 * 获取邮件统计信息
 * @returns {Promise} API响应
 */
export function getEmailStats() {
  return request({
    url: '/email/stats',
    method: 'get'
  })
}

/**
 * 初始化邮件检测权重
 * @param {number} emailId - 邮件ID
 * @returns {Promise} API响应
 */
export function initializeDetectionWeights(emailId) {
  return request({
    url: `/email/${emailId}/initialize-weights`,
    method: 'post'
  })
}

/**
 * 启动邮件内容检测
 * @param {number} emailId - 邮件ID
 * @returns {Promise} API响应
 */
export function detectEmailContent(emailId) {
  return request({
    url: `/email/${emailId}/detect/content`,
    method: 'post'
  })
}

/**
 * 启动邮件URL检测
 * @param {number} emailId - 邮件ID
 * @returns {Promise} API响应
 */
export function detectEmailUrls(emailId) {
  return request({
    url: `/email/${emailId}/detect/url`,
    method: 'post'
  })
}

/**
 * 启动邮件元数据检测
 * @param {number} emailId - 邮件ID
 * @returns {Promise} API响应
 */
export function detectEmailMetadata(emailId) {
  return request({
    url: `/email/${emailId}/detect/metadata`,
    method: 'post'
  })
}

/**
 * 获取邮件检测状态
 * @param {number} emailId - 邮件ID
 * @returns {Promise} API响应
 */
export function getDetectionStatus(emailId) {
  return request({
    url: `/email/${emailId}/detect/status`,
    method: 'get'
  })
}

// ==================== 检测会话状态管理 ====================

// 获取会话状态
export const getSessionState = () => {
  return request({
    url: '/detection/session',
    method: 'GET'
  })
}

// 更新会话状态
export const updateSessionState = (stateData) => {
  return request({
    url: '/detection/session',
    method: 'PUT',
    data: stateData
  })
}

// 更新特定检测模块状态
export const updateDetectionState = (detectionType, state) => {
  return request({
    url: `/detection/session/detection/${detectionType}`,
    method: 'PUT',
    data: { state }
  })
}

// 更新AI分析状态
export const updateAiAnalysisState = (state) => {
  return request({
    url: '/detection/session/ai-analysis',
    method: 'PUT',
    data: { state }
  })
}

// 更新会话阶段
export const updateSessionStage = (stage, status = null) => {
  return request({
    url: '/detection/session/stage',
    method: 'PUT',
    data: { stage, status }
  })
}

// 重置会话状态
export const resetSessionState = () => {
  return request({
    url: '/detection/session/reset',
    method: 'POST'
  })
}

// ==================== 新的统一检测接口 ====================

// 获取邮件检测概览（统一API）
export const getDetectionOverview = () => {
  return request({
    url: '/email/detection-overview',
    method: 'GET'
  })
}

// 启动邮件检测
export const startEmailDetection = (emailId) => {
  return request({
    url: `/email/${emailId}/start-detection`,
    method: 'POST'
  })
}
