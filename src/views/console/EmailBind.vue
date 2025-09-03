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
            <button class="tab-item">智能邮件全网监</button>
            <button class="tab-item">删除的历史记录</button>
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
                <th class="checkbox-col">
                  <input type="checkbox" class="table-checkbox" />
                </th>
                <th>邮箱地址</th>
                <th>邮箱厂商</th>
                <th>授权码</th>
                <th>状态</th>
                <th>创建时间</th>
                <th>IMAP服务器</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="email in emailList" :key="email.id" class="table-row">
                <td class="checkbox-col">
                  <input type="checkbox" class="table-checkbox" />
                </td>
                <td class="email-col">{{ email.emailAddress }}</td>
                <td class="provider-col">
                  <span class="provider-badge">
                    <img
                      v-if="email.providerIcon"
                      :src="email.providerIcon"
                      :alt="email.provider"
                      class="provider-icon"
                    />
                    {{ email.provider }}
                  </span>
                </td>
                <td class="authcode-col">
                  <span class="auth-text">{{ maskAuthCode(email.authCode) }}</span>
                  <button class="view-btn" title="查看">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                      <circle cx="12" cy="12" r="3" />
                    </svg>
                  </button>
                  <button class="copy-btn" title="复制">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
                      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
                    </svg>
                  </button>
                </td>
                <td class="status-col">
                  <span class="status-badge" :class="email.status">{{
                    getStatusText(email.status)
                  }}</span>
                </td>
                <td class="time-col">{{ email.createTime }}</td>
                <td class="imap-col">
                  <span class="imap-text">{{ email.imapServer }}</span>
                </td>
                <td class="action-col">
                  <button class="action-btn">编辑</button>
                  <button class="action-btn delete">删除</button>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- 空状态 -->
          <div v-if="emailList.length === 0" class="empty-state">
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
          <span class="page-info">第 1 - 2 条，共 2 条</span>
          <div class="page-controls">
            <button class="page-btn" disabled>&lt;</button>
            <span class="current-page">1</span>
            <button class="page-btn" disabled>&gt;</button>
            <select class="page-size">
              <option value="20">每页条数: 20</option>
              <option value="50">每页条数: 50</option>
              <option value="100">每页条数: 100</option>
            </select>
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
                <select v-model="bindForm.type" class="form-select">
                  <option value="">请选择邮箱类型</option>
                  <option value="gmail">Gmail</option>
                  <option value="outlook">Outlook</option>
                  <option value="yahoo">Yahoo Mail</option>
                  <option value="qq">QQ邮箱</option>
                  <option value="163">163邮箱</option>
                  <option value="126">126邮箱</option>
                  <option value="other">其他</option>
                </select>
              </div>

              <!-- 邮箱地址 -->
              <div class="form-field">
                <label class="field-label">邮箱地址</label>
                <input
                  type="email"
                  v-model="bindForm.email"
                  placeholder="请输入邮箱地址"
                  class="form-input"
                  required
                />
              </div>

              <!-- 授权码 -->
              <div class="form-field">
                <label class="field-label">授权码</label>
                <input
                  type="password"
                  v-model="bindForm.authCode"
                  placeholder="请输入邮箱授权码"
                  class="form-input"
                  required
                />
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
              <span v-if="!isBinding">绑定</span>
              <span v-else>绑定中...</span>
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineOptions({
  name: 'EmailBind',
})

// 响应式数据
const showModal = ref(false)
const isBinding = ref(false)

// 表单数据
const bindForm = ref({
  type: '',
  email: '',
  authCode: '',
})

// 邮箱列表数据（示例数据）
const emailList = ref([])

// 方法
const closeModal = () => {
  showModal.value = false
  bindForm.value = {
    type: '',
    email: '',
    authCode: '',
  }
}

const handleBind = async () => {
  if (!bindForm.value.type || !bindForm.value.email || !bindForm.value.authCode) {
    alert('请填写完整的绑定信息')
    return
  }

  isBinding.value = true

  try {
    // 这里添加绑定逻辑
    console.log('绑定邮箱:', bindForm.value)

    // 模拟API调用
    await new Promise((resolve) => setTimeout(resolve, 1500))

    alert('邮箱绑定成功！')
    closeModal()
  } catch (error) {
    console.error('绑定失败:', error)
    alert('绑定失败，请重试')
  } finally {
    isBinding.value = false
  }
}

const getStatusText = (status) => {
  const statusMap = {
    active: '已启用',
    inactive: '未激活',
    expired: '已过期',
  }
  return statusMap[status] || '未知'
}

// 授权码掉码显示
const maskAuthCode = (authCode) => {
  if (!authCode) return ''
  if (authCode.length <= 4) return '*'.repeat(authCode.length)
  return (
    authCode.substring(0, 2) +
    '*'.repeat(authCode.length - 4) +
    authCode.substring(authCode.length - 2)
  )
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

/* 隐藏滚动条 */
.table-container::-webkit-scrollbar {
  display: none;
}

.table-container {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.email-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.email-table th,
.email-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
}

.email-table th {
  background: #fafbfc;
  font-weight: 600;
  color: #374151;
  font-size: 13px;
}

.email-table tbody tr:hover {
  background: #f9fafb;
}

.checkbox-col {
  width: 40px;
}

.table-checkbox {
  width: 16px;
  height: 16px;
  cursor: pointer;
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
  font-family: monospace;
  font-size: 13px;
  color: #374151;
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
  padding: 4px 8px;
  background: #f3f4f6;
  border-radius: 6px;
  font-size: 12px;
  color: #374151;
}

.provider-icon {
  width: 16px;
  height: 16px;
  border-radius: 2px;
}

/* 授权码列 */
.authcode-col {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 150px;
}

.auth-text {
  font-family: monospace;
  font-size: 12px;
  color: #6b7280;
  background: #f9fafb;
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid #e5e7eb;
}

/* IMAP服务器列 */
.imap-col {
  max-width: 150px;
}

.imap-text {
  font-family: monospace;
  font-size: 12px;
  color: #6b7280;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: block;
}

.action-col {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 120px;
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
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1000000 !important;
  pointer-events: auto !important;
}

.modal-header {
  padding: 20px 24px 16px 24px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-title {
  font-size: 18px;
  font-weight: 600;
  color: #1c1f23;
  margin: 0;
}

.close-btn {
  padding: 4px;
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.close-btn svg {
  width: 20px;
  height: 20px;
}

.modal-body {
  padding: 20px 24px;
}

.bind-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field-label {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.form-input,
.form-select {
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.2s ease;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.field-hint {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  font-size: 12px;
  color: #6b7280;
  margin-top: 4px;
}

.hint-icon {
  width: 14px;
  height: 14px;
  margin-top: 1px;
  flex-shrink: 0;
}

.modal-footer {
  padding: 16px 24px 20px 24px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.cancel-btn {
  padding: 8px 16px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  color: #374151;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;
}

.cancel-btn:hover {
  background: #f3f4f6;
}

.confirm-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  background: #3b82f6;
  color: white;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;
}

.confirm-btn:hover:not(:disabled) {
  background: #2563eb;
}

.confirm-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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
