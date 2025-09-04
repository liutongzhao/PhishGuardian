<template>
  <div class="email-bind-page">
    <div class="page-header">
      <h1 class="page-title">邮箱绑定</h1>
      <p class="page-subtitle">管理和绑定您的邮箱账户，用于接收重要通知</p>
    </div>

    <div class="bind-content">
      <!-- 主卡片容器 -->
      <div class="bind-card">
        <!-- 卡片头部 -->
        <div class="card-header">
          <!-- 标签页 -->
          <div class="tabs">
            <button class="tab-item active">已绑定邮箱</button>
          </div>

          <!-- 右侧操作区 -->
          <div class="header-actions">
            <div class="search-container">
              <svg
                class="search-icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <circle cx="11" cy="11" r="8" />
                <path d="m21 21-4.35-4.35" />
              </svg>
              <input type="text" placeholder="请关键字搜索" class="search-input" />
            </div>
            <button class="add-btn" @click="showModal = true">
              <svg
                class="btn-icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path d="M12 5v14M5 12h14" />
              </svg>
              绑定邮箱
            </button>
          </div>
        </div>

        <!-- 表格区域 -->
        <div class="table-container">
          <table class="email-table">
            <thead>
              <tr>
                <th>邮箱地址</th>
                <th>邮箱厂商</th>
                <th>授权码</th>
                <th>状态</th>
                <th>创建时间</th>
                <th>IMAP服务器</th>
                <th>SMTP服务器</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="isLoadingBindings">
                <td colspan="8" class="loading-row">
                  <div class="loading-spinner"></div>
                  <span>加载中...</span>
                </td>
              </tr>
              <tr v-else v-for="email in emailList" :key="email.id" class="table-row">
                <td class="email-col">{{ email.email_address }}</td>
                <td class="provider-col">
                  <span class="provider-badge">
                    {{ email.provider_display_name }}
                  </span>
                </td>
                <td class="authcode-col">
                  <div class="authcode-content">
                    <span class="auth-text" :class="{ 'auth-visible': email.showAuthCode }">{{ email.showAuthCode ? email.auth_code : maskAuthCode(email.auth_code) }}</span>
                    <button class="view-btn" title="查看" @click="toggleAuthCodeVisibility(email.id)">
                      <svg v-if="!email.showAuthCode" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                        <circle cx="12" cy="12" r="3" />
                      </svg>
                      <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                        <line x1="1" y1="1" x2="23" y2="23"/>
                      </svg>
                    </button>
                    <button class="copy-btn" title="复制授权码" @click="copyToClipboard(email.auth_code)">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
                      </svg>
                    </button>
                  </div>
                </td>
                <td class="status-col">
                  <label class="status-switch">
                    <input 
                      type="checkbox" 
                      :checked="email.is_active" 
                      @change="toggleBindingStatus(email.id, $event.target.checked)"
                      class="switch-input"
                    />
                    <span class="switch-slider">
                      <span class="switch-text">{{ email.is_active ? '启用' : '禁用' }}</span>
                    </span>
                  </label>
                </td>
                <td class="time-col">{{ formatDate(email.created_at) }}</td>
                <td class="imap-col">
                  <span class="imap-text">{{ email.imap_server }}</span>
                </td>
                <td class="smtp-col">
                  <span class="smtp-text">{{ email.smtp_server }}</span>
                </td>
                <td class="action-col">
                  <div class="action-content">
                    <button class="action-btn delete" @click="deleteBinding(email.id)">删除</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- 空状态 -->
          <div v-if="emailList.length === 0 && !isLoadingBindings" class="empty-state">
            <div class="empty-icon">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.89 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"
                />
              </svg>
            </div>
            <h4 class="empty-title">暂无绑定的邮箱</h4>
            <p class="empty-description">点击"绑定邮箱"按钮开始添加您的第一个邮箱</p>
          </div>
        </div>

        <!-- 分页 -->
        <div class="pagination">
          <span class="page-info">
            第 {{ getStartIndex() }} - {{ getEndIndex() }} 条，共 {{ pagination.total }} 条
          </span>
          <div class="page-controls">
            <button 
              class="page-btn" 
              :disabled="pagination.current_page <= 1"
              @click="changePage(pagination.current_page - 1)"
            >&lt;</button>
            <span class="current-page">{{ pagination.current_page }}</span>
            <button 
              class="page-btn" 
              :disabled="pagination.current_page >= pagination.total_pages"
              @click="changePage(pagination.current_page + 1)"
            >&gt;</button>

          </div>
        </div>
      </div>
    </div>

    <!-- 绑定邮箱弹窗 -->
    <Teleport to="body">
      <div v-if="showModal" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3 class="modal-title">绑定邮箱</h3>
            <button class="close-btn" @click="closeModal">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>

          <div class="modal-body">
            <form class="bind-form" @submit.prevent="handleBind">
              <!-- 邮箱类型选择 -->
              <div class="form-field">
                <label class="field-label">邮箱类型</label>
                <select v-model="bindForm.type" class="form-select" :disabled="isLoadingProviders" @change="validateEmail">
                  <option value="">{{ isLoadingProviders ? '加载中...' : '请选择邮箱类型' }}</option>
                  <option 
                    v-for="provider in emailProviders" 
                    :key="provider.id" 
                    :value="provider.name"
                  >
                    {{ provider.display_name }}
                  </option>
                </select>
                <div v-if="formErrors.type" class="field-error">{{ formErrors.type }}</div>
              </div>

              <!-- 邮箱地址 -->
              <div class="form-field">
                <label class="field-label">邮箱地址</label>
                <input
                  type="email"
                  v-model="bindForm.email"
                  placeholder="请输入邮箱地址"
                  class="form-input"
                  :class="{ 'error': formErrors.email }"
                  @blur="validateEmail"
                  @input="formErrors.email = ''"
                  required
                />
                <div v-if="formErrors.email" class="field-error">{{ formErrors.email }}</div>
              </div>

              <!-- 授权码 -->
              <div class="form-field">
                <label class="field-label">授权码</label>
                <input
                  type="password"
                  v-model="bindForm.authCode"
                  placeholder="请输入邮箱授权码"
                  class="form-input"
                  :class="{ 'error': formErrors.authCode }"
                  @input="formErrors.authCode = ''"
                  required
                />
                <div v-if="formErrors.authCode" class="field-error">{{ formErrors.authCode }}</div>
                <div class="field-hint">
                  <svg class="hint-icon" viewBox="0 0 24 24" fill="currentColor">
                    <path
                      d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"
                    />
                  </svg>
                  请到邮箱设置中开启SMTP服务并获取授权码
                </div>
              </div>
            </form>
          </div>

          <div class="modal-footer">
            <button type="button" class="cancel-btn" @click="closeModal">取消</button>
            <button type="submit" class="confirm-btn" @click="handleBind" :disabled="isBinding">
              <div v-if="isBinding" class="loading-spinner"></div>
              <span v-if="!isBinding">绑定</span>
              <span v-else>验证中...</span>
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- 确认对话框 -->
    <ConfirmDialog
      v-model:visible="showConfirmDialog"
      :title="confirmDialogData.title"
      :message="confirmDialogData.message"
      @confirm="handleConfirm"
      @cancel="handleCancel"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/utils/api'
import { showToast } from '@/utils/toast'
import ConfirmDialog from '@/components/ConfirmDialog.vue'

defineOptions({
  name: 'EmailBind',
})

// 响应式数据
const showModal = ref(false)
const isBinding = ref(false)
const isLoadingProviders = ref(false)

// 表单数据
const bindForm = ref({
  type: '',
  email: '',
  authCode: '',
})

// 表单验证错误
const formErrors = ref({
  email: '',
  authCode: '',
  type: ''
})

// 邮箱列表数据
const emailList = ref([])
const isLoadingBindings = ref(false)

// 分页数据
const pagination = ref({
  current_page: 1,
  per_page: 10,
  total: 0,
  total_pages: 0
})

// 确认对话框
const showConfirmDialog = ref(false)
const confirmDialogData = ref({
  title: '',
  message: '',
  onConfirm: null
})

// 邮件厂商列表
const emailProviders = ref([])

// 方法
const closeModal = () => {
  showModal.value = false
  bindForm.value = {
    type: '',
    email: '',
    authCode: '',
  }
  // 清空表单错误
  formErrors.value = {
    email: '',
    authCode: '',
    type: ''
  }
}

// 邮箱格式验证
const validateEmail = () => {
  const email = bindForm.value.email.trim()
  const selectedProvider = emailProviders.value.find(p => p.name === bindForm.value.type)
  
  if (!email) {
    formErrors.value.email = '请输入邮箱地址'
    return false
  }
  
  // 基本邮箱格式验证
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email)) {
    formErrors.value.email = '请输入有效的邮箱地址'
    return false
  }
  
  // 验证邮箱后缀是否匹配选中的厂商
  if (selectedProvider && selectedProvider.email_suffix) {
    if (!email.toLowerCase().endsWith(selectedProvider.email_suffix.toLowerCase())) {
      formErrors.value.email = `邮箱地址必须以 ${selectedProvider.email_suffix} 结尾`
      return false
    }
  }
  
  formErrors.value.email = ''
  return true
}

// 表单验证
const validateForm = () => {
  let isValid = true
  
  // 验证邮箱类型
  if (!bindForm.value.type) {
    formErrors.value.type = '请选择邮箱类型'
    isValid = false
  } else {
    formErrors.value.type = ''
  }
  
  // 验证邮箱地址
  if (!validateEmail()) {
    isValid = false
  }
  
  // 验证授权码
  if (!bindForm.value.authCode.trim()) {
    formErrors.value.authCode = '请输入授权码'
    isValid = false
  } else {
    formErrors.value.authCode = ''
  }
  
  return isValid
}

const handleBind = async () => {
  // 表单验证
  if (!validateForm()) {
    showToast({ message: '请检查输入信息', type: 'error' })
    return
  }

  isBinding.value = true

  try {
    // 获取选中的邮箱厂商
    const selectedProvider = emailProviders.value.find(p => p.name === bindForm.value.type)
    if (!selectedProvider) {
      showToast({ message: '请选择有效的邮箱厂商', type: 'error' })
      return
    }

    // 调用后端API进行邮箱绑定
    const response = await api.post('/email/bindings', {
      email: bindForm.value.email.trim().toLowerCase(),
      auth_code: bindForm.value.authCode.trim(),
      provider_id: selectedProvider.id
    })

    if (response.success) {
      showToast({ message: '邮箱绑定成功！', type: 'success' })
      closeModal()
      // 刷新邮箱列表
      await fetchEmailBindings()
    } else {
      const errorMessage = (response.message && typeof response.message === 'string') ? response.message : '绑定失败，请重试'
      showToast({ message: errorMessage, type: 'error' })
    }
  } catch (error) {
    console.error('绑定失败:', error)
    if (error.response && error.response.data && error.response.data.message && typeof error.response.data.message === 'string') {
      showToast({ message: error.response.data.message, type: 'error' })
    } else {
      showToast({ message: '网络错误，请重试', type: 'error' })
    }
  } finally {
    isBinding.value = false
  }
}

// 获取邮件厂商列表
const fetchEmailProviders = async () => {
  try {
    isLoadingProviders.value = true
    const response = await api.get('/email/providers')
    if (response.success) {
      emailProviders.value = response.data.providers || []
    } else {
      const errorMessage = (response.message && typeof response.message === 'string') ? response.message : '获取邮件厂商列表失败'
      showToast({ message: errorMessage, type: 'error' })
    }
  } catch (error) {
    console.error('获取邮件厂商列表失败:', error)
    showToast({ message: '获取邮件厂商列表失败', type: 'error' })
  } finally {
    isLoadingProviders.value = false
  }
}

// 获取用户邮箱绑定列表
const fetchEmailBindings = async (page = 1, perPage = pagination.value.per_page) => {
  try {
    isLoadingBindings.value = true
    const response = await api.get('/email/bindings', {
      params: {
        page: page,
        per_page: perPage
      }
    })
    if (response.success) {
      const bindings = response.data.bindings || []
      // 为每个绑定添加授权码可见性状态
      emailList.value = bindings.map(binding => ({
        ...binding,
        showAuthCode: false
      }))
      
      // 更新分页信息
      pagination.value = {
        current_page: response.data.current_page || 1,
        per_page: response.data.per_page || 20,
        total: response.data.total || 0,
        total_pages: response.data.total_pages || 0
      }
    } else {
      const errorMessage = (response.message && typeof response.message === 'string') ? response.message : '获取邮箱绑定列表失败'
      showToast({ message: errorMessage, type: 'error' })
    }
  } catch (error) {
    console.error('获取邮箱绑定列表失败:', error)
    showToast({ message: '获取邮箱绑定列表失败', type: 'error' })
  } finally {
    isLoadingBindings.value = false
  }
}

// 删除邮箱绑定
const deleteBinding = (bindingId) => {
  confirmDialogData.value = {
    title: '删除确认',
    message: '确定要删除这个邮箱绑定吗？删除后将无法恢复。',
    onConfirm: () => performDelete(bindingId)
  }
  showConfirmDialog.value = true
}

// 执行删除操作
const performDelete = async (bindingId) => {
  try {
    const response = await api.delete(`/email/bindings/${bindingId}`)
    if (response.success) {
      showToast({ message: '删除成功', type: 'success' })
      await fetchEmailBindings()
    } else {
      const errorMessage = (response.message && typeof response.message === 'string') ? response.message : '删除失败'
      showToast({ message: errorMessage, type: 'error' })
    }
  } catch (error) {
    console.error('删除失败:', error)
    showToast({ message: '删除失败，请重试', type: 'error' })
  }
}

// 切换邮箱绑定状态
const toggleBindingStatus = async (bindingId, isActive) => {
  try {
    const response = await api.put(`/email/bindings/${bindingId}/status`, {
      is_active: isActive
    })
    
    if (response.success) {
      showToast({ 
        message: isActive ? '邮箱已启用' : '邮箱已禁用', 
        type: 'success' 
      })
      // 更新本地数据
      const binding = emailList.value.find(email => email.id === bindingId)
      if (binding) {
        binding.is_active = isActive
      }
    } else {
      const errorMessage = (response.message && typeof response.message === 'string') ? response.message : '状态更新失败'
      showToast({ message: errorMessage, type: 'error' })
      // 恢复开关状态
      await fetchEmailBindings()
    }
  } catch (error) {
    console.error('状态更新失败:', error)
    showToast({ message: '状态更新失败，请重试', type: 'error' })
    // 恢复开关状态
    await fetchEmailBindings()
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchEmailProviders()
  fetchEmailBindings()
})

const getStatusText = (status) => {
  const statusMap = {
    active: '已启用',
    inactive: '未激活',
    expired: '已过期',
  }
  return statusMap[status] || '未知'
}

// 授权码掩码显示
const maskAuthCode = (authCode) => {
  if (!authCode) return ''
  if (authCode.length <= 4) return '*'.repeat(authCode.length)
  return (
    authCode.substring(0, 2) +
    '*'.repeat(authCode.length - 4) +
    authCode.substring(authCode.length - 2)
  )
}

// 复制到剪贴板
const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    showToast({ message: '复制成功', type: 'success' })
  } catch (error) {
    console.error('复制失败:', error)
    showToast({ message: '复制失败', type: 'error' })
  }
}

// 日期格式化
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 切换授权码可见性
const toggleAuthCodeVisibility = (emailId) => {
  const email = emailList.value.find(e => e.id === emailId)
  if (email) {
    email.showAuthCode = !email.showAuthCode
  }
}

// 分页相关方法
const getStartIndex = () => {
  if (pagination.value.total === 0) return 0
  return (pagination.value.current_page - 1) * pagination.value.per_page + 1
}

const getEndIndex = () => {
  const end = pagination.value.current_page * pagination.value.per_page
  return Math.min(end, pagination.value.total)
}

const changePage = async (page) => {
  if (page >= 1 && page <= pagination.value.total_pages) {
    await fetchEmailBindings(page, 10)
  }
}

// 确认对话框处理
const handleConfirm = () => {
  if (confirmDialogData.value.onConfirm) {
    confirmDialogData.value.onConfirm()
  }
}

const handleCancel = () => {
  // 取消操作，不需要额外处理
}
</script>

<style scoped>
.email-bind-page {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-sizing: border-box;
  position: relative;
}

.page-header {
  margin-bottom: 24px;
  padding: 24px 32px 0 32px;
  flex-shrink: 0;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 6px 0;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 16px;
  color: #6b7280;
  margin: 0;
  line-height: 1.5;
}

.bind-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  overflow: hidden;
  padding: 0 32px 32px 32px;
}

.bind-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  overflow: hidden;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

/* 卡片头部样式 */
.card-header {
  padding: 16px 20px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fafbfc;
}

/* 标签页样式 */
.tabs {
  display: flex;
  gap: 2px;
}

.tab-item {
  padding: 8px 16px;
  background: none;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-item.active {
  background: #3b82f6;
  color: white;
}

.tab-item:hover:not(.active) {
  background: #f3f4f6;
  color: #374151;
}

/* 头部操作区 */
.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.search-container {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 10px;
  width: 16px;
  height: 16px;
  color: #9ca3af;
  z-index: 1;
}

.search-input {
  padding: 8px 12px 8px 32px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  width: 200px;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-btn:hover {
  background: #2563eb;
}

.btn-icon {
  width: 16px;
  height: 16px;
}

/* 表格样式 */
.table-container {
  overflow-y: auto;
  overflow-x: auto;
  flex: 1;
  min-height: 0;
}

/* 自定义滚动条样式 */
.table-container::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.table-container::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.table-container::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.table-container::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.table-container {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 #f1f5f9;
}

.email-table {
  width: 100%;
  min-width: 1000px;
  border-collapse: collapse;
  font-size: 14px;
}

.email-table th,
.email-table td {
  padding: 12px 16px;
  text-align: center;
  border-bottom: 1px solid #f0f0f0;
  vertical-align: middle;
}

.email-table th {
  background: #fafbfc;
  font-weight: 600;
  color: #374151;
  font-size: 14px;
  font-family: 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', Arial, sans-serif;
}

.email-table td {
  font-size: 14px;
  font-family: 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', Arial, sans-serif;
  color: #374151;
}

.email-table tbody tr:hover {
  background: #f9fafb;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.active {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.inactive {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.expired {
  background: #fee2e2;
  color: #991b1b;
}

.group-tag {
  display: inline-block;
  padding: 2px 8px;
  background: #eff6ff;
  color: #1d4ed8;
  border-radius: 4px;
  font-size: 12px;
}

/* 邮箱地址列 */
.email-col {
  font-family: 'SF Mono', 'Monaco', 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
  font-size: 14px;
  color: #374151;
  font-weight: 500;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 邮箱厂商列 */
.provider-col {
  width: 120px;
}

.provider-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  color: #475569;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.provider-icon {
  width: 16px;
  height: 16px;
  border-radius: 2px;
}

/* 授权码列 */
.authcode-col {
  min-width: 150px;
}

.authcode-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
}

.auth-text {
  font-family: 'SF Mono', 'Monaco', 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
  background: #f9fafb;
  padding: 4px 8px;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.auth-text.auth-visible {
  background: #eff6ff;
  border-color: #3b82f6;
  color: #1d4ed8;
}

/* IMAP服务器列 */
.imap-col {
  max-width: 150px;
}

.imap-text {
  font-family: 'SF Mono', 'Monaco', 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: block;
}

/* SMTP服务器列 */
.smtp-col {
  max-width: 150px;
}

.smtp-text {
  font-family: 'SF Mono', 'Monaco', 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: block;
}

.action-col {
  min-width: 120px;
}

.action-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
}

.copy-btn,
.view-btn {
  padding: 4px;
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.copy-btn:hover,
.view-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.copy-btn svg,
.view-btn svg {
  width: 14px;
  height: 14px;
}

.action-btn {
  padding: 4px 8px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 12px;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: #f3f4f6;
}

.action-btn.delete {
  color: #dc2626;
  border-color: #fecaca;
}

.action-btn.delete:hover {
  background: #fef2f2;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-icon {
  width: 64px;
  height: 64px;
  background: #f3f4f6;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  margin-bottom: 16px;
}

.empty-icon svg {
  width: 32px;
  height: 32px;
}

.empty-title {
  font-size: 18px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 8px 0;
}

.empty-description {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

/* 分页样式 */
.pagination {
  padding: 16px 20px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fafbfc;
}

.page-info {
  font-size: 14px;
  color: #6b7280;
}

.page-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-btn {
  padding: 6px 10px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  background: white;
  color: #374151;
  cursor: pointer;
  font-size: 14px;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.current-page {
  padding: 6px 10px;
  font-weight: 600;
  color: #374151;
}

.page-size {
  padding: 6px 8px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  background: white;
  font-size: 14px;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  background: rgba(0, 0, 0, 0.5) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  z-index: 999999 !important;
  margin: 0 !important;
  padding: 0 !important;
  box-sizing: border-box !important;
  pointer-events: auto !important;
}

.modal-content {
  background: white !important;
  border-radius: 16px;
  width: 90%;
  max-width: 520px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(255, 255, 255, 0.05);
  position: relative;
  z-index: 1000000 !important;
  pointer-events: auto !important;
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header {
  padding: 24px 28px 20px 28px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #fafbfc 0%, #f8fafc 100%);
  border-radius: 16px 16px 0 0;
}

.modal-title {
  font-size: 20px;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
  letter-spacing: -0.025em;
}

.close-btn {
  padding: 8px;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(0, 0, 0, 0.05);
  color: #6b7280;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s ease;
  backdrop-filter: blur(4px);
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.95);
  color: #374151;
  border-color: rgba(0, 0, 0, 0.1);
  transform: scale(1.05);
}

.close-btn svg {
  width: 18px;
  height: 18px;
}

.modal-body {
  padding: 24px 28px;
  background: white;
}

.bind-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.field-label {
  font-size: 15px;
  font-weight: 600;
  color: #2d3748;
  letter-spacing: -0.01em;
}

.form-input {
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  background: white;
  transition: all 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input:hover {
  border-color: #9ca3af;
}

/* 自定义下拉选择框样式 */
.form-select {
  position: relative;
  padding: 12px 40px 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  background: white;
  background-image: url('data:image/svg+xml;charset=US-ASCII,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%236b7280" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6,9 12,15 18,9"></polyline></svg>');
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 16px;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.form-select:hover {
  border-color: #9ca3af;
  background-image: url('data:image/svg+xml;charset=US-ASCII,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%23374151" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6,9 12,15 18,9"></polyline></svg>');
}

.form-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  background-image: url('data:image/svg+xml;charset=US-ASCII,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%233b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6,9 12,15 18,9"></polyline></svg>');
}

.form-select:disabled {
  background-color: #f9fafb;
  color: #9ca3af;
  cursor: not-allowed;
  border-color: #e5e7eb;
  background-image: url('data:image/svg+xml;charset=US-ASCII,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%23d1d5db" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6,9 12,15 18,9"></polyline></svg>');
}

/* 下拉选项样式 */
.form-select option {
  padding: 8px 12px;
  background: white;
  color: #374151;
  font-size: 14px;
}

.form-select option:hover {
  background: #f3f4f6;
}

.form-select option:checked {
  background: #3b82f6;
  color: white;
  font-weight: 500;
}

.field-hint {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 13px;
  color: #718096;
  margin-top: 6px;
  padding: 8px 12px;
  background: #f7fafc;
  border-radius: 6px;
  border-left: 3px solid #4299e1;
}

.hint-icon {
  width: 16px;
  height: 16px;
  margin-top: 1px;
  flex-shrink: 0;
  color: #4299e1;
}

.modal-footer {
  padding: 20px 28px 24px 28px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  background: linear-gradient(135deg, #fafbfc 0%, #f8fafc 100%);
  border-radius: 0 0 16px 16px;
}

.cancel-btn {
  padding: 12px 20px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  color: #4a5568;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.cancel-btn:hover {
  background: #f7fafc;
  border-color: #cbd5e0;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.confirm-btn {
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
  color: white;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s ease;
  box-shadow: 0 4px 6px rgba(66, 153, 225, 0.3);
}

.confirm-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #3182ce 0%, #2c5aa0 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 8px rgba(66, 153, 225, 0.4);
}

.confirm-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* 表单错误样式 */
.field-error {
  color: #dc2626;
  font-size: 12px;
  margin-top: 4px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.form-input.error,
.form-select.error {
  border-color: #dc2626;
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

/* Loading 动画 */
.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #f3f4f6;
  border-top: 2px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  display: inline-block;
  margin-right: 8px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-row {
  text-align: center;
  padding: 40px 20px;
  color: #6b7280;
}

.loading-row .loading-spinner {
  width: 20px;
  height: 20px;
  margin-right: 12px;
}

.confirm-btn .loading-spinner {
  width: 14px;
  height: 14px;
  border-width: 1.5px;
  margin-right: 6px;
}

/* 切换开关样式 */
.status-switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 28px;
  cursor: pointer;
}

.switch-input {
  opacity: 0;
  width: 0;
  height: 0;
}

.switch-slider {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  border-radius: 14px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.switch-text {
  color: white;
  font-size: 11px;
  font-weight: 500;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  user-select: none;
}

.switch-input:checked + .switch-slider {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.switch-input:focus + .switch-slider {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1), 0 0 0 3px rgba(139, 92, 246, 0.2);
}

.status-switch:hover .switch-slider {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.status-switch:active .switch-slider {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header {
    padding: 16px 20px 0 20px;
  }

  .bind-content {
    padding: 0 20px 20px 20px;
  }

  .card-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
    justify-content: space-between;
  }

  .search-input {
    width: 150px;
  }

  .email-table {
    font-size: 12px;
  }

  .email-table th,
  .email-table td {
    padding: 8px 12px;
  }

  .modal-content {
    margin: 20px;
    width: calc(100% - 40px);
  }
}

@media (max-width: 480px) {
  .page-header {
    padding: 12px 16px 0 16px;
  }

  .bind-content {
    padding: 0 16px 16px 16px;
  }

  .tabs {
    flex-wrap: wrap;
  }

  .search-input {
    width: 120px;
  }

  .add-btn {
    padding: 8px 12px;
    font-size: 13px;
  }
}
</style>
