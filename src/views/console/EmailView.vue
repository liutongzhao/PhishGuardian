<template>
  <div class="email-view-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">邮件查看</h1>
        <p class="page-subtitle">智能监控和分析您绑定邮箱中的所有邮件</p>
      </div>
      <div class="header-actions">
        <button class="refresh-btn">
          <svg
            class="btn-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M23 4v6h-6M1 20v-6h6M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"
            />
          </svg>
          刷新邮件
        </button>
      </div>
    </div>

    <!-- 筛选和统计区域 -->
    <div class="filter-section">
      <!-- 统计卡片 -->
      <div class="stats-overview">
        <div class="stat-item">
          <div class="stat-number">156</div>
          <div class="stat-label">总邮件</div>
        </div>
        <div class="stat-item danger">
          <div class="stat-number">3</div>
          <div class="stat-label">钓鱼邮件</div>
        </div>
        <div class="stat-item warning">
          <div class="stat-number">12</div>
          <div class="stat-label">可疑邮件</div>
        </div>
        <div class="stat-item success">
          <div class="stat-number">141</div>
          <div class="stat-label">安全邮件</div>
        </div>
      </div>

      <!-- 工具栏：筛选器 + 排序 + 视图切换 -->
      <div class="toolbar">
        <!-- 筛选器组 -->
        <div class="filters-group">
          <div class="filter-item">
            <label class="filter-label">具体邮箱</label>
            <select class="filter-select" v-model="filterEmail">
              <option value="">全部邮箱</option>
              <option value="user@gmail.com">user@gmail.com</option>
              <option value="business@outlook.com">business@outlook.com</option>
              <option value="support@company.cn">support@company.cn</option>
              <option value="admin@qq.com">admin@qq.com</option>
            </select>
          </div>
          <div class="filter-item">
            <label class="filter-label">邮箱厂商</label>
            <select class="filter-select" v-model="filterProvider">
              <option value="">全部</option>
              <option value="gmail">Gmail</option>
              <option value="outlook">Outlook</option>
              <option value="yahoo">Yahoo</option>
              <option value="qq">QQ邮箱</option>
              <option value="163">163邮箱</option>
            </select>
          </div>
          <div class="filter-item">
            <label class="filter-label">安全状态</label>
            <select class="filter-select" v-model="filterStatus">
              <option value="">全部</option>
              <option value="safe">安全</option>
              <option value="suspicious">可疑</option>
              <option value="phishing">钓鱼</option>
            </select>
          </div>
          <div class="filter-item">
            <label class="filter-label">重要程度</label>
            <select class="filter-select" v-model="filterImportance">
              <option value="">全部</option>
              <option value="high">高</option>
              <option value="medium">中</option>
              <option value="low">低</option>
            </select>
          </div>
          <div class="filter-item">
            <label class="filter-label">紧急程度</label>
            <select class="filter-select" v-model="filterUrgency">
              <option value="">全部</option>
              <option value="urgent">紧急</option>
              <option value="normal">普通</option>
            </select>
          </div>
        </div>

        <!-- 排序、视图和尺寸控制组 -->
        <div class="controls-group">
          <!-- 排序控制 -->
          <div class="sort-controls">
            <label class="control-label">排序</label>
            <div class="sort-wrapper">
              <select class="sort-select" v-model="sortBy" @change="handleSort">
                <option value="time">时间</option>
                <option value="importance">重要程度</option>
                <option value="urgency">紧急程度</option>
                <option value="sender">发件人</option>
                <option value="subject">邮件主题</option>
                <option value="status">安全状态</option>
              </select>
              <button
                class="sort-order-btn"
                @click="toggleSortOrder"
                :class="{ desc: sortOrder === 'desc' }"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M7 10l5 5 5-5" v-if="sortOrder === 'asc'" />
                  <path d="M7 14l5-5 5 5" v-else />
                </svg>
              </button>
            </div>
          </div>

          <!-- 显示大小控制（只在网格视图显示） -->
          <div class="size-controls" v-show="viewMode === 'grid'">
            <label class="control-label">显示大小</label>
            <select class="size-select" v-model="cardSize" @change="updateCardSize">
              <option value="compact">紧凑</option>
              <option value="normal">正常</option>
              <option value="large">大</option>
            </select>
          </div>

          <!-- 视图切换 -->
          <div class="view-toggle">
            <label class="control-label">视图</label>
            <div class="toggle-buttons">
              <button
                class="toggle-btn"
                :class="{ active: viewMode === 'grid' }"
                @click="setViewMode('grid')"
                title="网格视图"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="7" height="7" />
                  <rect x="14" y="3" width="7" height="7" />
                  <rect x="3" y="14" width="7" height="7" />
                  <rect x="14" y="14" width="7" height="7" />
                </svg>
              </button>
              <button
                class="toggle-btn"
                :class="{ active: viewMode === 'list' }"
                @click="setViewMode('list')"
                title="列表视图"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="8" y1="6" x2="21" y2="6" />
                  <line x1="8" y1="12" x2="21" y2="12" />
                  <line x1="8" y1="18" x2="21" y2="18" />
                  <line x1="3" y1="6" x2="3.01" y2="6" />
                  <line x1="3" y1="12" x2="3.01" y2="12" />
                  <line x1="3" y1="18" x2="3.01" y2="18" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 邮件列表容器 -->
      <div class="email-list-container">
        <!-- 网格布局容器 -->
        <div class="email-grid" :class="[`size-${cardSize}`, `view-${viewMode}`]">
          <!-- 邮件卡片循环渲染 -->
          <div
            v-for="email in emailList"
            :key="email.id"
            class="email-card"
            :class="email.status"
            @click="viewEmailDetail(email.id)"
          >
            <!-- 卡片头部 -->
            <div class="card-header">
              <div class="provider-logo">
                <div class="provider-icon" :class="email.provider">
                  <svg v-if="email.provider === 'gmail'" viewBox="0 0 24 24" fill="currentColor">
                    <path
                      d="M24 5.457v13.909c0 .904-.732 1.636-1.636 1.636h-3.819V11.73L12 16.64l-6.545-4.91v9.273H1.636A1.636 1.636 0 0 1 0 19.366V5.457c0-2.023 2.309-3.178 3.927-1.964L5.5 4.64 12 9.548l6.5-4.909 1.573-1.147C21.69 2.28 24 3.434 24 5.457z"
                    />
                  </svg>
                  <svg
                    v-else-if="email.provider === 'outlook'"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path
                      d="M7.462 0C3.316 0 0 3.247 0 7.302c0 4.056 3.316 7.302 7.462 7.302 4.147 0 7.463-3.246 7.463-7.302C14.925 3.247 11.609 0 7.462 0zM24 4.781v14.438c0 .431-.349.781-.781.781H15.61V4.781H24z"
                    />
                  </svg>
                  <svg v-else-if="email.provider === 'qq'" viewBox="0 0 24 24" fill="currentColor">
                    <path
                      d="M21.395 15.035a39.67 39.67 0 0 0-.803-2.264l-1.079-2.695c.001-.032.014-.562.014-.836C19.526 4.632 16.565 0 12.41 0c-4.157 0-7.118 4.632-7.118 9.24 0 .274.013.804.014.836l-1.08 2.695a39.67 39.67 0 0 0-.802 2.264c-.535 2.184-.527 3.347.072 3.956.72.73 2.454.577 4.460-.613.384.737.835 1.41 1.328 1.996.675.802 1.33 1.293 1.925 1.545.595-.252 1.25-.743 1.925-1.545.493-.586.944-1.259 1.328-1.996 2.006 1.19 3.74 1.343 4.46.613.599-.609.607-1.772.072-3.956z"
                    />
                  </svg>
                  <svg
                    v-else-if="email.provider === 'apple'"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path
                      d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"
                    />
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="currentColor">
                    <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z" />
                  </svg>
                </div>
                <div class="email-address">{{ email.senderEmail }}</div>
              </div>

              <div class="status-indicators">
                <div class="status-badge security" :class="email.status">
                  <svg
                    v-if="email.status === 'safe'"
                    class="status-icon"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <svg
                    v-else
                    class="status-icon"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <circle cx="12" cy="12" r="10" />
                    <line x1="12" y1="8" x2="12" y2="12" />
                    <line x1="12" y1="16" x2="12.01" y2="16" />
                  </svg>
                </div>
                <div v-if="email.urgency === 'urgent'" class="status-badge urgency urgent">
                  <svg
                    class="status-icon"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <circle cx="12" cy="12" r="10" />
                    <line x1="12" y1="8" x2="12" y2="12" />
                    <line x1="12" y1="16" x2="12.01" y2="16" />
                  </svg>
                </div>
              </div>
            </div>

            <div class="card-body">
              <div class="email-content">
                <div class="sender-email">发件人：{{ email.senderEmail }}</div>
                <h3 class="email-subject">{{ email.subject }}</h3>
                <p
                  class="email-preview"
                  :class="{ 'has-tooltip': shouldShowPreviewTooltip(email.preview) }"
                  :title="shouldShowPreviewTooltip(email.preview) ? email.preview : null"
                >
                  {{ email.preview }}
                </p>
              </div>

              <div class="card-footer">
                <div class="priority-tags">
                  <span class="priority-tag importance" :class="email.importance">
                    {{ getImportanceText(email.importance) }}
                  </span>
                  <span v-if="email.urgency === 'urgent'" class="priority-tag urgency urgent"
                    >紧急</span
                  >
                  <span class="priority-tag time">{{ email.time }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 分页容器 -->
      <div class="pagination-container">
        <div class="pagination">
          <div class="pagination-info">
            <span class="info-text"
              >显示 <strong>1-10</strong> 条，共 <strong>156</strong> 条邮件</span
            >
          </div>
          <div class="pagination-controls">
            <button class="page-btn prev-btn" disabled>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="15,18 9,12 15,6" />
              </svg>
              <span>上一页</span>
            </button>

            <div class="page-numbers">
              <button class="page-number active">1</button>
              <button class="page-number">2</button>
              <button class="page-number">3</button>
              <button class="page-number">4</button>
              <button class="page-number">5</button>
              <span class="page-dots">...</span>
              <button class="page-number">16</button>
            </div>

            <button class="page-btn next-btn">
              <span>下一页</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="9,18 15,12 9,6" />
              </svg>
            </button>
          </div>

          <div class="page-size-selector">
            <span class="selector-label">每页显示</span>
            <select class="page-size-select" v-model="pageSize">
              <option value="10">10 条</option>
              <option value="20">20 条</option>
              <option value="50">50 条</option>
              <option value="100">100 条</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- 邮件详情弹窗 -->
    <Teleport to="body">
      <div v-if="showEmailDetail" class="email-detail-modal" @click.self="closeEmailDetail">
        <div class="modal-content">
          <div class="modal-header">
            <h2 class="modal-title">邮件详情</h2>
            <button class="close-btn" @click="closeEmailDetail">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          <div class="modal-body" v-if="currentEmail">
            <!-- 邮件基本信息 -->
            <div class="email-basic-info">
              <div class="info-row">
                <span class="info-label">发件人：</span>
                <span class="info-value"
                  >{{ currentEmail.sender }} ({{ currentEmail.senderEmail }})</span
                >
              </div>
              <div class="info-row">
                <span class="info-label">邮件主题：</span>
                <span class="info-value">{{ currentEmail.subject }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">时间：</span>
                <span class="info-value">{{ currentEmail.time }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">安全状态：</span>
                <span class="info-value" :class="`status-${currentEmail.status}`">
                  {{
                    currentEmail.status === 'safe'
                      ? '安全'
                      : currentEmail.status === 'suspicious'
                        ? '可疑'
                        : currentEmail.status === 'phishing'
                          ? '钓鱼'
                          : '未知'
                  }}
                </span>
              </div>
              <div class="info-row">
                <span class="info-label">重要程度：</span>
                <span class="info-value" :class="`importance-${currentEmail.importance}`">
                  {{
                    currentEmail.importance === 'high'
                      ? '高'
                      : currentEmail.importance === 'medium'
                        ? '中'
                        : '低'
                  }}
                </span>
              </div>
              <div class="info-row">
                <span class="info-label">紧急程度：</span>
                <span class="info-value" :class="`urgency-${currentEmail.urgency}`">
                  {{ currentEmail.urgency === 'urgent' ? '紧急' : '普通' }}
                </span>
              </div>
            </div>

            <!-- 邮件内容 -->
            <div class="email-detail-content">
              <h3 class="content-title">邮件内容：</h3>
              <div class="content-body" v-html="currentEmail.content"></div>
            </div>

            <!-- 安全警告（仅钓鱼邮件显示） -->
            <div v-if="currentEmail.status === 'phishing'" class="security-warning">
              <div class="warning-header">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path
                    d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"
                  ></path>
                  <line x1="12" y1="9" x2="12" y2="13"></line>
                  <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
                <span>安全警告</span>
              </div>
              <p>该邮件已被识别为钓鱼邮件，请务必不要点击任何链接或下载附件！</p>
              <ul>
                <li>不要提供任何个人信息</li>
                <li>不要输入密码或账户信息</li>
                <li>建议直接删除此邮件</li>
              </ul>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn-secondary" @click="closeEmailDetail">关闭</button>
            <button v-if="currentEmail?.status === 'phishing'" class="btn-danger">举报钓鱼</button>
            <button v-else class="btn-primary">标记为已读</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineOptions({
  name: 'EmailView',
})

// 响应式数据
const cardSize = ref('normal') // compact, normal, large
const pageSize = ref('20')
const viewMode = ref('grid') // grid, list
const sortBy = ref('time') // time, importance, urgency, sender, subject, status
const sortOrder = ref('desc') // asc, desc

// 筛选数据
const filterEmail = ref('') // 新增具体邮箱筛选
const filterProvider = ref('')
const filterStatus = ref('')
const filterImportance = ref('')
const filterUrgency = ref('')

// 邮件详情弹窗状态
const showEmailDetail = ref(false)
const currentEmail = ref(null)

// 模拟邮件列表数据
const emailList = ref([
  {
    id: 1,
    sender: 'Google Security',
    senderEmail: 'security@google.com',
    subject: 'Google账户安全提醒',
    preview:
      '检测到新的登录活动，如果是您本人操作请忽略此邮件，如果不是请立即更改密码并启用两步验证保护您的账户安全。我们建议您定期检查账户活动并保持密码的复杂性。',
    content:
      '亲爱的用户，<br><br>我们检测到您的Google账户在以下时间和地点有新的登录活动：<br><br>时间：2024年12月30日 14:32<br>地点：上海，中国<br>设备：Windows 11 - Chrome浏览器<br><br>如果这是您的操作，您可以忽略此邮件。如果不是，请立即采取以下措施：<br><br>1. 立即更改您的密码<br>2. 启用两步验证<br>3. 检查您的账户活动<br><br>谢谢，<br>Google安全团队',
    time: '2024年12月30日',
    status: 'safe',
    importance: 'medium',
    urgency: 'normal',
    provider: 'gmail',
    providerName: 'Gmail邮箱',
  },
  {
    id: 2,
    sender: 'PayPal Service',
    senderEmail: 'noreply@paypal-security.net',
    subject: '【紧急】PayPal账户已被限制',
    preview:
      '由于安全原因，您的账户已被暂时限制，请立即验证身份。点击链接恢复账户访问权限，否则将永久停用您的账户。请在24小时内完成验证，超过时间将无法恢复。',
    content:
      '亲爱的PayPal用户，<br><br>我们检测到您的账户存在异常活动，为了保护您的资金安全，我们已暂时限制您的账户。<br><br>请立即点击以下链接验证您的身份：<br><br><a href="#" style="color: red;">立即验证账户</a><br><br>如果您不在24小时内完成验证，您的账户将被永久停用。<br><br>PayPal安全团队',
    time: '2024年12月30日',
    status: 'phishing',
    importance: 'high',
    urgency: 'urgent',
    provider: 'suspicious',
    providerName: '可疑邮箱',
  },
  {
    id: 3,
    sender: 'Microsoft Rewards',
    senderEmail: 'rewards@micr0soft.com',
    subject: '恭喜！获得1000美元奖励',
    preview:
      '您已被选中获得Microsoft Rewards特别奖励，请在24小时内领取。请点击以下链接完成身份验证并领取您的奖励。此奖励只对特定用户开放，请勿错过机会。',
    content:
      '恭喜您！<br><br>您已被选中参与Microsoft Rewards特别活动，可获得价值1000美元的奖励！<br><br>请在24小时内点击以下链接领取：<br><br><a href="#">立即领取奖励</a><br><br>此活动仅限受邀用户，请勿错过这个难得的机会。<br><br>Microsoft团队',
    time: '2024年12月29日',
    status: 'suspicious',
    importance: 'medium',
    urgency: 'urgent',
    provider: 'outlook',
    providerName: 'Outlook邮箱',
  },
  {
    id: 4,
    sender: '腾讯云',
    senderEmail: 'service@qcloud.com',
    subject: '云服务器即将到期提醒',
    preview:
      '您购买的云服务器将于7天后到期，请及时续费以免影响业务运行。我们为您提供了多种续费方案，请登录控制台查看详情。',
    content:
      '尊敬的腾讯云用户：<br><br>您好！您购买的云服务器实例即将到期：<br><br>实例ID：cvm-abc123<br>到期时间：2025年1月7日<br>配置：2核4G CentOS 7.6<br><br>为避免业务中断，请及时续费。我们为您推荐以下续费方案：<br><br>1. 月付：￥168/月<br>2. 年付：￥1680/年（享8.3折优惠）<br><br>腾讯云团队',
    time: '2024年12月27日',
    status: 'safe',
    importance: 'high',
    urgency: 'normal',
    provider: 'qq',
    providerName: 'QQ邮箱',
  },
  {
    id: 5,
    sender: 'GitHub',
    senderEmail: 'noreply@github.com',
    subject: '新的Pull Request',
    preview:
      '用户 john-doe 向您的仓库 awesome-project 提交了一个新的PR，请及时review。该PR包含了新功能的实现和相关测试用例。',
    content:
      '您好！<br><br>用户 john-doe 向您的仓库提交了一个新的Pull Request：<br><br>仓库：awesome-project<br>分支：feature/user-authentication<br>描述：添加用户认证功能<br><br>更改内容：<br>- 添加登录/注册页面<br>- 实现JWT认证<br>- 添加用户权限管理<br>- 更新相关测试<br><br>请及时进行代码审查。<br><br>GitHub团队',
    time: '2024年12月23日',
    status: 'safe',
    importance: 'low',
    urgency: 'normal',
    provider: 'gmail',
    providerName: 'Gmail邮箱',
  },
  {
    id: 6,
    sender: 'Apple',
    senderEmail: 'no_reply@apple.com',
    subject: 'App Store购买确认',
    preview:
      '您已成功购买 Adobe Photoshop，感谢您的使用。购买金额：￥148.00，订单号：MX12345678。如有问题请联系客服。',
    content:
      '感谢您的购买！<br><br>购买详情：<br><br>应用名称：Adobe Photoshop<br>购买时间：2024年12月16日<br>金额：￥148.00<br>订单号：MX12345678<br>付款方式：******1234<br><br>您可以在所有已登录相同Apple ID的设备上下载和使用此应用。<br><br>如有疑问，请联系Apple客服。<br><br>Apple团队',
    time: '2024年12月16日',
    status: 'safe',
    importance: 'low',
    urgency: 'normal',
    provider: 'apple',
    providerName: 'Apple邮箱',
  },
])

// 更新卡片大小
const updateCardSize = () => {
  console.log('切换卡片大小:', cardSize.value)
}

// 设置视图模式
const setViewMode = (mode) => {
  viewMode.value = mode
  console.log('切换视图模式:', mode)
}

// 切换排序顺序
const toggleSortOrder = () => {
  sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  handleSort()
}

// 处理排序
const handleSort = () => {
  console.log('排序方式:', sortBy.value, '排序顺序:', sortOrder.value)
  // 这里可以添加实际的排序逻辑
}

// 点击邮件查看详情
const viewEmailDetail = (emailId) => {
  currentEmail.value = emailList.value.find((email) => email.id === emailId)
  if (currentEmail.value) {
    showEmailDetail.value = true
  } else {
    console.log('邮件数据不存在:', emailId)
  }
}

// 关闭邮件详情弹窗
const closeEmailDetail = () => {
  showEmailDetail.value = false
  currentEmail.value = null
}

// 辅助方法：获取重要程度显示文本
const getImportanceText = (importance) => {
  const textMap = {
    high: '高',
    medium: '中',
    low: '低',
  }
  return textMap[importance] || '-'
}

// 辅助方法：判断是否需要显示预览悬浮提示
const shouldShowPreviewTooltip = (previewText) => {
  if (!previewText) return false
  // 如果文本长度超过120个字符，则显示悬浮提示
  return previewText.length > 120
}
</script>

<style scoped>
.email-view-page {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 24px 32px;
  box-sizing: border-box;
  /* 移除 overflow: hidden 和 height: 100%，允许整个页面滚动 */
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
  flex-shrink: 0;
}

.header-left {
  flex: 1;
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

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

/* 显示大小控制 */
.size-controls {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.size-select {
  padding: 6px 10px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  font-size: 13px;
  color: #374151;
  transition: all 0.2s ease;
  cursor: pointer;
  min-width: 70px;
}

.size-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

/* 新设计的卡片头部布局 */
.provider-logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.email-address {
  font-size: 12px;
  color: #4f46e5;
  font-family:
    'Inter',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    system-ui,
    sans-serif;
  font-weight: 600;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 150px;
  padding: 2px 6px;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border-radius: 6px;
  border: 1px solid #bae6fd;
  transition: all 0.2s ease;
  cursor: default;
}

.status-indicators {
  display: flex;
  align-items: center;
  gap: 6px;
}

/* 新的状态徽章样式 */
.status-badge {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  cursor: default;
  transition: all 0.2s ease;
}

.status-badge.security.safe {
  background: linear-gradient(135deg, #22c55e 0%, #059669 100%);
  color: white;
}

.status-badge.security.suspicious {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.status-badge.security.phishing {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
  color: white;
}

.status-badge.urgency.urgent {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
}

.status-badge.urgency.normal {
  background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
  color: white;
}

.status-badge .status-icon {
  width: 12px;
  height: 12px;
  stroke-width: 2.5;
}

/* 邮件内容区域重新设计 */
.email-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.email-content .sender-email {
  font-size: 13px;
  color: #1e40af;
  font-family:
    'Inter',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    system-ui,
    sans-serif;
  font-weight: 600;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  padding: 4px 8px;
  border-radius: 6px;
  border: 1px solid #bfdbfe;
  display: block;
  text-align: center;
  transition: all 0.2s ease;
  cursor: default;
  margin: 0 auto;
  width: fit-content;
}

.email-content .email-subject {
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.email-content .email-preview {
  color: #6b7280;
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
  cursor: default;
  transition: all 0.2s ease;
  word-break: break-word;
}

.email-content .email-preview:hover {
  color: #374151;
}

.email-content .email-preview.has-tooltip {
  cursor: help;
}

.email-content .email-preview.has-tooltip:hover {
  color: #1e40af;
  background: linear-gradient(135deg, #fefbff 0%, #f8fafc 100%);
  padding: 2px 4px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

/* 全局悬浮提示美化样式 */
[title]:not([title='']) {
  position: relative;
}

[title]:not([title='']):hover::after {
  content: attr(title);
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
  color: white;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
  z-index: 1000;
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: tooltipFadeIn 0.2s ease-out;
  max-width: 300px;
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.4;
}

[title]:not([title='']):hover::before {
  content: '';
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%) translateY(2px);
  width: 0;
  height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-top: 6px solid #374151;
  z-index: 1001;
  animation: tooltipFadeIn 0.2s ease-out;
}

@keyframes tooltipFadeIn {
  0% {
    opacity: 0;
    transform: translateX(-50%) translateY(-4px);
  }
  100% {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

/* 邮件详情弹窗样式 */
.email-detail-modal {
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
  padding: 20px !important;
  box-sizing: border-box !important;
  pointer-events: auto !important;
}

.modal-content {
  background: white !important;
  border-radius: 12px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow:
    0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
  position: relative;
  z-index: 1000000 !important;
  pointer-events: auto !important;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.modal-title {
  font-size: 20px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
}

.close-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  cursor: pointer;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.close-btn svg {
  width: 16px;
  height: 16px;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.email-basic-info {
  background: #f8fafc;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
}

.info-row {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.info-row:last-child {
  margin-bottom: 0;
}

.info-label {
  font-weight: 600;
  color: #374151;
  min-width: 80px;
  font-size: 14px;
}

.info-value {
  color: #1a1a1a;
  font-size: 14px;
}

.info-value.status-safe {
  color: #059669;
  font-weight: 600;
}

.info-value.status-suspicious {
  color: #d97706;
  font-weight: 600;
}

.info-value.status-phishing {
  color: #dc2626;
  font-weight: 600;
}

.info-value.importance-high {
  color: #dc2626;
  font-weight: 600;
}

.info-value.importance-medium {
  color: #d97706;
  font-weight: 600;
}

.info-value.importance-low {
  color: #6b7280;
  font-weight: 600;
}

.info-value.urgency-urgent {
  color: #7c3aed;
  font-weight: 600;
}

.info-value.urgency-normal {
  color: #06b6d4;
  font-weight: 600;
}

.email-detail-content {
  margin-bottom: 20px;
}

.content-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 12px 0;
}

.content-body {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  line-height: 1.6;
  color: #374151;
}

.security-warning {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  border: 1px solid #fca5a5;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
}

.warning-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  color: #dc2626;
  font-weight: 700;
  font-size: 16px;
}

.warning-header svg {
  width: 20px;
  height: 20px;
}

.security-warning p {
  color: #991b1b;
  margin: 0 0 12px 0;
  font-weight: 600;
}

.security-warning ul {
  color: #991b1b;
  margin: 0;
  padding-left: 20px;
}

.security-warning li {
  margin-bottom: 4px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid #e5e7eb;
  background: #f8fafc;
}

.btn-primary,
.btn-secondary,
.btn-danger {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-secondary:hover {
  background: #e5e7eb;
  color: #1a1a1a;
}

.btn-danger {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
  color: white;
}

.btn-danger:hover {
  background: linear-gradient(135deg, #b91c1c 0%, #991b1b 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
}

/* 重新设计的邮箱信息布局 */
.email-info {
  margin-bottom: 12px;
}

.email-info .sender-name {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.email-info .sender-email {
  font-size: 11px;
  color: #6b7280;
  font-family: 'SF Mono', 'Monaco', monospace;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 新的底部标签容器 */
.card-footer {
  margin-top: auto;
}

.priority-tags {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

/* 新的优先级标签样式 */
.priority-tag {
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 3px;
  transition: all 0.2s ease;
  cursor: default;
}

.priority-tag.importance.high {
  background: linear-gradient(135deg, #fee2e2 0%, #fca5a5 100%);
  color: #991b1b;
  border: 1px solid #fca5a5;
}

.priority-tag.importance.medium {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
  border: 1px solid #fde68a;
}

.priority-tag.importance.low {
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  color: #6b7280;
  border: 1px solid #e5e7eb;
}

.priority-tag.urgency.urgent {
  background: linear-gradient(135deg, #ddd6fe 0%, #c4b5fd 100%);
  color: #6b21a8;
  border: 1px solid #c4b5fd;
}

.priority-tag.urgency.normal {
  background: linear-gradient(135deg, #e0f2fe 0%, #b3e5fc 100%);
  color: #0277bd;
  border: 1px solid #b3e5fc;
}

.priority-tag.time {
  background: linear-gradient(135deg, #f0fdf4 0%, #bbf7d0 100%);
  color: #065f46;
  border: 1px solid #bbf7d0;
  margin-left: auto;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
}

.refresh-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
}

.btn-icon {
  width: 16px;
  height: 16px;
}

/* 筛选和统计区域 */
.filter-section {
  margin-bottom: 24px;
  flex-shrink: 0;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-item {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  transition: all 0.2s ease;
}

.stat-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.stat-item.danger {
  background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
  border-color: #fca5a5;
}

.stat-item.warning {
  background: linear-gradient(135deg, #fffbeb 0%, #fde68a 100%);
  border-color: #f59e0b;
}

.stat-item.success {
  background: linear-gradient(135deg, #f0fdf4 0%, #bbf7d0 100%);
  border-color: #22c55e;
}

.stat-number {
  font-size: 32px;
  font-weight: 800;
  color: #1a1a1a;
  margin-bottom: 4px;
  line-height: 1;
}

.stat-item.danger .stat-number {
  color: #dc2626;
}

.stat-item.warning .stat-number {
  color: #d97706;
}

.stat-item.success .stat-number {
  color: #059669;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

/* 工具栏 - 新设计 */
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 24px;
  padding: 16px 20px;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

/* 筛选器组 */
.filters-group {
  display: flex;
  align-items: flex-end;
  gap: 16px;
  flex-wrap: wrap;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 120px;
}

.filter-label {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 2px;
}

.filter-select {
  padding: 6px 10px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  font-size: 13px;
  color: #374151;
  transition: all 0.2s ease;
  cursor: pointer;
  min-width: 100px;
}

.filter-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

.filter-select:hover {
  border-color: #9ca3af;
}

/* 控制组 */
.controls-group {
  display: flex;
  align-items: flex-end;
  gap: 20px;
}

.control-label {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
  display: block;
}

/* 排序控制 */
.sort-controls {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.sort-wrapper {
  display: flex;
  align-items: center;
  gap: 4px;
}

.sort-select {
  padding: 6px 10px;
  border: 1px solid #d1d5db;
  border-radius: 6px 0 0 6px;
  background: white;
  font-size: 13px;
  color: #374151;
  transition: all 0.2s ease;
  cursor: pointer;
  min-width: 110px;
  border-right: none;
}

.sort-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
  z-index: 1;
  position: relative;
}

.sort-order-btn {
  padding: 6px 8px;
  border: 1px solid #d1d5db;
  border-radius: 0 6px 6px 0;
  background: white;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  border-left: none;
}

.sort-order-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.sort-order-btn.desc {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.sort-order-btn svg {
  width: 14px;
  height: 14px;
}

/* 视图切换 */
.view-toggle {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.toggle-buttons {
  display: flex;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  overflow: hidden;
  background: white;
}

.toggle-btn {
  padding: 6px 8px;
  border: none;
  background: white;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  border-right: 1px solid #e5e7eb;
}

.toggle-btn:last-child {
  border-right: none;
}

.toggle-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.toggle-btn.active {
  background: #3b82f6;
  color: white;
}

.toggle-btn svg {
  width: 16px;
  height: 16px;
}

/* 主要内容区域 - 修改为不限制高度 */
.main-content {
  display: flex;
  flex-direction: column;
  /* 移除 flex: 1 和 overflow 限制，允许内容自然扩展 */
}

/* 邮件列表容器 - 移除滚动限制 */
.email-list-container {
  /* 移除所有 overflow 和 flex 属性，让内容自然显示 */
}

/* 隐藏邮件列表的滚动条（不再需要） */
/* .email-list-container::-webkit-scrollbar {
  width: 8px;
}

.email-list-container::-webkit-scrollbar-track {
  background: transparent;
}

.email-list-container::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.3);
  border-radius: 4px;
  transition: background 0.2s ease;
}

.email-list-container::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.5);
}

.email-list-container {
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.3) transparent;
} */

/* 网格布局 - 响应式卡片大小 */
.email-grid {
  display: grid;
  gap: 16px;
  padding: 8px 0;
}

/* 网格视图模式 */
.email-grid.view-grid.size-compact {
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
}

.email-grid.view-grid.size-normal {
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 16px;
}

.email-grid.view-grid.size-large {
  grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
  gap: 20px;
}

/* 列表视图模式 */
.email-grid.view-list {
  grid-template-columns: 1fr;
  gap: 8px;
}

/* 列表视图下的邮件卡片样式 */
.email-grid.view-list .email-card {
  display: flex;
  flex-direction: row;
  height: auto;
  min-height: 80px;
  max-height: 100px;
}

.email-grid.view-list .card-header {
  width: 120px;
  flex-shrink: 0;
  flex-direction: column;
  gap: 8px;
  padding: 12px;
  justify-content: center;
}

.email-grid.view-list .card-body {
  flex: 1;
  padding: 12px 16px;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 16px;
}

.email-grid.view-list .sender-info {
  width: 180px;
  flex-shrink: 0;
  margin-bottom: 0;
}

.email-grid.view-list .email-content {
  flex: 1;
  min-width: 0;
}

.email-grid.view-list .email-subject {
  font-size: 14px;
  margin-bottom: 4px;
  -webkit-line-clamp: 1;
}

.email-grid.view-list .email-preview {
  font-size: 12px;
  -webkit-line-clamp: 2;
  margin-bottom: 0;
}

.email-grid.view-list .card-meta {
  width: 200px;
  flex-shrink: 0;
  margin-top: 0;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.email-grid.view-list .tags {
  justify-content: flex-end;
}

/* 邮件卡片 - 动态高度 */
.email-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  position: relative;
}

/* 不同尺寸的卡片高度 */
.size-compact .email-card {
  min-height: 180px;
}

.size-normal .email-card {
  min-height: 220px;
}

.size-large .email-card {
  min-height: 260px;
}

.email-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
  border-color: #3b82f6;
}

.email-card.safe {
  border-left: 4px solid #22c55e;
}

.email-card.suspicious {
  border-left: 4px solid #f59e0b;
}

.email-card.phishing {
  border-left: 4px solid #dc2626;
  background: linear-gradient(135deg, #fefcfc 0%, #fef7f7 100%);
}

/* 卡片头部 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-bottom: 1px solid #e2e8f0;
  flex-shrink: 0;
}

.size-compact .card-header {
  padding: 10px 12px;
}

.size-normal .card-header {
  padding: 12px 16px;
}

.size-large .card-header {
  padding: 14px 18px;
}

/* 卡片主体 */
.card-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.size-compact .card-body {
  padding: 12px;
}

.size-normal .card-body {
  padding: 14px 16px;
}

.size-large .card-body {
  padding: 16px 18px;
}

.provider-icon {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.provider-icon.gmail {
  background: linear-gradient(135deg, #ea4335 0%, #d33b2c 100%);
}

.provider-icon.outlook {
  background: linear-gradient(135deg, #0078d4 0%, #106ebe 100%);
}

.provider-icon.qq {
  background: linear-gradient(135deg, #12b7f5 0%, #0e9ad4 100%);
}

.provider-icon.apple {
  background: linear-gradient(135deg, #000000 0%, #333333 100%);
}

.provider-icon.suspicious {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.provider-icon svg {
  width: 14px;
  height: 14px;
}

.security-status {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.security-status.safe {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  color: #065f46;
}

.security-status.suspicious {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
}

.security-status.phishing {
  background: linear-gradient(135deg, #fee2e2 0%, #fca5a5 100%);
  color: #991b1b;
}

.status-icon {
  width: 10px;
  height: 10px;
}

.sender-info {
  margin-bottom: 12px;
}

.sender-name {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sender-email {
  font-size: 11px;
  color: #6b7280;
  font-family: 'SF Mono', 'Monaco', monospace;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.email-subject {
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.email-preview {
  color: #6b7280;
  line-height: 1.4;
  margin: 0 0 12px 0;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 响应式文字大小 */
.size-compact .email-subject {
  font-size: 13px;
  -webkit-line-clamp: 2;
}

.size-normal .email-subject {
  font-size: 14px;
  -webkit-line-clamp: 2;
}

.size-large .email-subject {
  font-size: 15px;
  -webkit-line-clamp: 3;
}

.size-compact .email-preview {
  font-size: 11px;
  -webkit-line-clamp: 2;
}

.size-normal .email-preview {
  font-size: 12px;
  -webkit-line-clamp: 3;
}

.size-large .email-preview {
  font-size: 13px;
  -webkit-line-clamp: 4;
}

.card-meta {
  margin-top: auto;
}

.tags {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.tag {
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 9px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  white-space: nowrap;
}

.tag.importance.high {
  background: linear-gradient(135deg, #fee2e2 0%, #fca5a5 100%);
  color: #991b1b;
}

.tag.importance.medium {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
}

.tag.importance.low {
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  color: #6b7280;
}

.tag.urgency.urgent {
  background: linear-gradient(135deg, #ddd6fe 0%, #c4b5fd 100%);
  color: #6b21a8;
}

.tag.urgency.normal {
  background: linear-gradient(135deg, #e0f2fe 0%, #b3e5fc 100%);
  color: #0277bd;
}

.tag.time {
  background: linear-gradient(135deg, #f0fdf4 0%, #bbf7d0 100%);
  color: #065f46;
  margin-left: auto;
}

/* 分页容器 - 正常显示在内容后面 */
.pagination-container {
  margin-top: 24px;
  border-top: 1px solid #e2e8f0;
  background: white;
}

.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  background: linear-gradient(135deg, #fafbfc 0%, #f8fafc 100%);
  border-radius: 12px;
  margin-top: 1px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.pagination-info {
  display: flex;
  align-items: center;
}

.info-text {
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
}

.info-text strong {
  color: #1e293b;
  font-weight: 700;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 16px;
}

.page-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: white;
  color: #374151;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 100px;
  justify-content: center;
}

.page-btn:not(:disabled):hover {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border-color: #3b82f6;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  background: #f8fafc;
  color: #94a3b8;
}

.page-btn svg {
  width: 16px;
  height: 16px;
}

.prev-btn svg {
  order: -1;
}

.next-btn svg {
  order: 1;
}

.page-numbers {
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-number {
  width: 40px;
  height: 40px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  color: #64748b;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.page-number:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
  color: #475569;
  transform: translateY(-1px);
}

.page-number.active {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border-color: #3b82f6;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.page-number.active:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-1px);
}

.page-dots {
  color: #94a3b8;
  font-weight: 600;
  padding: 0 4px;
  font-size: 16px;
}

.page-size-selector {
  display: flex;
  align-items: center;
  gap: 12px;
}

.selector-label {
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
  white-space: nowrap;
}

.page-size-select {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: white;
  font-size: 14px;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 80px;
}

.page-size-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.page-size-select:hover {
  border-color: #9ca3af;
}

/* 响应式设计改进 */
@media (max-width: 1400px) {
  .email-grid.view-grid.size-compact {
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  }

  .email-grid.view-grid.size-normal {
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  }

  .email-grid.view-grid.size-large {
    grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  }
}

@media (max-width: 1024px) {
  .stats-overview {
    grid-template-columns: repeat(2, 1fr);
  }

  .toolbar {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }

  .filters-group {
    justify-content: center;
  }

  .controls-group {
    justify-content: center;
  }

  .email-grid.view-grid.size-compact,
  .email-grid.view-grid.size-normal,
  .email-grid.view-grid.size-large {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }

  .size-compact .email-card,
  .size-normal .email-card,
  .size-large .email-card {
    min-height: 200px;
  }

  /* 列表视图在中等屏幕调整 */
  .email-grid.view-list .card-body {
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
  }

  .email-grid.view-list .sender-info,
  .email-grid.view-list .email-content,
  .email-grid.view-list .card-meta {
    width: 100%;
  }

  .email-grid.view-list .card-meta {
    justify-content: flex-start;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }

  .header-actions {
    justify-content: space-between;
  }

  .stats-overview {
    grid-template-columns: 1fr;
  }

  .toolbar {
    padding: 12px 16px;
  }

  .filters-group {
    gap: 12px;
  }

  .filter-item {
    min-width: 100px;
  }

  .controls-group {
    gap: 16px;
  }

  .email-grid.view-grid.size-compact,
  .email-grid.view-grid.size-normal,
  .email-grid.view-grid.size-large {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .size-compact .email-card,
  .size-normal .email-card,
  .size-large .email-card {
    min-height: auto;
    height: auto;
  }

  .pagination {
    flex-direction: column;
    gap: 16px;
    padding: 16px 20px;
  }

  .pagination-controls {
    order: 2;
  }

  .page-size-selector {
    order: 3;
  }

  .pagination-info {
    order: 1;
  }
}

@media (max-width: 480px) {
  .email-view-page {
    padding: 16px 20px;
  }

  .view-controls {
    padding: 6px 8px;
  }

  .view-controls .control-label {
    display: none; /* 在小屏幕上隐藏标签 */
  }

  .size-select {
    min-width: 60px;
    font-size: 12px;
  }

  .refresh-btn {
    padding: 8px 12px;
    font-size: 13px;
  }

  .refresh-btn span {
    display: none; /* 在小屏幕上只显示图标 */
  }

  .toolbar {
    padding: 8px 12px;
  }

  .filters-group {
    gap: 8px;
  }

  .filter-item {
    min-width: 80px;
  }

  .filter-label,
  .controls-group .control-label {
    font-size: 10px;
  }

  .filter-select,
  .sort-select {
    padding: 4px 6px;
    font-size: 12px;
  }

  .controls-group {
    gap: 12px;
  }

  .sort-controls .control-label,
  .view-toggle .control-label {
    display: none;
  }

  .pagination {
    padding: 12px 16px;
    gap: 12px;
  }

  .pagination-controls {
    gap: 8px;
  }

  .page-btn {
    padding: 8px 12px;
    min-width: 80px;
    font-size: 13px;
  }

  .page-btn span {
    display: none;
  }

  .page-btn svg {
    width: 14px;
    height: 14px;
  }

  .page-numbers {
    gap: 4px;
  }

  .page-number {
    width: 36px;
    height: 36px;
    font-size: 13px;
  }

  .page-size-selector {
    gap: 8px;
  }

  .selector-label {
    font-size: 13px;
  }

  .page-size-select {
    padding: 6px 8px;
    font-size: 13px;
    min-width: 70px;
  }
}
</style>
